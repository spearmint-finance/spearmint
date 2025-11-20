"""
Enhanced error handling for the Financial Analysis API.

Provides standardized error responses with detailed error codes,
categories, and helpful messages for debugging and user feedback.
"""

from typing import Optional, Dict, Any, List
from enum import Enum
from pydantic import BaseModel
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging

logger = logging.getLogger(__name__)


class ErrorCategory(str, Enum):
    """Error categories for classification."""
    VALIDATION = "validation"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    FORBIDDEN = "forbidden"
    DATABASE = "database"
    INTERNAL = "internal"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"


class ErrorCode(str, Enum):
    """Specific error codes for detailed error identification."""
    # Validation errors (1000-1999)
    INVALID_INPUT = "ERR_1000"
    MISSING_REQUIRED_FIELD = "ERR_1001"
    INVALID_DATE_RANGE = "ERR_1002"
    INVALID_AMOUNT = "ERR_1003"
    INVALID_CLASSIFICATION = "ERR_1004"
    
    # Not found errors (2000-2999)
    TRANSACTION_NOT_FOUND = "ERR_2000"
    CATEGORY_NOT_FOUND = "ERR_2001"
    CLASSIFICATION_NOT_FOUND = "ERR_2002"
    RULE_NOT_FOUND = "ERR_2003"
    RELATIONSHIP_NOT_FOUND = "ERR_2004"
    
    # Conflict errors (3000-3999)
    DUPLICATE_TRANSACTION = "ERR_3000"
    DUPLICATE_CATEGORY = "ERR_3001"
    DUPLICATE_CLASSIFICATION = "ERR_3002"
    DUPLICATE_RULE = "ERR_3003"
    RELATIONSHIP_EXISTS = "ERR_3004"
    
    # Forbidden errors (4000-4999)
    SYSTEM_CLASSIFICATION_PROTECTED = "ERR_4000"
    CANNOT_DELETE_IN_USE = "ERR_4001"
    OPERATION_NOT_ALLOWED = "ERR_4002"
    
    # Database errors (5000-5999)
    DATABASE_ERROR = "ERR_5000"
    INTEGRITY_CONSTRAINT = "ERR_5001"
    CONNECTION_ERROR = "ERR_5002"
    
    # Internal errors (9000-9999)
    INTERNAL_SERVER_ERROR = "ERR_9000"
    UNEXPECTED_ERROR = "ERR_9999"


class ValidationDetail(BaseModel):
    """Detailed validation error information."""
    field: str
    message: str
    value: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Standardized error response model."""
    error: str
    error_code: str
    category: ErrorCategory
    message: str
    details: Optional[Dict[str, Any]] = None
    validation_errors: Optional[List[ValidationDetail]] = None
    timestamp: Optional[str] = None
    path: Optional[str] = None


class APIError(HTTPException):
    """Base API error with enhanced error information."""
    
    def __init__(
        self,
        status_code: int,
        error_code: ErrorCode,
        category: ErrorCategory,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        validation_errors: Optional[List[ValidationDetail]] = None
    ):
        self.error_code = error_code
        self.category = category
        self.details = details
        self.validation_errors = validation_errors
        
        super().__init__(
            status_code=status_code,
            detail={
                "error": error_code.value,
                "error_code": error_code.value,
                "category": category.value,
                "message": message,
                "details": details,
                "validation_errors": [v.model_dump() for v in validation_errors] if validation_errors else None
            }
        )


# Specific error classes for common scenarios

class ValidationError(APIError):
    """Validation error (400)."""
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.INVALID_INPUT,
        details: Optional[Dict[str, Any]] = None,
        validation_errors: Optional[List[ValidationDetail]] = None
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=error_code,
            category=ErrorCategory.VALIDATION,
            message=message,
            details=details,
            validation_errors=validation_errors
        )


class NotFoundError(APIError):
    """Resource not found error (404)."""
    def __init__(
        self,
        resource: str,
        resource_id: Any,
        error_code: ErrorCode = ErrorCode.TRANSACTION_NOT_FOUND
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=error_code,
            category=ErrorCategory.NOT_FOUND,
            message=f"{resource} with ID {resource_id} not found",
            details={"resource": resource, "resource_id": str(resource_id)}
        )


class ConflictError(APIError):
    """Resource conflict error (409)."""
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.DUPLICATE_TRANSACTION,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code=error_code,
            category=ErrorCategory.CONFLICT,
            message=message,
            details=details
        )


class ForbiddenError(APIError):
    """Forbidden operation error (403)."""
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.OPERATION_NOT_ALLOWED,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=error_code,
            category=ErrorCategory.FORBIDDEN,
            message=message,
            details=details
        )


class DatabaseError(APIError):
    """Database operation error (500)."""
    def __init__(
        self,
        message: str = "Database operation failed",
        error_code: ErrorCode = ErrorCode.DATABASE_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code=error_code,
            category=ErrorCategory.DATABASE,
            message=message,
            details=details
        )


# Exception handlers

async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handle APIError exceptions."""
    logger.error(
        f"API Error: {exc.error_code.value} - {exc.detail.get('message')}",
        extra={
            "error_code": exc.error_code.value,
            "category": exc.category.value,
            "path": request.url.path,
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors."""
    validation_errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        validation_errors.append(
            ValidationDetail(
                field=field,
                message=error["msg"],
                value=error.get("input")
            ).model_dump()
        )
    
    logger.warning(
        f"Validation Error: {len(validation_errors)} field(s) failed validation",
        extra={
            "path": request.url.path,
            "method": request.method,
            "errors": validation_errors
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": ErrorCode.INVALID_INPUT.value,
            "error_code": ErrorCode.INVALID_INPUT.value,
            "category": ErrorCategory.VALIDATION.value,
            "message": "Request validation failed",
            "validation_errors": validation_errors,
            "path": request.url.path
        }
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle SQLAlchemy database errors."""
    error_code = ErrorCode.DATABASE_ERROR
    message = "Database operation failed"
    
    # Handle specific SQLAlchemy errors
    if isinstance(exc, IntegrityError):
        error_code = ErrorCode.INTEGRITY_CONSTRAINT
        message = "Database integrity constraint violated"
    
    logger.error(
        f"Database Error: {str(exc)}",
        extra={
            "error_type": type(exc).__name__,
            "path": request.url.path,
            "method": request.method
        },
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": error_code.value,
            "error_code": error_code.value,
            "category": ErrorCategory.DATABASE.value,
            "message": message,
            "path": request.url.path
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(
        f"Unexpected Error: {str(exc)}",
        extra={
            "error_type": type(exc).__name__,
            "path": request.url.path,
            "method": request.method
        },
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": ErrorCode.INTERNAL_SERVER_ERROR.value,
            "error_code": ErrorCode.INTERNAL_SERVER_ERROR.value,
            "category": ErrorCategory.INTERNAL.value,
            "message": "An unexpected error occurred",
            "path": request.url.path
        }
    )

