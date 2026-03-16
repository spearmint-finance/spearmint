"""Unified aggregator service facade for Plaid and Akoya providers."""

import logging
from typing import Dict, Optional

from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

from ..config import settings
from ..database.models import LinkedProvider

logger = logging.getLogger(__name__)


def _get_fernet() -> Fernet:
    """Get Fernet cipher for token encryption/decryption."""
    key = settings.PROVIDER_TOKEN_ENCRYPTION_KEY
    if not key:
        # Generate a key for development — in production this MUST be set
        logger.warning("PROVIDER_TOKEN_ENCRYPTION_KEY not set — using ephemeral key. Tokens will not survive restarts.")
        key = Fernet.generate_key().decode()
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_token(token: str) -> str:
    """Encrypt a provider access/refresh token."""
    return _get_fernet().encrypt(token.encode()).decode()


def decrypt_token(encrypted: str) -> str:
    """Decrypt a provider access/refresh token."""
    return _get_fernet().decrypt(encrypted.encode()).decode()


class AggregatorService:
    """
    Unified facade for bank data aggregation.

    Delegates to PlaidService or AkoyaService based on provider_type.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_providers(self):
        """List all linked providers."""
        return self.db.query(LinkedProvider).order_by(LinkedProvider.created_at.desc()).all()

    def get_provider(self, provider_id: int) -> Optional[LinkedProvider]:
        """Get a single linked provider by ID."""
        return self.db.query(LinkedProvider).filter(
            LinkedProvider.id == provider_id
        ).first()

    def sync(self, provider_id: int) -> Dict[str, int]:
        """Sync transactions, balances, and holdings for a provider."""
        provider = self.get_provider(provider_id)
        if not provider:
            raise ValueError(f"Provider {provider_id} not found")

        result = {'transactions_added': 0, 'transactions_modified': 0,
                  'transactions_removed': 0, 'balances_updated': 0, 'holdings_updated': 0}

        if provider.provider_type == 'plaid':
            from .plaid_service import PlaidService
            svc = PlaidService(self.db)
            txn_result = svc.sync_transactions(provider)
            result.update(txn_result)
            result['balances_updated'] = svc.sync_balances(provider)

        elif provider.provider_type == 'akoya':
            from .akoya_service import AkoyaService
            svc = AkoyaService(self.db)
            txn_result = svc.sync_transactions(provider)
            result.update(txn_result)
            result['balances_updated'] = svc.sync_balances(provider)
            result['holdings_updated'] = svc.sync_holdings(provider)

        return result

    def unlink(self, provider_id: int):
        """Deactivate a provider connection. Keeps accounts and transactions."""
        provider = self.get_provider(provider_id)
        if not provider:
            raise ValueError(f"Provider {provider_id} not found")

        provider.status = 'revoked'
        provider.access_token_encrypted = encrypt_token('revoked')
        provider.refresh_token_encrypted = None
        self.db.commit()
