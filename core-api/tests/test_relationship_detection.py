"""Tests for relationship detection service."""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from financial_analysis.database.base import Base
from financial_analysis.database.models import (
    Transaction, Category, TransactionClassification, TransactionRelationship
)
from financial_analysis.database.seed_data import seed_classifications
from financial_analysis.services.classification_service import ClassificationService


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed only classifications (not rules to avoid the pop() issue)
    seed_classifications(session)

    yield session

    session.close()


@pytest.fixture
def test_category(db_session):
    """Create a test category."""
    category = Category(
        category_name="Test Category",
        category_type="Both"
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def transfer_classification(db_session):
    """Get transfer classification."""
    return db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'TRANSFER'
    ).first()


@pytest.fixture
def cc_payment_classification(db_session):
    """Get credit card payment classification."""
    return db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'CC_PAYMENT'
    ).first()


@pytest.fixture
def cc_receipt_classification(db_session):
    """Get credit card receipt classification."""
    return db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'CC_RECEIPT'
    ).first()


def test_detect_transfer_pairs_exact_match(db_session, test_category, transfer_classification):
    """Test detection of transfer pairs with exact amount and same day."""
    # Create two transactions with same amount on same day
    tx1 = Transaction(
        transaction_date=date.today(),
        amount=Decimal('500.00'),
        transaction_type='Expense',
        category_id=test_category.category_id,
        description='Transfer to savings',
        classification_id=transfer_classification.classification_id
    )
    tx2 = Transaction(
        transaction_date=date.today(),
        amount=Decimal('500.00'),
        transaction_type='Income',
        category_id=test_category.category_id,
        description='Transfer from checking',
        classification_id=transfer_classification.classification_id
    )
    
    db_session.add_all([tx1, tx2])
    db_session.commit()
    
    service = ClassificationService(db_session)
    pairs = service.detect_transfer_pairs(date_tolerance_days=3, auto_link=False)
    
    assert len(pairs) > 0
    assert pairs[0]['confidence'] >= 0.8  # High confidence for exact match
    assert pairs[0]['amount_difference'] == Decimal('0.00')
    assert pairs[0]['date_difference_days'] == 0


def test_detect_transfer_pairs_with_date_difference(db_session, test_category, transfer_classification):
    """Test detection of transfer pairs with date difference."""
    today = date.today()
    
    tx1 = Transaction(
        transaction_date=today,
        amount=Decimal('1000.00'),
        transaction_type='Expense',
        category_id=test_category.category_id,
        description='Transfer out',
        classification_id=transfer_classification.classification_id
    )
    tx2 = Transaction(
        transaction_date=today + timedelta(days=2),
        amount=Decimal('1000.00'),
        transaction_type='Income',
        category_id=test_category.category_id,
        description='Transfer in',
        classification_id=transfer_classification.classification_id
    )
    
    db_session.add_all([tx1, tx2])
    db_session.commit()
    
    service = ClassificationService(db_session)
    pairs = service.detect_transfer_pairs(date_tolerance_days=3, auto_link=False)
    
    assert len(pairs) > 0
    assert pairs[0]['date_difference_days'] == 2
    assert pairs[0]['confidence'] > 0.6  # Good confidence


def test_detect_transfer_pairs_auto_link(db_session, test_category, transfer_classification):
    """Test automatic linking of high-confidence transfer pairs."""
    tx1 = Transaction(
        transaction_date=date.today(),
        amount=Decimal('750.00'),
        transaction_type='Expense',
        category_id=test_category.category_id,
        description='Transfer to savings',
        classification_id=transfer_classification.classification_id
    )
    tx2 = Transaction(
        transaction_date=date.today(),
        amount=Decimal('750.00'),
        transaction_type='Income',
        category_id=test_category.category_id,
        description='Transfer from checking',
        classification_id=transfer_classification.classification_id
    )
    
    db_session.add_all([tx1, tx2])
    db_session.commit()
    
    service = ClassificationService(db_session)
    pairs = service.detect_transfer_pairs(date_tolerance_days=3, auto_link=True)
    
    # Check that relationship was created
    relationships = db_session.query(TransactionRelationship).all()
    assert len(relationships) > 0
    assert relationships[0].relationship_type == 'TRANSFER_PAIR'


def test_detect_credit_card_payments(db_session, test_category, cc_payment_classification, cc_receipt_classification):
    """Test detection of credit card payment/receipt pairs."""
    today = date.today()
    
    payment = Transaction(
        transaction_date=today,
        amount=Decimal('250.00'),
        transaction_type='Expense',
        category_id=test_category.category_id,
        description='Credit card payment',
        classification_id=cc_payment_classification.classification_id
    )
    receipt = Transaction(
        transaction_date=today + timedelta(days=1),
        amount=Decimal('250.00'),
        transaction_type='Income',
        category_id=test_category.category_id,
        description='Payment received',
        classification_id=cc_receipt_classification.classification_id
    )
    
    db_session.add_all([payment, receipt])
    db_session.commit()
    
    service = ClassificationService(db_session)
    pairs = service.detect_credit_card_payments(date_tolerance_days=5, auto_link=False)
    
    assert len(pairs) > 0
    assert pairs[0]['confidence'] > 0.7
    assert pairs[0]['relationship_type'] == 'CC_PAYMENT_RECEIPT'


