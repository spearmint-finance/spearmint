"""
Tests for classification API endpoints.
"""

import pytest
from datetime import date
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from financial_analysis.database.base import Base
from financial_analysis.database.models import (
    Transaction, Category, TransactionClassification, ClassificationRule
)
from financial_analysis.database.seed_data import seed_classifications
from financial_analysis.api.main import app
from financial_analysis.database.base import get_db


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool  # Use StaticPool to share a single connection
    )
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed classifications
    seed_classifications(session)

    yield session

    session.close()


@pytest.fixture
def client(db_session):
    """Create a test client with database override."""
    # Save the original commit method
    original_commit = db_session.commit

    # Replace commit with flush during tests
    # This allows services to call commit() without creating transaction boundaries
    db_session.commit = db_session.flush

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client

    # Restore the original commit method
    db_session.commit = original_commit
    app.dependency_overrides.clear()


@pytest.fixture
def sample_data(db_session):
    """Create sample data for testing."""
    # Create category
    category = Category(category_name="Groceries", category_type="Expense")
    db_session.add(category)
    db_session.commit()
    
    # Get standard classification
    standard = db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'STANDARD'
    ).first()
    
    # Create transactions
    transactions = []
    for i in range(5):
        tx = Transaction(
            transaction_date=date.today(),
            amount=Decimal('100.00'),
            transaction_type='Expense',
            category_id=category.category_id,
            description=f'Test transaction {i}',
            source='Test Source',
            classification_id=standard.classification_id
        )
        db_session.add(tx)
        transactions.append(tx)
    
    db_session.commit()
    
    return {
        'category': category,
        'standard': standard,
        'transactions': transactions
    }


def test_list_classifications(client, db_session):
    """Test listing all classifications."""
    response = client.get("/api/classifications")
    
    assert response.status_code == 200
    data = response.json()
    
    assert 'classifications' in data
    assert 'total' in data
    assert data['total'] >= 10  # Should have at least 10 system classifications
    
    # Verify structure
    for classification in data['classifications']:
        assert 'classification_id' in classification
        assert 'classification_name' in classification
        assert 'classification_code' in classification
        assert 'is_system_classification' in classification


def test_list_system_classifications_only(client, db_session):
    """Test listing only system classifications."""
    response = client.get("/api/classifications?system_only=true")
    
    assert response.status_code == 200
    data = response.json()
    
    # All should be system classifications
    for classification in data['classifications']:
        assert classification['is_system_classification'] is True


def test_get_classification(client, db_session):
    """Test getting a specific classification."""
    # Get standard classification
    standard = db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'STANDARD'
    ).first()
    
    response = client.get(f"/api/classifications/{standard.classification_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data['classification_id'] == standard.classification_id
    assert data['classification_name'] == 'Standard Transaction'
    assert data['classification_code'] == 'STANDARD'


def test_get_classification_not_found(client, db_session):
    """Test getting a non-existent classification."""
    response = client.get("/api/classifications/99999")
    
    assert response.status_code == 404


def test_create_classification(client, db_session):
    """Test creating a new classification."""
    new_classification = {
        "classification_name": "Custom Classification",
        "classification_code": "CUSTOM",
        "description": "A custom classification for testing",
        "exclude_from_income_calc": False,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": False
    }
    
    response = client.post("/api/classifications", json=new_classification)
    
    assert response.status_code == 201
    data = response.json()
    
    assert data['classification_name'] == "Custom Classification"
    assert data['classification_code'] == "CUSTOM"
    assert data['is_system_classification'] is False


def test_create_classification_duplicate_code(client, db_session):
    """Test creating a classification with duplicate code."""
    new_classification = {
        "classification_name": "Duplicate",
        "classification_code": "STANDARD",  # Already exists
        "description": "Should fail",
        "exclude_from_income_calc": False,
        "exclude_from_expense_calc": False,
        "exclude_from_cashflow_calc": False
    }
    
    response = client.post("/api/classifications", json=new_classification)
    
    assert response.status_code == 400


def test_classify_transaction(client, db_session, sample_data):
    """Test classifying a single transaction."""
    transaction = sample_data['transactions'][0]
    transfer = db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'TRANSFER'
    ).first()
    
    response = client.post(
        f"/api/transactions/{transaction.transaction_id}/classify",
        json={"classification_id": transfer.classification_id}
    )
    
    assert response.status_code == 200
    
    # Verify transaction was updated
    db_session.refresh(transaction)
    assert transaction.classification_id == transfer.classification_id


