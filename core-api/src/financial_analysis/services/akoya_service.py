"""Akoya data provider service for Fidelity account linking and data sync."""

import logging
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Optional, Dict
from urllib.parse import urlencode

import requests
from sqlalchemy.orm import Session

from ..config import settings
from ..database.models import (
    LinkedProvider, Account, Transaction, AccountBalance, InvestmentHolding
)

logger = logging.getLogger(__name__)

# Akoya FDX account type -> Spearmint account_type mapping
AKOYA_ACCOUNT_TYPE_MAP = {
    'CHECKING': 'checking',
    'SAVINGS': 'savings',
    'MONEY_MARKET': 'savings',
    'CD': 'savings',
    'CREDITCARD': 'credit_card',
    'LINEOFCREDIT': 'loan',
    'LOAN': 'loan',
    'MORTGAGE': 'loan',
    'AUTO': 'loan',
    'STUDENT': 'loan',
    'BROKERAGE': 'brokerage',
    'INDIVIDUAL': 'brokerage',
    'JOINT': 'brokerage',
    'INVESTMENT': 'investment',
    'RETIREMENT': 'ira',
    'IRA': 'ira',
    'ROTH_IRA': 'ira',
    'SEP_IRA': 'ira',
    'SIMPLE_IRA': 'ira',
    'TRADITIONAL_IRA': 'ira',
    '401K': '401k',
    '403B': '401k',
    '457': '401k',
    'KEOGH': 'ira',
}

AKOYA_BASE_URLS = {
    'sandbox': 'https://sandbox.ddp.akoya.com',
    'production': 'https://products.ddp.akoya.com',
}

AKOYA_AUTH_URLS = {
    'sandbox': 'https://sandbox.ddp.akoya.com',
    'production': 'https://idp.ddp.akoya.com',
}

# Fidelity's provider ID on Akoya
FIDELITY_PROVIDER_ID = 'fidelity'


