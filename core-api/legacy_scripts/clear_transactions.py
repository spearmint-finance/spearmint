"""Script to clear all transactions from the database."""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database URL - SQLite
BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/financial_analysis.db"

print(f"Using database: {DATABASE_URL}")

# Create database session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Delete in order (foreign key constraints)
    transaction_tags_deleted = db.execute(text("DELETE FROM transaction_tags")).rowcount
    transactions_deleted = db.execute(text("DELETE FROM transactions")).rowcount
    import_history_deleted = db.execute(text("DELETE FROM import_history")).rowcount

    db.commit()

    print("=" * 80)
    print("DATABASE CLEARED SUCCESSFULLY")
    print("=" * 80)
    print(f"Deleted {transaction_tags_deleted} transaction tags")
    print(f"Deleted {transactions_deleted} transactions")
    print(f"Deleted {import_history_deleted} import history records")
    print("=" * 80)

except Exception as e:
    db.rollback()
    print(f"ERROR: Failed to clear database: {e}")

finally:
    db.close()
