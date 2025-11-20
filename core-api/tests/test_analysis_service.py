"""
Tests for analysis service.

Verifies income, expense, cash flow, and financial health analysis.
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from financial_analysis.database.base import Base
from financial_analysis.database.models import (
    Transaction, Category, TransactionClassification
)
from financial_analysis.services.analysis_service import (
    AnalysisService, DateRange, AnalysisMode, TimePeriod
)


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    # Create default classification
    standard_class = TransactionClassification(
        classification_name="Standard Transaction",
        classification_code="STANDARD",
        exclude_from_income_calc=False,
        exclude_from_expense_calc=False,
        exclude_from_cashflow_calc=False
    )
    session.add(standard_class)
    
    # Create transfer classification
    transfer_class = TransactionClassification(
        classification_name="Internal Transfer",
        classification_code="TRANSFER",
        exclude_from_income_calc=True,
        exclude_from_expense_calc=True,
        exclude_from_cashflow_calc=True
    )
    session.add(transfer_class)
    
    # Create categories
    salary_cat = Category(category_name="Salary", category_type="Income")
    groceries_cat = Category(category_name="Groceries", category_type="Expense")
    rent_cat = Category(category_name="Rent", category_type="Expense")
    transfer_cat = Category(category_name="Transfer", category_type="Both", is_transfer_category=True)
    
    session.add_all([salary_cat, groceries_cat, rent_cat, transfer_cat])
    session.commit()
    
    yield session
    
    session.close()


@pytest.fixture
def sample_transactions(db_session):
    """Create sample transactions for testing."""
    # Get categories and classifications
    salary_cat = db_session.query(Category).filter_by(category_name="Salary").first()
    groceries_cat = db_session.query(Category).filter_by(category_name="Groceries").first()
    rent_cat = db_session.query(Category).filter_by(category_name="Rent").first()
    transfer_cat = db_session.query(Category).filter_by(category_name="Transfer").first()
    
    standard_class = db_session.query(TransactionClassification).filter_by(
        classification_code="STANDARD"
    ).first()
    transfer_class = db_session.query(TransactionClassification).filter_by(
        classification_code="TRANSFER"
    ).first()
    
    # Create transactions
    today = date.today()
    
    transactions = [
        # Income
        Transaction(
            transaction_date=today - timedelta(days=30),
            amount=Decimal("5000.00"),
            transaction_type="Income",
            category_id=salary_cat.category_id,
            classification_id=standard_class.classification_id,
            description="Monthly salary",
            include_in_analysis=True
        ),
        Transaction(
            transaction_date=today - timedelta(days=60),
            amount=Decimal("5000.00"),
            transaction_type="Income",
            category_id=salary_cat.category_id,
            classification_id=standard_class.classification_id,
            description="Monthly salary",
            include_in_analysis=True
        ),
        # Expenses
        Transaction(
            transaction_date=today - timedelta(days=25),
            amount=Decimal("1500.00"),
            transaction_type="Expense",
            category_id=rent_cat.category_id,
            classification_id=standard_class.classification_id,
            description="Rent payment",
            include_in_analysis=True
        ),
        Transaction(
            transaction_date=today - timedelta(days=20),
            amount=Decimal("200.00"),
            transaction_type="Expense",
            category_id=groceries_cat.category_id,
            classification_id=standard_class.classification_id,
            description="Grocery shopping",
            include_in_analysis=True
        ),
        Transaction(
            transaction_date=today - timedelta(days=15),
            amount=Decimal("150.00"),
            transaction_type="Expense",
            category_id=groceries_cat.category_id,
            classification_id=standard_class.classification_id,
            description="Grocery shopping",
            include_in_analysis=True
        ),
        # Transfer (should be excluded from analysis)
        Transaction(
            transaction_date=today - timedelta(days=10),
            amount=Decimal("1000.00"),
            transaction_type="Expense",
            category_id=transfer_cat.category_id,
            classification_id=transfer_class.classification_id,
            description="Transfer to savings",
            include_in_analysis=False,
            is_transfer=True
        ),
    ]
    
    db_session.add_all(transactions)
    db_session.commit()
    
    return transactions


def test_analyze_income(db_session, sample_transactions):
    """Test income analysis."""
    service = AnalysisService(db_session)
    
    # Analyze all income
    result = service.analyze_income(mode=AnalysisMode.ANALYSIS)
    
    assert result.total_income == Decimal("10000.00")  # 2 x 5000
    assert result.transaction_count == 2
    assert result.average_transaction == Decimal("5000.00")
    assert result.mode == AnalysisMode.ANALYSIS
    assert "Salary" in result.breakdown_by_category


def test_analyze_expenses(db_session, sample_transactions):
    """Test expense analysis."""
    service = AnalysisService(db_session)
    
    # Analyze all expenses (should exclude transfer)
    result = service.analyze_expenses(mode=AnalysisMode.ANALYSIS)
    
    assert result.total_expenses == Decimal("1850.00")  # 1500 + 200 + 150
    assert result.transaction_count == 3
    assert result.mode == AnalysisMode.ANALYSIS
    assert "Rent" in result.breakdown_by_category
    assert "Groceries" in result.breakdown_by_category
    assert "Transfer" not in result.breakdown_by_category  # Should be excluded


def test_analyze_cash_flow(db_session, sample_transactions):
    """Test cash flow analysis."""
    service = AnalysisService(db_session)
    
    # Analyze cash flow
    result = service.analyze_cash_flow(mode=AnalysisMode.ANALYSIS)
    
    assert result.total_income == Decimal("10000.00")
    assert result.total_expenses == Decimal("1850.00")
    assert result.net_cash_flow == Decimal("8150.00")  # 10000 - 1850
    assert result.income_count == 2
    assert result.expense_count == 3


def test_financial_health_indicators(db_session, sample_transactions):
    """Test financial health indicators."""
    service = AnalysisService(db_session)
    
    # Get indicators
    result = service.get_financial_health_indicators()
    
    assert result.income_to_expense_ratio is not None
    assert result.income_to_expense_ratio > 1.0  # Income > Expenses
    assert result.savings_rate is not None
    assert result.savings_rate > 0.0  # Positive savings
    assert result.average_daily_income > Decimal(0)
    assert result.average_daily_expense > Decimal(0)


def test_date_range_filtering(db_session, sample_transactions):
    """Test date range filtering."""
    service = AnalysisService(db_session)
    
    today = date.today()
    date_range = DateRange(
        start_date=today - timedelta(days=35),
        end_date=today - timedelta(days=5)
    )
    
    # Analyze income in date range
    result = service.analyze_income(date_range=date_range, mode=AnalysisMode.ANALYSIS)
    
    # Should only include one salary transaction
    assert result.total_income == Decimal("5000.00")
    assert result.transaction_count == 1


def test_analysis_mode_complete(db_session, sample_transactions):
    """Test complete mode includes all transactions."""
    service = AnalysisService(db_session)
    
    # Analyze expenses in complete mode
    result = service.analyze_expenses(mode=AnalysisMode.COMPLETE)
    
    # Should include transfer in complete mode
    assert result.transaction_count == 4  # 3 regular + 1 transfer
    assert result.total_expenses == Decimal("2850.00")  # 1850 + 1000


def test_income_trends(db_session, sample_transactions):
    """Test income trends."""
    service = AnalysisService(db_session)
    
    # Get monthly trends
    trends = service.get_income_trends(period=TimePeriod.MONTHLY, mode=AnalysisMode.ANALYSIS)
    
    assert len(trends) > 0
    assert all(hasattr(t, 'period') for t in trends)
    assert all(hasattr(t, 'value') for t in trends)
    assert all(hasattr(t, 'count') for t in trends)


def test_expense_breakdown_by_category(db_session, sample_transactions):
    """Test expense breakdown by category."""
    service = AnalysisService(db_session)
    
    result = service.analyze_expenses(mode=AnalysisMode.ANALYSIS)
    
    # Check breakdown
    assert "Rent" in result.breakdown_by_category
    assert "Groceries" in result.breakdown_by_category
    
    # Check Rent category
    rent_data = result.breakdown_by_category["Rent"]
    assert rent_data['total'] == Decimal("1500.00")
    assert rent_data['count'] == 1
    
    # Check Groceries category
    groceries_data = result.breakdown_by_category["Groceries"]
    assert groceries_data['total'] == Decimal("350.00")  # 200 + 150
    assert groceries_data['count'] == 2

