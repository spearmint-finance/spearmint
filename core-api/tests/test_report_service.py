"""
Tests for report service.
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from financial_analysis.database.base import Base
from financial_analysis.database.models import Transaction, Category, TransactionClassification
from financial_analysis.database.seed_data import seed_classifications
from financial_analysis.services.report_service import ReportService, AnalysisMode


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
    # Create categories
    income_cat = Category(category_name="Salary", category_type="Income")
    expense_cat1 = Category(category_name="Groceries", category_type="Expense")
    expense_cat2 = Category(category_name="Utilities", category_type="Expense")
    
    db_session.add_all([income_cat, expense_cat1, expense_cat2])
    db_session.commit()
    
    # Get standard classification
    standard_class = db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'STANDARD'
    ).first()
    
    # Create transactions for last 30 days
    base_date = date.today() - timedelta(days=30)
    
    # Income transactions
    for i in range(5):
        tx = Transaction(
            transaction_date=base_date + timedelta(days=i*6),
            amount=Decimal('1000.00'),
            transaction_type='Income',
            category_id=income_cat.category_id,
            description=f'Salary payment {i}',
            source='Test Source',
            classification_id=standard_class.classification_id
        )
        db_session.add(tx)
    
    # Expense transactions - Groceries
    for i in range(10):
        tx = Transaction(
            transaction_date=base_date + timedelta(days=i*3),
            amount=Decimal('50.00'),
            transaction_type='Expense',
            category_id=expense_cat1.category_id,
            description=f'Grocery shopping {i}',
            source='Test Source',
            classification_id=standard_class.classification_id
        )
        db_session.add(tx)
    
    # Expense transactions - Utilities
    for i in range(3):
        tx = Transaction(
            transaction_date=base_date + timedelta(days=i*10),
            amount=Decimal('100.00'),
            transaction_type='Expense',
            category_id=expense_cat2.category_id,
            description=f'Utility bill {i}',
            source='Test Source',
            classification_id=standard_class.classification_id
        )
        db_session.add(tx)
    
    db_session.commit()
    
    return {
        'start_date': base_date,
        'end_date': date.today(),
        'income_total': Decimal('5000.00'),  # 5 * 1000
        'expense_total': Decimal('800.00'),   # 10 * 50 + 3 * 100
        'transaction_count': 18
    }


def test_generate_summary_report(db_session, sample_data):
    """Test summary report generation."""
    service = ReportService(db_session)
    
    report = service.generate_summary_report(
        start_date=sample_data['start_date'],
        end_date=sample_data['end_date'],
        mode=AnalysisMode.ANALYSIS
    )
    
    # Verify structure
    assert report['report_type'] == 'summary'
    assert report['mode'] == 'analysis'
    
    # Verify period
    assert 'period' in report
    assert report['period']['start_date'] == sample_data['start_date'].isoformat()
    assert report['period']['end_date'] == sample_data['end_date'].isoformat()
    
    # Verify income
    assert 'income' in report
    assert report['income']['total'] == float(sample_data['income_total'])
    assert report['income']['transaction_count'] == 5
    assert len(report['income']['top_categories']) > 0
    
    # Verify expenses
    assert 'expenses' in report
    assert report['expenses']['total'] == float(sample_data['expense_total'])
    assert report['expenses']['transaction_count'] == 13
    assert len(report['expenses']['top_categories']) > 0
    
    # Verify cashflow
    assert 'cashflow' in report
    expected_cashflow = float(sample_data['income_total'] - sample_data['expense_total'])
    assert report['cashflow']['net_cashflow'] == expected_cashflow
    
    # Verify health indicators
    assert 'health_indicators' in report
    assert report['health_indicators']['income_to_expense_ratio'] > 0
    assert report['health_indicators']['savings_rate'] is not None


def test_generate_income_detail_report(db_session, sample_data):
    """Test income detail report generation."""
    service = ReportService(db_session)
    
    report = service.generate_income_detail_report(
        start_date=sample_data['start_date'],
        end_date=sample_data['end_date'],
        mode=AnalysisMode.ANALYSIS
    )
    
    # Verify structure
    assert report['report_type'] == 'income_detail'
    assert report['total_income'] == float(sample_data['income_total'])
    assert report['transaction_count'] == 5
    
    # Verify categories
    assert 'categories' in report
    assert len(report['categories']) > 0
    
    # Check category details
    for category in report['categories']:
        assert 'category' in category
        assert 'total' in category
        assert 'count' in category
        assert 'average' in category
        assert 'percentage' in category


def test_generate_expense_detail_report(db_session, sample_data):
    """Test expense detail report generation."""
    service = ReportService(db_session)
    
    report = service.generate_expense_detail_report(
        start_date=sample_data['start_date'],
        end_date=sample_data['end_date'],
        mode=AnalysisMode.ANALYSIS
    )
    
    # Verify structure
    assert report['report_type'] == 'expense_detail'
    assert report['total_expenses'] == float(sample_data['expense_total'])
    assert report['transaction_count'] == 13
    
    # Verify categories
    assert 'categories' in report
    assert len(report['categories']) == 2  # Groceries and Utilities
    
    # Verify categories are sorted by total (descending)
    if len(report['categories']) > 1:
        assert report['categories'][0]['total'] >= report['categories'][1]['total']


def test_generate_reconciliation_report(db_session, sample_data):
    """Test reconciliation report generation."""
    service = ReportService(db_session)
    
    report = service.generate_reconciliation_report(
        start_date=sample_data['start_date'],
        end_date=sample_data['end_date']
    )
    
    # Verify structure
    assert report['report_type'] == 'reconciliation'
    assert report['mode'] == 'complete'
    
    # Verify summary
    assert 'summary' in report
    assert report['summary']['total_income'] == float(sample_data['income_total'])
    assert report['summary']['total_expenses'] == float(sample_data['expense_total'])
    assert report['summary']['transaction_count'] == sample_data['transaction_count']
    
    # Verify transactions
    assert 'transactions' in report
    assert len(report['transactions']) == sample_data['transaction_count']
    
    # Verify transaction details
    for tx in report['transactions']:
        assert 'date' in tx
        assert 'description' in tx
        assert 'category' in tx
        assert 'type' in tx
        assert 'amount' in tx
        assert 'classification' in tx
        assert 'source' in tx


def test_export_to_csv_reconciliation(db_session, sample_data):
    """Test CSV export for reconciliation report."""
    service = ReportService(db_session)
    
    report = service.generate_reconciliation_report(
        start_date=sample_data['start_date'],
        end_date=sample_data['end_date']
    )
    
    csv_output = service.export_to_csv(report)
    
    # Verify CSV output
    assert csv_output is not None
    assert len(csv_output) > 0
    
    # Check for CSV headers
    assert 'date' in csv_output
    assert 'description' in csv_output
    assert 'category' in csv_output
    assert 'amount' in csv_output
    
    # Check that we have data rows (header + transactions)
    lines = csv_output.strip().split('\n')
    assert len(lines) == sample_data['transaction_count'] + 1  # +1 for header


def test_export_to_csv_income_detail(db_session, sample_data):
    """Test CSV export for income detail report."""
    service = ReportService(db_session)
    
    report = service.generate_income_detail_report(
        start_date=sample_data['start_date'],
        end_date=sample_data['end_date'],
        mode=AnalysisMode.ANALYSIS
    )
    
    csv_output = service.export_to_csv(report)
    
    # Verify CSV output
    assert csv_output is not None
    assert 'category' in csv_output
    assert 'total' in csv_output
    assert 'count' in csv_output
    assert 'average' in csv_output
    assert 'percentage' in csv_output


def test_default_date_range(db_session, sample_data):
    """Test that default date range works (last 30 days)."""
    service = ReportService(db_session)
    
    # Call without specifying dates
    report = service.generate_summary_report(mode=AnalysisMode.ANALYSIS)
    
    # Should have period information
    assert 'period' in report
    assert 'start_date' in report['period']
    assert 'end_date' in report['period']
    
    # End date should be today
    assert report['period']['end_date'] == date.today().isoformat()

