# Database Module

This module contains the database schema, models, and initialization scripts for the financial analysis tool.

## Overview

The database is designed to support comprehensive financial transaction tracking with intelligent classification to prevent double-counting in financial calculations.

## Database Schema

### Core Tables

#### 1. **transaction_classifications**
Stores classification types that determine how transactions are treated in financial calculations.

**Key Fields:**
- `classification_code`: Unique code (e.g., STANDARD, TRANSFER, CC_PAYMENT)
- `exclude_from_income_calc`: Boolean flag to exclude from income calculations
- `exclude_from_expense_calc`: Boolean flag to exclude from expense calculations
- `exclude_from_cashflow_calc`: Boolean flag to exclude from cashflow calculations

**Default Classifications:**
1. `STANDARD` - Regular income/expense transactions
2. `TRANSFER` - Internal transfers (excluded from all calculations)
3. `CC_PAYMENT` - Credit card payments (excluded from expense calculations)
4. `CC_RECEIPT` - Credit card receipts (excluded from income calculations)
5. `REIMB_PAID` - Reimbursable expenses
6. `REIMB_RECEIVED` - Reimbursement income (excluded from income calculations)
7. `REFUND` - Refunds (excluded from income calculations)
8. `LOAN_DISB` - Loan disbursements (excluded from income calculations)
9. `LOAN_PRINCIPAL` - Loan principal payments (excluded from expense calculations)
10. `LOAN_INTEREST` - Loan interest payments (included as expense)

#### 2. **categories**
Hierarchical categorization system for transactions.

**Key Fields:**
- `category_name`: Unique category name
- `category_type`: Income, Expense, or Both
- `parent_category_id`: Self-referencing foreign key for hierarchy
- `is_transfer_category`: Flag for transfer categories

#### 3. **transactions**
Core table storing all financial transactions.

**Key Fields:**
- `transaction_date`: Date of transaction
- `amount`: Transaction amount (Decimal)
- `transaction_type`: Income or Expense
- `category_id`: Foreign key to categories
- `classification_id`: Foreign key to transaction_classifications
- `include_in_analysis`: Boolean flag (default: True)
- `is_transfer`: Boolean flag for transfers
- `related_transaction_id`: Self-referencing for related transactions

**Indexes:**
- `transaction_date`, `transaction_type`, `category_id`
- `classification_id`, `include_in_analysis`, `is_transfer`
- `related_transaction_id`

#### 4. **transaction_relationships**
Links related transactions (e.g., transfer pairs, credit card payment/receipt pairs).

**Key Fields:**
- `transaction_id_1`, `transaction_id_2`: Foreign keys to transactions
- `relationship_type`: Type of relationship (e.g., "transfer_pair", "cc_payment_pair")
- Unique constraint on (transaction_id_1, transaction_id_2, relationship_type)

#### 5. **classification_rules**
Pattern-based rules for automatic transaction classification.

**Key Fields:**
- `rule_name`: Descriptive name
- `rule_priority`: Lower number = higher priority
- `classification_id`: Target classification
- `description_pattern`, `category_pattern`, `source_pattern`: Pattern matching fields
- `amount_min`, `amount_max`: Amount range filters
- `set_include_in_analysis`, `set_is_transfer`: Actions to apply

#### 6. **tags** and **transaction_tags**
Flexible tagging system for transactions (many-to-many relationship).

#### 7. **import_history**
Tracks data import operations.

**Key Fields:**
- `file_name`, `file_path`: Source file information
- `total_rows`, `successful_rows`, `failed_rows`: Import statistics
- `classified_rows`: Number of automatically classified transactions
- `import_mode`: Import mode (e.g., "append", "replace")

#### 8. **budgets**
Budget tracking by category (future enhancement).

### Database Views

#### 1. **v_analysis_transactions**
All transactions where `include_in_analysis = True`, joined with category and classification information.

#### 2. **v_income_analysis**
Income transactions filtered by:
- `transaction_type = 'Income'`
- `include_in_analysis = True`
- `exclude_from_income_calc = False` (or NULL)

#### 3. **v_expense_analysis**
Expense transactions filtered by:
- `transaction_type = 'Expense'`
- `include_in_analysis = True`
- `exclude_from_expense_calc = False` (or NULL)

#### 4. **v_transfer_transactions**
All transfer transactions with relationship information.

## Usage

### Initialize Database

```python
from financial_analysis.database.init_db import initialize_database

# Create tables, views, and seed default data
initialize_database()

# Reset database (WARNING: deletes all data)
initialize_database(reset=True)
```

Or use the CLI:

```bash
# Initialize database
python src/financial_analysis/database/init_db.py

# Reset database
python src/financial_analysis/database/init_db.py --reset
```

### Working with Models

```python
from financial_analysis.database.base import SessionLocal
from financial_analysis.database.models import Transaction, Category, TransactionClassification
from datetime import date
from decimal import Decimal

# Create a session
db = SessionLocal()

# Create a category
category = Category(
    category_name="Groceries",
    category_type="Expense"
)
db.add(category)
db.commit()

# Get a classification
classification = db.query(TransactionClassification).filter_by(
    classification_code="STANDARD"
).first()

# Create a transaction
transaction = Transaction(
    transaction_date=date(2025, 1, 15),
    amount=Decimal("125.50"),
    transaction_type="Expense",
    category_id=category.category_id,
    classification_id=classification.classification_id,
    description="Weekly groceries",
    source="Whole Foods"
)
db.add(transaction)
db.commit()

# Close session
db.close()
```

### Querying Views

```python
from sqlalchemy import text

# Query analysis-ready transactions
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM v_analysis_transactions"))
    for row in result:
        print(row)
```

## Testing

Run the database schema tests:

```bash
pytest tests/test_database_schema.py -v
```

## Files

- `base.py` - Database engine, session management, and base model
- `models.py` - SQLAlchemy ORM models for all tables
- `views.py` - Database view definitions and creation utilities
- `seed_data.py` - Default data seeding (classifications and rules)
- `init_db.py` - Database initialization script with CLI support

## Design Principles

1. **Prevent Double-Counting**: Classification system ensures transactions are correctly included/excluded from financial calculations
2. **Relationship Tracking**: Link related transactions (transfers, credit card payments) to maintain data integrity
3. **Flexible Classification**: Pattern-based rules enable automatic classification with priority ordering
4. **Audit Trail**: Track all imports and maintain creation/update timestamps
5. **Hierarchical Categories**: Support nested categories for detailed organization
6. **Extensibility**: Tag system allows flexible custom categorization

## Future Enhancements

- Budget tracking and alerts
- Recurring transaction templates
- Multi-currency support
- Advanced pattern matching with regex
- Machine learning-based classification

