"""
Pytest configuration and fixtures for integration tests.

Provides shared fixtures for database setup, test client, and test data.
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from financial_analysis.database.models import Base, Category, Transaction, TransactionClassification
from financial_analysis.api.dependencies import get_db
from financial_analysis.database.seed_data import seed_classifications as project_seed_classifications


# Test database URL (in-memory SQLite with shared cache for better session isolation)
TEST_DATABASE_URL = None  # Will be set per test


@pytest.fixture(scope="function")
def test_db_engine():
    """Create a test database engine."""
    # Use in-memory database with StaticPool to ensure all connections share the same database
    # This solves the session isolation issue where different sessions couldn't see each other's data
    test_db_url = "sqlite:///:memory:"

    engine = create_engine(
        test_db_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Use StaticPool to share a single connection
        echo=False  # Set to True for SQL debugging
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """Create a test database session.

    Uses a simple approach: create a fresh session for each test and rely on
    the in-memory database being recreated for each test.
    """
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_db_engine,
        expire_on_commit=False
    )
    session = TestingSessionLocal()

    # Seed system classifications using the project's canonical seeder
    project_seed_classifications(session)

    yield session

    session.close()


@pytest.fixture(scope="function")
def client(test_db_session):
    """Create a test client with database override.

    Key insight: We need to ensure all API calls see the same session state.
    The issue was that service commits were creating transaction boundaries.

    Solution: Monkey-patch the session's commit method to use flush instead during tests.
    This allows services to "commit" (which becomes a flush) without creating isolation.
    """
    from financial_analysis.api.main import app
    from financial_analysis.api.dependencies import get_db

    # Save the original commit method
    original_commit = test_db_session.commit

    # Replace commit with flush during tests
    # This allows services to call commit() without creating transaction boundaries
    test_db_session.commit = test_db_session.flush

    # Override get_db to use the test session
    def override_get_db():
        try:
            yield test_db_session
        finally:
            pass  # Session is managed by the fixture

    # Clear any existing overrides first
    app.dependency_overrides.clear()

    # Set the override
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Restore the original commit method
    test_db_session.commit = original_commit

    # Clean up
    app.dependency_overrides.clear()


    


@pytest.fixture(scope="function")
def sample_categories(test_db_session):
    """Create sample categories for testing."""
    categories = [
        Category(
            category_id=1,
            category_name="Salary",
            category_type="Income",
            parent_category_id=None
        ),
        Category(
            category_id=2,
            category_name="Groceries",
            category_type="Expense",
            parent_category_id=None
        ),
        Category(
            category_id=3,
            category_name="Utilities",
            category_type="Expense",
            parent_category_id=None
        ),
        Category(
            category_id=4,
            category_name="Entertainment",
            category_type="Expense",
            parent_category_id=None
        ),
    ]

    for category in categories:
        test_db_session.add(category)

    test_db_session.commit()

    return categories


@pytest.fixture(scope="function")
def sample_transactions(test_db_session, sample_categories):
    """Create sample transactions for testing."""
    today = date.today()
    
    transactions = [
        # Income transactions
        Transaction(
            transaction_id=1,
            transaction_date=today - timedelta(days=30),
            description="Monthly Salary",
            amount=Decimal("5000.00"),
            transaction_type="Income",
            category_id=1,
            classification_id=1
        ),
        Transaction(
            transaction_id=2,
            transaction_date=today - timedelta(days=15),
            description="Bonus",
            amount=Decimal("1000.00"),
            transaction_type="Income",
            category_id=1,
            classification_id=1
        ),
        # Expense transactions
        Transaction(
            transaction_id=3,
            transaction_date=today - timedelta(days=25),
            description="Grocery Shopping",
            amount=Decimal("150.00"),
            transaction_type="Expense",
            category_id=2,
            classification_id=1
        ),
        Transaction(
            transaction_id=4,
            transaction_date=today - timedelta(days=20),
            description="Electric Bill",
            amount=Decimal("100.00"),
            transaction_type="Expense",
            category_id=3,
            classification_id=1
        ),
        Transaction(
            transaction_id=5,
            transaction_date=today - timedelta(days=10),
            description="Movie Tickets",
            amount=Decimal("50.00"),
            transaction_type="Expense",
            category_id=4,
            classification_id=1
        ),
        # Transfer pair
        Transaction(
            transaction_id=6,
            transaction_date=today - timedelta(days=5),
            description="Transfer to Savings",
            amount=Decimal("500.00"),
            transaction_type="Expense",
            category_id=2,  # Need a category
            classification_id=2,
            include_in_analysis=False
        ),
        Transaction(
            transaction_id=7,
            transaction_date=today - timedelta(days=5),
            description="Transfer from Checking",
            amount=Decimal("500.00"),
            transaction_type="Income",
            category_id=1,  # Need a category
            classification_id=2,
            include_in_analysis=False
        ),
    ]
    
    for transaction in transactions:
        test_db_session.add(transaction)
    
    test_db_session.commit()
    
    return transactions


@pytest.fixture(scope="function")
def auth_headers():
    """Create authentication headers (for future use)."""
    return {
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="function")
def sample_csv_data():
    """Create sample CSV data for import testing."""
    csv_content = """Date,Description,Amount,Type,Category
2025-01-01,Salary,5000.00,CREDIT,Salary
2025-01-05,Groceries,150.00,DEBIT,Groceries
2025-01-10,Electric Bill,100.00,DEBIT,Utilities
2025-01-15,Bonus,1000.00,CREDIT,Salary
2025-01-20,Movie Tickets,50.00,DEBIT,Entertainment
"""
    return csv_content


# Helper functions for common operations

def create_transaction(client, transaction_data):
    """Helper to create a transaction via API."""
    response = client.post("/api/transactions", json=transaction_data)
    return response


def get_transaction(client, transaction_id):
    """Helper to get a transaction via API."""
    response = client.get(f"/api/transactions/{transaction_id}")
    return response


def create_category(client, category_data):
    """Helper to create a category via API."""
    response = client.post("/api/categories", json=category_data)
    return response


def get_income_analysis(client, start_date=None, end_date=None, mode="analysis"):
    """Helper to get income analysis via API."""
    params = {"mode": mode}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    
    response = client.get("/api/analysis/income", params=params)
    return response


def get_expense_analysis(client, start_date=None, end_date=None, mode="analysis"):
    """Helper to get expense analysis via API."""
    params = {"mode": mode}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    
    response = client.get("/api/analysis/expenses", params=params)
    return response

