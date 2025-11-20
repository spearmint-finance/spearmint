"""
Seed standard transaction classifications.

This script adds predefined classification types for handling special
transaction types like refunds, reimbursements, and rewards.
"""

from sqlalchemy.orm import Session
from .base import SessionLocal
from .models import TransactionClassification


STANDARD_CLASSIFICATIONS = [
    {
        "classification_name": "Transfer",
        "classification_code": "TRANSFER",
        "description": "Money moved between accounts (excluded from all analysis)",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": True,
        "exclude_from_cashflow_calc": True,
        "is_system_classification": True,
    },
    {
        "classification_name": "Refund/Return",
        "classification_code": "REFUND",
        "description": "Money returned from a previous purchase (offsets expenses, not counted as income)",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": False,
        "is_system_classification": True,
    },
    {
        "classification_name": "Credit Card Reward",
        "classification_code": "CREDIT_CARD_REWARD",
        "description": "Credit card points/cashback redemption (offsets expenses, not earned income)",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": False,
        "is_system_classification": True,
    },
    {
        "classification_name": "Work Reimbursement",
        "classification_code": "REIMBURSEMENT",
        "description": "Employer reimbursement for work expenses (not counted as income)",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": False,
        "is_system_classification": True,
    },
    {
        "classification_name": "Reimbursable Expense",
        "classification_code": "REIMBURSABLE_EXPENSE",
        "description": "Expense that will be reimbursed (not counted as personal expense)",
        "exclude_from_income_calc": False,
        "exclude_from_expense_calc": True,
        "exclude_from_cashflow_calc": False,
        "is_system_classification": True,
    },
    {
        "classification_name": "Insurance Reimbursement",
        "classification_code": "INSURANCE_REIMBURSEMENT",
        "description": "Insurance reimbursement for medical/other expenses (not counted as income)",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": False,
        "is_system_classification": True,
    },
    {
        "classification_name": "Investment Distribution",
        "classification_code": "INVESTMENT_DISTRIBUTION",
        "description": "Dividend or capital gains distribution (counted as income)",
        "exclude_from_income_calc": False,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": False,
        "is_system_classification": True,
    },
    {
        "classification_name": "Dividend Reinvestment",
        "classification_code": "DIVIDEND_REINVESTMENT",
        "description": "Automatic reinvestment of dividend income into the same security. Apply to EXPENSE transactions representing the purchase of additional shares. The dividend itself should use INVESTMENT_DISTRIBUTION classification. Not counted as expense (it's an investment) and excluded from cash flow (automatic reinvestment).",
        "exclude_from_income_calc": True,
        "exclude_from_expense_calc": True,
        "exclude_from_cashflow_calc": True,
        "is_system_classification": True,
    },
    {
        "classification_name": "Regular Transaction",
        "classification_code": "REGULAR",
        "description": "Standard transaction (included in all calculations)",
        "exclude_from_income_calc": False,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": False,
        "is_system_classification": True,
    },
]


def seed_classifications(db: Session) -> None:
    """
    Seed standard transaction classifications.

    Args:
        db: Database session
    """
    print("Seeding transaction classifications...")

    for classification_data in STANDARD_CLASSIFICATIONS:
        # Check if classification already exists
        existing = db.query(TransactionClassification).filter_by(
            classification_code=classification_data["classification_code"]
        ).first()

        if existing:
            print(f"  [SKIP] '{classification_data['classification_name']}' (already exists)")
            continue

        # Create new classification
        classification = TransactionClassification(**classification_data)
        db.add(classification)
        print(f"  [ADDED] '{classification_data['classification_name']}'")

    db.commit()
    print("[SUCCESS] Classification seeding complete!")


def main():
    """Run the seeding script."""
    db = SessionLocal()
    try:
        seed_classifications(db)
    except Exception as e:
        print(f"[ERROR] Error seeding classifications: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
