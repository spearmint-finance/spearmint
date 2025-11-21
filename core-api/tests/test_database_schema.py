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
    TransactionClassification,
    Category,
    Transaction,
    TransactionRelationship,
    ClassificationRule,
    Tag,
    TransactionTag,
    ImportHistory,
    Budget
)
from financial_analysis.database.seed_data import seed_classifications


@pytest.fixture
def db_session():
    """Create a test database session."""
    # Use in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Seed classifications for tests
    seed_classifications(session)
    
    yield session
    
    session.close()


def test_transaction_classification_creation(db_session):
    """Test creating a transaction classification."""
    classification = TransactionClassification(
        classification_name="Test Classification",
        classification_code="TEST",
        description="Test description",
        exclude_from_income_calc=False,
        exclude_from_expense_calc=True,
        exclude_from_cashflow_calc=False,
        is_system_classification=False
    )
    
    db_session.add(classification)
    db_session.commit()
    
    # Verify
    result = db_session.query(TransactionClassification).filter_by(
        classification_code="TEST"
    ).first()
    
    assert result is not None
    assert result.classification_name == "Test Classification"
    assert result.exclude_from_expense_calc is True


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
    
    # Get classification
    classification = db_session.query(TransactionClassification).filter_by(
        classification_code="STANDARD"
    ).first()
    
    # Create transaction
    transaction = Transaction(
        transaction_date=date(2025, 1, 15),
        amount=Decimal("125.50"),
        transaction_type="Expense",
        category_id=category.category_id,
        source="Whole Foods",
        description="Weekly groceries",
        payment_method="Credit Card",
        classification_id=classification.classification_id,
        include_in_analysis=True,
        is_transfer=False
    )
    
    db_session.add(transaction)
    db_session.commit()
    
    # Verify
    result = db_session.query(Transaction).first()
    assert result is not None
    assert result.amount == Decimal("125.50")
    assert result.category.category_name == "Groceries"
    assert result.classification.classification_code == "STANDARD"


def test_transaction_relationship(db_session):
    """Test linking two transactions with a relationship."""
    # Create category
    category = Category(category_name="Transfer", category_type="Both")
    db_session.add(category)
    db_session.commit()
    
    # Get transfer classification
    classification = db_session.query(TransactionClassification).filter_by(
        classification_code="TRANSFER"
    ).first()
    
    # Create two transactions
    tx1 = Transaction(
        transaction_date=date(2025, 1, 15),
        amount=Decimal("1000.00"),
        transaction_type="Expense",
        category_id=category.category_id,
        description="Transfer from Checking",
        classification_id=classification.classification_id,
        is_transfer=True,
        transfer_account_from="Checking",
        transfer_account_to="Savings"
    )
    
    tx2 = Transaction(
        transaction_date=date(2025, 1, 15),
        amount=Decimal("1000.00"),
        transaction_type="Income",
        category_id=category.category_id,
        description="Transfer to Savings",
        classification_id=classification.classification_id,
        is_transfer=True,
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


def test_classification_rule(db_session):
    """Test creating a classification rule."""
    # Get classification
    classification = db_session.query(TransactionClassification).filter_by(
        classification_code="CC_PAYMENT"
    ).first()
    
    # Create rule
    rule = ClassificationRule(
        rule_name="Detect Credit Card Payments",
        rule_priority=10,
        classification_id=classification.classification_id,
        description_pattern="%credit card%",
        is_active=True,
        set_include_in_analysis=False,
        set_is_transfer=True
    )
    
    db_session.add(rule)
    db_session.commit()
    
    # Verify
    result = db_session.query(ClassificationRule).filter_by(
        rule_name="Detect Credit Card Payments"
    ).first()
    
    assert result is not None
    assert result.rule_priority == 10
    assert result.classification.classification_code == "CC_PAYMENT"


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


def test_seeded_classifications(db_session):
    """Test that all 12 default classifications were seeded."""
    classifications = db_session.query(TransactionClassification).all()

    # Should have 12 default classifications
    assert len(classifications) == 12

    # Verify specific classifications exist
    codes = [c.classification_code for c in classifications]
    expected_codes = [
        "STANDARD", "TRANSFER", "CC_PAYMENT", "CC_RECEIPT",
        "REIMB_PAID", "REIMB_RECEIVED", "REFUND",
        "LOAN_DISB", "LOAN_PRINCIPAL", "LOAN_INTEREST",
        "CAPITAL_EXPENSE", "REINVESTMENT"
    ]
    
    for code in expected_codes:
        assert code in codes
    
    # Verify exclusion flags for TRANSFER
    transfer = db_session.query(TransactionClassification).filter_by(
        classification_code="TRANSFER"
    ).first()
    
    assert transfer.exclude_from_income_calc is True
    assert transfer.exclude_from_expense_calc is True
    assert transfer.exclude_from_cashflow_calc is True

