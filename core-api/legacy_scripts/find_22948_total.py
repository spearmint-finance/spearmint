"""
Find which combination of filters produces 138 transactions totaling $22,948.31
"""

import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

target_count = 138
target_total = 22948.31

print(f"Looking for: {target_count} transactions, ${target_total:,.2f}")

# Check unclassified only (all dates)
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_type = 'Expense'
    AND classification_id IS NULL
    AND (is_transfer = 0 OR is_transfer IS NULL)
""")
result = cursor.fetchone()
print(f"\n=== ALL UNCLASSIFIED NON-TRANSFER EXPENSES ===")
print(f"Count: {result[0]}, Total: ${result[1]:,.2f}")
if result[0] == target_count:
    print("  *** MATCH ON COUNT! ***")

# Check September unclassified
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND classification_id IS NULL
    AND (is_transfer = 0 OR is_transfer IS NULL)
""")
result = cursor.fetchone()
print(f"\n=== SEPTEMBER UNCLASSIFIED NON-TRANSFER EXPENSES ===")
print(f"Count: {result[0]}, Total: ${result[1]:,.2f}")

# Maybe it's filtered to show ONLY Regular Transaction classification?
# Or maybe it's showing transactions WITHOUT certain classifications?

# Let me check if it's showing transactions with classification_id = 21 (Regular Transaction)
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_type = 'Expense'
    AND classification_id = 21
    AND (is_transfer = 0 OR is_transfer IS NULL)
""")
result = cursor.fetchone()
print(f"\n=== ALL 'REGULAR TRANSACTION' EXPENSES ===")
print(f"Count: {result[0]}, Total: ${result[1]:,.2f}")

# Check September Regular Transaction
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND classification_id = 21
    AND (is_transfer = 0 OR is_transfer IS NULL)
""")
result = cursor.fetchone()
print(f"\n=== SEPTEMBER 'REGULAR TRANSACTION' EXPENSES ===")
print(f"Count: {result[0]}, Total: ${result[1]:,.2f}")

# Maybe the page is paginated and showing a subset?
# Let me check the last 138 unclassified transactions
cursor.execute("""
    SELECT COUNT(*) as cnt, SUM(ABS(amount)) as total
    FROM (
        SELECT amount
        FROM transactions
        WHERE transaction_type = 'Expense'
        AND classification_id IS NULL
        AND (is_transfer = 0 OR is_transfer IS NULL)
        ORDER BY transaction_date DESC
        LIMIT 138
    )
""")
result = cursor.fetchone()
print(f"\n=== LAST 138 UNCLASSIFIED NON-TRANSFER EXPENSES ===")
print(f"Count: {result[0]}, Total: ${result[1]:,.2f}")
if abs(result[1] - target_total) < 1:
    print("  *** MATCH ON TOTAL! ***")

# Check different date ranges
# Maybe it's August + September?
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_date BETWEEN '2025-08-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND classification_id IS NULL
    AND (is_transfer = 0 OR is_transfer IS NULL)
""")
result = cursor.fetchone()
print(f"\n=== AUG + SEPT UNCLASSIFIED NON-TRANSFER EXPENSES ===")
print(f"Count: {result[0]}, Total: ${result[1]:,.2f}")

# Maybe July + August + September?
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_date BETWEEN '2025-07-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND classification_id IS NULL
    AND (is_transfer = 0 OR is_transfer IS NULL)
""")
result = cursor.fetchone()
print(f"\n=== JUL + AUG + SEPT UNCLASSIFIED NON-TRANSFER EXPENSES ===")
print(f"Count: {result[0]}, Total: ${result[1]:,.2f}")
if result[0] == target_count:
    print("  *** MATCH ON COUNT! ***")
if abs(result[1] - target_total) < 1:
    print("  *** MATCH ON TOTAL! ***")

# Let me check without the is_transfer filter
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_date BETWEEN '2025-07-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND classification_id IS NULL
""")
result = cursor.fetchone()
print(f"\n=== JUL + AUG + SEPT UNCLASSIFIED (INCLUDING TRANSFERS) ===")
print(f"Count: {result[0]}, Total: ${result[1]:,.2f}")

# Or maybe it's Q3 (July, August, September)?
cursor.execute("""
    SELECT
        MIN(transaction_date) as first_date,
        MAX(transaction_date) as last_date,
        COUNT(*),
        SUM(ABS(amount))
    FROM (
        SELECT transaction_date, amount
        FROM transactions
        WHERE transaction_type = 'Expense'
        AND classification_id IS NULL
        AND (is_transfer = 0 OR is_transfer IS NULL)
        ORDER BY transaction_date DESC
        LIMIT 138
    )
""")
result = cursor.fetchone()
print(f"\n=== LAST 138 TRANSACTIONS DATE RANGE ===")
print(f"Date range: {result[0]} to {result[1]}")
print(f"Count: {result[2]}, Total: ${result[3]:,.2f}")
if abs(result[3] - target_total) < 1:
    print("  *** MATCH ON TOTAL! This is what the tool is showing! ***")

conn.close()
