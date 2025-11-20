from src.financial_analysis.database.base import SessionLocal
from src.financial_analysis.database.models import TransactionClassification, Transaction

db = SessionLocal()

print("Available Classifications:")
print("-" * 80)
classifications = db.query(TransactionClassification).all()
for c in classifications:
    print(f"{c.classification_id:3d} | {c.classification_code:30s} | {c.classification_name}")

print("\n" + "=" * 80)
print("Checking for dividend/reinvestment transactions:")
print("=" * 80)

# Check for INVESTMENT_DISTRIBUTION classification
div_class = db.query(TransactionClassification).filter(
    TransactionClassification.classification_code == 'INVESTMENT_DISTRIBUTION'
).first()

if div_class:
    print(f"\n✓ Found INVESTMENT_DISTRIBUTION classification (ID: {div_class.classification_id})")
    div_count = db.query(Transaction).filter(
        Transaction.classification_id == div_class.classification_id
    ).count()
    print(f"  Transactions with this classification: {div_count}")
else:
    print("\n✗ INVESTMENT_DISTRIBUTION classification not found!")

# Check for DIVIDEND_REINVESTMENT classification
reinv_class = db.query(TransactionClassification).filter(
    TransactionClassification.classification_code == 'DIVIDEND_REINVESTMENT'
).first()

if reinv_class:
    print(f"\n✓ Found DIVIDEND_REINVESTMENT classification (ID: {reinv_class.classification_id})")
    reinv_count = db.query(Transaction).filter(
        Transaction.classification_id == reinv_class.classification_id
    ).count()
    print(f"  Transactions with this classification: {reinv_count}")
else:
    print("\n✗ DIVIDEND_REINVESTMENT classification not found!")

# Check for transactions with "dividend" or "reinvest" in description
print("\n" + "=" * 80)
print("Transactions with 'dividend' or 'reinvest' in description:")
print("=" * 80)

dividend_txns = db.query(Transaction).filter(
    Transaction.description.ilike('%dividend%')
).limit(5).all()

print(f"\nFound {len(dividend_txns)} transactions with 'dividend' in description (showing first 5):")
for tx in dividend_txns:
    classification = db.query(TransactionClassification).filter(
        TransactionClassification.classification_id == tx.classification_id
    ).first()
    class_name = classification.classification_name if classification else "None"
    print(f"  ID: {tx.transaction_id:5d} | Date: {tx.transaction_date} | Amount: ${tx.amount:10.2f} | Type: {tx.transaction_type:8s} | Classification: {class_name}")

reinvest_txns = db.query(Transaction).filter(
    Transaction.description.ilike('%reinvest%')
).limit(5).all()

print(f"\nFound {len(reinvest_txns)} transactions with 'reinvest' in description (showing first 5):")
for tx in reinvest_txns:
    classification = db.query(TransactionClassification).filter(
        TransactionClassification.classification_id == tx.classification_id
    ).first()
    class_name = classification.classification_name if classification else "None"
    print(f"  ID: {tx.transaction_id:5d} | Date: {tx.transaction_date} | Amount: ${tx.amount:10.2f} | Type: {tx.transaction_type:8s} | Classification: {class_name}")

db.close()