def test_detect_reimbursement_pairs(db_session, test_category):
    """Test detection of reimbursement pairs."""
    # Get reimbursement classifications
    reimb_paid = db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'REIMB_PAID'
    ).first()
    reimb_received = db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'REIMB_RECEIVED'
    ).first()
    
    today = date.today()
    
    expense = Transaction(
        transaction_date=today,
        amount=Decimal('150.00'),
        transaction_type='Expense',
        category_id=test_category.category_id,
        description='Business expense',
        classification_id=reimb_paid.classification_id
    )
    reimbursement = Transaction(
        transaction_date=today + timedelta(days=10),
        amount=Decimal('150.00'),
        transaction_type='Income',
        category_id=test_category.category_id,
        description='Business expense reimbursement',
        classification_id=reimb_received.classification_id
    )
    
    db_session.add_all([expense, reimbursement])
    db_session.commit()
    
    service = ClassificationService(db_session)
    pairs = service.detect_reimbursement_pairs(date_tolerance_days=30, auto_link=False)
    
    assert len(pairs) > 0
    assert pairs[0]['confidence'] > 0.5
    assert pairs[0]['relationship_type'] == 'REIMBURSEMENT_PAIR'


def test_detect_all_relationships(db_session, test_category, transfer_classification):
    """Test detection of all relationship types."""
    # Create various transaction pairs
    today = date.today()
    
    # Transfer pair
    tx1 = Transaction(
        transaction_date=today,
        amount=Decimal('500.00'),
        transaction_type='Expense',
        category_id=test_category.category_id,
        description='Transfer',
        classification_id=transfer_classification.classification_id
    )
    tx2 = Transaction(
        transaction_date=today,
        amount=Decimal('500.00'),
        transaction_type='Income',
        category_id=test_category.category_id,
        description='Transfer',
        classification_id=transfer_classification.classification_id
    )
    
    db_session.add_all([tx1, tx2])
    db_session.commit()
    
    service = ClassificationService(db_session)
    result = service.detect_all_relationships(auto_link=False, date_tolerance_days=3)
    
    assert 'transfer_pairs' in result
    assert 'credit_card_pairs' in result
    assert 'reimbursement_pairs' in result
    assert result['total_detected'] >= 0


def test_create_and_delete_relationship(db_session, test_category):
    """Test manual creation and deletion of relationships."""
    tx1 = Transaction(
        transaction_date=date.today(),
        amount=Decimal('100.00'),
        transaction_type='Expense',
        category_id=test_category.category_id,
        description='Test transaction 1'
    )
    tx2 = Transaction(
        transaction_date=date.today(),
        amount=Decimal('100.00'),
        transaction_type='Income',
        category_id=test_category.category_id,
        description='Test transaction 2'
    )
    
    db_session.add_all([tx1, tx2])
    db_session.commit()
    
    service = ClassificationService(db_session)
    
    # Create relationship
    relationship = service.create_relationship(
        tx1.transaction_id,
        tx2.transaction_id,
        'TRANSFER_PAIR',
        'Manual test relationship'
    )
    
    assert relationship is not None
    assert relationship.relationship_type == 'TRANSFER_PAIR'
    
    # Delete relationship
    success = service.delete_relationship(relationship.relationship_id)
    assert success is True
    
    # Verify deletion
    deleted = db_session.query(TransactionRelationship).filter(
        TransactionRelationship.relationship_id == relationship.relationship_id
    ).first()
    assert deleted is None


def test_get_related_transactions(db_session, test_category):
    """Test retrieving related transactions."""
    tx1 = Transaction(
        transaction_date=date.today(),
        amount=Decimal('200.00'),
        transaction_type='Expense',
        category_id=test_category.category_id,
        description='Transaction 1'
    )
    tx2 = Transaction(
        transaction_date=date.today(),
        amount=Decimal('200.00'),
        transaction_type='Income',
        category_id=test_category.category_id,
        description='Transaction 2'
    )
    
    db_session.add_all([tx1, tx2])
    db_session.commit()
    
    service = ClassificationService(db_session)
    
    # Create relationship
    service.create_relationship(
        tx1.transaction_id,
        tx2.transaction_id,
        'TRANSFER_PAIR'
    )
    
    # Get related transactions
    related = service.get_related_transactions(tx1.transaction_id)
    
    assert len(related) == 1
    assert related[0]['transaction'].transaction_id == tx2.transaction_id
    assert related[0]['relationship_type'] == 'TRANSFER_PAIR'

