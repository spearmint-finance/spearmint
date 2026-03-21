"""
Seed standard transaction tags.

These tags replace common classification use-cases with a more flexible
tagging system (Phase 1 of the classification-to-tags refactor).
"""

from sqlalchemy.orm import Session
from .base import SessionLocal
from .models import Tag


STANDARD_TAGS = [
    {
        "tag_name": "capital-expense",
        "description": "Capital expenditure (replaces CAPITAL_EXPENSE classification)",
    },
    {
        "tag_name": "tax-deductible",
        "description": "Tax deductible expense",
    },
    {
        "tag_name": "recurring",
        "description": "Recurring transaction",
    },
    {
        "tag_name": "reimbursable",
        "description": "Expense that should be reimbursed",
    },
    {
        "tag_name": "exclude-from-income",
        "description": "Exclude from income analysis (replaces exclude_from_income_calc)",
    },
    {
        "tag_name": "exclude-from-expenses",
        "description": "Exclude from expense analysis (replaces exclude_from_expense_calc)",
    },
]


def seed_tags(db: Session) -> None:
    """
    Seed standard transaction tags.

    Args:
        db: Database session
    """
    print("Seeding transaction tags...")

    for tag_data in STANDARD_TAGS:
        # Check if tag already exists
        existing = db.query(Tag).filter_by(
            tag_name=tag_data["tag_name"]
        ).first()

        if existing:
            print(f"  [SKIP] '{tag_data['tag_name']}' (already exists)")
            continue

        # Create new tag (Tag model only has tag_name; description is for documentation)
        tag = Tag(tag_name=tag_data["tag_name"])
        db.add(tag)
        print(f"  [ADDED] '{tag_data['tag_name']}'")

    db.commit()
    print("[SUCCESS] Tag seeding complete!")


def main():
    """Run the seeding script."""
    db = SessionLocal()
    try:
        seed_tags(db)
    except Exception as e:
        print(f"[ERROR] Error seeding tags: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
