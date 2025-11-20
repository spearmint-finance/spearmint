"""Check which income transactions are marked as transfers."""
import sys
sys.path.insert(0, '.')

from src.financial_analysis.database.base import get_db
from src.financial_analysis.database.models import Transaction

db = next(get_db())

# Get income transactions marked as transfers
transfers = db.query(Transaction).filter(
    Transaction.transaction_type == 'Income',
    Transaction.is_transfer == True
).all()

print(f"\nIncome transactions marked as transfers ({len(transfers)} total):")
for t in transfers:
    cat_name = t.category.category_name if t.category else "None"
    print(f"  - {t.transaction_date}: {t.description} = ${t.amount} (category: {cat_name})")

# Get "Credit Card Payment" income transactions
ccp_transactions = db.query(Transaction).filter(
    Transaction.transaction_type == 'Income'
).join(Transaction.category).filter(
    Transaction.category.has(category_name='Credit Card Payment')
).all()

print(f"\n'Credit Card Payment' income transactions ({len(ccp_transactions)} total):")
for t in ccp_transactions:
    print(f"  - {t.transaction_date}: {t.description} = ${t.amount} (is_transfer: {t.is_transfer})")

db.close()
