"""
Check the current state of the database to understand what needs to be migrated.
"""

import sqlite3
from pathlib import Path

def check_database_state(db_file="financial_data.db"):
    """Check the current state of the database."""

    db_path = Path(db_file)

    if not db_path.exists():
        print("ERROR: Database file not found!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 60)
    print("DATABASE STATE CHECK")
    print("=" * 60)

    # Check existing tables
    print("\n1. Existing Tables:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    for table in tables:
        print(f"   - {table[0]}")

    # Check columns in transactions table
    print("\n2. Transactions Table Columns:")
    cursor.execute("PRAGMA table_info(transactions)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"   - {col[1]} ({col[2]})")

    # Check if new tables exist
    print("\n3. Account System Tables:")
    account_tables = ['accounts', 'account_balances', 'investment_holdings', 'reconciliations']
    for table_name in account_tables:
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        exists = cursor.fetchone()[0] > 0
        print(f"   - {table_name}: {'EXISTS' if exists else 'MISSING'}")

    # Check if new columns exist in transactions
    print("\n4. New Columns in Transactions:")
    new_columns = ['account_id', 'is_cleared', 'cleared_date', 'affects_cash_balance',
                   'affects_investment_value', 'security_symbol', 'security_quantity']
    cursor.execute("PRAGMA table_info(transactions)")
    existing_columns = [col[1] for col in cursor.fetchall()]

    for col_name in new_columns:
        exists = col_name in existing_columns
        print(f"   - {col_name}: {'EXISTS' if exists else 'MISSING'}")

    # Count transactions
    print("\n5. Data Statistics:")
    cursor.execute("SELECT COUNT(*) FROM transactions")
    tx_count = cursor.fetchone()[0]
    print(f"   - Total transactions: {tx_count}")

    # Check if any transactions have account_id set
    if 'account_id' in existing_columns:
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE account_id IS NOT NULL")
        linked_count = cursor.fetchone()[0]
        print(f"   - Transactions with account_id: {linked_count}")

    conn.close()

    print("\n" + "=" * 60)
    print("Check complete!")
    print("=" * 60)

if __name__ == "__main__":
    import sys
    db_file = sys.argv[1] if len(sys.argv) > 1 else "financial_data.db"
    print(f"Checking database: {db_file}\n")
    check_database_state(db_file)