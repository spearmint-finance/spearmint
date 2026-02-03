"""
Authentication service for managing API keys.

Handles API key generation, validation, and revocation for MCP server
client authentication.
"""

import hashlib
import secrets
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from ..database.models import APIKey


# Key format: smint_live_ + 32 random alphanumeric characters
KEY_PREFIX = "smint_live_"
KEY_LENGTH = 32  # Length of the random part


class AuthService:
    """Service for managing API keys and authentication."""

    def __init__(self, db: Session):
        """Initialize the auth service with a database session."""
        self.db = db

    def _generate_key(self) -> str:
        """
        Generate a new API key.

        Returns:
            Full API key string (smint_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)
        """
        random_part = secrets.token_urlsafe(KEY_LENGTH)[:KEY_LENGTH]
        return f"{KEY_PREFIX}{random_part}"

    def _hash_key(self, key: str) -> str:
        """
        Hash an API key using SHA-256.

        Args:
            key: Full API key string

        Returns:
            SHA-256 hash of the key
        """
        return hashlib.sha256(key.encode()).hexdigest()

    def _get_key_prefix(self, key: str) -> str:
        """
        Get the display prefix of an API key.

        Args:
            key: Full API key string

        Returns:
            Key prefix for display (e.g., 'smint_live_xxxx')
        """
        # Show the prefix plus first 4 chars of the random part
        return key[:len(KEY_PREFIX) + 4]

    def create_key(
        self,
        name: str,
        expires_at: Optional[datetime] = None
    ) -> Tuple[APIKey, str]:
        """
        Create a new API key.

        Args:
            name: Descriptive name for the key (e.g., "Claude Desktop")
            expires_at: Optional expiration date

        Returns:
            Tuple of (APIKey model, full_key_string)
            The full key string should only be shown once at creation time.
        """
        # Generate the key
        full_key = self._generate_key()
        key_hash = self._hash_key(full_key)
        key_prefix = self._get_key_prefix(full_key)

        # Create the database record
        api_key = APIKey(
            name=name,
            key_prefix=key_prefix,
            key_hash=key_hash,
            is_active=True,
            expires_at=expires_at
        )

        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)

        return api_key, full_key

    def validate_key(self, key: str) -> Tuple[bool, Optional[APIKey], Optional[str]]:
        """
        Validate an API key.

        Args:
            key: Full API key string to validate

        Returns:
            Tuple of (is_valid, api_key_if_valid, error_message_if_invalid)
        """
        # Check key format
        if not key.startswith(KEY_PREFIX):
            return False, None, "Invalid key format"

        # Hash the provided key
        key_hash = self._hash_key(key)

        # Look up the key by hash
        api_key = self.db.query(APIKey).filter(
            APIKey.key_hash == key_hash
        ).first()

        if not api_key:
            return False, None, "Invalid API key"

        # Check if key is active
        if not api_key.is_active:
            return False, None, "API key has been revoked"

        # Check expiration
        if api_key.expires_at:
            if api_key.expires_at < datetime.now(timezone.utc):
                return False, None, "API key has expired"

        # Update last used timestamp
        api_key.last_used_at = datetime.now(timezone.utc)
        self.db.commit()

        return True, api_key, None

    def get_key(self, key_id: int) -> Optional[APIKey]:
        """
        Get an API key by ID.

        Args:
            key_id: ID of the API key

        Returns:
            APIKey model or None if not found
        """
        return self.db.query(APIKey).filter(
            APIKey.key_id == key_id
        ).first()

    def get_keys(self, include_inactive: bool = False) -> List[APIKey]:
        """
        Get all API keys.

        Args:
            include_inactive: Whether to include inactive (revoked) keys

        Returns:
            List of APIKey models
        """
        query = self.db.query(APIKey)

        if not include_inactive:
            query = query.filter(APIKey.is_active == True)

        return query.order_by(APIKey.created_at.desc()).all()

    def revoke_key(self, key_id: int) -> bool:
        """
        Revoke an API key.

        Args:
            key_id: ID of the API key to revoke

        Returns:
            True if successful, False if key not found
        """
        api_key = self.get_key(key_id)
        if not api_key:
            return False

        api_key.is_active = False
        self.db.commit()

        return True

    def delete_key(self, key_id: int) -> bool:
        """
        Permanently delete an API key.

        Args:
            key_id: ID of the API key to delete

        Returns:
            True if successful, False if key not found
        """
        api_key = self.get_key(key_id)
        if not api_key:
            return False

        self.db.delete(api_key)
        self.db.commit()

        return True
