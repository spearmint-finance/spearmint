"""
Seed data for database initialization.

Populates default API keys and tags.
"""

import hashlib
import os
from sqlalchemy.orm import Session
from .models import APIKey
from .seed_tags import seed_tags


# Demo API key for development/testing (43 chars total)
# Key: smint_live_demokey1234567890abcdefghijklmn
DEMO_API_KEY = "smint_live_demokey1234567890abcdefghijklmn"
DEMO_API_KEY_HASH = hashlib.sha256(DEMO_API_KEY.encode()).hexdigest()


def seed_api_keys(db: Session) -> None:
    """
    Seed a demo API key for development/testing.

    The demo key is: smint_live_demo1234567890abcdef

    Args:
        db: Database session
    """
    print("\nSeeding demo API key...")

    # Check if demo key already exists
    existing = db.query(APIKey).filter_by(name="Demo Key (Development)").first()

    if not existing:
        demo_key = APIKey(
            name="Demo Key (Development)",
            key_prefix="smint_live_demo...",
            key_hash=DEMO_API_KEY_HASH,
            is_active=True,
        )
        db.add(demo_key)
        db.commit()
        print(f"  [OK] Added demo API key")
        print(f"  [INFO] Demo key for testing: {DEMO_API_KEY}")
    else:
        print(f"  - Skipped (exists): Demo Key")


def seed_all(db: Session) -> None:
    """
    Seed all default data.

    Args:
        db: Database session
    """
    seed_api_keys(db)
    seed_tags(db)
    print("\n[OK] All seed data loaded successfully")
