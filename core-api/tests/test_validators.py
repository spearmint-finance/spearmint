"""Tests for data validators."""

import pytest
from datetime import date, datetime, timedelta
from decimal import Decimal

from financial_analysis.utils.validators import (
    DataValidator,
    DuplicateDetector,
    ValidationError
)


class TestDataValidator:
    """Test DataValidator class."""
    
    def test_validate_date_valid(self):
        """Test valid date validation."""
        validator = DataValidator()
        
        # Test with date object
        today = date.today()
        assert validator.validate_date(today) == today
        
        # Test with datetime object
        now = datetime.now()
        assert validator.validate_date(now) == now.date()
        
        # Test with string formats
        assert validator.validate_date("2024-01-15") == date(2024, 1, 15)
        assert validator.validate_date("01/15/2024") == date(2024, 1, 15)
    
    def test_validate_date_future(self):
        """Test that future dates are rejected."""
        validator = DataValidator()
        future_date = date.today() + timedelta(days=1)
        
        with pytest.raises(ValidationError, match="cannot be in the future"):
            validator.validate_date(future_date)
    
    def test_validate_date_invalid(self):
        """Test invalid date validation."""
        validator = DataValidator()
        
        with pytest.raises(ValidationError):
            validator.validate_date("invalid-date")
        
        with pytest.raises(ValidationError):
            validator.validate_date(None)
    
    def test_validate_amount_valid(self):
        """Test valid amount validation."""
        validator = DataValidator()
        
        assert validator.validate_amount(100) == Decimal("100")
        assert validator.validate_amount(100.50) == Decimal("100.50")
        assert validator.validate_amount("100.50") == Decimal("100.50")
        assert validator.validate_amount("$100.50") == Decimal("100.50")
        assert validator.validate_amount("1,000.50") == Decimal("1000.50")
    
    def test_validate_amount_zero(self):
        """Test that zero amounts are rejected by default."""
        validator = DataValidator()
        
        with pytest.raises(ValidationError, match="cannot be zero"):
            validator.validate_amount(0)
        
        # But allowed when allow_zero=True
        assert validator.validate_amount(0, allow_zero=True) == Decimal("0")
    
    def test_validate_amount_invalid(self):
        """Test invalid amount validation."""
        validator = DataValidator()
        
        with pytest.raises(ValidationError):
            validator.validate_amount("invalid")
        
        with pytest.raises(ValidationError):
            validator.validate_amount(None)
    
    def test_validate_transaction_type_valid(self):
        """Test valid transaction type validation."""
        validator = DataValidator()
        
        assert validator.validate_transaction_type("Income") == "Income"
        assert validator.validate_transaction_type("Expense") == "Expense"
        assert validator.validate_transaction_type("income") == "Income"  # Case insensitive
        assert validator.validate_transaction_type("EXPENSE") == "Expense"
    
    def test_validate_transaction_type_invalid(self):
        """Test invalid transaction type validation."""
        validator = DataValidator()
        
        with pytest.raises(ValidationError, match="must be one of"):
            validator.validate_transaction_type("Invalid")
        
        with pytest.raises(ValidationError):
            validator.validate_transaction_type(None)
    
    def test_validate_category_valid(self):
        """Test valid category validation."""
        validator = DataValidator()
        
        assert validator.validate_category("Groceries") == "Groceries"
        assert validator.validate_category("  Groceries  ") == "Groceries"  # Trimmed
    
    def test_validate_category_invalid(self):
        """Test invalid category validation."""
        validator = DataValidator()
        
        with pytest.raises(ValidationError, match="required and cannot be empty"):
            validator.validate_category("")
        
        with pytest.raises(ValidationError):
            validator.validate_category(None)
    
    def test_validate_optional_string(self):
        """Test optional string validation."""
        validator = DataValidator()
        
        assert validator.validate_optional_string("test", "Field") == "test"
        assert validator.validate_optional_string("  test  ", "Field") == "test"
        assert validator.validate_optional_string(None, "Field") is None
        assert validator.validate_optional_string("", "Field") is None
        
        # Test max length
        with pytest.raises(ValidationError, match="exceeds maximum length"):
            validator.validate_optional_string("a" * 100, "Field", max_length=50)
    
    def test_validate_boolean(self):
        """Test boolean validation."""
        validator = DataValidator()
        
        assert validator.validate_boolean(True, "Field") is True
        assert validator.validate_boolean(False, "Field") is False
        assert validator.validate_boolean("true", "Field") is True
        assert validator.validate_boolean("false", "Field") is False
        assert validator.validate_boolean("1", "Field") is True
        assert validator.validate_boolean("0", "Field") is False
        assert validator.validate_boolean(1, "Field") is True
        assert validator.validate_boolean(0, "Field") is False
        assert validator.validate_boolean(None, "Field", default=True) is True
    
    def test_validate_import_mode(self):
        """Test import mode validation."""
        validator = DataValidator()
        
        assert validator.validate_import_mode("full") == "full"
        assert validator.validate_import_mode("incremental") == "incremental"
        assert validator.validate_import_mode("update") == "update"
        
        with pytest.raises(ValidationError, match="must be one of"):
            validator.validate_import_mode("invalid")
    
    def test_validate_tags(self):
        """Test tags validation."""
        validator = DataValidator()
        
        assert validator.validate_tags("tag1,tag2,tag3") == ["tag1", "tag2", "tag3"]
        assert validator.validate_tags("  tag1  ,  tag2  ") == ["tag1", "tag2"]
        assert validator.validate_tags(["tag1", "tag2"]) == ["tag1", "tag2"]
        assert validator.validate_tags(None) == []
        assert validator.validate_tags("") == []


class TestDuplicateDetector:
    """Test DuplicateDetector class."""
    
    def test_generate_duplicate_key(self):
        """Test duplicate key generation."""
        detector = DuplicateDetector()
        
        key1 = detector.generate_duplicate_key(
            date(2024, 1, 15),
            Decimal("100.50"),
            "Test transaction"
        )
        
        key2 = detector.generate_duplicate_key(
            date(2024, 1, 15),
            Decimal("100.50"),
            "Test transaction"
        )
        
        # Same inputs should generate same key
        assert key1 == key2
        
        # Different inputs should generate different keys
        key3 = detector.generate_duplicate_key(
            date(2024, 1, 16),
            Decimal("100.50"),
            "Test transaction"
        )
        assert key1 != key3
    
    def test_is_duplicate(self):
        """Test duplicate detection."""
        detector = DuplicateDetector()
        
        key1 = detector.generate_duplicate_key(
            date(2024, 1, 15),
            Decimal("100.50"),
            "Test transaction"
        )
        
        existing_keys = {key1}
        
        assert detector.is_duplicate(key1, existing_keys) is True
        
        key2 = detector.generate_duplicate_key(
            date(2024, 1, 16),
            Decimal("100.50"),
            "Test transaction"
        )
        
        assert detector.is_duplicate(key2, existing_keys) is False

