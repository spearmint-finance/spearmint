"""FastAPI main application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from ..config import settings
from .error_handlers import (
    APIError,
    api_error_handler,
    validation_error_handler,
    sqlalchemy_error_handler,
    general_exception_handler
)
from .logging_config import RequestLoggingMiddleware, setup_logging
from .openapi_config import get_openapi_config, customize_openapi_schema

# Setup logging
setup_logging()

# Get OpenAPI configuration
openapi_config = get_openapi_config()

# Create FastAPI application
app = FastAPI(
    **openapi_config,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
# For development, allow all origins from localhost
cors_origins = settings.CORS_ORIGINS if not settings.DEBUG else ["*"]
print(f"DEBUG: CORS Origins: {cors_origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=False if cors_origins == ["*"] else True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Register exception handlers
app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
app.add_exception_handler(Exception, general_exception_handler)


# Health check endpoint
@app.get("/api/health", tags=["system"])
async def health_check():
    """Health check endpoint.
    
    Returns basic health status and API version information.
    Used by monitoring systems and load balancers to verify API availability.
    """
    return {"status": "healthy", "version": "0.0.75"}


# Import routers
from .routes import (
    transactions, categories, import_routes, analysis, relationships, projections, reports, classifications,
    persons, splits, scenarios, accounts, maintenance, auth, assistant, agents
)

# Register routers
app.include_router(transactions.router, prefix="/api", tags=["transactions"])
app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(import_routes.router, prefix="/api", tags=["import"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])
app.include_router(relationships.router, prefix="/api", tags=["relationships"])
app.include_router(projections.router, prefix="/api", tags=["projections"])
app.include_router(reports.router, prefix="/api", tags=["reports"])
app.include_router(classifications.router, prefix="/api", tags=["classifications"])
app.include_router(persons.router, prefix="/api", tags=["persons"])
app.include_router(splits.router, prefix="/api", tags=["splits"])
app.include_router(scenarios.router, prefix="/api", tags=["scenarios"])
app.include_router(accounts.router, prefix="/api", tags=["accounts"])
app.include_router(maintenance.router, prefix="/api", tags=["maintenance"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(assistant.router, prefix="/api", tags=["assistant"])
app.include_router(agents.router, prefix="/a2a", tags=["a2a-agents"])


# Root endpoint
@app.get("/", tags=["system"])
async def root():
    """Root endpoint."""
    return {
        "message": "Financial Analysis API",
        "version": "0.0.75",
        "docs": "/api/docs"
    }

# Customize OpenAPI schema
def custom_openapi():
    """Generate custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema

    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
        servers=app.servers,
    )

    # Customize the schema
    openapi_schema = customize_openapi_schema(openapi_schema)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Override the default OpenAPI schema
app.openapi = custom_openapi
