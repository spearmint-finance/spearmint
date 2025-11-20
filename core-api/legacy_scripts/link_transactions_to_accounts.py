"""
Phase 4: Link existing transactions to accounts based on their source.

This script:
1. Creates real accounts based on transaction sources
2. Links transactions to appropriate accounts
3. Validates the linking process
"""

import sys
from pathlib import Path
from datetime import date
from collections import defaultdict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from financial_analysis.database.models import Transaction, Account
from financial_analysis.services.account_service import AccountService


def analyze_transaction_sources():
    """Analyze unique transaction sources to understand account needs."""

    engine = create_engine('sqlite:///financial_analysis.db')
    Session = sessionmaker(bind=engine)
    db = Session()

    print("=" * 70)
    print("ANALYZING TRANSACTION SOURCES")
    print("=" * 70)

    # Get unique sources and their transaction counts
    sources = db.execute(text("""
        SELECT source, COUNT(*) as count,
               SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_income,
               SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END) as total_expense
        FROM transactions
        WHERE source IS NOT NULL AND source != ''
        GROUP BY source
        ORDER BY count DESC
    """)).fetchall()

    print(f"\nFound {len(sources)} unique sources:\n")

    # Categorize sources
    account_mapping = {}

    for source, count, total_income, total_expense in sources:
        # Determine account type based on source name
        source_lower = source.lower()

        if 'investment' in source_lower or 'fidelity' in source_lower and 'investment' in source_lower:
            account_type = 'brokerage'
            institution = 'Fidelity Investments'
        elif 'direct deposit' in source_lower:
            account_type = 'checking'
            institution = 'Fidelity'
        elif 'checking' in source_lower or 'bank' in source_lower:
            account_type = 'checking'
            institution = source.split()[0] if ' ' in source else source
        elif 'savings' in source_lower or 'emergency' in source_lower:
            account_type = 'savings'
            institution = 'Fidelity'
        elif 'credit' in source_lower or 'card' in source_lower or 'citi' in source_lower or 'chase' in source_lower or 'amex' in source_lower or 'platinum' in source_lower:
            account_type = 'credit_card'
            # Extract institution from card name
            if 'citi' in source_lower:
                institution = 'Citibank'
            elif 'chase' in source_lower:
                institution = 'Chase'
            elif 'amex' in source_lower or 'american express' in source_lower:
                institution = 'American Express'
            else:
                institution = source.split()[0] if ' ' in source else 'Unknown'
        elif '401' in source or '401k' in source_lower or '401(k)' in source_lower:
            account_type = '401k'
            institution = 'Amazon' if 'amazon' in source_lower else 'Employer'
        elif 'ira' in source_lower:
            account_type = 'ira'
            institution = 'Fidelity'
        elif 'loan' in source_lower or 'mortgage' in source_lower or 'newport' in source_lower:
            account_type = 'loan'
            institution = 'Mortgage Lender'
        elif 'rsu' in source_lower or 'vested' in source_lower:
            account_type = 'brokerage'
            institution = 'Fidelity'
        else:
            account_type = 'other'
            institution = 'Unknown'

        account_mapping[source] = {
            'type': account_type,
            'institution': institution,
            'count': count,
            'income': float(total_income or 0),
            'expense': float(total_expense or 0)
        }

        net = float(total_income or 0) - float(total_expense or 0)
        print(f"{source[:40]:40} | {count:5} txns | ${net:12,.2f} net | Type: {account_type}")

    db.close()
    return account_mapping


def create_real_accounts(account_mapping):
    """Create real accounts based on transaction sources."""

    engine = create_engine('sqlite:///financial_analysis.db')
    Session = sessionmaker(bind=engine)
    db = Session()
    service = AccountService(db)

    print("\n" + "=" * 70)
    print("CREATING REAL ACCOUNTS")
    print("=" * 70)

    created_accounts = {}

    # Group sources by similar names to avoid duplicates
    account_groups = defaultdict(list)

    for source, info in account_mapping.items():
        # Create a normalized key for grouping
        key = source

        # Group similar credit card accounts
        if info['type'] == 'credit_card':
            if 'citi' in source.lower() and 'aadvantage' in source.lower():
                key = 'Citi AAdvantage Card'
            elif 'chase sapphire' in source.lower():
                key = 'Chase Sapphire Card'
            elif 'business platinum' in source.lower():
                key = 'Amex Business Platinum'
            elif 'credit card' in source.lower():
                if '9983' in source:
                    key = 'Citi AAdvantage Card'
                else:
                    key = source
        # Group investment accounts
        elif info['type'] == 'brokerage':
            if 'investments' in source.lower():
                key = 'Fidelity Investments'
            elif 'rsu' in source.lower():
                key = 'Fidelity RSU Account'
        # Group 401k accounts
        elif info['type'] == '401k':
            key = 'Amazon 401(k)'
        # Group checking accounts
        elif info['type'] == 'checking' and 'direct deposit' in source.lower():
            key = 'Fidelity Cash Management'

        account_groups[key].append(source)

    # Create accounts for each group
    for account_name, sources in account_groups.items():
        info = account_mapping[sources[0]]  # Use first source for info

        # Check if account already exists
        existing = db.query(Account).filter(Account.account_name == account_name).first()

        if existing:
            print(f"  Account already exists: {account_name}")
            created_accounts[account_name] = existing
            # Map all sources to this account
            for source in sources:
                account_mapping[source]['account_id'] = existing.account_id
        else:
            # Determine account properties
            account_data = {
                'account_name': account_name,
                'account_type': info['type'],
                'institution_name': info['institution'],
            }

            # Add special properties for brokerage accounts
            if info['type'] == 'brokerage':
                account_data['account_subtype'] = 'hybrid'
                account_data['notes'] = f"Linked to sources: {', '.join(sources[:3])}"

            try:
                account = service.create_account(**account_data)
                print(f"  + Created: {account_name} ({info['type']}) - {len(sources)} sources")
                created_accounts[account_name] = account

                # Map all sources to this account
                for source in sources:
                    account_mapping[source]['account_id'] = account.account_id

            except Exception as e:
                print(f"  ERROR creating {account_name}: {e}")

    db.commit()
    db.close()
    return created_accounts, account_mapping


