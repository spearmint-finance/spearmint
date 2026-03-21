"""Tests for relationship detection service."""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from financial_analysis.database.base import Base
from financial_analysis.database.models import (
    Transaction, Category, TransactionRelationship, Account, Tag, TransactionTag
)
from financial_analysis.services.relationship_service import RelationshipService


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
def test_category(db_session):
    """Create a test category (general purpose)."""
    category = Category(
        category_name="Test Category",
        category_type="Both"
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def transfer_category(db_session):
    """Create a transfer category for transfer detection tests."""
    category = Category(
        category_name="Transfer",
        category_type="Transfer"
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


def test_detect_transfer_pairs_exact_match(db_session, transfer_category):
    """Test detection of transfer pairs with exact amount and same day."""
    tx1 = Transaction(
        transaction_date=date.today(),
        amount=Decimal('500.00'),
        transaction_type='Expense',
        category_id=transfer_category.category_id,
        description='Transfer to savings',
    )
    tx2 = Transaction(
        transaction_date=date.today(),
        amount=Decimal('500.00'),
        transaction_type='Income',
        category_id=transfer_category.category_id,
        description='Transfer from checking',
    )

    db_session.add_all([tx1, tx2])
    db_session.commit()

    service = RelationshipService(db_session)
    pairs = service.detect_transfer_pairs(date_tolerance_days=3, auto_link=False)

    assert len(pairs) > 0
    assert pairs[0]['confidence'] >= 0.8  # High confidence for exact match
    assert pairs[0]['amount_difference'] == Decimal('0.00')
    assert pairs[0]['date_difference_days'] == 0


def test_detect_transfer_pairs_with_date_difference(db_session, transfer_category):
    """Test detection of transfer pairs with date difference."""
    today = date.today()

    tx1 = Transaction(
        transaction_date=today,
        amount=Decimal('1000.00'),
        transaction_type='Expense',
        category_id=transfer_category.category_id,
        description='Transfer out',
    )
    tx2 = Transaction(
        transaction_date=today + timedelta(days=2),
        amount=Decimal('1000.00'),
        transaction_type='Income',
        category_id=transfer_category.category_id,
        description='Transfer in',
    )

    db_session.add_all([tx1, tx2])
    db_session.commit()

    service = RelationshipService(db_session)
    pairs = service.detect_transfer_pairs(date_tolerance_days=3, auto_link=False)

    assert len(pairs) > 0
    assert pairs[0]['date_difference_days'] == 2
    assert pairs[0]['confidence'] > 0.6  # Good confidence


def test_detect_transfer_pairs_auto_link(db_session, transfer_category):
    """Test automatic linking of high-confidence transfer pairs."""
    tx1 = Transaction(
        transaction_date=date.today(),
        amount=Decimal('750.00'),
        transaction_type='Expense',
        category_id=transfer_category.category_id,
        description='Transfer to savings',
    )
    tx2 = Transaction(
        transaction_date=date.today(),
        amount=Decimal('750.00'),
        transaction_type='Income',
        category_id=transfer_category.category_id,
        description='Transfer from checking',
    )

    db_session.add_all([tx1, tx2])
    db_session.commit()

    service = RelationshipService(db_session)
    pairs = service.detect_transfer_pairs(date_tolerance_days=3, auto_link=True)

    # Check that relationship was created
    relationships = db_session.query(TransactionRelationship).all()
    assert len(relationships) > 0
    assert relationships[0].relationship_type == 'TRANSFER_PAIR'


def test_detect_credit_card_payments(db_session, transfer_category):
    """Test detection of credit card payment/receipt pairs."""
    today = date.today()

    # Create accounts (required by account-based CC detection)
    checking = Account(account_name="Checking", account_type="checking")
    cc_account = Account(account_name="Visa CC", account_type="credit_card")
    db_session.add_all([checking, cc_account])
    db_session.commit()
    db_session.refresh(checking)
    db_session.refresh(cc_account)

    payment = Transaction(
        transaction_date=today,
        amount=Decimal('-250.00'),
        transaction_type='Expense',
        category_id=transfer_category.category_id,
        account_id=checking.account_id,
        description='Credit card payment',
    )
    receipt = Transaction(
        transaction_date=today + timedelta(days=1),
        amount=Decimal('250.00'),
        transaction_type='Income',
        category_id=transfer_category.category_id,
        account_id=cc_account.account_id,
        description='Payment received',
    )

    db_session.add_all([payment, receipt])
    db_session.commit()

    service = RelationshipService(db_session)
    pairs = service.detect_credit_card_payments(date_tolerance_days=5, auto_link=False)

    assert len(pairs) > 0
    assert pairs[0]['confidence'] > 0.7
    assert pairs[0]['relationship_type'] == 'CC_PAYMENT_RECEIPT'


def test_detect_reimbursement_pairs(db_session, test_category):
    """Test detection of reimbursement pairs."""
    today = date.today()

    # Create 'reimbursable' tag (required by tag-based detection)
    tag = Tag(tag_name="reimbursable")
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)

    expense = Transaction(
        transaction_date=today,
        amount=Decimal('150.00'),
        transaction_type='Expense',
        category_id=test_category.category_id,
        description='Business expense',
    )
    reimbursement = Transaction(
        transaction_date=today + timedelta(days=10),
        amount=Decimal('150.00'),
        transaction_type='Income',
        category_id=test_category.category_id,
        description='Business expense reimbursement',
    )

    db_session.add_all([expense, reimbursement])
    db_session.flush()

    # Tag the expense as reimbursable
    tx_tag = TransactionTag(transaction_id=expense.transaction_id, tag_id=tag.tag_id)
    db_session.add(tx_tag)
    db_session.commit()

    service = RelationshipService(db_session)
    pairs = service.detect_reimbursement_pairs(date_tolerance_days=30, auto_link=False)

    assert len(pairs) > 0
    assert pairs[0]['confidence'] > 0.5
    assert pairs[0]['relationship_type'] == 'REIMBURSEMENT_PAIR'


def test_detect_all_relationships(db_session, transfer_category):
    """Test detection of all relationship types."""
    today = date.today()

    # Transfer pair
    tx1 = Transaction(
        transaction_date=today,
        amount=Decimal('500.00'),
        transaction_type='Expense',
        category_id=transfer_category.category_id,
        description='Transfer',
    )
    tx2 = Transaction(
        transaction_date=today,
        amount=Decimal('500.00'),
        transaction_type='Income',
        category_id=transfer_category.category_id,
        description='Transfer',
    )

    db_session.add_all([tx1, tx2])
    db_session.commit()

    service = RelationshipService(db_session)
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

    service = RelationshipService(db_session)

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

    service = RelationshipService(db_session)

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
