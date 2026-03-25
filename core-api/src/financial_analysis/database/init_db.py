"""
Database initialization script.

Creates all tables, views, and seeds default data.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from financial_analysis.database.base import init_db, drop_db, SessionLocal
from financial_analysis.database.views import create_views, drop_views
from financial_analysis.database.seed_data import seed_all


def initialize_database(reset: bool = False):
    """
    Initialize the database with tables, views, and seed data.

    Args:
        reset: If True, drop existing tables before creating new ones
    """
    print("=" * 60)
    print("Financial Analysis Tool - Database Initialization")
    print("=" * 60)
    
    if reset:
        print("\nWARNING:  WARNING: Resetting database (all data will be lost)")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            return
        
        print("\nDropping existing views...")
        drop_views()
        
        print("\nDropping existing tables...")
        drop_db()
    
    print("\nCreating database tables...")
    init_db()
    print("+ Tables created successfully")
    
    print("\nCreating database views...")
    create_views()
    
    print("\nSeeding default data...")
    db = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()

    print("\n" + "=" * 60)
    print("+ Database initialization complete!")
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize the financial analysis database")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset the database (drop all tables and recreate)"
    )
    args = parser.parse_args()
    initialize_database(reset=args.reset)

