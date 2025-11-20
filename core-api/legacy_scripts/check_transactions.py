"""Script to check transaction count in database."""
from pathlib import Path
from sqlalchemy import create_engine, text

# Database URL - SQLite
BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/financial_analysis.db"

# Create database session
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Count transactions
    result = conn.execute(text("SELECT COUNT(*) FROM transactions"))
    count = result.scalar()

    # Get some sample data
    sample = conn.execute(text("""
        SELECT transaction_date, amount, description, category_id
        FROM transactions
        LIMIT 5
    """))

    print("=" * 80)
    print("DATABASE STATUS")
    print("=" * 80)
    print(f"Total transactions: {count}")
    print("\nSample transactions:")
    print("-" * 80)
    for row in sample:
        print(f"Date: {row[0]}, Amount: ${row[1]:.2f}, Description: {row[2][:50]}")
    print("=" * 80)
