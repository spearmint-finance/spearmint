"""
Tests for projection service.
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.financial_analysis.database.base import Base
from src.financial_analysis.database.models import Transaction, Category, TransactionClassification
from src.financial_analysis.database.seed_data import seed_classifications
from src.financial_analysis.services.projection_service import ProjectionService, ProjectionMethod


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Seed classifications
    seed_classifications(session)
    
    yield session
    
    session.close()


@pytest.fixture
def sample_data(db_session):
    """Create sample transaction data for testing."""
    # Create category
    category = Category(
        category_name="Test Income",
        category_type="Income"
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    
    # Get standard classification
    standard_class = db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'STANDARD'
    ).first()
    
    # Create 90 days of historical data with upward trend
    base_date = date.today() - timedelta(days=90)
    transactions = []
    
    for i in range(90):
        tx_date = base_date + timedelta(days=i)
        # Create income with slight upward trend
        amount = Decimal('100.00') + Decimal(str(i * 0.5))  # Increases by $0.50 per day
        
        tx = Transaction(
            transaction_date=tx_date,
            amount=amount,
            transaction_type='Income',
            category_id=category.category_id,
            description=f'Daily income {i}',
            source='Test Source',
            classification_id=standard_class.classification_id
        )
        transactions.append(tx)
    
    db_session.add_all(transactions)
    db_session.commit()
    
    return {
        'category': category,
        'classification': standard_class,
        'start_date': base_date,
        'end_date': date.today() - timedelta(days=1),
        'transaction_count': 90
    }


def test_project_income_linear_regression(db_session, sample_data):
    """Test income projection using linear regression."""
    service = ProjectionService(db_session)
    
    result = service.project_income(
        start_date=sample_data['start_date'],
        end_date=sample_data['end_date'],
        projection_days=30,
        method=ProjectionMethod.LINEAR_REGRESSION,
        confidence_level=0.95
    )
    
    # Verify structure
    assert result['projection_type'] == 'income'
    assert result['method'] == ProjectionMethod.LINEAR_REGRESSION
    assert result['confidence_level'] == 0.95
    
    # Verify historical period
    assert result['historical_period']['days'] == 89  # 90 days - 1
    assert result['historical_period']['total_income'] > 0
    
    # Verify projection period
    assert result['projection_period']['days'] == 30
    
    # Verify projections
    assert result['projected_total'] > 0
    assert result['confidence_interval']['lower'] <= result['projected_total']
    assert result['confidence_interval']['upper'] >= result['projected_total']
    
    # Verify daily projections
    assert len(result['daily_projections']) == 30
    assert all('date' in dp for dp in result['daily_projections'])
    assert all('projected_value' in dp for dp in result['daily_projections'])
    
    # Verify model metrics
    assert 'r_squared' in result['model_metrics']
    assert 'slope' in result['model_metrics']
    assert result['model_metrics']['slope'] > 0  # Should detect upward trend


def test_project_income_moving_average(db_session, sample_data):
    """Test income projection using moving average."""
    service = ProjectionService(db_session)
    
    result = service.project_income(
        start_date=sample_data['start_date'],
        end_date=sample_data['end_date'],
        projection_days=30,
        method=ProjectionMethod.MOVING_AVERAGE,
        confidence_level=0.95
    )
    
    assert result['projection_type'] == 'income'
    assert result['method'] == ProjectionMethod.MOVING_AVERAGE
    assert result['projected_total'] > 0
    assert 'moving_average' in result['model_metrics']


def test_project_income_exponential_smoothing(db_session, sample_data):
    """Test income projection using exponential smoothing."""
    service = ProjectionService(db_session)
    
    result = service.project_income(
        start_date=sample_data['start_date'],
        end_date=sample_data['end_date'],
        projection_days=30,
        method=ProjectionMethod.EXPONENTIAL_SMOOTHING,
        confidence_level=0.95
    )
    
    assert result['projection_type'] == 'income'
    assert result['method'] == ProjectionMethod.EXPONENTIAL_SMOOTHING
    assert result['projected_total'] > 0
    assert 'smoothed_value' in result['model_metrics']
    assert 'alpha' in result['model_metrics']


def test_project_income_weighted_average(db_session, sample_data):
    """Test income projection using weighted average."""
    service = ProjectionService(db_session)
    
    result = service.project_income(
        start_date=sample_data['start_date'],
        end_date=sample_data['end_date'],
        projection_days=30,
        method=ProjectionMethod.WEIGHTED_AVERAGE,
        confidence_level=0.95
    )
    
    assert result['projection_type'] == 'income'
    assert result['method'] == ProjectionMethod.WEIGHTED_AVERAGE
    assert result['projected_total'] > 0
    assert 'weighted_average' in result['model_metrics']


def test_project_expenses(db_session):
    """Test expense projection."""
    # Create expense category and transactions
    category = Category(
        category_name="Test Expenses",
        category_type="Expense"
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    
    standard_class = db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'STANDARD'
    ).first()
    
    # Create 60 days of expense data
    base_date = date.today() - timedelta(days=60)
    for i in range(60):
        tx = Transaction(
            transaction_date=base_date + timedelta(days=i),
            amount=Decimal('50.00'),
            transaction_type='Expense',
            category_id=category.category_id,
            description=f'Daily expense {i}',
            source='Test Source',
            classification_id=standard_class.classification_id
        )
        db_session.add(tx)
    
    db_session.commit()
    
    service = ProjectionService(db_session)
    result = service.project_expenses(
        start_date=base_date,
        end_date=date.today() - timedelta(days=1),
        projection_days=30,
        method=ProjectionMethod.LINEAR_REGRESSION
    )
    
    assert result['projection_type'] == 'expenses'
    assert result['projected_total'] > 0
    assert len(result['daily_projections']) == 30


def test_project_cashflow(db_session, sample_data):
    """Test cash flow projection with scenarios."""
    # Add some expenses
    expense_category = Category(
        category_name="Test Expenses",
        category_type="Expense"
    )
    db_session.add(expense_category)
    db_session.commit()
    db_session.refresh(expense_category)
    
    standard_class = db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'STANDARD'
    ).first()
    
    base_date = sample_data['start_date']
    for i in range(90):
        tx = Transaction(
            transaction_date=base_date + timedelta(days=i),
            amount=Decimal('60.00'),
            transaction_type='Expense',
            category_id=expense_category.category_id,
            description=f'Daily expense {i}',
            source='Test Source',
            classification_id=standard_class.classification_id
        )
        db_session.add(tx)
    
    db_session.commit()
    
    service = ProjectionService(db_session)
    result = service.project_cashflow(
        start_date=sample_data['start_date'],
        end_date=sample_data['end_date'],
        projection_days=30,
        method=ProjectionMethod.LINEAR_REGRESSION,
        include_scenarios=True
    )
    
    # Verify structure
    assert result['projection_type'] == 'cashflow'
    assert result['projected_income'] > 0
    assert result['projected_expenses'] > 0
    assert result['projected_cashflow'] == result['projected_income'] - result['projected_expenses']
    
    # Verify confidence intervals
    assert result['confidence_interval']['lower'] <= result['projected_cashflow']
    assert result['confidence_interval']['upper'] >= result['projected_cashflow']
    
    # Verify daily projections
    assert len(result['daily_projections']) == 30
    for dp in result['daily_projections']:
        assert 'projected_income' in dp
        assert 'projected_expenses' in dp
        assert 'projected_cashflow' in dp
        assert dp['projected_cashflow'] == dp['projected_income'] - dp['projected_expenses']
    
    # Verify scenarios
    assert 'scenarios' in result
    assert 'expected' in result['scenarios']
    assert 'best_case' in result['scenarios']
    assert 'worst_case' in result['scenarios']
    
    # Best case should have highest or equal cash flow
    assert result['scenarios']['best_case']['cashflow'] >= result['scenarios']['expected']['cashflow']
    # Worst case should have lowest or equal cash flow
    assert result['scenarios']['worst_case']['cashflow'] <= result['scenarios']['expected']['cashflow']


def test_calculate_accuracy_metrics(db_session):
    """Test accuracy metrics calculation."""
    service = ProjectionService(db_session)
    
    actual = [100.0, 105.0, 110.0, 108.0, 115.0]
    predicted = [98.0, 107.0, 109.0, 110.0, 113.0]
    
    metrics = service.calculate_accuracy_metrics(actual, predicted)
    
    assert 'mape' in metrics
    assert 'rmse' in metrics
    assert 'mae' in metrics
    assert 'r_squared' in metrics
    assert 'accuracy_grade' in metrics
    assert metrics['sample_size'] == 5
    
    # MAPE should be reasonable for this data
    assert 0 < metrics['mape'] < 10  # Should be "Excellent"
    assert metrics['accuracy_grade'] == "Excellent"


def test_empty_data_projection(db_session):
    """Test projection with no historical data."""
    service = ProjectionService(db_session)
    
    result = service.project_income(
        start_date=date.today() - timedelta(days=30),
        end_date=date.today(),
        projection_days=30,
        method=ProjectionMethod.LINEAR_REGRESSION
    )
    
    # Should return empty result
    assert result['projected_total'] == 0.0
    assert 'error' in result
    assert len(result['daily_projections']) == 0

