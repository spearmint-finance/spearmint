"""Tests for import profile functionality."""

import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from financial_analysis.database.base import Base
from financial_analysis.database.models import Account, ImportProfile
from financial_analysis.services.import_service import ImportService


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    # Create test account
    account = Account(
        account_name="Chase Checking",
        account_type="checking",
        institution_name="Chase Bank"
    )
    session.add(account)
    session.commit()
    
    yield session
    
    session.close()


class TestImportProfileCRUD:
    """Test ImportProfile CRUD operations."""
    
    def test_create_profile(self, db_session):
        """Test creating an import profile."""
        service = ImportService(db_session)
        
        profile = service.create_profile(
            name="Chase Credit Card",
            column_mappings={
                "Posting Date": "date",
                "Description": "description",
                "Amount": "amount"
            },
            date_format="%m/%d/%Y",
            skip_rows=0
        )
        
        assert profile.profile_id is not None
        assert profile.name == "Chase Credit Card"
        assert profile.column_mappings["Posting Date"] == "date"
        assert profile.date_format == "%m/%d/%Y"
        assert profile.is_active is True
    
    def test_create_profile_with_account(self, db_session):
        """Test creating a profile linked to an account."""
        service = ImportService(db_session)
        account = db_session.query(Account).first()
        
        profile = service.create_profile(
            name="Chase Checking Import",
            column_mappings={"Date": "date", "Amount": "amount"},
            account_id=account.account_id
        )
        
        assert profile.account_id == account.account_id
        assert profile.account.account_name == "Chase Checking"
    
    def test_create_profile_invalid_account(self, db_session):
        """Test creating a profile with invalid account ID."""
        service = ImportService(db_session)
        
        with pytest.raises(ValueError, match="Account 9999 not found"):
            service.create_profile(
                name="Invalid Profile",
                column_mappings={"Date": "date"},
                account_id=9999
            )
    
    def test_get_profile(self, db_session):
        """Test getting a profile by ID."""
        service = ImportService(db_session)
        
        created = service.create_profile(
            name="Test Profile",
            column_mappings={"Date": "date"}
        )
        
        fetched = service.get_profile(created.profile_id)
        assert fetched is not None
        assert fetched.name == "Test Profile"
    
    def test_get_profile_not_found(self, db_session):
        """Test getting a non-existent profile."""
        service = ImportService(db_session)
        
        fetched = service.get_profile(9999)
        assert fetched is None
    
    def test_get_profiles(self, db_session):
        """Test listing all profiles."""
        service = ImportService(db_session)
        
        service.create_profile(name="Profile 1", column_mappings={"A": "a"})
        service.create_profile(name="Profile 2", column_mappings={"B": "b"})
        
        profiles = service.get_profiles()
        assert len(profiles) == 2
    
    def test_get_profiles_filter_active(self, db_session):
        """Test filtering profiles by active status."""
        service = ImportService(db_session)
        
        p1 = service.create_profile(name="Active", column_mappings={"A": "a"})
        p2 = service.create_profile(name="Inactive", column_mappings={"B": "b"})
        service.update_profile(p2.profile_id, is_active=False)
        
        active = service.get_profiles(is_active=True)
        assert len(active) == 1
        assert active[0].name == "Active"
    
    def test_update_profile(self, db_session):
        """Test updating a profile."""
        service = ImportService(db_session)
        
        profile = service.create_profile(
            name="Original Name",
            column_mappings={"Date": "date"}
        )
        
        updated = service.update_profile(
            profile.profile_id,
            name="Updated Name",
            skip_rows=2
        )
        
        assert updated.name == "Updated Name"
        assert updated.skip_rows == 2
    
    def test_delete_profile(self, db_session):
        """Test deleting a profile."""
        service = ImportService(db_session)

        profile = service.create_profile(
            name="To Delete",
            column_mappings={"Date": "date"}
        )

        result = service.delete_profile(profile.profile_id)
        assert result is True

        fetched = service.get_profile(profile.profile_id)
        assert fetched is None

    def test_delete_profile_not_found(self, db_session):
        """Test deleting a non-existent profile."""
        service = ImportService(db_session)

        result = service.delete_profile(9999)
        assert result is False


class TestProfileSuggestions:
    """Test profile suggestion functionality."""

    def test_suggest_profiles_exact_match(self, db_session):
        """Test suggesting profiles with exact column match."""
        service = ImportService(db_session)

        service.create_profile(
            name="Chase Format",
            column_mappings={
                "Posting Date": "date",
                "Description": "description",
                "Amount": "amount"
            }
        )

        suggestions = service.suggest_profiles([
            "Posting Date", "Description", "Amount", "Category"
        ])

        assert len(suggestions) == 1
        assert suggestions[0]['name'] == "Chase Format"
        assert suggestions[0]['match_score'] == 100.0

    def test_suggest_profiles_partial_match(self, db_session):
        """Test suggesting profiles with partial column match."""
        service = ImportService(db_session)

        service.create_profile(
            name="Bank Format",
            column_mappings={
                "Date": "date",
                "Description": "description",
                "Amount": "amount",
                "Category": "category"
            }
        )

        # Only 2 of 4 columns match
        suggestions = service.suggest_profiles(["Date", "Amount"])

        assert len(suggestions) == 1
        assert suggestions[0]['match_score'] == 50.0

    def test_suggest_profiles_no_match(self, db_session):
        """Test suggesting profiles with no matching columns."""
        service = ImportService(db_session)

        service.create_profile(
            name="Bank Format",
            column_mappings={"Date": "date", "Amount": "amount"}
        )

        suggestions = service.suggest_profiles(["Column1", "Column2"])

        assert len(suggestions) == 0

    def test_suggest_profiles_sorted_by_score(self, db_session):
        """Test that suggestions are sorted by match score."""
        service = ImportService(db_session)

        service.create_profile(
            name="Low Match",
            column_mappings={"Date": "date", "Amount": "amount", "Extra": "extra"}
        )
        service.create_profile(
            name="High Match",
            column_mappings={"Date": "date", "Amount": "amount"}
        )

        suggestions = service.suggest_profiles(["Date", "Amount"])

        assert len(suggestions) == 2
        assert suggestions[0]['name'] == "High Match"
        assert suggestions[0]['match_score'] > suggestions[1]['match_score']

