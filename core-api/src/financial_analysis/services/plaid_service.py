"""Plaid data provider service for bank account linking and transaction sync."""

import logging
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional, List, Dict, Any, Tuple

from sqlalchemy.orm import Session

import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

from ..config import settings
from ..database.models import LinkedProvider, Account, Transaction, AccountBalance

logger = logging.getLogger(__name__)


# Plaid account type/subtype -> Spearmint account_type mapping
PLAID_ACCOUNT_TYPE_MAP = {
    ('depository', 'checking'): 'checking',
    ('depository', 'savings'): 'savings',
    ('depository', 'money market'): 'savings',
    ('depository', 'cd'): 'savings',
    ('depository', 'cash management'): 'checking',
    ('credit', 'credit card'): 'credit_card',
    ('loan', 'student'): 'loan',
    ('loan', 'mortgage'): 'loan',
    ('loan', 'auto'): 'loan',
    ('loan', 'personal'): 'loan',
    ('loan', 'line of credit'): 'loan',
    ('investment', 'brokerage'): 'brokerage',
    ('investment', '401k'): '401k',
    ('investment', '401a'): '401k',
    ('investment', 'ira'): 'ira',
    ('investment', 'roth'): 'ira',
    ('investment', 'roth 401k'): '401k',
    ('investment', 'sep ira'): 'ira',
    ('investment', 'simple ira'): 'ira',
}


def _get_plaid_client() -> plaid_api.PlaidApi:
    """Create a Plaid API client from settings."""
    env_map = {
        'sandbox': plaid.Environment.Sandbox,
        'development': plaid.Environment.Development,
        'production': plaid.Environment.Production,
    }
    configuration = plaid.Configuration(
        host=env_map.get(settings.PLAID_ENV, plaid.Environment.Sandbox),
        api_key={
            'clientId': settings.PLAID_CLIENT_ID,
            'secret': settings.PLAID_SECRET,
        }
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)


