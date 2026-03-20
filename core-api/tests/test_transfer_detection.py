"""Tests for transfer detection during import."""

import pytest
from datetime import date
from decimal import Decimal
import pandas as pd
from io import BytesIO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from financial_analysis.database.base import Base
from financial_analysis.services.import_service import ImportService
from financial_analysis.database.models import Category, Transaction, TransactionClassification
from financial_analysis.database.seed_data import seed_classifications


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Seed classifications
    seed_classifications(session)

    yield session

    session.close()


class TestTransferDetection:
    """Test transfer detection functionality in import service."""

    def test_transfer_category_detection_new_category(self, db_session):
        """Test that new 'Transfer' category is created with Transfer category_type."""
        service = ImportService(db_session)

        # Create Excel data with Transfer category
        data = {
            'Date': [date(2025, 1, 1)],
            'Amount': [-1000.00],
            'Category': ['Transfer'],
            'Description': ['Wire Transfer to Bank']
        }
        df = pd.DataFrame(data)

        # Save to Excel file
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, sheet_name='transactions')
        excel_buffer.seek(0)

        # Save to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp.write(excel_buffer.getvalue())
            tmp_path = tmp.name

        try:
            # Import
            result = service.import_from_excel(tmp_path, mode='incremental')

            # Verify import succeeded
            assert result.failed_rows == 0
            assert result.successful_rows == 1

            # Verify category was created with Transfer type
            category = db_session.query(Category).filter_by(category_name='Transfer').first()
            assert category is not None
            assert category.category_type == 'Transfer'

            # Verify transaction is excluded from analysis
            transaction = db_session.query(Transaction).first()
            assert transaction is not None
            assert transaction.include_in_analysis is False

        finally:
            import os
            os.unlink(tmp_path)

    def test_transfer_category_case_insensitive(self, db_session):
        """Test that transfer detection is case-insensitive."""
        service = ImportService(db_session)

        # Test different cases
        test_cases = ['Transfer', 'TRANSFER', 'transfer', 'TrAnSfEr']

        for i, category_name in enumerate(test_cases):
            data = {
                'Date': [date(2025, 1, i+1)],
                'Amount': [-100.00],
                'Category': [category_name],
                'Description': [f'Test transfer {i}']
            }
            df = pd.DataFrame(data)

            excel_buffer = BytesIO()
            df.to_excel(excel_buffer, index=False, sheet_name='transactions')
            excel_buffer.seek(0)

            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                tmp.write(excel_buffer.getvalue())
                tmp_path = tmp.name

            try:
                result = service.import_from_excel(tmp_path, mode='incremental')
                assert result.failed_rows == 0

                # All should use the same category (first one created)
                categories = db_session.query(Category).filter(
                    Category.category_name.in_(test_cases)
                ).all()

                # All transfer categories should have Transfer type
                for cat in categories:
                    assert cat.category_type == 'Transfer'

            finally:
                import os
                os.unlink(tmp_path)

    def test_non_transfer_category_not_marked(self, db_session):
        """Test that non-transfer categories are not given Transfer type."""
        service = ImportService(db_session)

        # Create Excel data with non-transfer category
        data = {
            'Date': [date(2025, 1, 1)],
            'Amount': [-50.00],
            'Category': ['Groceries'],
            'Description': ['Supermarket purchase']
        }
        df = pd.DataFrame(data)

        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, sheet_name='transactions')
        excel_buffer.seek(0)

        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp.write(excel_buffer.getvalue())
            tmp_path = tmp.name

        try:
            result = service.import_from_excel(tmp_path, mode='incremental')

            assert result.failed_rows == 0
            assert result.successful_rows == 1

            # Verify category does NOT have Transfer type
            category = db_session.query(Category).filter_by(category_name='Groceries').first()
            assert category is not None
            assert category.category_type != 'Transfer'

            # Verify transaction is included in analysis
            transaction = db_session.query(Transaction).first()
            assert transaction is not None
            assert transaction.include_in_analysis is True  # Default

        finally:
            import os
            os.unlink(tmp_path)

    def test_existing_transfer_category_updated(self, db_session):
        """Test that existing 'Transfer' category is updated to Transfer type."""
        # Create existing Transfer category without Transfer type
        existing_category = Category(
            category_name='Transfer',
            category_type='Expense'
        )
        db_session.add(existing_category)
        db_session.commit()

        service = ImportService(db_session)

        # Import transaction with Transfer category
        data = {
            'Date': [date(2025, 1, 1)],
            'Amount': [-500.00],
            'Category': ['Transfer'],
            'Description': ['Bank transfer']
        }
        df = pd.DataFrame(data)

        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, sheet_name='transactions')
        excel_buffer.seek(0)

        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp.write(excel_buffer.getvalue())
            tmp_path = tmp.name

        try:
            result = service.import_from_excel(tmp_path, mode='incremental')

            assert result.failed_rows == 0

            # Verify category was updated to Transfer type
            db_session.refresh(existing_category)
            assert existing_category.category_type == 'Transfer'

            # Verify only one Transfer category exists
            transfer_categories = db_session.query(Category).filter_by(
                category_name='Transfer'
            ).all()
            assert len(transfer_categories) == 1

        finally:
            import os
            os.unlink(tmp_path)

    def test_multiple_transfers_in_one_import(self, db_session):
        """Test importing multiple transfer transactions at once."""
        service = ImportService(db_session)

        # Create Excel data with multiple transfers
        data = {
            'Date': [date(2025, 1, 1), date(2025, 1, 2), date(2025, 1, 3)],
            'Amount': [-1000.00, -500.00, -250.00],
            'Category': ['Transfer', 'Transfer', 'Transfer'],
            'Description': ['Wire 1', 'Wire 2', 'Wire 3']
        }
        df = pd.DataFrame(data)

        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, sheet_name='transactions')
        excel_buffer.seek(0)

        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp.write(excel_buffer.getvalue())
            tmp_path = tmp.name

        try:
            result = service.import_from_excel(tmp_path, mode='incremental')

            assert result.failed_rows == 0
            assert result.successful_rows == 3

            # Verify all transactions have a Transfer-type category and are excluded from analysis
            transactions = db_session.query(Transaction).all()
            assert len(transactions) == 3

            for tx in transactions:
                assert tx.category.category_type == 'Transfer'
                assert tx.include_in_analysis is False

            # Verify only one Transfer category was created
            categories = db_session.query(Category).filter_by(
                category_name='Transfer'
            ).all()
            assert len(categories) == 1
            assert categories[0].category_type == 'Transfer'

        finally:
            import os
            os.unlink(tmp_path)

    def test_mixed_transfer_and_regular_transactions(self, db_session):
        """Test importing mix of transfer and regular transactions."""
        service = ImportService(db_session)

        # Create Excel data with mix of transfers and regular transactions
        data = {
            'Date': [date(2025, 1, 1), date(2025, 1, 2), date(2025, 1, 3)],
            'Amount': [-1000.00, -50.00, -500.00],
            'Category': ['Transfer', 'Groceries', 'Transfer'],
            'Description': ['Wire transfer', 'Supermarket', 'Bank transfer']
        }
        df = pd.DataFrame(data)

        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, sheet_name='transactions')
        excel_buffer.seek(0)

        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp.write(excel_buffer.getvalue())
            tmp_path = tmp.name

        try:
            result = service.import_from_excel(tmp_path, mode='incremental')

            assert result.failed_rows == 0
            assert result.successful_rows == 3

            # Verify transfers are identified by joining to category
            transfers = db_session.query(Transaction).join(Category).filter(
                Category.category_type == 'Transfer'
            ).all()
            assert len(transfers) == 2
            for tx in transfers:
                assert tx.include_in_analysis is False

            # Verify regular transaction does not have Transfer category type
            regular = db_session.query(Transaction).join(Category).filter(
                Category.category_type != 'Transfer'
            ).all()
            assert len(regular) == 1
            assert regular[0].include_in_analysis is True
            assert regular[0].category.category_name == 'Groceries'

        finally:
            import os
            os.unlink(tmp_path)
