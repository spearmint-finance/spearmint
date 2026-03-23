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
    return {"status": "healthy", "version": "0.0.119"}


# Import routers
from .routes import (
    transactions, categories, import_routes, analysis, relationships, projections, reports,
    persons, splits, scenarios, accounts, maintenance, auth, assistant, agents, aggregator, entities
)

# Register routers
app.include_router(transactions.router, prefix="/api", tags=["transactions"])
app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(import_routes.router, prefix="/api", tags=["import"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])
app.include_router(relationships.router, prefix="/api", tags=["relationships"])
app.include_router(projections.router, prefix="/api", tags=["projections"])
app.include_router(reports.router, prefix="/api", tags=["reports"])
app.include_router(persons.router, prefix="/api", tags=["persons"])
app.include_router(splits.router, prefix="/api", tags=["splits"])
app.include_router(scenarios.router, prefix="/api", tags=["scenarios"])
app.include_router(accounts.router, prefix="/api", tags=["accounts"])
app.include_router(entities.router, prefix="/api", tags=["entities"])
app.include_router(maintenance.router, prefix="/api", tags=["maintenance"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(assistant.router, prefix="/api", tags=["assistant"])
app.include_router(aggregator.router, prefix="/api", tags=["link"])
app.include_router(agents.router, prefix="/a2a", tags=["a2a-agents"])


# Ensure database tables exist on startup
@app.on_event("startup")
def ensure_database_tables():
    """Create database tables if they don't exist, and run lightweight migrations."""
    from ..database.base import engine, Base
    from ..database import models  # noqa: F401 — registers all models
    Base.metadata.create_all(bind=engine)

    # Lightweight migrations for existing databases
    from sqlalchemy import inspect, text
    inspector = inspect(engine)

    # Migration: add entity_id to categories
    if inspector.has_table("categories"):
        columns = [c["name"] for c in inspector.get_columns("categories")]
        if "entity_id" not in columns:
            with engine.begin() as conn:
                conn.execute(text(
                    "ALTER TABLE categories ADD COLUMN entity_id INTEGER "
                    "REFERENCES entities(entity_id)"
                ))

    # Migration: add missing columns to transactions
    if inspector.has_table("transactions"):
        columns = [c["name"] for c in inspector.get_columns("transactions")]
        tx_additions = [
            ("entity_id", "INTEGER REFERENCES entities(entity_id)"),
            ("is_capital_expense", "BOOLEAN DEFAULT 0"),
            ("is_tax_deductible", "BOOLEAN DEFAULT 0"),
            ("is_recurring", "BOOLEAN DEFAULT 0"),
            ("is_reimbursable", "BOOLEAN DEFAULT 0"),
            ("exclude_from_income", "BOOLEAN DEFAULT 0"),
            ("exclude_from_expenses", "BOOLEAN DEFAULT 0"),
        ]
        with engine.begin() as conn:
            for col_name, col_def in tx_additions:
                if col_name not in columns:
                    conn.execute(text(
                        f"ALTER TABLE transactions ADD COLUMN {col_name} {col_def}"
                    ))

    # Migration: repurpose transaction_splits from person-based to category-based
    if inspector.has_table("transaction_splits"):
        columns = [c["name"] for c in inspector.get_columns("transaction_splits")]
        if "person_id" in columns:
            with engine.begin() as conn:
                conn.execute(text("DROP TABLE transaction_splits"))
            # create_all below will recreate with new schema
    Base.metadata.create_all(bind=engine)  # ensure new table exists after drop

    # Migration: convert Transfer transaction_type to Income/Expense based on amount sign
    if inspector.has_table("transactions"):
        columns = [c["name"] for c in inspector.get_columns("transactions")]
        if "transaction_type" in columns:
            with engine.begin() as conn:
                conn.execute(text(
                    "UPDATE transactions SET transaction_type = "
                    "CASE WHEN amount >= 0 THEN 'Income' ELSE 'Expense' END "
                    "WHERE transaction_type = 'Transfer'"
                ))

    # Migration: update categories CHECK constraint to include 'Transfer' type
    # SQLite can't ALTER constraints, so we recreate the table if needed.
    if inspector.has_table("categories"):
        result = engine.connect().execute(text(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='categories'"
        )).fetchone()
        if result and "'Transfer'" not in result[0]:
            with engine.begin() as conn:
                conn.execute(text("PRAGMA foreign_keys = OFF"))
                conn.execute(text("""
                    CREATE TABLE categories_new (
                        category_id INTEGER NOT NULL,
                        category_name VARCHAR(100) NOT NULL,
                        category_type VARCHAR(10) NOT NULL,
                        parent_category_id INTEGER,
                        description TEXT,
                        is_transfer_category BOOLEAN,
                        is_fixed_obligation BOOLEAN,
                        created_at DATETIME,
                        entity_id INTEGER REFERENCES entities(entity_id),
                        PRIMARY KEY (category_id),
                        CONSTRAINT check_category_type CHECK (category_type IN ('Income', 'Expense', 'Transfer', 'Both')),
                        UNIQUE (category_name),
                        FOREIGN KEY(parent_category_id) REFERENCES categories_new (category_id)
                    )
                """))
                conn.execute(text(
                    "INSERT INTO categories_new SELECT category_id, category_name, category_type, "
                    "parent_category_id, description, is_transfer_category, is_fixed_obligation, "
                    "created_at, entity_id FROM categories"
                ))
                conn.execute(text("DROP TABLE categories"))
                conn.execute(text("ALTER TABLE categories_new RENAME TO categories"))
                conn.execute(text("PRAGMA foreign_keys = ON"))

    # Migration: migrate account.entity_id data to account_entities join table
    if inspector.has_table("accounts") and inspector.has_table("account_entities"):
        columns = [c["name"] for c in inspector.get_columns("accounts")]
        if "entity_id" in columns:
            with engine.begin() as conn:
                # Copy existing entity_id assignments to the join table
                conn.execute(text(
                    "INSERT OR IGNORE INTO account_entities (account_id, entity_id) "
                    "SELECT account_id, entity_id FROM accounts "
                    "WHERE entity_id IS NOT NULL"
                ))


# Root endpoint
@app.get("/", tags=["system"])
async def root():
    """Root endpoint."""
    return {
        "message": "Financial Analysis API",
        "version": "0.0.119",
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