def test_classify_transaction_not_found(client, db_session):
    """Test classifying a non-existent transaction."""
    response = client.post(
        "/api/transactions/99999/classify",
        json={"classification_id": 1}
    )
    
    assert response.status_code == 404


def test_bulk_classify_transactions(client, db_session, sample_data):
    """Test bulk classifying transactions."""
    transaction_ids = [tx.transaction_id for tx in sample_data['transactions'][:3]]
    transfer = db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'TRANSFER'
    ).first()
    
    response = client.post(
        "/api/transactions/classify/bulk",
        json={
            "transaction_ids": transaction_ids,
            "classification_id": transfer.classification_id
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data['success_count'] == 3
    assert data['failed_count'] == 0
    assert len(data['failed_ids']) == 0


def test_auto_classify_transactions(client, db_session, sample_data):
    """Test auto-classifying transactions."""
    response = client.post(
        "/api/transactions/auto-classify",
        json={
            "transaction_ids": None,
            "force_reclassify": False
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert 'total_processed' in data
    assert 'classified_count' in data
    assert 'skipped_count' in data


def test_list_classification_rules(client, db_session):
    """Test listing classification rules."""
    response = client.get("/api/classification-rules")
    
    assert response.status_code == 200
    data = response.json()
    
    assert 'rules' in data
    assert 'total' in data


def test_create_classification_rule(client, db_session):
    """Test creating a classification rule."""
    transfer = db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'TRANSFER'
    ).first()
    
    new_rule = {
        "rule_name": "Test Transfer Rule",
        "rule_priority": 50,
        "classification_id": transfer.classification_id,
        "is_active": True,
        "description_pattern": "%transfer%"
    }
    
    response = client.post("/api/classification-rules", json=new_rule)
    
    assert response.status_code == 201
    data = response.json()
    
    assert data['rule_name'] == "Test Transfer Rule"
    assert data['rule_priority'] == 50
    assert data['description_pattern'] == "%transfer%"


def test_test_classification_rule(client, db_session, sample_data):
    """Test testing a classification rule."""
    response = client.post(
        "/api/classification-rules/test",
        json={
            "description_pattern": "%Test%",
            "amount_min": 50.0,
            "amount_max": 150.0
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert 'matching_transactions' in data
    assert 'sample_transaction_ids' in data
    assert data['matching_transactions'] >= 0


def test_update_classification_rule_clear_pattern(client, db_session):
    """Test updating a classification rule to clear a pattern field."""
    # First create a rule with patterns
    transfer = db_session.query(TransactionClassification).filter(
        TransactionClassification.classification_code == 'TRANSFER'
    ).first()

    new_rule = {
        "rule_name": "Test Rule for Update",
        "rule_priority": 50,
        "classification_id": transfer.classification_id,
        "is_active": True,
        "description_pattern": "%transfer%",
        "category_pattern": "%savings%",
        "source_pattern": "%bank%"
    }

    create_response = client.post("/api/classification-rules", json=new_rule)
    assert create_response.status_code == 201
    created_rule = create_response.json()
    rule_id = created_rule['rule_id']

    # Verify the rule was created with patterns
    assert created_rule['description_pattern'] == "%transfer%"
    assert created_rule['category_pattern'] == "%savings%"
    assert created_rule['source_pattern'] == "%bank%"

    # Now update the rule to clear the description_pattern
    update_data = {
        "description_pattern": None,  # Clear this field
        "category_pattern": None,     # Clear this field too
        # source_pattern is not included, so it should remain unchanged
    }

    update_response = client.put(
        f"/api/classification-rules/{rule_id}",
        json=update_data
    )

    assert update_response.status_code == 200
    updated_rule = update_response.json()

    # Verify the patterns were cleared
    assert updated_rule['description_pattern'] is None
    assert updated_rule['category_pattern'] is None
    assert updated_rule['source_pattern'] == "%bank%"  # Should remain unchanged

    # Verify by fetching the rule again
    get_response = client.get(f"/api/classification-rules/{rule_id}")
    assert get_response.status_code == 200
    fetched_rule = get_response.json()

    assert fetched_rule['description_pattern'] is None
    assert fetched_rule['category_pattern'] is None
    assert fetched_rule['source_pattern'] == "%bank%"

