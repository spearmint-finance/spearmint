"""
Migration: add real estate fields to accounts table.

Adds three nullable columns to support real estate account modeling:
  - property_value:              current market value of the property
  - property_type:               'primary_residence' | 'rental' | 'vacation'
  - linked_mortgage_account_id:  FK to another account row (the mortgage/loan)

This migration is purely ADDITIVE — it never drops or modifies existing rows.
The accounts CHECK constraint cannot be altered in SQLite without rebuilding
the table; validation of the new 'real_estate' type is handled at the
application layer (Pydantic schema) for existing databases.

Safe to run multiple times (idempotent via column-existence checks).
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text, inspect

from financial_analysis.config import DATABASE_URL


def column_exists(engine, table: str, column: str) -> bool:
    inspector = inspect(engine)
    return column in {c["name"] for c in inspector.get_columns(table)}


def run_migration(database_url: str | None = None) -> None:
    url = database_url or DATABASE_URL
    engine = create_engine(url)

    with engine.connect() as conn:
        # Add property_value
        if not column_exists(engine, "accounts", "property_value"):
            conn.execute(text("ALTER TABLE accounts ADD COLUMN property_value REAL"))
            print("  ✓ Added column: accounts.property_value")
        else:
            print("  · Skipped (exists): accounts.property_value")

        # Add property_type
        if not column_exists(engine, "accounts", "property_type"):
            conn.execute(text("ALTER TABLE accounts ADD COLUMN property_type TEXT"))
            print("  ✓ Added column: accounts.property_type")
        else:
            print("  · Skipped (exists): accounts.property_type")

        # Add linked_mortgage_account_id
        if not column_exists(engine, "accounts", "linked_mortgage_account_id"):
            conn.execute(text(
                "ALTER TABLE accounts ADD COLUMN linked_mortgage_account_id INTEGER "
                "REFERENCES accounts(account_id)"
            ))
            print("  ✓ Added column: accounts.linked_mortgage_account_id")
        else:
            print("  · Skipped (exists): accounts.linked_mortgage_account_id")

        conn.commit()

    engine.dispose()
    print("\nMigration complete. Existing data is unchanged.")


if __name__ == "__main__":
    print("=" * 60)
    print("Migration: add_real_estate_fields")
    print("=" * 60)
    run_migration()
