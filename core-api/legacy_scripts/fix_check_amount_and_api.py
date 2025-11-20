"""
Fix two issues:
1. Change Check Paid # 1001 amount from positive to negative
2. Note: API calculation will be fixed separately in the code file
"""

import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

# Check current state
print("=== BEFORE FIX ===")
cursor.execute("""
    SELECT transaction_id, transaction_date, description, amount, transaction_type
    FROM transactions
    WHERE description = 'Check Paid # 1001'
    AND transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
""")
result = cursor.fetchone()
if result:
    print(f"ID {result[0]}: {result[1]} | {result[2]} | Amount: ${result[3]:,.2f} | Type: {result[4]}")

# Fix the amount - make it negative
cursor.execute("""
    UPDATE transactions
    SET amount = -21895.78,
        updated_at = CURRENT_TIMESTAMP
    WHERE transaction_id = 459
""")
print(f"\nUpdated transaction 459 amount from $21,895.78 to -$21,895.78")

conn.commit()

# Verify update
print("\n=== AFTER FIX ===")
cursor.execute("""
    SELECT transaction_id, transaction_date, description, amount, transaction_type
    FROM transactions
    WHERE description = 'Check Paid # 1001'
    AND transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
""")
result = cursor.fetchone()
if result:
    print(f"ID {result[0]}: {result[1]} | {result[2]} | Amount: ${result[3]:,.2f} | Type: {result[4]}")

# Now check what the NEW total should be
print("\n=== RECALCULATING TOTALS ===")

# With the OLD (buggy) calculation
cursor.execute("""
    SELECT SUM(amount)
    FROM transactions
    WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND (is_transfer = 0 OR is_transfer IS NULL)
""")
sum_with_signs = cursor.fetchone()[0]
print(f"Old calculation [abs(sum)]: ${abs(sum_with_signs):,.2f}")

# With the CORRECT calculation
cursor.execute("""
    SELECT SUM(ABS(amount))
    FROM transactions
    WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND (is_transfer = 0 OR is_transfer IS NULL)
""")
sum_of_abs = cursor.fetchone()[0]
print(f"New calculation [sum(abs)]: ${sum_of_abs:,.2f}")

cursor.execute("""
    SELECT COUNT(*)
    FROM transactions
    WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND (is_transfer = 0 OR is_transfer IS NULL)
""")
count = cursor.fetchone()[0]

print(f"\n=== SUMMARY ===")
print(f"After fixing both the amount sign AND the API calculation:")
print(f"  {count} transactions, ${sum_of_abs:,.2f}")
print(f"\nThis should match your Excel after removing the 5 reinvestments:")
print(f"  Your Excel: 132 transactions, $26,240.31")
print(f"  Difference: {count - 132} transactions, ${sum_of_abs - 26240.31:,.2f}")

conn.close()

print("\nDatabase updated successfully!")
print("Next step: Fix the API calculation in the code")
