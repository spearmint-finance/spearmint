# How to Classify Transactions as Capital Expenses

## Quick Start

### Step 1: One-Time Setup (5 minutes)

Run this command once:
```bash
python add_capital_expense_classification.py --simple
```

This creates the "Capital Expense" classification in your database.

### Step 2: Classify Individual Transactions

#### Method 1: Through Classifications Page (Recommended for Bulk)

1. Go to **Classifications** page in the UI (`/classifications`)
2. Click on **Classification Rules** tab
3. Create a rule:
   - **Rule Name**: "Auto-classify large purchases"
   - **Conditions**:
     - Amount less than -$1,000
     - AND Category contains "Vehicle" OR "Equipment" OR "Property"
   - **Action**: Apply classification "Capital Expense"
4. Click **Save**

Now all future large purchases in those categories will be automatically classified!

#### Method 2: Through Transaction Edit (For Individual Transactions)

Currently, you need to use the database directly or create a classification rule. **We'll add a quick-classify button to the transaction UI soon!**

For now, you can:

1. Create appropriate **Categories** first:
   - Vehicle Purchase
   - Equipment
   - Home Improvement
   - Property Investment

2. Categorize your transaction with one of these categories

3. Create a **Classification Rule** that auto-classifies transactions in these categories

### Step 3: Using the Three-Way Toggle

On the Analysis page, you now have three options:

```
[Operating] [+ Capital] [All]
```

#### Operating (Default)
- ✅ Shows: Regular operating income and expenses only
- ❌ Hides: Transfers AND capital expenses
- 📊 Use for: Monthly budgets, spending trends, savings rate

**Example:**
```
September Operating Expenses:
- Groceries: $800
- Utilities: $200
- Gas: $150
Total: $1,150 ✅ Clean monthly average
```

#### + Capital (New!)
- ✅ Shows: Operating expenses AND capital expenses
- ❌ Hides: Transfers only
- 📊 Use for: Total spending analysis without transfer noise

**Example:**
```
September with Capital:
- Operating: $1,150
- Car Purchase: $35,000
Total: $36,150 ✅ Total spending, no transfer clutter
```

#### All
- ✅ Shows: Everything including transfers
- 📊 Use for: Reconciliation, tax prep, complete picture

**Example:**
```
September All Transactions:
- Operating: $1,150
- Car Purchase: $35,000
- Transfer to Savings: $5,000
Total: $41,150 ✅ Complete cash movement
```

## Manual Classification (Until UI is Updated)

### Using SQLite Command

If you need to manually classify a specific transaction:

```bash
python -c "
import sqlite3
conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

# Find the capital expense classification ID
cursor.execute(\"SELECT classification_id FROM transaction_classifications WHERE classification_code = 'CAPITAL_EXPENSE'\")
capex_id = cursor.fetchone()[0]

# Update a specific transaction (replace 12345 with your transaction ID)
cursor.execute(\"UPDATE transactions SET classification_id = ? WHERE id = ?\", (capex_id, 12345))

conn.commit()
print(f'Transaction 12345 classified as capital expense')
"
```

### Using Python Script

Create a file `classify_transaction.py`:

```python
import sqlite3
import sys

def classify_as_capital_expense(transaction_id):
    conn = sqlite3.connect('financial_analysis.db')
    cursor = conn.cursor()

    # Get capital expense classification ID
    cursor.execute(
        "SELECT classification_id FROM transaction_classifications "
        "WHERE classification_code = 'CAPITAL_EXPENSE'"
    )
    result = cursor.fetchone()

    if not result:
        print("Error: Capital Expense classification not found!")
        print("Run: python add_capital_expense_classification.py --simple")
        return

    capex_id = result[0]

    # Update transaction
    cursor.execute(
        "UPDATE transactions SET classification_id = ? WHERE id = ?",
        (capex_id, transaction_id)
    )

    conn.commit()
    print(f"✅ Transaction {transaction_id} classified as Capital Expense")
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python classify_transaction.py <transaction_id>")
        print("Example: python classify_transaction.py 12345")
        sys.exit(1)

    transaction_id = int(sys.argv[1])
    classify_as_capital_expense(transaction_id)
```

