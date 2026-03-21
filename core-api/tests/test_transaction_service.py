"""Tests for transaction service."""

import pytest
from datetime import date
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from financial_analysis.database.base import Base
from financial_analysis.database.models import Category
from financial_analysis.services.transaction_service import TransactionService, TransactionFilter
from financial_analysis.utils.validators import ValidationError


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Create test categories
    category1 = Category(
        category_name="Salary",
        category_type="Income"
    )
    category2 = Category(
        category_name="Groceries",
        category_type="Expense"
    )
    session.add_all([category1, category2])
    session.commit()
    
    yield session
    
    session.close()


class TestTransactionService:
    """Test TransactionService class."""
    
    def test_create_transaction(self, db_session):
        """Test creating a transaction."""
        service = TransactionService(db_session)
        
        # Get category
        category = db_session.query(Category).filter(Category.category_name == "Salary").first()
        
        transaction = service.create_transaction(
            transaction_date=date(2024, 1, 15),
            amount=Decimal("5000.00"),
            transaction_type="Income",
            category_id=category.category_id,
            description="Monthly salary"
        )
        
        assert transaction.transaction_id is not None
        assert transaction.amount == Decimal("5000.00")
        assert transaction.transaction_type == "Income"
        assert transaction.description == "Monthly salary"
    
    def test_create_transaction_with_tags(self, db_session):
        """Test creating a transaction with tags."""
        service = TransactionService(db_session)
        
        category = db_session.query(Category).filter(Category.category_name == "Groceries").first()
        
        transaction = service.create_transaction(
            transaction_date=date(2024, 1, 15),
            amount=Decimal("150.00"),
            transaction_type="Expense",
            category_id=category.category_id,
            description="Weekly groceries",
            tag_names=["food", "weekly"]
        )
        
        assert transaction.transaction_id is not None
        assert len(transaction.tags) == 2
        tag_names = [tag.tag_name for tag in transaction.tags]
        assert "food" in tag_names
        assert "weekly" in tag_names
    
    def test_create_transaction_invalid_category(self, db_session):
        """Test creating a transaction with invalid category."""
        service = TransactionService(db_session)
        
        with pytest.raises(ValidationError, match="Category with ID 999 not found"):
            service.create_transaction(
                transaction_date=date(2024, 1, 15),
                amount=Decimal("100.00"),
                transaction_type="Income",
                category_id=999
            )
    
    def test_get_transaction(self, db_session):
        """Test getting a transaction by ID."""
        service = TransactionService(db_session)
        
        category = db_session.query(Category).filter(Category.category_name == "Salary").first()
        
        # Create transaction
        created = service.create_transaction(
            transaction_date=date(2024, 1, 15),
            amount=Decimal("5000.00"),
            transaction_type="Income",
            category_id=category.category_id
        )
        
        # Get transaction
        retrieved = service.get_transaction(created.transaction_id)
        
        assert retrieved is not None
        assert retrieved.transaction_id == created.transaction_id
        assert retrieved.amount == Decimal("5000.00")
    
    def test_get_transaction_not_found(self, db_session):
        """Test getting a non-existent transaction."""
        service = TransactionService(db_session)
        
        transaction = service.get_transaction(999)
        assert transaction is None
    
    def test_list_transactions(self, db_session):
        """Test listing transactions."""
        service = TransactionService(db_session)
        
        category = db_session.query(Category).filter(Category.category_name == "Groceries").first()
        
        # Create multiple transactions
        for i in range(5):
            service.create_transaction(
                transaction_date=date(2024, 1, i + 1),
                amount=Decimal(f"{100 + i * 10}.00"),
                transaction_type="Expense",
                category_id=category.category_id,
                description=f"Transaction {i + 1}"
            )
        
        # List all transactions
        transactions = service.list_transactions()
        assert len(transactions) == 5
    
    def test_list_transactions_with_filters(self, db_session):
        """Test listing transactions with filters."""
        service = TransactionService(db_session)
        
        income_cat = db_session.query(Category).filter(Category.category_name == "Salary").first()
        expense_cat = db_session.query(Category).filter(Category.category_name == "Groceries").first()
        
        # Create income transactions
        for i in range(3):
            service.create_transaction(
                transaction_date=date(2024, 1, i + 1),
                amount=Decimal("5000.00"),
                transaction_type="Income",
                category_id=income_cat.category_id
            )
        
        # Create expense transactions
        for i in range(2):
            service.create_transaction(
                transaction_date=date(2024, 1, i + 1),
                amount=Decimal("100.00"),
                transaction_type="Expense",
                category_id=expense_cat.category_id
            )
        
        # Filter by type
        filters = TransactionFilter(transaction_type="Income")
        income_transactions = service.list_transactions(filters)
        assert len(income_transactions) == 3
        
        filters = TransactionFilter(transaction_type="Expense")
        expense_transactions = service.list_transactions(filters)
        assert len(expense_transactions) == 2
    
    def test_update_transaction(self, db_session):
        """Test updating a transaction."""
        service = TransactionService(db_session)
        
        category = db_session.query(Category).filter(Category.category_name == "Groceries").first()
        
        # Create transaction
        transaction = service.create_transaction(
            transaction_date=date(2024, 1, 15),
            amount=Decimal("100.00"),
            transaction_type="Expense",
            category_id=category.category_id,
            description="Original description"
        )
        
        # Update transaction
        updated = service.update_transaction(
            transaction.transaction_id,
            amount=Decimal("150.00"),
            description="Updated description"
        )
        
        assert updated is not None
        assert updated.amount == Decimal("150.00")
        assert updated.description == "Updated description"
    
    def test_update_transaction_not_found(self, db_session):
        """Test updating a non-existent transaction."""
        service = TransactionService(db_session)
        
        updated = service.update_transaction(999, amount=Decimal("100.00"))
        assert updated is None
    
    def test_delete_transaction(self, db_session):
        """Test deleting a transaction."""
        service = TransactionService(db_session)
        
        category = db_session.query(Category).filter(Category.category_name == "Groceries").first()
        
        # Create transaction
        transaction = service.create_transaction(
            transaction_date=date(2024, 1, 15),
            amount=Decimal("100.00"),
            transaction_type="Expense",
            category_id=category.category_id
        )
        
        # Delete transaction
        deleted = service.delete_transaction(transaction.transaction_id)
        assert deleted is True
        
        # Verify deletion
        retrieved = service.get_transaction(transaction.transaction_id)
        assert retrieved is None
    
    def test_delete_transaction_not_found(self, db_session):
        """Test deleting a non-existent transaction."""
        service = TransactionService(db_session)
        
        deleted = service.delete_transaction(999)
        assert deleted is False

