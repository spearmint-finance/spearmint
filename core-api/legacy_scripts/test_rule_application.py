"""
Test classification rule application.
"""
from src.financial_analysis.database.base import SessionLocal
from src.financial_analysis.database.models import Transaction, ClassificationRule, TransactionClassification
from sqlalchemy import and_

db = SessionLocal()

print("=" * 80)
print("Testing Classification Rule Application")
print("=" * 80)

# Get all active rules
rules = db.query(ClassificationRule).filter(
    ClassificationRule.is_active == True
).order_by(ClassificationRule.rule_priority).all()

print(f"\nFound {len(rules)} active rules:")
for rule in rules:
    print(f"  - {rule.rule_name} (Priority: {rule.rule_priority})")
    print(f"    Pattern: {rule.description_pattern}")
    print(f"    Classification ID: {rule.classification_id}")

print("\n" + "=" * 80)
print("Testing Pattern Matching")
print("=" * 80)

for rule in rules:
    print(f"\nRule: {rule.rule_name}")
    print(f"Pattern: {rule.description_pattern}")
    
    # Build query for matching transactions
    trans_query = db.query(Transaction)
    conditions = []
    
    if rule.description_pattern:
        conditions.append(Transaction.description.ilike(rule.description_pattern))
    
    if conditions:
        trans_query = trans_query.filter(and_(*conditions))
    
    # Get matching transactions
    matching_transactions = trans_query.limit(5).all()
    
    print(f"Matched {trans_query.count()} transactions (showing first 5):")
    for txn in matching_transactions:
        print(f"  - ID {txn.transaction_id}: {txn.description[:80]}")
        print(f"    Current Classification: {txn.classification_id}")

print("\n" + "=" * 80)
print("Sample Dividend Transactions")
print("=" * 80)

dividend_txns = db.query(Transaction).filter(
    Transaction.description.ilike('%dividend%')
).limit(10).all()

print(f"\nFound {len(dividend_txns)} dividend transactions:")
for txn in dividend_txns:
    classification = db.query(TransactionClassification).filter(
        TransactionClassification.classification_id == txn.classification_id
    ).first()
    
    print(f"\nID {txn.transaction_id}:")
    print(f"  Description: {txn.description[:80]}")
    print(f"  Type: {txn.transaction_type}")
    print(f"  Classification: {classification.classification_name if classification else 'None'} (ID: {txn.classification_id})")

db.close()