Then use it:
```bash
python classify_transaction.py 12345
```

## Bulk Classification Script

To classify multiple transactions at once, create `bulk_classify.py`:

```python
import sqlite3

def bulk_classify_capital_expenses():
    conn = sqlite3.connect('financial_analysis.db')
    cursor = conn.cursor()

    # Get capital expense classification ID
    cursor.execute(
        "SELECT classification_id FROM transaction_classifications "
        "WHERE classification_code = 'CAPITAL_EXPENSE'"
    )
    capex_id = cursor.fetchone()[0]

    # Classify all transactions in "Vehicle Purchase" category
    cursor.execute("""
        UPDATE transactions
        SET classification_id = ?
        WHERE category_id IN (
            SELECT category_id FROM categories
            WHERE category_name IN ('Vehicle Purchase', 'Equipment', 'Home Improvement', 'Property Investment')
        )
        AND amount < -1000
    """, (capex_id,))

    rows_updated = cursor.rowcount
    conn.commit()

    print(f"✅ Classified {rows_updated} transactions as Capital Expenses")
    conn.close()

if __name__ == "__main__":
    bulk_classify_capital_expenses()
```

Run it:
```bash
python bulk_classify.py
```

## Classification Rules (Recommended Approach)

Instead of manual classification, set up rules through the UI:

### Rule 1: Vehicle Purchases
```
Name: Capital Expense - Vehicles
Conditions:
  - Category = "Vehicle Purchase"
  OR
  - Amount < -$5,000 AND Description contains "car|vehicle|auto|truck"
Action: Apply "Capital Expense" classification
```

### Rule 2: Equipment
```
Name: Capital Expense - Equipment
Conditions:
  - Category = "Equipment" AND Amount < -$1,000
  OR
  - Description contains "laptop|computer|macbook|desk|chair|furniture"
    AND Amount < -$500
Action: Apply "Capital Expense" classification
```

### Rule 3: Property Improvements
```
Name: Capital Expense - Property
Conditions:
  - Category = "Home Improvement" AND Amount < -$2,000
  OR
  - Description contains "roof|hvac|renovation|remodel|addition"
Action: Apply "Capital Expense" classification
```

## Verifying Classification

To see all capital expenses:

```bash
python view_capital_expenses.py
```

Or query directly:
```bash
python -c "
import sqlite3
conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT
        t.id,
        DATE(t.transaction_date) as date,
        t.description,
        t.amount,
        c.category_name
    FROM transactions t
    LEFT JOIN categories c ON t.category_id = c.category_id
    LEFT JOIN transaction_classifications tc ON t.classification_id = tc.classification_id
    WHERE tc.classification_code = 'CAPITAL_EXPENSE'
    ORDER BY t.transaction_date DESC
    LIMIT 20
''')

rows = cursor.fetchall()
print(f'{'ID':<8} {'Date':<12} {'Description':<40} {'Amount':<12} {'Category':<20}')
print('-' * 100)
for r in rows:
    print(f'{r[0]:<8} {r[1]:<12} {r[2]:<40.37} ${abs(r[3]):<11.2f} {r[4] or \"None\":<20}')
"
```

## Summary

### Quick Classification Workflow:

1. **Setup** (once): `python add_capital_expense_classification.py --simple`
2. **Create Categories**: Vehicle Purchase, Equipment, etc.
3. **Create Rules**: Auto-classify based on category + amount
4. **Use Toggle**: Switch between Operating, + Capital, and All views
5. **Verify**: `python view_capital_expenses.py`

### Future Enhancement

We're working on adding a **Quick Classify** button directly in the transaction UI, so you can classify with one click!

For now, use classification rules for the best experience.

---

**Questions?** See the full guide at `capital-expenses-guide.md`
