"""
Migration script to add the category_rules table.

This script adds the category_rules table to an existing database
without affecting any existing data.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from sqlalchemy import text
from financial_analysis.database.base import SessionLocal, engine


def add_category_rules_table():
    """Add the category_rules table to the database."""
    
    print("=" * 60)
    print("Adding category_rules table to database")
    print("=" * 60)
    
    # SQL to create the category_rules table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS category_rules (
        rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_name VARCHAR(100) NOT NULL,
        rule_priority INTEGER DEFAULT 100,
        category_id INTEGER NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        description_pattern VARCHAR(255),
        source_pattern VARCHAR(255),
        amount_min DECIMAL(10, 2),
        amount_max DECIMAL(10, 2),
        payment_method_pattern VARCHAR(50),
        transaction_type_pattern VARCHAR(10),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );
    """
    
    # SQL to create indexes
    create_indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_category_rules_category ON category_rules(category_id);",
        "CREATE INDEX IF NOT EXISTS idx_category_rules_priority ON category_rules(rule_priority);",
        "CREATE INDEX IF NOT EXISTS idx_category_rules_active ON category_rules(is_active);"
    ]
    
    db = SessionLocal()
    try:
        # Check if table already exists
        result = db.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='category_rules';"
        ))
        table_exists = result.fetchone() is not None
        
        if table_exists:
            print("\n✓ category_rules table already exists")
        else:
            print("\nCreating category_rules table...")
            db.execute(text(create_table_sql))
            db.commit()
            print("✓ category_rules table created successfully")
            
            print("\nCreating indexes...")
            for index_sql in create_indexes_sql:
                db.execute(text(index_sql))
            db.commit()
            print("✓ Indexes created successfully")
        
        # Verify table structure
        result = db.execute(text("PRAGMA table_info(category_rules);"))
        columns = result.fetchall()
        print(f"\n✓ Table has {len(columns)} columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        print("\n" + "=" * 60)
        print("✓ Migration complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_category_rules_table()