class PlaidService:
    """Service for Plaid bank account linking and data synchronization."""

    def __init__(self, db: Session):
        self.db = db
        self.client = _get_plaid_client()

    def create_link_token(self) -> Dict[str, str]:
        """Create a Plaid Link token for the frontend."""
        products = [Products(p) for p in settings.PLAID_PRODUCTS.split(',') if p] \
            if hasattr(settings, 'PLAID_PRODUCTS') and settings.PLAID_PRODUCTS \
            else [Products('transactions')]

        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id='spearmint-user'),
            client_name='Spearmint Finance',
            products=products,
            country_codes=[CountryCode('US')],
            language='en',
        )

        if settings.PLAID_WEBHOOK_URL:
            request.webhook = settings.PLAID_WEBHOOK_URL

        response = self.client.link_token_create(request)
        return {
            'link_token': response.link_token,
            'expiration': response.expiration.isoformat(),
        }

    def exchange_public_token(
        self,
        public_token: str,
        institution_id: Optional[str] = None,
        institution_name: Optional[str] = None,
        encrypt_fn=None,
    ) -> LinkedProvider:
        """Exchange a public token for an access token and create provider + accounts."""
        from .aggregator_service import encrypt_token

        _encrypt = encrypt_fn or encrypt_token

        # Exchange token
        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = self.client.item_public_token_exchange(exchange_request)

        access_token = exchange_response.access_token
        item_id = exchange_response.item_id

        # Create LinkedProvider record
        provider = LinkedProvider(
            provider_type='plaid',
            provider_item_id=item_id,
            access_token_encrypted=_encrypt(access_token),
            institution_id=institution_id,
            institution_name=institution_name,
            status='active',
        )
        self.db.add(provider)
        self.db.flush()

        # Fetch accounts from Plaid and create local Account records
        self._create_accounts_from_plaid(provider, access_token)

        self.db.commit()
        self.db.refresh(provider)
        return provider

    def _create_accounts_from_plaid(self, provider: LinkedProvider, access_token: str):
        """Fetch Plaid accounts and create local Account records."""
        balance_request = AccountsBalanceGetRequest(access_token=access_token)
        response = self.client.accounts_balance_get(balance_request)

        for plaid_account in response.accounts:
            account_type = self._map_account_type(
                str(plaid_account.type),
                str(plaid_account.subtype) if plaid_account.subtype else None,
            )

            has_cash = account_type in ('checking', 'savings', 'brokerage')
            has_investments = account_type in ('brokerage', 'investment', '401k', 'ira')

            current_balance = Decimal(str(plaid_account.balances.current or 0))

            account = Account(
                account_name=plaid_account.name or plaid_account.official_name or 'Linked Account',
                account_type=account_type,
                institution_name=provider.institution_name,
                account_number_last4=plaid_account.mask,
                has_cash_component=has_cash,
                has_investment_component=has_investments,
                opening_balance=current_balance,
                opening_balance_date=date.today(),
                linked_provider_id=provider.id,
                external_account_id=plaid_account.account_id,
                link_type='plaid',
                notes=plaid_account.official_name,
            )
            self.db.add(account)

    def sync_transactions(self, provider: LinkedProvider, decrypt_fn=None) -> Dict[str, int]:
        """Sync transactions using Plaid's /transactions/sync endpoint."""
        from .aggregator_service import decrypt_token

        _decrypt = decrypt_fn or decrypt_token
        access_token = _decrypt(provider.access_token_encrypted)

        added_count = 0
        modified_count = 0
        removed_count = 0

        cursor = provider.sync_cursor or ''
        has_more = True

        while has_more:
            request = TransactionsSyncRequest(
                access_token=access_token,
                cursor=cursor,
            )
            response = self.client.transactions_sync(request)

            # Process added transactions
            for txn in response.added:
                added_count += self._upsert_transaction(provider, txn, is_new=True)

            # Process modified transactions
            for txn in response.modified:
                modified_count += self._upsert_transaction(provider, txn, is_new=False)

            # Process removed transactions
            for txn in response.removed:
                existing = self.db.query(Transaction).filter(
                    Transaction.external_transaction_id == txn.transaction_id
                ).first()
                if existing:
                    self.db.delete(existing)
                    removed_count += 1

            cursor = response.next_cursor
            has_more = response.has_more

        # Update cursor and sync timestamp
        provider.sync_cursor = cursor
        provider.last_synced_at = datetime.now(timezone.utc)
        self.db.commit()

        return {
            'transactions_added': added_count,
            'transactions_modified': modified_count,
            'transactions_removed': removed_count,
        }

    def _upsert_transaction(self, provider: LinkedProvider, plaid_txn, is_new: bool) -> int:
        """Create or update a transaction from Plaid data. Returns 1 if processed, 0 if skipped."""
        plaid_txn_id = plaid_txn.transaction_id

        # Find the local account for this transaction
        account = self.db.query(Account).filter(
            Account.linked_provider_id == provider.id,
            Account.external_account_id == plaid_txn.account_id,
        ).first()

        if not account:
            logger.warning(f"No local account found for Plaid account {plaid_txn.account_id}")
            return 0

        # Plaid: positive amount = money leaving account (expense)
        # Spearmint: amount is always positive, type determines direction
        amount = Decimal(str(abs(plaid_txn.amount)))
        transaction_type = 'Expense' if plaid_txn.amount > 0 else 'Income'

        existing = self.db.query(Transaction).filter(
            Transaction.external_transaction_id == plaid_txn_id
        ).first()

        if existing:
            # Update existing transaction
            existing.amount = amount
            existing.transaction_type = transaction_type
            existing.description = plaid_txn.name or plaid_txn.merchant_name
            existing.source = plaid_txn.merchant_name
            existing.transaction_date = plaid_txn.date
            existing.is_cleared = not getattr(plaid_txn, 'pending', False)
            existing.updated_at = datetime.now(timezone.utc)
            return 1

        # Create new transaction — use a default category
        # Look up or create an "Uncategorized" category
        from ..database.models import Category
        uncategorized = self.db.query(Category).filter(
            Category.category_name == 'Uncategorized'
        ).first()
        category_id = uncategorized.category_id if uncategorized else 1

        # Try to map Plaid category
        if hasattr(plaid_txn, 'personal_finance_category') and plaid_txn.personal_finance_category:
            primary_cat = plaid_txn.personal_finance_category.primary
            mapped = self.db.query(Category).filter(
                Category.category_name.ilike(f'%{primary_cat}%')
            ).first()
            if mapped:
                category_id = mapped.category_id

        txn = Transaction(
            transaction_date=plaid_txn.date,
            amount=amount,
            transaction_type=transaction_type,
            category_id=category_id,
            description=plaid_txn.name or plaid_txn.merchant_name,
            source=plaid_txn.merchant_name,
            payment_method=getattr(plaid_txn, 'payment_channel', None),
            account_id=account.account_id,
            external_transaction_id=plaid_txn_id,
            is_cleared=not getattr(plaid_txn, 'pending', False),
        )
        self.db.add(txn)
        return 1

    def sync_balances(self, provider: LinkedProvider, decrypt_fn=None) -> int:
        """Pull current balances for all accounts in this provider."""
        from .aggregator_service import decrypt_token

        _decrypt = decrypt_fn or decrypt_token
        access_token = _decrypt(provider.access_token_encrypted)

        balance_request = AccountsBalanceGetRequest(access_token=access_token)
        response = self.client.accounts_balance_get(balance_request)
        updated = 0

        for plaid_account in response.accounts:
            account = self.db.query(Account).filter(
                Account.linked_provider_id == provider.id,
                Account.external_account_id == plaid_account.account_id,
            ).first()

            if not account:
                continue

            current_balance = Decimal(str(plaid_account.balances.current or 0))

            # Update account's current balance
            account.current_balance = current_balance
            account.updated_at = datetime.now(timezone.utc)

            # Create balance snapshot
            today = date.today()
            existing_snapshot = self.db.query(AccountBalance).filter(
                AccountBalance.account_id == account.account_id,
                AccountBalance.balance_date == today,
                AccountBalance.balance_type == 'statement',
            ).first()

            if existing_snapshot:
                existing_snapshot.total_balance = current_balance
            else:
                snapshot = AccountBalance(
                    account_id=account.account_id,
                    balance_date=today,
                    total_balance=current_balance,
                    balance_type='statement',
                )
                self.db.add(snapshot)

            updated += 1

        self.db.commit()
        return updated

    def handle_webhook(self, webhook_type: str, webhook_code: str, item_id: str):
        """Handle incoming Plaid webhooks."""
        provider = self.db.query(LinkedProvider).filter(
            LinkedProvider.provider_item_id == item_id
        ).first()

        if not provider:
            logger.warning(f"Webhook for unknown Plaid item: {item_id}")
            return

        if webhook_type == 'TRANSACTIONS' and webhook_code == 'SYNC_UPDATES_AVAILABLE':
            self.sync_transactions(provider)
            self.sync_balances(provider)

        elif webhook_type == 'ITEM' and webhook_code == 'ERROR':
            provider.status = 'login_required'
            provider.error_code = 'ITEM_LOGIN_REQUIRED'
            provider.error_message = 'Bank login credentials need to be updated'
            self.db.commit()

        elif webhook_type == 'ITEM' and webhook_code == 'PENDING_EXPIRATION':
            provider.status = 'login_required'
            provider.error_message = 'Connection will expire soon — please re-authenticate'
            self.db.commit()

    @staticmethod
    def _map_account_type(plaid_type: str, plaid_subtype: Optional[str]) -> str:
        """Map Plaid account type/subtype to Spearmint account type."""
        key = (plaid_type.lower(), (plaid_subtype or '').lower())
        mapped = PLAID_ACCOUNT_TYPE_MAP.get(key)
        if mapped:
            return mapped

        # Fallback by type only
        type_fallbacks = {
            'depository': 'checking',
            'credit': 'credit_card',
            'loan': 'loan',
            'investment': 'investment',
        }
        return type_fallbacks.get(plaid_type.lower(), 'other')
