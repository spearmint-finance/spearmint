"""
Check what the database returns with EXACTLY the filters shown in the tool:
- Start Date: 09/01/2025
- End Date: 09/30/2025
- Transaction Type: Expense
- Is Transfer: No
- Classification: (empty - all classifications)
"""

import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

# This is EXACTLY what the tool is querying
cursor.execute("""
    SELECT COUNT(*), SUM(ABS(amount))
    FROM transactions
    WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND (is_transfer = 0 OR is_transfer IS NULL)
""")
result = cursor.fetchone()

print(f"=== TOOL QUERY (NO CLASSIFICATION FILTER) ===")
print(f"Count: {result[0]}")
print(f"Total: ${result[1]:,.2f}")

# Show breakdown by classification
print(f"\n=== BREAKDOWN BY CLASSIFICATION ===")
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

conn.close()

print(f"\n=== ANSWER ===")
print(f"The tool is showing ALL September expenses (excluding transfers)")
print(f"It is NOT automatically excluding capital expenses or credit card payments")
print(f"This is why you see a higher total than your Excel spreadsheet")
