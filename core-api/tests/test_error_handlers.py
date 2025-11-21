"""
Tests for API error handlers.

Tests the enhanced error handling system including error responses,
error codes, and exception handlers.
"""

import pytest
from fastapi import status
from financial_analysis.api.error_handlers import (
    ErrorCategory,
    ErrorCode,
    ValidationDetail,
    APIError,
    ValidationError,
    NotFoundError,
    ConflictError,
    ForbiddenError,
    DatabaseError
)


class TestErrorClasses:
    """Test error class creation and properties."""
    
    def test_validation_error(self):
        """Test ValidationError creation."""
        error = ValidationError(
            message="Invalid input",
            error_code=ErrorCode.INVALID_INPUT,
            details={"field": "amount"}
        )
        
        assert error.status_code == status.HTTP_400_BAD_REQUEST
        assert error.error_code == ErrorCode.INVALID_INPUT
        assert error.category == ErrorCategory.VALIDATION
        assert error.detail["message"] == "Invalid input"
        assert error.detail["details"]["field"] == "amount"
    
    def test_validation_error_with_field_details(self):
        """Test ValidationError with field-level validation details."""
        validation_errors = [
            ValidationDetail(
                field="amount",
                message="must be greater than zero",
                value=-10
            ),
            ValidationDetail(
                field="transaction_date",
                message="field required",
                value=None
            )
        ]
        
        error = ValidationError(
            message="Request validation failed",
            validation_errors=validation_errors
        )
        
        assert error.status_code == status.HTTP_400_BAD_REQUEST
        assert len(error.detail["validation_errors"]) == 2
        assert error.detail["validation_errors"][0]["field"] == "amount"
        assert error.detail["validation_errors"][1]["field"] == "transaction_date"
    
    def test_not_found_error(self):
        """Test NotFoundError creation."""
        error = NotFoundError(
            resource="Transaction",
            resource_id=123,
            error_code=ErrorCode.TRANSACTION_NOT_FOUND
        )
        
        assert error.status_code == status.HTTP_404_NOT_FOUND
        assert error.error_code == ErrorCode.TRANSACTION_NOT_FOUND
        assert error.category == ErrorCategory.NOT_FOUND
        assert "123" in error.detail["message"]
        assert error.detail["details"]["resource"] == "Transaction"
        assert error.detail["details"]["resource_id"] == "123"
    
    def test_conflict_error(self):
        """Test ConflictError creation."""
        error = ConflictError(
            message="Classification already exists",
            error_code=ErrorCode.DUPLICATE_CLASSIFICATION,
            details={"code": "TRANSFER"}
        )
        
        assert error.status_code == status.HTTP_409_CONFLICT
        assert error.error_code == ErrorCode.DUPLICATE_CLASSIFICATION
        assert error.category == ErrorCategory.CONFLICT
        assert error.detail["message"] == "Classification already exists"
        assert error.detail["details"]["code"] == "TRANSFER"
    
    def test_forbidden_error(self):
        """Test ForbiddenError creation."""
        error = ForbiddenError(
            message="System classifications cannot be modified",
            error_code=ErrorCode.SYSTEM_CLASSIFICATION_PROTECTED
        )
        
        assert error.status_code == status.HTTP_403_FORBIDDEN
        assert error.error_code == ErrorCode.SYSTEM_CLASSIFICATION_PROTECTED
        assert error.category == ErrorCategory.FORBIDDEN
        assert "System classifications" in error.detail["message"]
    
    def test_database_error(self):
        """Test DatabaseError creation."""
        error = DatabaseError(
            message="Database operation failed",
            error_code=ErrorCode.DATABASE_ERROR,
            details={"operation": "insert"}
        )
        
        assert error.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert error.error_code == ErrorCode.DATABASE_ERROR
        assert error.category == ErrorCategory.DATABASE
        assert error.detail["message"] == "Database operation failed"
        assert error.detail["details"]["operation"] == "insert"


