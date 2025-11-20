"""
Database migration to add the accounts system tables and fields.

This migration adds support for account balance tracking, reconciliation,
and investment holdings management.

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
from financial_analysis.database.models import (
    Account, AccountBalance, InvestmentHolding, Reconciliation, Transaction
)


def check_table_exists(engine, table_name):
    """Check if a table exists in the database."""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def check_column_exists(engine, table_name, column_name):
    """Check if a column exists in a table."""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns


def run_migration(database_path=None):
    """
    Run the migration to add account system tables and fields.

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
            # Create new tables if they don't exist

            # 1. Create accounts table
            if not check_table_exists(engine, 'accounts'):
                print("Creating accounts table...")
                conn.execute(text("""
                    CREATE TABLE accounts (
                        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        account_name VARCHAR(100) NOT NULL,
                        account_type VARCHAR(50) NOT NULL,
                        account_subtype VARCHAR(50),
                        institution_name VARCHAR(100),
                        account_number_last4 VARCHAR(4),
                        currency VARCHAR(3) DEFAULT 'USD',
                        is_active BOOLEAN DEFAULT 1,
                        has_cash_component BOOLEAN DEFAULT 0,
                        has_investment_component BOOLEAN DEFAULT 0,
                        opening_balance NUMERIC(15, 2) DEFAULT 0,
                        opening_balance_date DATE,
                        notes TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        CHECK (account_type IN ('checking', 'savings', 'brokerage', 'investment',
                                'credit_card', 'loan', '401k', 'ira', 'other'))
                    )
                """))

                # Create indexes
                conn.execute(text("CREATE INDEX idx_account_type ON accounts(account_type)"))
                conn.execute(text("CREATE INDEX idx_account_active ON accounts(is_active)"))
                conn.execute(text("CREATE INDEX idx_account_institution ON accounts(institution_name)"))
                print("+ Accounts table created")
            else:
                print("Accounts table already exists")

            # 2. Create account_balances table
            if not check_table_exists(engine, 'account_balances'):
                print("Creating account_balances table...")
                conn.execute(text("""
                    CREATE TABLE account_balances (
                        balance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        account_id INTEGER NOT NULL,
                        balance_date DATE NOT NULL,
                        total_balance NUMERIC(15, 2) NOT NULL,
                        balance_type VARCHAR(20) DEFAULT 'statement',
                        cash_balance NUMERIC(15, 2),
                        investment_value NUMERIC(15, 2),
                        notes TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
                        UNIQUE (account_id, balance_date, balance_type),
                        CHECK (balance_type IN ('statement', 'calculated', 'reconciled'))
                    )
                """))

                # Create indexes
                conn.execute(text("CREATE INDEX idx_balance_account ON account_balances(account_id)"))
                conn.execute(text("CREATE INDEX idx_balance_date ON account_balances(balance_date)"))
                conn.execute(text("CREATE INDEX idx_balance_type ON account_balances(balance_type)"))
                print("+ Account balances table created")
            else:
                print("Account balances table already exists")

            # 3. Create investment_holdings table
            if not check_table_exists(engine, 'investment_holdings'):
                print("Creating investment_holdings table...")
                conn.execute(text("""
                    CREATE TABLE investment_holdings (
                        holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        account_id INTEGER NOT NULL,
                        symbol VARCHAR(20) NOT NULL,
                        description VARCHAR(200),
                        quantity NUMERIC(15, 6) NOT NULL,
                        cost_basis NUMERIC(15, 2),
                        current_value NUMERIC(15, 2),
                        as_of_date DATE NOT NULL,
                        asset_class VARCHAR(50),
                        sector VARCHAR(50),
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
                        UNIQUE (account_id, symbol, as_of_date)
                    )
                """))

                # Create indexes
                conn.execute(text("CREATE INDEX idx_holding_account ON investment_holdings(account_id)"))
                conn.execute(text("CREATE INDEX idx_holding_symbol ON investment_holdings(symbol)"))
                conn.execute(text("CREATE INDEX idx_holding_date ON investment_holdings(as_of_date)"))
                print("+ Investment holdings table created")
            else:
                print("Investment holdings table already exists")

            # 4. Create reconciliations table
            if not check_table_exists(engine, 'reconciliations'):
                print("Creating reconciliations table...")
                conn.execute(text("""
                    CREATE TABLE reconciliations (
                        reconciliation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        account_id INTEGER NOT NULL,
                        statement_date DATE NOT NULL,
                        statement_balance NUMERIC(15, 2) NOT NULL,
                        calculated_balance NUMERIC(15, 2) NOT NULL,
                        statement_cash_balance NUMERIC(15, 2),
                        calculated_cash_balance NUMERIC(15, 2),
                        statement_investment_value NUMERIC(15, 2),
                        calculated_investment_value NUMERIC(15, 2),
                        discrepancy_amount NUMERIC(15, 2),
                        is_reconciled BOOLEAN DEFAULT 0,
                        reconciled_at DATETIME,
                        reconciled_by VARCHAR(100),
                        transactions_cleared_count INTEGER DEFAULT 0,
                        transactions_pending_count INTEGER DEFAULT 0,
                        notes TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
                        UNIQUE (account_id, statement_date)
                    )
                """))

                # Create indexes
                conn.execute(text("CREATE INDEX idx_reconciliation_account ON reconciliations(account_id)"))
                conn.execute(text("CREATE INDEX idx_reconciliation_date ON reconciliations(statement_date)"))
                conn.execute(text("CREATE INDEX idx_reconciliation_status ON reconciliations(is_reconciled)"))
                print("+ Reconciliations table created")
            else:
                print("Reconciliations table already exists")

            # 5. Add new columns to transactions table
            if check_table_exists(engine, 'transactions'):
                print("Adding new columns to transactions table...")

                # Add account_id
                if not check_column_exists(engine, 'transactions', 'account_id'):
                    conn.execute(text("ALTER TABLE transactions ADD COLUMN account_id INTEGER REFERENCES accounts(account_id)"))
                    conn.execute(text("CREATE INDEX idx_account_id ON transactions(account_id)"))
                    print("+ Added account_id column")

                # Add is_cleared
                if not check_column_exists(engine, 'transactions', 'is_cleared'):
                    conn.execute(text("ALTER TABLE transactions ADD COLUMN is_cleared BOOLEAN DEFAULT 0"))
                    conn.execute(text("CREATE INDEX idx_is_cleared ON transactions(is_cleared)"))
                    print("+ Added is_cleared column")

                # Add cleared_date
                if not check_column_exists(engine, 'transactions', 'cleared_date'):
                    conn.execute(text("ALTER TABLE transactions ADD COLUMN cleared_date DATE"))
                    print("+ Added cleared_date column")

                # Add investment transaction fields
                if not check_column_exists(engine, 'transactions', 'affects_cash_balance'):
                    conn.execute(text("ALTER TABLE transactions ADD COLUMN affects_cash_balance BOOLEAN DEFAULT 1"))
                    print("+ Added affects_cash_balance column")

                if not check_column_exists(engine, 'transactions', 'affects_investment_value'):
                    conn.execute(text("ALTER TABLE transactions ADD COLUMN affects_investment_value BOOLEAN DEFAULT 0"))
                    print("+ Added affects_investment_value column")

                if not check_column_exists(engine, 'transactions', 'security_symbol'):
                    conn.execute(text("ALTER TABLE transactions ADD COLUMN security_symbol VARCHAR(20)"))
                    conn.execute(text("CREATE INDEX idx_security_symbol ON transactions(security_symbol)"))
                    print("+ Added security_symbol column")

                if not check_column_exists(engine, 'transactions', 'security_quantity'):
                    conn.execute(text("ALTER TABLE transactions ADD COLUMN security_quantity NUMERIC(15, 6)"))
                    print("+ Added security_quantity column")

                print("+ Transaction table updates complete")
            else:
                print("Warning: transactions table not found")

            # 6. Create initial accounts based on existing transaction data
            print("\nCreating initial accounts from existing transaction data...")

            # Get unique source values from transactions
            result = conn.execute(text("""
                SELECT DISTINCT source
                FROM transactions
                WHERE source IS NOT NULL AND source != ''
            """))

            sources = result.fetchall()

            if sources:
                print(f"Found {len(sources)} unique transaction sources")

                for source_row in sources:
                    source = source_row[0]

                    # Check if account already exists
                    existing = conn.execute(text("""
                        SELECT account_id FROM accounts
                        WHERE account_name = :name
                    """), {'name': source}).fetchone()

                    if not existing:
                        # Determine account type based on source name
                        account_type = 'other'  # Default

                        source_lower = source.lower()
                        if 'checking' in source_lower or 'direct deposit' in source_lower:
                            account_type = 'checking'
                        elif 'savings' in source_lower or 'emergency' in source_lower:
                            account_type = 'savings'
                        elif 'credit' in source_lower or 'card' in source_lower:
                            account_type = 'credit_card'
                        elif 'investment' in source_lower or 'brokerage' in source_lower or 'fidelity' in source_lower or 'vanguard' in source_lower:
                            account_type = 'brokerage'
                        elif '401k' in source_lower or '401(k)' in source_lower:
                            account_type = '401k'
                        elif 'ira' in source_lower:
                            account_type = 'ira'
                        elif 'loan' in source_lower or 'mortgage' in source_lower:
                            account_type = 'loan'

                        # Determine capabilities
                        has_cash = account_type in ['checking', 'savings', 'brokerage']
                        has_investments = account_type in ['brokerage', 'investment', '401k', 'ira']

                        # Create account
                        conn.execute(text("""
                            INSERT INTO accounts (
                                account_name, account_type, has_cash_component,
                                has_investment_component, is_active
                            ) VALUES (
                                :name, :type, :has_cash, :has_investments, 1
                            )
                        """), {
                            'name': source,
                            'type': account_type,
                            'has_cash': has_cash,
                            'has_investments': has_investments
                        })

                        print(f"  Created account: {source} ({account_type})")

                # Link transactions to accounts
                print("\nLinking transactions to accounts...")
                conn.execute(text("""
                    UPDATE transactions
                    SET account_id = (
                        SELECT account_id FROM accounts
                        WHERE accounts.account_name = transactions.source
                    )
                    WHERE source IS NOT NULL
                    AND source != ''
                    AND account_id IS NULL
                """))

                print("+ Transactions linked to accounts")
            else:
                print("No existing transaction sources found")

            print("\n+++ Migration completed successfully!")

    except OperationalError as e:
        print(f"ERROR: Migration failed: {e}")
        raise
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        raise


if __name__ == "__main__":
    # Allow specifying database path as command line argument
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else None
    run_migration(db_path)