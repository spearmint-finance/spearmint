"""
Check what the tool is showing without any filters applied
"""

import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

# Get excluded classification IDs
cursor.execute("""
    SELECT classification_id, classification_name, exclude_from_expense_calc
    FROM transaction_classifications
    WHERE exclude_from_expense_calc = 1
""")
excluded_classifications = cursor.fetchall()
excluded_ids = [row[0] for row in excluded_classifications]

print("=== EXCLUDED CLASSIFICATIONS ===")
for c in excluded_classifications:
    print(f"  ID {c[0]}: {c[1]}")

# Check what transactions are being shown (NO filters - just like the page in screenshot)
# The page appears to show ALL September transactions without date filter
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_type = 'Expense'
""")
result = cursor.fetchone()
print(f"\n=== ALL EXPENSES (NO FILTERS) ===")
print(f"Count: {result[0]}")
print(f"Total: ${result[1]:,.2f}")

# Check September specifically
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
""")
result = cursor.fetchone()
print(f"\n=== SEPTEMBER EXPENSES (ALL) ===")
print(f"Count: {result[0]}")
print(f"Total: ${result[1]:,.2f}")

# Check what visible transactions are shown (looking at the screenshot dates)
# They appear to be from 09/23 to 09/27
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_date BETWEEN '2025-09-23' AND '2025-09-27'
    AND transaction_type = 'Expense'
""")
result = cursor.fetchone()
print(f"\n=== 09/23/2025 to 09/27/2025 EXPENSES ===")
print(f"Count: {result[0]}")
print(f"Total: ${result[1]:,.2f}")

# Check with NO date filter, NO transfer filter, NO classification filter
# This would be the default view when page loads
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_type = 'Expense'
    ORDER BY transaction_date DESC
    LIMIT 138
""")
result = cursor.fetchone()
print(f"\n=== LAST 138 EXPENSE TRANSACTIONS ===")
print(f"Count: {result[0]}")
print(f"Total: ${result[1]:,.2f}")

# Let me check what 138 transactions with total ~$22,948 could be
# Maybe it's filtered by something we're not seeing
cursor.execute("""
    SELECT transaction_date, COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_type = 'Expense'
    GROUP BY transaction_date
    ORDER BY transaction_date DESC
    LIMIT 10
""")
print(f"\n=== RECENT EXPENSES BY DATE ===")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} transactions, ${row[2]:,.2f}")

# Check if there's a specific subset that equals 138 and ~$22,948
# Let me check September with certain exclusions
excluded_ids_str = ','.join(map(str, excluded_ids))

cursor.execute(f"""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND (is_transfer = 0 OR is_transfer IS NULL)
    AND (classification_id NOT IN ({excluded_ids_str}) OR classification_id IS NULL)
""")
result = cursor.fetchone()
print(f"\n=== SEPTEMBER FILTERED (EXCL TRANSFERS & CLASSIFICATIONS) ===")
print(f"Count: {result[0]}")
print(f"Total: ${result[1]:,.2f}")

# Maybe it's ALL transactions (not just September) with filters
cursor.execute(f"""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_type = 'Expense'
    AND (is_transfer = 0 OR is_transfer IS NULL)
    AND (classification_id NOT IN ({excluded_ids_str}) OR classification_id IS NULL)
""")
result = cursor.fetchone()
print(f"\n=== ALL EXPENSES FILTERED (EXCL TRANSFERS & CLASSIFICATIONS) ===")
print(f"Count: {result[0]}")
print(f"Total: ${result[1]:,.2f}")

# Check unclassified only
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_type = 'Expense'
    AND classification_id IS NULL
""")
result = cursor.fetchone()
print(f"\n=== UNCLASSIFIED EXPENSES ONLY ===")
print(f"Count: {result[0]}")
print(f"Total: ${result[1]:,.2f}")

# Check unclassified September
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
print(f"Count: {result[0]}")
print(f"Total: ${result[1]:,.2f}")

conn.close()
