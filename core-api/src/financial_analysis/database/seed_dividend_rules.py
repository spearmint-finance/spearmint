"""
Seed classification rules for dividend reinvestment detection.

This script adds auto-classification rules to detect dividend reinvestment
transactions based on description patterns.
"""

from sqlalchemy.orm import Session
from .models import TransactionClassification, ClassificationRule


DIVIDEND_REINVESTMENT_RULES = [
    {
        "rule_name": "Dividend Reinvestment - DRIP",
        "classification_code": "DIVIDEND_REINVESTMENT",
        "description_pattern": "%DRIP%",
        "rule_priority": 15,
        "description": "Detect DRIP (Dividend Reinvestment Plan) transactions"
    },
    {
        "rule_name": "Dividend Reinvestment - Reinvest",
        "classification_code": "DIVIDEND_REINVESTMENT",
        "description_pattern": "%REINVEST%",
        "rule_priority": 15,
        "description": "Detect reinvestment transactions"
    },
    {
        "rule_name": "Dividend Reinvestment - Auto Reinvest",
        "classification_code": "DIVIDEND_REINVESTMENT",
        "description_pattern": "%AUTO REINVEST%",
        "rule_priority": 14,
        "description": "Detect automatic reinvestment transactions"
    },
    {
        "rule_name": "Dividend Reinvestment - Dividend Reinvestment",
        "classification_code": "DIVIDEND_REINVESTMENT",
        "description_pattern": "%DIVIDEND REINVESTMENT%",
        "rule_priority": 13,
        "description": "Detect dividend reinvestment transactions"
    },
    {
        "rule_name": "Dividend Reinvestment - Reinvestment of Dividend",
        "classification_code": "DIVIDEND_REINVESTMENT",
        "description_pattern": "%REINVESTMENT OF DIVIDEND%",
        "rule_priority": 13,
        "description": "Detect reinvestment of dividend transactions"
    }
]


def seed_dividend_reinvestment_rules(db: Session) -> None:
    """
    Seed classification rules for dividend reinvestment detection.
    
    Args:
        db: Database session
    """
    print("\n" + "="*80)
    print("Seeding Dividend Reinvestment Classification Rules")
    print("="*80)
    
    # Get the DIVIDEND_REINVESTMENT classification
    classification = db.query(TransactionClassification).filter_by(
        classification_code="DIVIDEND_REINVESTMENT"
    ).first()
    
    if not classification:
        print("[ERROR] DIVIDEND_REINVESTMENT classification not found!")
        print("        Please run seed_classifications.py first to create the classification.")
        return
    
    print(f"[INFO] Found classification: {classification.classification_name}")
    print(f"       Classification ID: {classification.classification_id}")
    print()
    
    added_count = 0
    updated_count = 0
    skipped_count = 0
    
    for rule_data in DIVIDEND_REINVESTMENT_RULES:
        # Check if rule already exists
        existing_rule = db.query(ClassificationRule).filter_by(
            rule_name=rule_data["rule_name"]
        ).first()
        
        if existing_rule:
            # Update existing rule
            existing_rule.classification_id = classification.classification_id
            existing_rule.description_pattern = rule_data["description_pattern"]
            existing_rule.rule_priority = rule_data["rule_priority"]
            print(f"[UPDATED] '{rule_data['rule_name']}'")
            updated_count += 1
        else:
            # Create new rule
            new_rule = ClassificationRule(
                classification_id=classification.classification_id,
                rule_name=rule_data["rule_name"],
                description_pattern=rule_data["description_pattern"],
                rule_priority=rule_data["rule_priority"],
                is_active=True
            )
            db.add(new_rule)
            print(f"[ADDED] '{rule_data['rule_name']}'")
            added_count += 1
    
    try:
        db.commit()
        print()
        print("="*80)
        print("[SUCCESS] Dividend reinvestment rule seeding complete!")
        print(f"          Added: {added_count} rules")
        print(f"          Updated: {updated_count} rules")
        print(f"          Skipped: {skipped_count} rules")
        print("="*80)
    except Exception as e:
        db.rollback()
        print()
        print("="*80)
        print(f"[ERROR] Failed to seed rules: {str(e)}")
        print("="*80)
        raise


if __name__ == "__main__":
    """Run the seeding script directly."""
    from .base import SessionLocal
    
    db = SessionLocal()
    try:
        seed_dividend_reinvestment_rules(db)
    finally:
        db.close()