def link_transactions_to_accounts(account_mapping):
    """Link transactions to their appropriate accounts."""

    engine = create_engine('sqlite:///financial_analysis.db')
    Session = sessionmaker(bind=engine)
    db = Session()

    print("\n" + "=" * 70)
    print("LINKING TRANSACTIONS TO ACCOUNTS")
    print("=" * 70)

    # Update transactions with account_id based on source
    total_updated = 0

    for source, info in account_mapping.items():
        if 'account_id' in info:
            count = db.execute(text("""
                UPDATE transactions
                SET account_id = :account_id
                WHERE source = :source
                AND account_id IS NULL
            """), {'account_id': info['account_id'], 'source': source}).rowcount

            if count > 0:
                total_updated += count
                print(f"  Linked {count} transactions from '{source[:40]}' to account_id {info['account_id']}")

    db.commit()

    # Verify the linking
    linked_count = db.query(Transaction).filter(Transaction.account_id.isnot(None)).count()
    unlinked_count = db.query(Transaction).filter(Transaction.account_id.is_(None)).count()

    print(f"\n  Total transactions updated: {total_updated}")
    print(f"  Transactions with accounts: {linked_count}")
    print(f"  Transactions without accounts: {unlinked_count}")

    db.close()
    return total_updated


def calculate_account_balances():
    """Calculate and display account balances from transactions."""

    engine = create_engine('sqlite:///financial_analysis.db')
    Session = sessionmaker(bind=engine)
    db = Session()
    service = AccountService(db)

    print("\n" + "=" * 70)
    print("CALCULATING ACCOUNT BALANCES")
    print("=" * 70)

    accounts = service.get_accounts(is_active=True)

    total_assets = 0
    total_liabilities = 0

    for account in accounts:
        # Calculate balance from transactions
        calculated = service.calculate_balance_from_transactions(
            account.account_id,
            date.today()
        )

        balance = calculated['total']

        # Add a balance snapshot
        if balance != 0:
            try:
                service.add_balance_snapshot(
                    account_id=account.account_id,
                    balance_date=date.today(),
                    total_balance=balance,
                    balance_type='calculated',
                    notes='Calculated from transaction history'
                )
            except:
                pass  # Balance might already exist

        # Track totals
        if account.account_type in ['credit_card', 'loan']:
            total_liabilities += abs(balance) if balance < 0 else balance
        else:
            total_assets += balance

        print(f"  {account.account_name:40} | ${balance:12,.2f}")

    print("\n  " + "-" * 60)
    print(f"  {'Total Assets':40} | ${total_assets:12,.2f}")
    print(f"  {'Total Liabilities':40} | ${total_liabilities:12,.2f}")
    print(f"  {'Net Worth':40} | ${(total_assets - total_liabilities):12,.2f}")

    db.close()


def cleanup_test_accounts():
    """Remove test accounts created during development."""

    engine = create_engine('sqlite:///financial_analysis.db')
    Session = sessionmaker(bind=engine)
    db = Session()

    print("\n" + "=" * 70)
    print("CLEANING UP TEST ACCOUNTS")
    print("=" * 70)

    # Test account names to remove
    test_account_names = [
        'Chase Checking',
        'Chase Sapphire',
        'Fidelity Investments',  # The test one without transactions
        'Direct Deposit',  # Test duplicates
        'INVESTMENTS',  # Test account
    ]

    for name in test_account_names:
        # Only delete if it has no linked transactions
        account = db.query(Account).filter(Account.account_name == name).first()
        if account:
            tx_count = db.query(Transaction).filter(Transaction.account_id == account.account_id).count()
            if tx_count == 0:
                db.delete(account)
                print(f"  Deleted test account: {name}")
            else:
                print(f"  Kept account with transactions: {name} ({tx_count} transactions)")

    db.commit()
    db.close()


def main():
    """Run the complete Phase 4 implementation."""

    print("\n" + "=" * 70)
    print("PHASE 4: MULTI-ACCOUNT SUPPORT IMPLEMENTATION")
    print("=" * 70)

    # Step 1: Analyze sources
    account_mapping = analyze_transaction_sources()

    # Step 2: Clean up test accounts
    cleanup_test_accounts()

    # Step 3: Create real accounts
    accounts, account_mapping = create_real_accounts(account_mapping)

    # Step 4: Link transactions
    link_transactions_to_accounts(account_mapping)

    # Step 5: Calculate balances
    calculate_account_balances()

    print("\n" + "=" * 70)
    print("PHASE 4 COMPLETE!")
    print("=" * 70)
    print("\nYour transactions are now linked to accounts.")
    print("Navigate to http://localhost:5173/accounts to see your real account balances.")


if __name__ == "__main__":
    # Auto-run for Phase 4 implementation
    print("\nStarting Phase 4: Linking transactions to accounts...")
    main()