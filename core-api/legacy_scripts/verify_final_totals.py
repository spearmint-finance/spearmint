"""
Verify what the tool will show after both fixes
"""

import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

print("=== VERIFICATION ===")
print("\nWith filters:")
print("  - Date: 09/01/2025 to 09/30/2025")
print("  - Type: Expense")
print("  - Is Transfer: No")
print("  - Classification: (all)")

# This is what the tool will query
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND (is_transfer = 0 OR is_transfer IS NULL)
""")
count, total = cursor.fetchone()

print(f"\nTool will show: {count} transactions, ${total:,.2f}")

# Breakdown by classification
print(f"\n=== BREAKDOWN ===")
cursor.execute("""
    SELECT
        COALESCE(tc.classification_name, 'Unclassified') as classification,
        COUNT(*) as count,
        SUM(ABS(t.amount)) as total
    FROM transactions t
    LEFT JOIN transaction_classifications tc ON t.classification_id = tc.classification_id
    WHERE t.transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND t.transaction_type = 'Expense'
    AND (t.is_transfer = 0 OR t.is_transfer IS NULL)
    GROUP BY tc.classification_name
    ORDER BY total DESC
""")

for row in cursor.fetchall():
    print(f"{row[0]:30s}: {row[1]:3d} transactions, ${row[2]:>10,.2f}")

# Get excluded classification IDs
cursor.execute("""
    SELECT classification_id
    FROM transaction_classifications
    WHERE exclude_from_expense_calc = 1
""")
excluded_ids = [row[0] for row in cursor.fetchall()]
excluded_ids_str = ','.join(map(str, excluded_ids))

# What it SHOULD show if we exclude capital expenses and credit card payments
cursor.execute(f"""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND (is_transfer = 0 OR is_transfer IS NULL)
    AND (classification_id NOT IN ({excluded_ids_str}) OR classification_id IS NULL)
""")
filtered_count, filtered_total = cursor.fetchone()

print(f"\n=== WHAT YOU EXPECT TO SEE ===")
print(f"If you want to match your Excel (excluding capital expenses & CC payments):")
print(f"You need to ADD these filters in the 'More Filters' dialog:")
print(f"  - Exclude Capital Expense classification")
print(f"  - Exclude Credit Card Payment classification")
print(f"\nThen it will show: {filtered_count} transactions, ${filtered_total:,.2f}")
print(f"Your Excel shows: 132 transactions, $26,240.31")
print(f"Difference: {filtered_count - 132} transactions, ${filtered_total - 26240.31:,.2f}")

conn.close()

print(f"\n=== SUMMARY ===")
print(f"✓ Fixed Check Paid # 1001 amount sign (positive to negative)")
print(f"✓ Fixed API calculation (abs(sum) to sum(abs))")
print(f"\nAfter refresh, the tool will show the CORRECT total of ${total:,.2f}")
print(f"This includes ALL September expenses (capital expenses, CC payments, everything)")
print(f"\nTo match your Excel, you need to manually exclude those classifications in the filter dialog.")
