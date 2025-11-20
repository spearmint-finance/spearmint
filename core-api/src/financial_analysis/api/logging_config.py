"""
Comprehensive logging configuration for the Financial Analysis API.

Provides structured logging with request/response tracking, performance metrics,
error tracking, and audit trail logging.
"""

import logging
import logging.config
import sys
import time
import json
from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)


# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "json": {
            "format": "%(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": sys.stdout
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": str(LOGS_DIR / "app.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "detailed",
            "filename": str(LOGS_DIR / "error.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        },
        "audit_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": str(LOGS_DIR / "audit.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 10
        },
        "performance_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": str(LOGS_DIR / "performance.log"),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    },
    "loggers": {
        "": {  # Root logger
            "level": "INFO",
            "handlers": ["console", "file", "error_file"]
        },
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False
        },
        "sqlalchemy.engine": {
            "level": "WARNING",
            "handlers": ["file"],
            "propagate": False
        },
        "audit": {
            "level": "INFO",
            "handlers": ["audit_file"],
            "propagate": False
        },
        "performance": {
            "level": "INFO",
            "handlers": ["performance_file"],
            "propagate": False
        }
    }
}


# JSON formatting helper function
def format_json_log(record: logging.LogRecord) -> str:
    """Format log record as JSON string."""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": record.levelname,
        "logger": record.name,
        "message": record.getMessage(),
        "module": record.module,
        "function": record.funcName,
        "line": record.lineno
    }

    # Add extra fields if present
    if hasattr(record, "extra"):
        log_data.update(record.extra)

    # Add exception info if present
    if record.exc_info:
        log_data["exception"] = logging.Formatter().formatException(record.exc_info)

    return json.dumps(log_data)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger("api.requests")
        self.performance_logger = logging.getLogger("performance")
        self.audit_logger = logging.getLogger("audit")
    
    async def dispatch(self, request: Request, call_next):
        """Log request and response with performance metrics."""
        # Generate request ID
        request_id = f"{int(time.time() * 1000)}-{id(request)}"
        
        # Log request
        request_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_host": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent")
        }
        
        self.logger.info(
            f"{request.method} {request.url.path}",
            extra=request_data
        )
        
        # Track performance
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            response_data = {
                **request_data,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2)
            }
            
            self.logger.info(
                f"{request.method} {request.url.path} - {response.status_code} - {duration:.3f}s",
                extra=response_data
            )
            
            # Log performance metrics
            self.performance_logger.info(
                "Request completed",
                extra=response_data
            )
            
            # Log audit trail for write operations
            if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
                self.audit_logger.info(
                    f"{request.method} operation on {request.url.path}",
                    extra=response_data
                )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as exc:
            # Log error
            duration = time.time() - start_time
            
            error_data = {
                **request_data,
                "error": str(exc),
                "error_type": type(exc).__name__,
                "duration_ms": round(duration * 1000, 2)
            }
            
            self.logger.error(
                f"{request.method} {request.url.path} - Error: {str(exc)}",
                extra=error_data,
                exc_info=True
            )
            
            raise


class AuditLogger:
    """Audit logger for tracking important operations."""
    
    def __init__(self):
        self.logger = logging.getLogger("audit")
    
    def log_classification_change(
        self,
        transaction_id: int,
        old_classification: Optional[str],
        new_classification: str,
        user: Optional[str] = None,
        reason: Optional[str] = None
    ):
        """Log transaction classification change."""
        self.logger.info(
            "Classification changed",
            extra={
                "event_type": "classification_change",
                "transaction_id": transaction_id,
                "old_classification": old_classification,
                "new_classification": new_classification,
                "user": user,
                "reason": reason
            }
        )
    
    def log_relationship_created(
        self,
        transaction_id_1: int,
        transaction_id_2: int,
        relationship_type: str,
        confidence: Optional[float] = None,
        auto_detected: bool = False
    ):
        """Log relationship creation."""
        self.logger.info(
            "Relationship created",
            extra={
                "event_type": "relationship_created",
                "transaction_id_1": transaction_id_1,
                "transaction_id_2": transaction_id_2,
                "relationship_type": relationship_type,
                "confidence": confidence,
                "auto_detected": auto_detected
            }
        )
    
    def log_bulk_operation(
        self,
        operation: str,
        count: int,
        success_count: int,
        failed_count: int,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log bulk operation."""
        self.logger.info(
            f"Bulk operation: {operation}",
            extra={
                "event_type": "bulk_operation",
                "operation": operation,
                "total_count": count,
                "success_count": success_count,
                "failed_count": failed_count,
                "details": details
            }
        )
    
    def log_data_export(
        self,
        export_type: str,
        format: str,
        record_count: int,
        user: Optional[str] = None
    ):
        """Log data export operation."""
        self.logger.info(
            f"Data exported: {export_type}",
            extra={
                "event_type": "data_export",
                "export_type": export_type,
                "format": format,
                "record_count": record_count,
                "user": user
            }
        )


def setup_logging():
    """Configure logging for the application."""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")


def get_audit_logger() -> AuditLogger:
    """Get audit logger instance."""
    return AuditLogger()


# Initialize logging on module import
setup_logging()

