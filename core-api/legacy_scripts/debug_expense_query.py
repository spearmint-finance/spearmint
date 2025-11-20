from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from src.financial_analysis.database.models import Transaction, TransactionClassification
from datetime import datetime

engine = create_engine('sqlite:///./financial_analysis.db')
Session = sessionmaker(bind=engine)
db = Session()

print("=== Testing Expense Query Logic ===\n")

# Build the query like the backend does
query = db.query(Transaction).filter(Transaction.amount < 0)
query = query.filter(Transaction.include_in_analysis == True)
query = query.filter(Transaction.is_transfer == False)

# Join with classifications
query = query.outerjoin(
    TransactionClassification,
    Transaction.classification_id == TransactionClassification.classification_id
)

# Filter out capital expenses (exclude_from_expense_calc == True)
query = query.filter(
    or_(
        TransactionClassification.exclude_from_expense_calc == False,
        TransactionClassification.exclude_from_expense_calc == None
    )
)

transactions = query.all()

print(f"Total expense transactions in ANALYSIS mode: {len(transactions)}")
print(f"Total expense amount: ${sum(t.amount for t in transactions):,.2f}\n")

# Check if any capital expense transactions are in the results
capital_expense_in_results = [t for t in transactions if t.classification and t.classification.classification_code == 'CAPITAL_EXPENSE']

print(f"Capital expense transactions in results: {len(capital_expense_in_results)}")

if capital_expense_in_results:
    print("\n❌ ERROR: Capital expenses are NOT being excluded!")
    print("Sample capital expense transactions that shouldn't be included:")
    for t in capital_expense_in_results[:3]:
        print(f"  - ID: {t.transaction_id}, Amount: ${t.amount:,.2f}, Classification: {t.classification.classification_name if t.classification else 'None'}")
else:
    print("\n✅ SUCCESS: Capital expenses are correctly excluded!")

db.close()
