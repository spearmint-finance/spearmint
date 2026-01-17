"""
Database migration to add the import_profiles table.

This migration adds support for saving column mappings for different
bank/institution export formats.

Run this script to apply the migration to an existing database.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError

# Import after path is set
from financial_analysis.database.base import Base
from financial_analysis.database.models import ImportProfile


def check_table_exists(engine, table_name):
    """Check if a table exists in the database."""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def run_migration(database_path=None):
    """
    Run the migration to add import_profiles table.

    Args:
        database_path: Path to the SQLite database (optional)
    """
    # Determine database path
    if database_path is None:
        database_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', '..', '..', '..', 'data', 'financial_analysis.db'
        )

    # Create engine
    engine = create_engine(f'sqlite:///{database_path}')

    print(f"Running migration on database: {database_path}")

    try:
        with engine.begin() as conn:
            # Create import_profiles table if it doesn't exist
            if not check_table_exists(engine, 'import_profiles'):
                print("Creating import_profiles table...")
                conn.execute(text("""
                    CREATE TABLE import_profiles (
                        profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(100) NOT NULL,
                        account_id INTEGER,
                        column_mappings JSON NOT NULL,
                        date_format VARCHAR(50),
                        skip_rows INTEGER DEFAULT 0,
                        is_active BOOLEAN DEFAULT 1,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (account_id) REFERENCES accounts(account_id)
                    )
                """))

                # Create indexes
                conn.execute(text("CREATE INDEX idx_import_profile_name ON import_profiles(name)"))
                conn.execute(text("CREATE INDEX idx_import_profile_account ON import_profiles(account_id)"))
                conn.execute(text("CREATE INDEX idx_import_profile_active ON import_profiles(is_active)"))
                print("+ import_profiles table created with indexes")
            else:
                print("import_profiles table already exists")

        print("\nMigration completed successfully!")

    except OperationalError as e:
        print(f"Database error: {e}")
        raise
    except Exception as e:
        print(f"Migration failed: {e}")
        raise


if __name__ == "__main__":
    # Allow passing database path as command line argument
    db_path = sys.argv[1] if len(sys.argv) > 1 else None
    run_migration(db_path)

