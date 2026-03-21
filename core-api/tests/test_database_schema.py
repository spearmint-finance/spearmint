"""
Tests for database schema and models.

Verifies that all tables, relationships, and constraints are properly configured.
"""

import pytest
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from financial_analysis.database.base import Base
from financial_analysis.database.models import (
    Category,
    Transaction,
    TransactionRelationship,
    Tag,
    TransactionTag,
    ImportHistory,
    Budget
)


@pytest.fixture
def db_session():
    """Create a test database session."""
    # Use in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


def test_category_hierarchy(db_session):
    """Test category parent-child relationships."""
    # Create parent category
    parent = Category(
        category_name="Parent Category",
        category_type="Expense",
        description="Parent category"
    )
    db_session.add(parent)
    db_session.commit()

    # Create child category
    child = Category(
        category_name="Child Category",
        category_type="Expense",
        parent_category_id=parent.category_id,
        description="Child category"
    )
    db_session.add(child)
    db_session.commit()

    # Verify relationship
    assert child.parent_category.category_id == parent.category_id
    assert len(parent.subcategories) == 1
    assert parent.subcategories[0].category_name == "Child Category"


def test_transaction_creation(db_session):
    """Test creating a transaction with all required fields."""
    # Create category first
    category = Category(
        category_name="Groceries",
        category_type="Expense"
    )
    db_session.add(category)
    db_session.commit()

    # Create transaction
    transaction = Transaction(
        transaction_date=date(2025, 1, 15),
        amount=Decimal("125.50"),
        transaction_type="Expense",
        category_id=category.category_id,
        source="Whole Foods",
        description="Weekly groceries",
        payment_method="Credit Card",
        include_in_analysis=True
    )

    db_session.add(transaction)
    db_session.commit()

    # Verify
    result = db_session.query(Transaction).first()
    assert result is not None
    assert result.amount == Decimal("125.50")
    assert result.category.category_name == "Groceries"


def test_transaction_relationship(db_session):
    """Test linking two transactions with a relationship."""
    # Create category
    category = Category(category_name="Transfer", category_type="Transfer")
    db_session.add(category)
    db_session.commit()

    # Create two transactions
    tx1 = Transaction(
        transaction_date=date(2025, 1, 15),
        amount=Decimal("1000.00"),
        transaction_type="Expense",
        category_id=category.category_id,
        description="Transfer from Checking",
        transfer_account_from="Checking",
        transfer_account_to="Savings"
    )

    tx2 = Transaction(
        transaction_date=date(2025, 1, 15),
        amount=Decimal("1000.00"),
        transaction_type="Income",
        category_id=category.category_id,
        description="Transfer to Savings",
        transfer_account_from="Checking",
        transfer_account_to="Savings"
    )

    db_session.add_all([tx1, tx2])
    db_session.commit()

    # Create relationship
    relationship = TransactionRelationship(
        transaction_id_1=tx1.transaction_id,
        transaction_id_2=tx2.transaction_id,
        relationship_type="transfer_pair",
        description="Internal transfer between accounts"
    )

    db_session.add(relationship)
    db_session.commit()

    # Verify
    result = db_session.query(TransactionRelationship).first()
    assert result is not None
    assert result.relationship_type == "transfer_pair"


def test_tags_and_transaction_tags(db_session):
    """Test tagging transactions."""
    # Create category and transaction
    category = Category(category_name="Dining", category_type="Expense")
    db_session.add(category)
    db_session.commit()

    transaction = Transaction(
        transaction_date=date(2025, 1, 15),
        amount=Decimal("45.00"),
        transaction_type="Expense",
        category_id=category.category_id,
        description="Dinner with client"
    )
    db_session.add(transaction)
    db_session.commit()

    # Create tags
    tag1 = Tag(tag_name="business")
    tag2 = Tag(tag_name="deductible")
    db_session.add_all([tag1, tag2])
    db_session.commit()

    # Associate tags with transaction
    transaction.tags.append(tag1)
    transaction.tags.append(tag2)
    db_session.commit()

    # Verify
    result = db_session.query(Transaction).first()
    assert len(result.tags) == 2
    assert "business" in [tag.tag_name for tag in result.tags]
    assert "deductible" in [tag.tag_name for tag in result.tags]


def test_import_history(db_session):
    """Test recording import history."""
    import_record = ImportHistory(
        file_name="transactions_2025_01.xlsx",
        file_path="/data/transactions_2025_01.xlsx",
        total_rows=100,
        successful_rows=95,
        failed_rows=5,
        classified_rows=90,
        import_mode="append"
    )

    db_session.add(import_record)
    db_session.commit()

    # Verify
    result = db_session.query(ImportHistory).first()
    assert result is not None
    assert result.total_rows == 100
    assert result.successful_rows == 95
    assert result.failed_rows == 5


def test_budget(db_session):
    """Test creating a budget."""
    # Create category
    category = Category(category_name="Groceries", category_type="Expense")
    db_session.add(category)
    db_session.commit()

    # Create budget
    budget = Budget(
        category_id=category.category_id,
        budget_amount=Decimal("500.00"),
        period_type="Monthly",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31)
    )

    db_session.add(budget)
    db_session.commit()

    # Verify
    result = db_session.query(Budget).first()
    assert result is not None
    assert result.budget_amount == Decimal("500.00")
    assert result.period_type == "Monthly"