class AkoyaService:
    """Service for Akoya (Fidelity) account linking and data synchronization."""

    def __init__(self, db: Session):
        self.db = db
        self.base_url = AKOYA_BASE_URLS.get(settings.AKOYA_ENV, AKOYA_BASE_URLS['sandbox'])
        self.auth_url = AKOYA_AUTH_URLS.get(settings.AKOYA_ENV, AKOYA_AUTH_URLS['sandbox'])

    def get_authorization_url(self, provider_id: str = FIDELITY_PROVIDER_ID) -> str:
        """Get the Akoya OAuth authorization URL for user redirect."""
        params = {
            'connector': provider_id,
            'client_id': settings.AKOYA_CLIENT_ID,
            'redirect_uri': settings.AKOYA_REDIRECT_URI,
            'response_type': 'code',
            'scope': 'openid offline_access',
        }
        return f"{self.auth_url}/auth?{urlencode(params)}"

    def exchange_auth_code(
        self,
        auth_code: str,
        provider_id: str = FIDELITY_PROVIDER_ID,
        encrypt_fn=None,
    ) -> LinkedProvider:
        """Exchange an authorization code for tokens and create provider + accounts."""
        from .aggregator_service import encrypt_token

        _encrypt = encrypt_fn or encrypt_token

        # Exchange auth code for tokens
        token_response = requests.post(
            f"{self.auth_url}/token",
            data={
                'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': settings.AKOYA_REDIRECT_URI,
                'client_id': settings.AKOYA_CLIENT_ID,
                'client_secret': settings.AKOYA_CLIENT_SECRET,
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        token_response.raise_for_status()
        tokens = token_response.json()

        id_token = tokens['id_token']
        refresh_token = tokens.get('refresh_token', '')

        # Create LinkedProvider
        provider = LinkedProvider(
            provider_type='akoya',
            provider_item_id=f"akoya:{provider_id}:{auth_code[:16]}",
            access_token_encrypted=_encrypt(id_token),
            refresh_token_encrypted=_encrypt(refresh_token) if refresh_token else None,
            institution_id=provider_id,
            institution_name=self._get_institution_name(provider_id),
            status='active',
        )
        self.db.add(provider)
        self.db.flush()

        # Fetch accounts and create local records
        self._create_accounts_from_akoya(provider, id_token, provider_id)

        self.db.commit()
        self.db.refresh(provider)
        return provider

    def _get_institution_name(self, provider_id: str) -> str:
        """Map provider ID to human-readable name."""
        names = {
            'fidelity': 'Fidelity Investments',
            'mikomo': 'Mikomo Bank (Sandbox)',
        }
        return names.get(provider_id, provider_id.title())

    def _create_accounts_from_akoya(
        self, provider: LinkedProvider, id_token: str, provider_id: str
    ):
        """Fetch Akoya accounts and create local Account records."""
        accounts_data = self._api_get(
            f"/accounts/v2/{provider_id}", id_token
        )

        for acct in accounts_data.get('accounts', []):
            account_type_raw = acct.get('accountType', 'OTHER')
            account_type = self._map_account_type(account_type_raw)

            has_cash = account_type in ('checking', 'savings', 'brokerage')
            has_investments = account_type in ('brokerage', 'investment', '401k', 'ira')

            balance = Decimal(str(acct.get('currentBalance', 0)))

            account = Account(
                account_name=acct.get('accountNickname') or acct.get('displayName') or 'Fidelity Account',
                account_type=account_type,
                institution_name=provider.institution_name,
                account_number_last4=acct.get('accountNumberDisplay', '')[-4:] or None,
                has_cash_component=has_cash,
                has_investment_component=has_investments,
                opening_balance=balance,
                opening_balance_date=date.today(),
                linked_provider_id=provider.id,
                external_account_id=acct.get('accountId'),
                link_type='akoya',
            )
            self.db.add(account)

    def sync_transactions(self, provider: LinkedProvider, decrypt_fn=None) -> Dict[str, int]:
        """Sync transactions from Akoya."""
        from .aggregator_service import decrypt_token

        _decrypt = decrypt_fn or decrypt_token
        id_token = self._ensure_valid_token(provider, _decrypt)

        added_count = 0
        provider_id = provider.institution_id or FIDELITY_PROVIDER_ID

        accounts = self.db.query(Account).filter(
            Account.linked_provider_id == provider.id
        ).all()

        for account in accounts:
            if not account.external_account_id:
                continue

            txns_data = self._api_get(
                f"/transactions/v2/{provider_id}/{account.external_account_id}",
                id_token,
            )

            for txn in txns_data.get('transactions', []):
                txn_id = txn.get('transactionId')
                if not txn_id:
                    continue

                # Check for existing
                existing = self.db.query(Transaction).filter(
                    Transaction.external_transaction_id == txn_id
                ).first()
                if existing:
                    continue

                amount = Decimal(str(abs(float(txn.get('amount', 0)))))
                # FDX: DEBIT = money out, CREDIT = money in
                debit_credit = txn.get('debitCreditMemo', 'DEBIT')
                transaction_type = 'Income' if debit_credit == 'CREDIT' else 'Expense'

                from ..database.models import Category
                uncategorized = self.db.query(Category).filter(
                    Category.category_name == 'Uncategorized'
                ).first()
                category_id = uncategorized.category_id if uncategorized else 1

                new_txn = Transaction(
                    transaction_date=date.fromisoformat(txn.get('postedTimestamp', txn.get('transactionTimestamp', str(date.today())))[:10]),
                    amount=amount,
                    transaction_type=transaction_type,
                    category_id=category_id,
                    description=txn.get('description', ''),
                    source=txn.get('merchantName') or txn.get('payee'),
                    account_id=account.account_id,
                    external_transaction_id=txn_id,
                    is_cleared=txn.get('status', '').upper() == 'POSTED',
                )
                self.db.add(new_txn)
                added_count += 1

        provider.last_synced_at = datetime.now(timezone.utc)
        self.db.commit()
        return {'transactions_added': added_count, 'transactions_modified': 0, 'transactions_removed': 0}

    def sync_balances(self, provider: LinkedProvider, decrypt_fn=None) -> int:
        """Pull current balances from Akoya."""
        from .aggregator_service import decrypt_token

        _decrypt = decrypt_fn or decrypt_token
        id_token = self._ensure_valid_token(provider, _decrypt)

        provider_id = provider.institution_id or FIDELITY_PROVIDER_ID
        updated = 0

        accounts = self.db.query(Account).filter(
            Account.linked_provider_id == provider.id
        ).all()

        for account in accounts:
            if not account.external_account_id:
                continue

            balance_data = self._api_get(
                f"/balances/v2/{provider_id}/{account.external_account_id}",
                id_token,
            )

            current_balance = Decimal(str(balance_data.get('currentBalance', 0)))
            today = date.today()

            # Create/update balance snapshot
            existing = self.db.query(AccountBalance).filter(
                AccountBalance.account_id == account.account_id,
                AccountBalance.balance_date == today,
                AccountBalance.balance_type == 'statement',
            ).first()

            if existing:
                existing.total_balance = current_balance
            else:
                self.db.add(AccountBalance(
                    account_id=account.account_id,
                    balance_date=today,
                    total_balance=current_balance,
                    balance_type='statement',
                ))
            updated += 1

        self.db.commit()
        return updated

    def sync_holdings(self, provider: LinkedProvider, decrypt_fn=None) -> int:
        """Pull investment holdings from Akoya."""
        from .aggregator_service import decrypt_token

        _decrypt = decrypt_fn or decrypt_token
        id_token = self._ensure_valid_token(provider, _decrypt)

        provider_id = provider.institution_id or FIDELITY_PROVIDER_ID
        updated = 0

        accounts = self.db.query(Account).filter(
            Account.linked_provider_id == provider.id,
            Account.has_investment_component == True,
        ).all()

        today = date.today()

        for account in accounts:
            if not account.external_account_id:
                continue

            invest_data = self._api_get(
                f"/investments/v2/{provider_id}/{account.external_account_id}",
                id_token,
            )

            for holding in invest_data.get('holdings', []):
                symbol = holding.get('securityId') or holding.get('symbol') or 'UNKNOWN'
                quantity = Decimal(str(holding.get('units', holding.get('quantity', 0))))
                cost_basis = Decimal(str(holding.get('costBasis', 0)))
                current_value = Decimal(str(holding.get('marketValue', 0)))

                # Upsert holding by (account_id, symbol, as_of_date)
                existing = self.db.query(InvestmentHolding).filter(
                    InvestmentHolding.account_id == account.account_id,
                    InvestmentHolding.symbol == symbol,
                    InvestmentHolding.as_of_date == today,
                ).first()

                if existing:
                    existing.quantity = quantity
                    existing.cost_basis = cost_basis
                    existing.current_value = current_value
                else:
                    self.db.add(InvestmentHolding(
                        account_id=account.account_id,
                        symbol=symbol,
                        description=holding.get('description') or holding.get('securityName'),
                        quantity=quantity,
                        cost_basis=cost_basis,
                        current_value=current_value,
                        as_of_date=today,
                    ))
                updated += 1

        self.db.commit()
        return updated

    def _ensure_valid_token(self, provider: LinkedProvider, decrypt_fn) -> str:
        """Get a valid ID token, refreshing if needed."""
        from .aggregator_service import encrypt_token

        id_token = decrypt_fn(provider.access_token_encrypted)

        # Akoya ID tokens expire in ~15 minutes. Try to refresh.
        if provider.refresh_token_encrypted:
            try:
                refresh_token = decrypt_fn(provider.refresh_token_encrypted)
                token_response = requests.post(
                    f"{self.auth_url}/token",
                    data={
                        'grant_type': 'refresh_token',
                        'refresh_token': refresh_token,
                        'client_id': settings.AKOYA_CLIENT_ID,
                        'client_secret': settings.AKOYA_CLIENT_SECRET,
                    },
                    headers={'Content-Type': 'application/x-www-form-urlencoded'},
                )
                if token_response.ok:
                    tokens = token_response.json()
                    id_token = tokens['id_token']
                    provider.access_token_encrypted = encrypt_token(id_token)
                    if tokens.get('refresh_token'):
                        provider.refresh_token_encrypted = encrypt_token(tokens['refresh_token'])
                    self.db.flush()
            except Exception as e:
                logger.warning(f"Token refresh failed, using existing token: {e}")

        return id_token

    def _api_get(self, path: str, id_token: str) -> dict:
        """Make an authenticated GET request to the Akoya API."""
        response = requests.get(
            f"{self.base_url}{path}",
            headers={
                'Authorization': f'Bearer {id_token}',
                'Accept': 'application/json',
            },
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _map_account_type(akoya_type: str) -> str:
        """Map Akoya/FDX account type to Spearmint account type."""
        return AKOYA_ACCOUNT_TYPE_MAP.get(akoya_type.upper(), 'other')
