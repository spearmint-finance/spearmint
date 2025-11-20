"""
Apply classification rules directly to transactions.
"""
from src.financial_analysis.database.base import SessionLocal
from src.financial_analysis.database.models import Transaction, ClassificationRule
from sqlalchemy import and_

db = SessionLocal()

print("=" * 80)
print("Applying Classification Rules to Transactions")
print("=" * 80)

# Get all active rules ordered by priority
rules = db.query(ClassificationRule).filter(
    ClassificationRule.is_active == True
).order_by(ClassificationRule.rule_priority).all()

print(f"\nFound {len(rules)} active rules")

total_updated = 0

for rule in rules:
    print(f"\nProcessing: {rule.rule_name} (Priority: {rule.rule_priority})")
    
    # Build query for matching transactions
    trans_query = db.query(Transaction)
    conditions = []
    
    if rule.description_pattern:
        conditions.append(Transaction.description.ilike(rule.description_pattern))
    
    if rule.category_pattern:
        from src.financial_analysis.database.models import Category
        trans_query = trans_query.join(Category, Transaction.category_id == Category.category_id, isouter=True)
        conditions.append(Category.category_name.ilike(rule.category_pattern))
    
    if rule.source_pattern:
        conditions.append(Transaction.source.ilike(rule.source_pattern))
    
    if rule.amount_min is not None:
        conditions.append(Transaction.amount >= rule.amount_min)
    
    if rule.amount_max is not None:
        conditions.append(Transaction.amount <= rule.amount_max)
    
    if rule.payment_method_pattern:
        conditions.append(Transaction.payment_method.ilike(rule.payment_method_pattern))
    
    if conditions:
        trans_query = trans_query.filter(and_(*conditions))
    
    # Get matching transactions
    matching_transactions = trans_query.all()
    count = len(matching_transactions)
    
    if count > 0:
        # Update classification for all matching transactions
        transaction_ids = [t.transaction_id for t in matching_transactions]
        db.query(Transaction).filter(
            Transaction.transaction_id.in_(transaction_ids)
        ).update(
            {Transaction.classification_id: rule.classification_id},
            synchronize_session=False
        )
        
        print(f"  ✓ Updated {count} transactions to classification ID {rule.classification_id}")
        total_updated += count
    else:
        print(f"  - No matching transactions")

# Commit all changes
db.commit()

print("\n" + "=" * 80)
print(f"✓ Successfully updated {total_updated} transactions!")
print("=" * 80)

# Verify the updates
print("\nVerifying updates...")
dividend_income = db.query(Transaction).filter(
    Transaction.classification_id == 17  # Investment Distribution
).count()

dividend_reinv = db.query(Transaction).filter(
    Transaction.classification_id == 18  # Dividend Reinvestment
).count()

print(f"  - Investment Distribution (ID 17): {dividend_income} transactions")
print(f"  - Dividend Reinvestment (ID 18): {dividend_reinv} transactions")

db.close()

print("\n" + "=" * 80)
print("Next step: Go to Transactions page and click 'Detect Relationships'!")
print("=" * 80)

