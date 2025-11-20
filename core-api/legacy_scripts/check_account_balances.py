"""Check account balances and identify issues."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.financial_analysis.database.session import SessionLocal
from src.financial_analysis.database.models import Account, Transaction
from sqlalchemy import func
from decimal import Decimal

def main():
    db = SessionLocal()

    print("\n" + "=" * 70)
    print("ACCOUNT BALANCE ANALYSIS")
    print("=" * 70)

    # Get all accounts with their stored balances
    accounts = db.query(Account).order_by(Account.account_name).all()

    print("\nStored Account Balances:")
    print("-" * 70)
    total_assets = Decimal(0)
    total_liabilities = Decimal(0)

    for account in accounts:
        balance = account.current_balance or Decimal(0)
        print(f"{account.account_name:<40} | ${balance:>12,.2f}")

        if account.account_type in ['checking', 'savings', 'brokerage', '401k']:
            total_assets += balance
        elif account.account_type in ['credit_card', 'loan']:
            total_liabilities += balance

    print("-" * 70)
    print(f"{'Total Assets':<40} | ${total_assets:>12,.2f}")
    print(f"{'Total Liabilities':<40} | ${total_liabilities:>12,.2f}")
    print(f"{'Net Worth':<40} | ${(total_assets + total_liabilities):>12,.2f}")

    # Check transaction sums by account
    print("\nTransaction Sums by Account (Raw):")
    print("-" * 70)

    results = db.query(
        Account.account_name,
        Account.account_type,
        func.sum(Transaction.amount).label('total'),
        func.count(Transaction.transaction_id).label('count')
    ).join(Transaction).group_by(Account.account_id).all()

    for name, acc_type, total, count in results:
        total_val = float(total or 0)
        print(f"{name:<40} | ${total_val:>12,.2f} | {count:>5} txns | Type: {acc_type}")

    # Check for income/expense classification issues
    print("\nTransaction Type Analysis:")
    print("-" * 70)

    for account in accounts:
        income_sum = db.query(func.sum(Transaction.amount)).filter(
            Transaction.account_id == account.account_id,
            Transaction.transaction_type == 'Income'
        ).scalar() or 0

        expense_sum = db.query(func.sum(Transaction.amount)).filter(
            Transaction.account_id == account.account_id,
            Transaction.transaction_type == 'Expense'
        ).scalar() or 0

        if income_sum != 0 or expense_sum != 0:
            print(f"{account.account_name:<30} | Income: ${float(income_sum):>12,.2f} | Expense: ${float(expense_sum):>12,.2f}")

    # Check specific problematic accounts
    print("\nPotential Issues:")
    print("-" * 70)

    # Check 401k transactions
    amazon_401k = db.query(Account).filter_by(account_name='Amazon 401(k)').first()
    if amazon_401k:
        transactions = db.query(Transaction).filter_by(account_id=amazon_401k.account_id).limit(5).all()
        print(f"\nSample Amazon 401(k) transactions:")
        for t in transactions:
            print(f"  {t.transaction_date} | {t.description[:40]:<40} | ${t.amount:>12,.2f} | {t.transaction_type}")

    # Check if transfers are being double counted
    transfer_count = db.query(func.count(Transaction.transaction_id)).filter(
        Transaction.is_transfer == True
    ).scalar()

    non_transfer_count = db.query(func.count(Transaction.transaction_id)).filter(
        Transaction.is_transfer == False
    ).scalar()

    print(f"\nTransfer Status:")
    print(f"  Transfers: {transfer_count}")
    print(f"  Non-transfers: {non_transfer_count}")

    db.close()

if __name__ == "__main__":
    main()