"""
Seed data for database initialization.

Populates default transaction classifications and sample classification rules
as specified in PRD Section 3.2.2.
"""

import hashlib
import os
from sqlalchemy.orm import Session
from .models import TransactionClassification, ClassificationRule, APIKey


DEFAULT_CLASSIFICATIONS = [
    {
        "classification_name": "Standard Transaction",
        "classification_code": "STANDARD",
        "description": "Regular income or expense transaction",
        "exclude_from_income_calc": False,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": False,
        "is_system_classification": True
    },
    {
        "classification_name": "Internal Transfer",
        "classification_code": "TRANSFER",
        "description": "Transfer between own accounts (excluded from all calculations)",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": True,
        "exclude_from_cashflow_calc": True,
        "is_system_classification": True
    },
    {
        "classification_name": "Credit Card Payment",
        "classification_code": "CC_PAYMENT",
        "description": "Payment to credit card (excluded from all calculations to prevent double-counting)",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": True,
        "exclude_from_cashflow_calc": True,
        "is_system_classification": True
    },
    {
        "classification_name": "Credit Card Receipt",
        "classification_code": "CC_RECEIPT",
        "description": "Credit card company receiving payment (excluded from all calculations to prevent double-counting)",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": True,
        "exclude_from_cashflow_calc": True,
        "is_system_classification": True
    },
    {
        "classification_name": "Reimbursement Paid",
        "classification_code": "REIMB_PAID",
        "description": "Expense paid that will be reimbursed",
        "exclude_from_income_calc": False,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": False,
        "is_system_classification": True
    },
    {
        "classification_name": "Reimbursement Received",
        "classification_code": "REIMB_RECEIVED",
        "description": "Reimbursement income received (excluded from income calculations)",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": True,
        "is_system_classification": True
    },
    {
        "classification_name": "Refund",
        "classification_code": "REFUND",
        "description": "Refund of previous expense (excluded from income calculations)",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": False,
        "is_system_classification": True
    },
    {
        "classification_name": "Loan Disbursement",
        "classification_code": "LOAN_DISB",
        "description": "Loan amount received (excluded from income calculations)",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": True,
        "is_system_classification": True
    },
    {
        "classification_name": "Loan Payment - Principal",
        "classification_code": "LOAN_PRINCIPAL",
        "description": "Principal portion of loan payment (excluded from expense calculations)",
        "exclude_from_income_calc": False,
        "exclude_from_expense_calc": True,
        "exclude_from_cashflow_calc": True,
        "is_system_classification": True
    },
    {
        "classification_name": "Loan Payment - Interest",
        "classification_code": "LOAN_INTEREST",
        "description": "Interest portion of loan payment (included as expense)",
        "exclude_from_income_calc": False,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": False,
        "is_system_classification": True
    },
    {
        "classification_name": "Capital Expense",
        "classification_code": "CAPITAL_EXPENSE",
        "description": "Purchase of long-term assets (property, equipment, vehicles) excluded from operating expenses",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": True,
        "exclude_from_cashflow_calc": True,
        "is_system_classification": True
    },
    {
        "classification_name": "Reinvestment",
        "classification_code": "REINVESTMENT",
        "description": "Reinvestment of dividends or capital gains (excluded from all calculations)",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": True,
        "exclude_from_cashflow_calc": True,
        "is_system_classification": True
    }
]


DEFAULT_CLASSIFICATION_RULES = [
    {
        "rule_name": "Credit Card Payment Detection",
        "rule_priority": 10,
        "classification_code": "CC_PAYMENT",
        "description_pattern": "%credit card payment%",
        "set_include_in_analysis": False,
        "set_is_transfer": True,
        "is_active": True
    },
    {
        "rule_name": "Transfer Detection",
        "rule_priority": 20,
        "classification_code": "TRANSFER",
        "description_pattern": "%transfer%",
        "set_include_in_analysis": False,
        "set_is_transfer": True,
        "is_active": True
    },
    {
        "rule_name": "Reimbursement Detection",
        "rule_priority": 30,
        "classification_code": "REIMB_RECEIVED",
        "description_pattern": "%reimbursement%",
        "set_include_in_analysis": False,
        "set_is_transfer": False,
        "is_active": True
    },
    {
        "rule_name": "Default: Standard Transaction",
        "rule_priority": 9999,
        "classification_code": "STANDARD",
        # No patterns => matches everything, but runs last due to low priority
        "is_active": True
    }
]


def seed_classifications(db: Session) -> None:
    """
    Seed default transaction classifications.
    
    Args:
        db: Database session
    """
    print("Seeding transaction classifications...")
    
    for classification_data in DEFAULT_CLASSIFICATIONS:
        # Check if classification already exists
        existing = db.query(TransactionClassification).filter_by(
            classification_code=classification_data["classification_code"]
        ).first()
        
        if not existing:
            classification = TransactionClassification(**classification_data)
            db.add(classification)
            print(f"  [OK] Added: {classification_data['classification_name']}")
        else:
            print(f"  - Skipped (exists): {classification_data['classification_name']}")

    db.commit()
    print("[OK] Transaction classifications seeded successfully")


def seed_classification_rules(db: Session) -> None:
    """
    Seed default classification rules.
    
    Args:
        db: Database session
    """
    print("\nSeeding classification rules...")
    
    for rule_data in DEFAULT_CLASSIFICATION_RULES:
        # Get classification ID
        classification = db.query(TransactionClassification).filter_by(
            classification_code=rule_data.pop("classification_code")
        ).first()
        
        if not classification:
            print(f"  [ERROR] Classification not found for rule: {rule_data['rule_name']}")
            continue

        # Check if rule already exists
        existing = db.query(ClassificationRule).filter_by(
            rule_name=rule_data["rule_name"]
        ).first()

        if not existing:
            rule = ClassificationRule(
                classification_id=classification.classification_id,
                **rule_data
            )
            db.add(rule)
            print(f"  [OK] Added: {rule_data['rule_name']}")
        else:
            print(f"  - Skipped (exists): {rule_data['rule_name']}")

    db.commit()
    print("[OK] Classification rules seeded successfully")


# Demo API key for development/testing (43 chars total)
# Key: smint_live_demokey1234567890abcdefghijklmn
DEMO_API_KEY = "smint_live_demokey1234567890abcdefghijklmn"
DEMO_API_KEY_HASH = hashlib.sha256(DEMO_API_KEY.encode()).hexdigest()


def seed_api_keys(db: Session) -> None:
    """
    Seed a demo API key for development/testing.

    The demo key is: smint_live_demo1234567890abcdef

    Args:
        db: Database session
    """
    print("\nSeeding demo API key...")

    # Check if demo key already exists
    existing = db.query(APIKey).filter_by(name="Demo Key (Development)").first()

    if not existing:
        demo_key = APIKey(
            name="Demo Key (Development)",
            key_prefix="smint_live_demo...",
            key_hash=DEMO_API_KEY_HASH,
            is_active=True,
        )
        db.add(demo_key)
        db.commit()
        print(f"  [OK] Added demo API key")
        print(f"  [INFO] Demo key for testing: {DEMO_API_KEY}")
    else:
        print(f"  - Skipped (exists): Demo Key")


def seed_all(db: Session) -> None:
    """
    Seed all default data.

    Args:
        db: Database session
    """
    seed_classifications(db)
    seed_classification_rules(db)
    seed_api_keys(db)
    print("\n[OK] All seed data loaded successfully")

