#!/bin/bash
set -e

echo "=== Spearmint Core API Startup ==="

# Initialize database (creates tables if they don't exist)
echo "Initializing database..."
python -c "
from src.financial_analysis.database.base import Base, engine
from src.financial_analysis.database.models import *  # Import all models including APIKey

# Create all tables
Base.metadata.create_all(bind=engine)
print('Database tables initialized.')
"

# Seed default data if database is empty
echo "Checking for seed data..."
python -c "
from src.financial_analysis.database.base import SessionLocal
from src.financial_analysis.database.models import TransactionClassification
from src.financial_analysis.database.seed_data import seed_all

db = SessionLocal()
try:
    # Check if classifications exist (indicator of seeded data)
    count = db.query(TransactionClassification).count()
    if count == 0:
        print('Seeding default data...')
        seed_all(db)
        print('Default data seeded.')
    else:
        print(f'Database already has {count} classifications, skipping seed.')
finally:
    db.close()
"

echo "Starting uvicorn server..."
exec uvicorn src.financial_analysis.api.main:app --host 0.0.0.0 --port 8000 "$@"
