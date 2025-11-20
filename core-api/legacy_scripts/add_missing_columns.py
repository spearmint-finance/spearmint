"""
Safe migration to add missing columns to the transactions table.
This script only adds columns that don't already exist.
"""

import sqlite3
from pathlib import Path

def add_missing_columns(db_path="financial_analysis.db"):
    """Add missing columns to the transactions table."""

    if not Path(db_path).exists():
        print(f"ERROR: Database {db_path} not found!")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 60)
    print(f"Adding Missing Columns to {db_path}")
    print("=" * 60)

    # Get existing columns
    cursor.execute("PRAGMA table_info(transactions)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    print(f"\nExisting columns: {len(existing_columns)}")

    # Define columns to add
    columns_to_add = [
        ("account_id", "INTEGER REFERENCES accounts(account_id)"),
        ("is_cleared", "BOOLEAN DEFAULT 0"),
        ("cleared_date", "DATE"),
        ("affects_cash_balance", "BOOLEAN DEFAULT 1"),
        ("affects_investment_value", "BOOLEAN DEFAULT 0"),
        ("security_symbol", "VARCHAR(20)"),
        ("security_quantity", "NUMERIC(15, 6)")
    ]

    # Add missing columns
    added_count = 0
    for col_name, col_def in columns_to_add:
        if col_name not in existing_columns:
            try:
                sql = f"ALTER TABLE transactions ADD COLUMN {col_name} {col_def}"
                cursor.execute(sql)
                print(f"  + Added column: {col_name}")
                added_count += 1
            except Exception as e:
                print(f"  ERROR adding {col_name}: {e}")
        else:
            print(f"  - Column exists: {col_name}")

    # Add indexes for new columns (only if they don't exist)
    indexes_to_add = [
        ("idx_account_id", "account_id"),
        ("idx_is_cleared", "is_cleared"),
        ("idx_security_symbol", "security_symbol")
    ]

    print("\nAdding indexes...")
    for idx_name, col_name in indexes_to_add:
        try:
            # Check if column exists before creating index
            if col_name in existing_columns or any(c[0] == col_name for c in columns_to_add):
                cursor.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON transactions({col_name})")
                print(f"  + Created index: {idx_name}")
        except Exception as e:
            print(f"  - Index may already exist: {idx_name}")

    # Commit changes
    conn.commit()

    # Verify the changes
    cursor.execute("PRAGMA table_info(transactions)")
    new_columns = [col[1] for col in cursor.fetchall()]
    print(f"\nFinal column count: {len(new_columns)}")
    print(f"Columns added: {added_count}")

    # Test query to ensure nothing is broken
    try:
        cursor.execute("SELECT COUNT(*) FROM transactions")
        count = cursor.fetchone()[0]
        print(f"Transaction count (verification): {count}")
        print("\n+ Migration completed successfully!")
    except Exception as e:
        print(f"\nERROR during verification: {e}")
        return False

    conn.close()
    return True

if __name__ == "__main__":
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else "financial_analysis.db"

    # Confirm before proceeding
    print(f"This will modify: {db_path}")
    print("A backup should already exist.")
    response = input("Continue? (yes/no): ")

    if response.lower() == 'yes':
        success = add_missing_columns(db_path)
        if success:
            print("\nSuccess! The database has been updated.")
            print("The application should now work correctly.")
        else:
            print("\nMigration failed. Please restore from backup.")
    else:
        print("Migration cancelled.")