import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

# Find reinvestment transactions in September
query = """
SELECT
    transaction_id,
    transaction_date,
    amount,
    description,
    classification_id,
    is_transfer,
    include_in_analysis
FROM transactions
WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND description LIKE '%REINVESTMENT%'
ORDER BY transaction_date
"""

cursor.execute(query)
reinvestments = cursor.fetchall()

print("=== REINVESTMENT TRANSACTIONS IN SEPTEMBER 2025 ===\n")
total = 0
for row in reinvestments:
    print(f"ID: {row[0]}")
    print(f"  Date: {row[1]}")
    print(f"  Amount: ${abs(float(row[2])):,.2f}")
    print(f"  Description: {row[3][:60]}")
    print(f"  Classification ID: {row[4]}")
    print(f"  Is Transfer: {row[5]}")
    print(f"  Include in Analysis: {row[6]}")
    print()
    total += abs(float(row[2]))

print(f"Total Reinvestments: {len(reinvestments)}")
print(f"Total Amount: ${total:,.2f}")

# Check what classification these should have
cursor.execute("""
SELECT classification_id, classification_name, exclude_from_expense_calc
FROM transaction_classifications
WHERE classification_name LIKE '%invest%'
   OR classification_name LIKE '%distribut%'
""")

print("\n=== INVESTMENT-RELATED CLASSIFICATIONS ===\n")
for row in cursor.fetchall():
    print(f"ID {row[0]}: {row[1]} (exclude_from_expense_calc: {row[2]})")

conn.close()
