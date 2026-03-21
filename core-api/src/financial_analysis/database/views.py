"""
Database views for financial analysis (PRD Section 3.3).

These views provide filtered and aggregated data for analysis purposes.
"""

from sqlalchemy import text
from .base import engine


# View definitions as SQL
VIEWS = {
    "v_analysis_transactions": """
        CREATE VIEW IF NOT EXISTS v_analysis_transactions AS
        SELECT
            t.*,
            c.category_name,
            c.category_type
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.category_id
        WHERE t.include_in_analysis = 1
    """,

    "v_income_analysis": """
        CREATE VIEW IF NOT EXISTS v_income_analysis AS
        SELECT
            t.*,
            c.category_name
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.category_id
        WHERE t.transaction_type = 'Income'
          AND t.include_in_analysis = 1
          AND t.transaction_id NOT IN (
              SELECT tt.transaction_id FROM transaction_tags tt
              JOIN tags tg ON tt.tag_id = tg.tag_id
              WHERE tg.tag_name = 'exclude-from-income'
          )
    """,

    "v_expense_analysis": """
        CREATE VIEW IF NOT EXISTS v_expense_analysis AS
        SELECT
            t.*,
            c.category_name
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.category_id
        WHERE t.transaction_type = 'Expense'
          AND t.include_in_analysis = 1
          AND t.transaction_id NOT IN (
              SELECT tt.transaction_id FROM transaction_tags tt
              JOIN tags tg ON tt.tag_id = tg.tag_id
              WHERE tg.tag_name = 'exclude-from-expenses'
          )
    """,

    "v_transfer_transactions": """
        CREATE VIEW IF NOT EXISTS v_transfer_transactions AS
        SELECT
            t.*,
            c.category_name,
            tr.relationship_type,
            t2.transaction_id as related_tx_id,
            t2.description as related_tx_description
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.category_id
        LEFT JOIN transaction_relationships tr
            ON t.transaction_id = tr.transaction_id_1 OR t.transaction_id = tr.transaction_id_2
        LEFT JOIN transactions t2
            ON (tr.transaction_id_1 = t2.transaction_id AND tr.transaction_id_2 = t.transaction_id)
            OR (tr.transaction_id_2 = t2.transaction_id AND tr.transaction_id_1 = t.transaction_id)
        WHERE c.category_type = 'Transfer'
    """
}


def create_views():
    """Create all database views."""
    with engine.connect() as conn:
        for view_name, view_sql in VIEWS.items():
            try:
                conn.execute(text(view_sql))
                conn.commit()
                print(f"+ Created view: {view_name}")
            except Exception as e:
                print(f"- Error creating view {view_name}: {e}")


def drop_views():
    """Drop all database views."""
    with engine.connect() as conn:
        for view_name in VIEWS.keys():
            try:
                conn.execute(text(f"DROP VIEW IF EXISTS {view_name}"))
                conn.commit()
                print(f"+ Dropped view: {view_name}")
            except Exception as e:
                print(f"- Error dropping view {view_name}: {e}")