class TestErrorCodes:
    """Test error code definitions."""
    
    def test_validation_error_codes(self):
        """Test validation error codes (1000-1999)."""
        assert ErrorCode.INVALID_INPUT.value == "ERR_1000"
        assert ErrorCode.MISSING_REQUIRED_FIELD.value == "ERR_1001"
        assert ErrorCode.INVALID_DATE_RANGE.value == "ERR_1002"
        assert ErrorCode.INVALID_AMOUNT.value == "ERR_1003"
        assert ErrorCode.INVALID_CLASSIFICATION.value == "ERR_1004"
    
    def test_not_found_error_codes(self):
        """Test not found error codes (2000-2999)."""
        assert ErrorCode.TRANSACTION_NOT_FOUND.value == "ERR_2000"
        assert ErrorCode.CATEGORY_NOT_FOUND.value == "ERR_2001"
        assert ErrorCode.CLASSIFICATION_NOT_FOUND.value == "ERR_2002"
        assert ErrorCode.RULE_NOT_FOUND.value == "ERR_2003"
        assert ErrorCode.RELATIONSHIP_NOT_FOUND.value == "ERR_2004"
    
    def test_conflict_error_codes(self):
        """Test conflict error codes (3000-3999)."""
        assert ErrorCode.DUPLICATE_TRANSACTION.value == "ERR_3000"
        assert ErrorCode.DUPLICATE_CATEGORY.value == "ERR_3001"
        assert ErrorCode.DUPLICATE_CLASSIFICATION.value == "ERR_3002"
        assert ErrorCode.DUPLICATE_RULE.value == "ERR_3003"
        assert ErrorCode.RELATIONSHIP_EXISTS.value == "ERR_3004"
    
    def test_forbidden_error_codes(self):
        """Test forbidden error codes (4000-4999)."""
        assert ErrorCode.SYSTEM_CLASSIFICATION_PROTECTED.value == "ERR_4000"
        assert ErrorCode.CANNOT_DELETE_IN_USE.value == "ERR_4001"
        assert ErrorCode.OPERATION_NOT_ALLOWED.value == "ERR_4002"
    
    def test_database_error_codes(self):
        """Test database error codes (5000-5999)."""
        assert ErrorCode.DATABASE_ERROR.value == "ERR_5000"
        assert ErrorCode.INTEGRITY_CONSTRAINT.value == "ERR_5001"
        assert ErrorCode.CONNECTION_ERROR.value == "ERR_5002"
    
    def test_internal_error_codes(self):
        """Test internal error codes (9000-9999)."""
        assert ErrorCode.INTERNAL_SERVER_ERROR.value == "ERR_9000"
        assert ErrorCode.UNEXPECTED_ERROR.value == "ERR_9999"


class TestErrorCategories:
    """Test error category definitions."""
    
    def test_error_categories(self):
        """Test all error categories are defined."""
        assert ErrorCategory.VALIDATION.value == "validation"
        assert ErrorCategory.NOT_FOUND.value == "not_found"
        assert ErrorCategory.CONFLICT.value == "conflict"
        assert ErrorCategory.FORBIDDEN.value == "forbidden"
        assert ErrorCategory.DATABASE.value == "database"
        assert ErrorCategory.INTERNAL.value == "internal"
        assert ErrorCategory.AUTHENTICATION.value == "authentication"
        assert ErrorCategory.AUTHORIZATION.value == "authorization"


class TestValidationDetail:
    """Test ValidationDetail model."""
    
    def test_validation_detail_creation(self):
        """Test ValidationDetail creation."""
        detail = ValidationDetail(
            field="amount",
            message="must be greater than zero",
            value=-10
        )
        
        assert detail.field == "amount"
        assert detail.message == "must be greater than zero"
        assert detail.value == -10
    
    def test_validation_detail_dict(self):
        """Test ValidationDetail dict conversion."""
        detail = ValidationDetail(
            field="transaction_date",
            message="field required",
            value=None
        )

        detail_dict = detail.model_dump()
        assert detail_dict["field"] == "transaction_date"
        assert detail_dict["message"] == "field required"
        assert detail_dict["value"] is None


class TestErrorResponseStructure:
    """Test error response structure."""
    
    def test_error_response_has_required_fields(self):
        """Test error response contains all required fields."""
        error = NotFoundError(
            resource="Transaction",
            resource_id=123
        )
        
        detail = error.detail
        assert "error" in detail
        assert "error_code" in detail
        assert "category" in detail
        assert "message" in detail
        assert "details" in detail
    
    def test_error_response_consistency(self):
        """Test error response format is consistent."""
        errors = [
            ValidationError(message="Invalid input"),
            NotFoundError(resource="Transaction", resource_id=123),
            ConflictError(message="Duplicate resource"),
            ForbiddenError(message="Operation not allowed"),
            DatabaseError(message="Database error")
        ]
        
        for error in errors:
            detail = error.detail
            # All errors should have these fields
            assert "error" in detail
            assert "error_code" in detail
            assert "category" in detail
            assert "message" in detail
            # error and error_code should be the same
            assert detail["error"] == detail["error_code"]
            # error_code should start with "ERR_"
            assert detail["error_code"].startswith("ERR_")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

