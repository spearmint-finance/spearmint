"""
Tests for report service.
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from financial_analysis.database.base import Base
from financial_analysis.database.models import Transaction, Category, TransactionRelationship
from financial_analysis.services.report_service import ReportService, AnalysisMode


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
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
        # classification field removed
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


@pytest.fixture
def capex_data(db_session):
    """Create sample CapEx transaction data for testing."""
    # Create CapEx categories
    vehicle_cat = Category(category_name="Vehicle Purchase", category_type="Expense")
    equipment_cat = Category(category_name="Equipment", category_type="Expense")

    db_session.add_all([vehicle_cat, equipment_cat])
    db_session.commit()

    # Create CapEx transactions
    base_date = date.today() - timedelta(days=180)

    # Vehicle purchase
    tx1 = Transaction(
        transaction_date=base_date + timedelta(days=30),
        amount=Decimal('-25000.00'),
        transaction_type='Expense',
        category_id=vehicle_cat.category_id,
        description='Used Toyota Camry',
        source='Test Source',
        notes='Company vehicle purchase',
        is_capital_expense=True
    )
    db_session.add(tx1)

    # Equipment purchases
    tx2 = Transaction(
        transaction_date=base_date + timedelta(days=60),
        amount=Decimal('-3000.00'),
        transaction_type='Expense',
        category_id=equipment_cat.category_id,
        description='MacBook Pro',
        source='Test Source',
        notes='Work laptop',
        is_capital_expense=True
    )
    db_session.add(tx2)

    tx3 = Transaction(
        transaction_date=base_date + timedelta(days=90),
        amount=Decimal('-2000.00'),
        transaction_type='Expense',
        category_id=equipment_cat.category_id,
        description='Office Furniture',
        source='Test Source',
        notes='Desk and chair',
        is_capital_expense=True
    )
    db_session.add(tx3)

    db_session.commit()

    return {
        'start_date': base_date,
        'end_date': date.today(),
        'total_capex': Decimal('30000.00'),  # 25000 + 3000 + 2000
        'transaction_count': 3,
        'vehicle_total': Decimal('25000.00'),
        'equipment_total': Decimal('5000.00')
    }


def test_generate_capex_report(db_session, capex_data):
    """Test CapEx report generation."""
    service = ReportService(db_session)

    report = service.generate_capex_report(
        start_date=capex_data['start_date'],
        end_date=capex_data['end_date']
    )

    # Verify structure
    assert report['report_type'] == 'capex'

    # Verify period
    assert 'period' in report
    assert report['period']['start_date'] == capex_data['start_date'].isoformat()
    assert report['period']['end_date'] == capex_data['end_date'].isoformat()

    # Verify summary
    assert 'summary' in report
    assert report['summary']['total_capex'] == float(capex_data['total_capex'])
    assert report['summary']['transaction_count'] == capex_data['transaction_count']
    assert report['summary']['average_transaction'] == float(capex_data['total_capex']) / capex_data['transaction_count']

    # Verify category breakdown
    assert 'by_category' in report
    assert len(report['by_category']) == 2  # Vehicle Purchase and Equipment

    # Check categories are sorted by total (descending)
    assert report['by_category'][0]['total'] >= report['by_category'][1]['total']

    # Verify Vehicle Purchase is first (highest amount)
    assert report['by_category'][0]['category'] == 'Vehicle Purchase'
    assert report['by_category'][0]['total'] == float(capex_data['vehicle_total'])

    # Verify Equipment
    assert report['by_category'][1]['category'] == 'Equipment'
    assert report['by_category'][1]['total'] == float(capex_data['equipment_total'])

    # Verify percentages add up to 100%
    total_percentage = sum(cat['percentage'] for cat in report['by_category'])
    assert abs(total_percentage - 100.0) < 0.1

    # Verify transactions
    assert 'transactions' in report
    assert len(report['transactions']) == capex_data['transaction_count']

    # Verify transaction structure
    for tx in report['transactions']:
        assert 'transaction_id' in tx
        assert 'date' in tx
        assert 'description' in tx
        assert 'amount' in tx
        assert 'category' in tx
        # classification field removed


def test_get_total_capex(db_session, capex_data):
    """Test the lightweight get_total_capex method."""
    service = ReportService(db_session)

    total = service.get_total_capex(
        start_date=capex_data['start_date'],
        end_date=capex_data['end_date']
    )

    assert total == float(capex_data['total_capex'])


def test_summary_report_includes_total_capex(db_session, capex_data):
    """Test that summary report includes total_capex field."""
    service = ReportService(db_session)

    report = service.generate_summary_report(
        start_date=capex_data['start_date'],
        end_date=capex_data['end_date'],
        mode=AnalysisMode.ANALYSIS
    )

    # Verify total_capex is included
    assert 'total_capex' in report
    assert report['total_capex'] == float(capex_data['total_capex'])


def test_summary_report_includes_total_receivables(db_session, receivables_data):
    """Test that summary report includes total_receivables field."""
    service = ReportService(db_session)

    report = service.generate_summary_report(
        start_date=receivables_data['start_date'],
        end_date=receivables_data['end_date'],
        mode=AnalysisMode.ANALYSIS
    )

    # Verify total_receivables is included
    assert 'total_receivables' in report
    assert report['total_receivables'] == float(receivables_data['total_outstanding'])


def test_capex_report_empty_when_no_capex_transactions(db_session, sample_data):
    """Test CapEx report returns empty results when no CapEx transactions exist."""
    service = ReportService(db_session)

    report = service.generate_capex_report(
        start_date=sample_data['start_date'],
        end_date=sample_data['end_date']
    )

    # Verify empty results
    assert report['summary']['total_capex'] == 0.0
    assert report['summary']['transaction_count'] == 0
    assert report['summary']['average_transaction'] == 0.0
    assert len(report['by_category']) == 0
    assert len(report['transactions']) == 0


def test_capex_report_date_filtering(db_session, capex_data):
    """Test that CapEx report respects date filtering."""
    service = ReportService(db_session)

    # Only query a period with 1 transaction (first 45 days)
    report = service.generate_capex_report(
        start_date=capex_data['start_date'],
        end_date=capex_data['start_date'] + timedelta(days=45)
    )

    # Should only include the first transaction (vehicle purchase at day 30)
    assert report['summary']['transaction_count'] == 1
    assert report['summary']['total_capex'] == float(capex_data['vehicle_total'])


def test_export_to_csv_capex(db_session, capex_data):
    """Test CSV export for CapEx report."""
    service = ReportService(db_session)

    report = service.generate_capex_report(
        start_date=capex_data['start_date'],
        end_date=capex_data['end_date']
    )

    csv_output = service.export_to_csv(report)

    # Verify CSV output
    assert csv_output is not None
    assert len(csv_output) > 0

    # Check for CSV headers
    assert 'transaction_id' in csv_output
    assert 'date' in csv_output
    assert 'description' in csv_output
    assert 'amount' in csv_output
    assert 'category' in csv_output
    # classification field removed

    # Check that we have data rows (header + transactions)
    lines = csv_output.strip().split('\n')
    assert len(lines) == capex_data['transaction_count'] + 1  # +1 for header


# ==============================================================================
# Receivables Report Tests
# ==============================================================================


@pytest.fixture
def receivables_data(db_session):
    """Create sample receivables data for testing."""
    # Create a category for reimbursable expenses
    expense_cat = Category(category_name="Business Travel", category_type="Expense")
    db_session.add(expense_cat)
    db_session.commit()



    today = date.today()
    start_date = today - timedelta(days=60)
    end_date = today

    # Create reimbursable expenses (REIMB_PAID)
    expense1 = Transaction(
        transaction_date=today - timedelta(days=30),
        amount=Decimal('-150.00'),
        transaction_type='Expense',
        description='Client dinner - Chicago trip',
        category_id=expense_cat.category_id,
        is_reimbursable=True,
    )
    expense2 = Transaction(
        transaction_date=today - timedelta(days=20),
        amount=Decimal('-350.00'),
        transaction_type='Expense',
        description='Hotel for conference',
        category_id=expense_cat.category_id,
        is_reimbursable=True,
    )
    expense3 = Transaction(
        transaction_date=today - timedelta(days=10),
        amount=Decimal('-75.00'),
        transaction_type='Expense',
        description='Office supplies',
        category_id=expense_cat.category_id,
        is_reimbursable=True,
    )
    db_session.add_all([expense1, expense2, expense3])
    db_session.commit()

    # Create a reimbursement for expense1 (linked)
    reimbursement1 = Transaction(
        transaction_date=today - timedelta(days=15),
        amount=Decimal('150.00'),
        transaction_type='Income',
        description='Expense reimbursement - Chicago trip',
        category_id=expense_cat.category_id,
    )
    db_session.add(reimbursement1)
    db_session.commit()

    # Link expense1 and reimbursement1
    relationship = TransactionRelationship(
        transaction_id_1=expense1.transaction_id,
        transaction_id_2=reimbursement1.transaction_id,
        relationship_type='REIMBURSEMENT_PAIR',
        description='Client dinner reimbursement'
    )
    db_session.add(relationship)
    db_session.commit()

    return {
        'start_date': start_date,
        'end_date': end_date,
        'expense1': expense1,  # Reimbursed
        'expense2': expense2,  # Outstanding
        'expense3': expense3,  # Outstanding
        'reimbursement1': reimbursement1,
        'category': expense_cat,
        'outstanding_count': 2,  # expense2 and expense3
        'reimbursed_count': 1,   # expense1
        'total_outstanding': Decimal('425.00'),  # 350 + 75
        'total_reimbursed': Decimal('150.00')
    }


def test_generate_receivables_report(db_session, receivables_data):
    """Test generating a receivables report."""
    service = ReportService(db_session)

    report = service.generate_receivables_report(
        start_date=receivables_data['start_date'],
        end_date=receivables_data['end_date']
    )

    assert report['report_type'] == 'receivables'
    assert 'period' in report
    assert 'summary' in report
    assert 'by_category' in report
    assert 'outstanding' in report
    assert 'recently_reimbursed' in report

    # Verify summary
    summary = report['summary']
    assert summary['outstanding_count'] == receivables_data['outstanding_count']
    assert summary['reimbursed_count'] == receivables_data['reimbursed_count']
    assert summary['total_outstanding'] == float(receivables_data['total_outstanding'])
    assert summary['total_reimbursed'] == float(receivables_data['total_reimbursed'])
    assert summary['oldest_outstanding_days'] >= 0
    assert summary['average_days_outstanding'] >= 0


def test_get_total_receivables(db_session, receivables_data):
    """Test getting total outstanding receivables amount."""
    service = ReportService(db_session)

    total = service.get_total_receivables(
        start_date=receivables_data['start_date'],
        end_date=receivables_data['end_date']
    )

    # Should only include outstanding (unlinked) expenses
    assert total == float(receivables_data['total_outstanding'])


def test_receivables_report_empty_when_no_receivables(db_session):
    """Test receivables report when there are no reimbursable expenses."""
    service = ReportService(db_session)
    today = date.today()

    report = service.generate_receivables_report(
        start_date=today - timedelta(days=30),
        end_date=today
    )

    assert report['report_type'] == 'receivables'
    assert report['summary']['outstanding_count'] == 0
    assert report['summary']['reimbursed_count'] == 0
    assert report['summary']['total_outstanding'] == 0.0
    assert len(report['outstanding']) == 0
    assert len(report['recently_reimbursed']) == 0


def test_receivables_outstanding_list(db_session, receivables_data):
    """Test that outstanding receivables list contains correct transactions."""
    service = ReportService(db_session)

    report = service.generate_receivables_report(
        start_date=receivables_data['start_date'],
        end_date=receivables_data['end_date']
    )

    outstanding = report['outstanding']
    assert len(outstanding) == 2

    # Check that outstanding transactions are not marked as reimbursed
    for tx in outstanding:
        assert tx['is_reimbursed'] is False
        assert tx['reimbursement_id'] is None
        assert tx['days_outstanding'] >= 0


def test_receivables_reimbursed_list(db_session, receivables_data):
    """Test that recently reimbursed list contains linked transactions."""
    service = ReportService(db_session)

    report = service.generate_receivables_report(
        start_date=receivables_data['start_date'],
        end_date=receivables_data['end_date'],
        include_reimbursed=True
    )

    reimbursed = report['recently_reimbursed']
    assert len(reimbursed) == 1

    # Check that the transaction is marked as reimbursed
    tx = reimbursed[0]
    assert tx['is_reimbursed'] is True
    assert tx['reimbursement_id'] == receivables_data['reimbursement1'].transaction_id


def test_export_to_csv_receivables(db_session, receivables_data):
    """Test CSV export for receivables report."""
    service = ReportService(db_session)

    report = service.generate_receivables_report(
        start_date=receivables_data['start_date'],
        end_date=receivables_data['end_date']
    )

    csv_output = service.export_to_csv(report)

    # Verify CSV output
    assert csv_output is not None
    assert len(csv_output) > 0

    # Check for CSV headers
    assert 'transaction_id' in csv_output
    assert 'date' in csv_output
    assert 'days_outstanding' in csv_output
    assert 'is_reimbursed' in csv_output

    # Check that we have data rows (header + outstanding transactions)
    lines = csv_output.strip().split('\n')
    assert len(lines) == receivables_data['outstanding_count'] + 1  # +1 for header
