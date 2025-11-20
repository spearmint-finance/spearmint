"""
Create classification rules for dividend and reinvestment transactions.
This will allow the system to automatically classify dividend income and reinvestment expenses.
"""
from src.financial_analysis.database.base import SessionLocal
from src.financial_analysis.database.models import TransactionClassification, ClassificationRule

db = SessionLocal()

try:
    # Get the classification IDs
    investment_dist_class = db.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'INVESTMENT_DISTRIBUTION'
    ).first()
    
    dividend_reinv_class = db.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'DIVIDEND_REINVESTMENT'
    ).first()
    
    if not investment_dist_class or not dividend_reinv_class:
        print("ERROR: Required classifications not found!")
        db.close()
        exit(1)
    
    print(f"Investment Distribution Classification ID: {investment_dist_class.classification_id}")
    print(f"Dividend Reinvestment Classification ID: {dividend_reinv_class.classification_id}")
    print()
    
    # Create rules for dividend income (INVESTMENT_DISTRIBUTION)
    # Note: description_pattern uses SQL LIKE syntax, so % is wildcard
    dividend_rules = [
        {
            'rule_name': 'Dividend Income - Contains "DIVIDEND RECEIVED"',
            'classification_id': investment_dist_class.classification_id,
            'description_pattern': '%DIVIDEND RECEIVED%',
            'rule_priority': 100,
        },
        {
            'rule_name': 'Dividend Income - Contains "DIVIDEND"',
            'classification_id': investment_dist_class.classification_id,
            'description_pattern': '%DIVIDEND%',
            'rule_priority': 90,
        },
        {
            'rule_name': 'Dividend Income - Contains "DIV"',
            'classification_id': investment_dist_class.classification_id,
            'description_pattern': '% DIV %',
            'rule_priority': 85,
        },
    ]

    # Create rules for reinvestment expenses (DIVIDEND_REINVESTMENT)
    reinvestment_rules = [
        {
            'rule_name': 'Dividend Reinvestment - Contains "REINVESTMENT"',
            'classification_id': dividend_reinv_class.classification_id,
            'description_pattern': '%REINVESTMENT%',
            'rule_priority': 100,
        },
        {
            'rule_name': 'Dividend Reinvestment - Contains "REINVEST"',
            'classification_id': dividend_reinv_class.classification_id,
            'description_pattern': '%REINVEST%',
            'rule_priority': 95,
        },
        {
            'rule_name': 'Dividend Reinvestment - Contains "DRIP"',
            'classification_id': dividend_reinv_class.classification_id,
            'description_pattern': '%DRIP%',
            'rule_priority': 90,
        },
        {
            'rule_name': 'Dividend Reinvestment - Contains "AUTO REINVEST"',
            'classification_id': dividend_reinv_class.classification_id,
            'description_pattern': '%AUTO REINVEST%',
            'rule_priority': 95,
        },
    ]
    
    all_rules = dividend_rules + reinvestment_rules
    
    print("Creating classification rules...")
    print("=" * 80)
    
    created_count = 0
    skipped_count = 0
    
    for rule_data in all_rules:
        # Check if rule already exists
        existing_rule = db.query(ClassificationRule).filter(
            ClassificationRule.rule_name == rule_data['rule_name']
        ).first()
        
        if existing_rule:
            print(f"⊘ SKIPPED: {rule_data['rule_name']} (already exists)")
            skipped_count += 1
            continue
        
        # Create new rule
        new_rule = ClassificationRule(
            rule_name=rule_data['rule_name'],
            classification_id=rule_data['classification_id'],
            description_pattern=rule_data['description_pattern'],
            rule_priority=rule_data['rule_priority'],
            is_active=True
        )
        
        db.add(new_rule)
        print(f"✓ CREATED: {rule_data['rule_name']}")
        created_count += 1
    
    db.commit()
    
    print()
    print("=" * 80)
    print(f"Summary:")
    print(f"  Created: {created_count} rules")
    print(f"  Skipped: {skipped_count} rules (already existed)")
    print()
    print("✓ Classification rules created successfully!")
    print()
    print("Next steps:")
    print("1. Go to the Classifications page in the UI")
    print("2. Click 'Apply Rules' to classify existing transactions")
    print("3. Or use the API: POST /api/classifications/apply-rules")
    print("4. Then click 'Detect Relationships' to link dividend/reinvestment pairs")
    
except Exception as e:
    print(f"ERROR: {e}")
    db.rollback()
    raise
finally:
    db.close()

