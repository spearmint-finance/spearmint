"""
Check income calculation for the date range shown in the screenshot.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from datetime import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from financial_analysis.database.models import Transaction

# Database connection
DATABASE_URL = "sqlite:///./financial_data.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Date range from screenshot (Sep 2 - Oct 2, 2025)
start_date = datetime(2025, 9, 2).date()
end_date = datetime(2025, 10, 2).date()

print(f"\n{'='*80}")
print(f"Checking Income Calculation for {start_date} to {end_date}")
print(f"{'='*80}\n")

# Get income transactions in this range
income_txns = db.query(Transaction).filter(
    Transaction.transaction_type == 'Income',
    Transaction.transaction_date >= start_date,
    Transaction.transaction_date <= end_date
).order_by(Transaction.transaction_date).all()

print(f"Found {len(income_txns)} income transactions\n")

if income_txns:
    print(f"{'Date':<12} {'Description':<50} {'Amount':>15} {'Include in Analysis':<20}")
    print(f"{'-'*100}")

    total = 0
    analysis_total = 0

    for t in income_txns:
        include_flag = "Yes" if t.include_in_analysis else "No"
        print(f"{str(t.transaction_date):<12} {t.description[:48]:<50} ${t.amount:>12,.2f}   {include_flag:<20}")
        total += t.amount
        if t.include_in_analysis:
            analysis_total += t.amount

    print(f"\n{'-'*100}")
    print(f"{'TOTAL (All):':<62} ${total:>12,.2f}")
    print(f"{'TOTAL (Analysis Mode - include_in_analysis=True):':<62} ${analysis_total:>12,.2f}")
else:
    print("No income transactions found in this date range.")

# Also check what the API would return
print(f"\n{'='*80}")
print(f"Checking what the API endpoint would calculate...")
print(f"{'='*80}\n")

# Simulate the analysis service logic
query = db.query(Transaction).filter(
    Transaction.transaction_type == 'Income'
)

# Apply ANALYSIS mode filter (like the API does)
query = query.filter(Transaction.include_in_analysis == True)

# Apply date range
query = query.filter(Transaction.transaction_date >= start_date)
query = query.filter(Transaction.transaction_date <= end_date)

api_transactions = query.all()
api_total = sum(t.amount for t in api_transactions)

print(f"API would return {len(api_transactions)} transactions")
print(f"API total income: ${api_total:,.2f}")

db.close()
