"""
OpenAPI/Swagger configuration for the Financial Analysis API.

Provides enhanced API documentation with detailed descriptions,
examples, and interactive documentation.
"""

from typing import Dict, Any


# API metadata
API_TITLE = "Financial Analysis API"
API_VERSION = "0.0.63"
API_DESCRIPTION = """
# Financial Analysis API

A comprehensive REST API for financial transaction analysis and management.

## Features

### Transaction Management
- Import transactions from CSV files
- CRUD operations for transactions and categories
- Advanced filtering and search capabilities

### Analysis & Insights
- Income and expense analysis with category breakdowns
- Cash flow analysis and trends
- Financial health indicators
- Time-series analysis (daily, weekly, monthly, quarterly, yearly)

### Relationship Detection
- Automatic transfer pair detection
- Credit card payment/receipt matching
- Reimbursement pair detection
- Manual relationship management

### Projections & Forecasting
- Income and expense projections
- Cash flow forecasting
- Multiple projection algorithms (linear regression, moving average, exponential smoothing, weighted average)
- Scenario analysis (best case, worst case, expected)
- Accuracy metrics (MAPE, RMSE, MAE, R-squared)

### Reporting & Export
- Summary reports with key metrics
- Detailed income/expense reports
- Reconciliation reports
- Export to JSON and CSV formats

### Classification System
- 10 system classifications for transaction types
- Custom user-defined classifications
- Pattern-based classification rules
- Bulk and automatic classification
- Classification-aware calculations

### Error Handling & Logging
- Standardized error responses with detailed error codes
- Comprehensive request/response logging
- Performance monitoring
- Audit trail for data modifications

## Analysis Modes

The API supports two analysis modes:

- **ANALYSIS** (default) - Excludes transfers, reimbursements, and other non-income/expense transactions for accurate financial analysis
- **COMPLETE** - Includes all transactions for reconciliation and complete transaction history

## Authentication

Currently, the API does not require authentication. Authentication will be added in a future release.

## Rate Limiting

Currently, there are no rate limits. Rate limiting will be added in a future release.

## Support

For issues, questions, or feature requests, please contact the development team.
"""

# Contact information
API_CONTACT = {
    "name": "Financial Analysis API Team",
    "email": "support@example.com",
}

# License information
API_LICENSE = {
    "name": "MIT",
    "url": "https://opensource.org/licenses/MIT",
}

# Tags for grouping endpoints
API_TAGS = [
    {
        "name": "transactions",
        "description": "Transaction management operations. Create, read, update, and delete transactions.",
    },
    {
        "name": "categories",
        "description": "Category management operations. Manage transaction categories and subcategories.",
    },
    {
        "name": "import",
        "description": "Data import operations. Import transactions from CSV files with automatic category detection.",
    },
    {
        "name": "analysis",
        "description": "Financial analysis operations. Analyze income, expenses, cash flow, and financial health indicators.",
    },
    {
        "name": "relationships",
        "description": "Transaction relationship operations. Detect and manage relationships between transactions (transfers, credit card payments, reimbursements).",
    },
    {
        "name": "projections",
        "description": "Financial projection operations. Project future income, expenses, and cash flow using multiple algorithms.",
    },
    {
        "name": "reports",
        "description": "Report generation operations. Generate summary, detail, and reconciliation reports with export capabilities.",
    },
    {
        "name": "classifications",
        "description": "Classification management operations. Manage transaction classifications, rules, and automatic classification.",
    },
]

# Servers configuration
API_SERVERS = [
    {
        "url": "http://localhost:8000",
        "description": "Development server",
    },
    {
        "url": "http://localhost:8000",
        "description": "Production server (update with actual URL)",
    },
]

# Common response examples
COMMON_RESPONSES = {
    "400": {
        "description": "Bad Request - Invalid input",
        "content": {
            "application/json": {
                "example": {
                    "error": "ERR_1000",
                    "error_code": "ERR_1000",
                    "category": "validation",
                    "message": "Request validation failed",
                    "validation_errors": [
                        {
                            "field": "amount",
                            "message": "value is not a valid decimal",
                            "value": "invalid"
                        }
                    ],
                    "path": "/api/transactions"
                }
            }
        }
    },
    "404": {
        "description": "Not Found - Resource not found",
        "content": {
            "application/json": {
                "example": {
                    "error": "ERR_2000",
                    "error_code": "ERR_2000",
                    "category": "not_found",
                    "message": "Transaction with ID 123 not found",
                    "details": {
                        "resource": "Transaction",
                        "resource_id": "123"
                    },
                    "path": "/api/transactions/123"
                }
            }
        }
    },
    "409": {
        "description": "Conflict - Resource conflict",
        "content": {
            "application/json": {
                "example": {
                    "error": "ERR_3000",
                    "error_code": "ERR_3000",
                    "category": "conflict",
                    "message": "Classification with code 'TRANSFER' already exists",
                    "details": {
                        "code": "TRANSFER"
                    },
                    "path": "/api/classifications"
                }
            }
        }
    },
    "500": {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {
                    "error": "ERR_9000",
                    "error_code": "ERR_9000",
                    "category": "internal",
                    "message": "An unexpected error occurred",
                    "path": "/api/transactions"
                }
            }
        }
    },
}


def get_openapi_config() -> Dict[str, Any]:
    """Get OpenAPI configuration for FastAPI."""
    return {
        "title": API_TITLE,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "contact": API_CONTACT,
        "license_info": API_LICENSE,
        "openapi_tags": API_TAGS,
        "servers": API_SERVERS,
    }


def customize_openapi_schema(openapi_schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Customize the OpenAPI schema with additional information.
    
    Args:
        openapi_schema: The generated OpenAPI schema
        
    Returns:
        The customized OpenAPI schema
    """
    # 1. Generate Unique Operation IDs
    # LibLab and other generators require unique operationIds to generate clean method names.
    paths = openapi_schema.get('paths', {})
    for path, methods in paths.items():
        for method, details in methods.items():
            if 'operationId' not in details:
                # Create a unique ID based on tags and method
                # e.g. transactions_get, maintenance_fix_classifications_post
                tags = details.get('tags', ['default'])
                tag = tags[0] if tags else 'default'
                
                # Clean path for ID generation
                clean_path = path.replace('/api/', '').replace('/', '_').replace('{', '').replace('}', '')
                if clean_path.startswith('_'): clean_path = clean_path[1:]
                
                operation_id = f"{method}_{clean_path}"
                details['operationId'] = operation_id

    # Add security schemes (for future authentication)
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT authentication (to be implemented)"
        },
        "apiKey": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API key authentication (to be implemented)"
        }
    }
    
    # Add common response schemas
    if "responses" not in openapi_schema["components"]:
        openapi_schema["components"]["responses"] = {}
    
    openapi_schema["components"]["responses"].update(COMMON_RESPONSES)
    
    # Add external documentation
    openapi_schema["externalDocs"] = {
        "description": "Find more information in the project documentation",
        "url": "https://github.com/spearmint-finance/spearmint"
    }
    
    return openapi_schema

