"""
Fix classification for 3 September transactions:
- Check Paid # 1001 -> Capital Expense (ID 22)
- Two CITI AUTOPAY PAYMENT -> Credit Card Payment (ID 3)
"""

import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

# Get classification IDs
cursor.execute("SELECT classification_id, classification_name FROM transaction_classifications WHERE classification_name IN ('Capital Expense', 'Credit Card Payment')")
classifications = cursor.fetchall()
print("Available classifications:")
for c in classifications:
    print(f"  ID {c[0]}: {c[1]}")

capital_expense_id = None
credit_card_payment_id = None

for c in classifications:
    if c[1] == 'Capital Expense':
        capital_expense_id = c[0]
    elif c[1] == 'Credit Card Payment':
        credit_card_payment_id = c[0]

print(f"\nCapital Expense ID: {capital_expense_id}")
print(f"Credit Card Payment ID: {credit_card_payment_id}")

# Check current state
print("\n=== BEFORE UPDATE ===")
cursor.execute("""
    SELECT transaction_id, transaction_date, description, amount, classification_id, is_transfer
    FROM transactions
    WHERE description IN ('DIRECT DEBIT CITI AUTOPAY PAYMENT', 'Check Paid # 1001')
    AND transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    ORDER BY transaction_date
""")
transactions = cursor.fetchall()
for t in transactions:
    print(f"ID {t[0]}: {t[1]} | {t[2][:40]:40s} | ${t[3]:>10.2f} | Classification: {t[4]} | Transfer: {t[5]}")

# Update Check Paid # 1001 to Capital Expense
print(f"\n=== UPDATING ===")
cursor.execute("""
    UPDATE transactions
    SET classification_id = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE transaction_id = 459
""", (capital_expense_id,))
print(f"Updated transaction 459 (Check Paid # 1001) to Capital Expense (ID {capital_expense_id})")

# Update CITI AUTOPAY payments to Credit Card Payment
cursor.execute("""
    UPDATE transactions
    SET classification_id = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE transaction_id IN (555, 562)
""", (credit_card_payment_id,))
print(f"Updated transactions 555, 562 (CITI AUTOPAY) to Credit Card Payment (ID {credit_card_payment_id})")

conn.commit()

# Verify updates
print("\n=== AFTER UPDATE ===")
cursor.execute("""
    SELECT transaction_id, transaction_date, description, amount, classification_id, is_transfer
    FROM transactions
    WHERE description IN ('DIRECT DEBIT CITI AUTOPAY PAYMENT', 'Check Paid # 1001')
    AND transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    ORDER BY transaction_date
""")
transactions = cursor.fetchall()
for t in transactions:
    print(f"ID {t[0]}: {t[1]} | {t[2][:40]:40s} | ${t[3]:>10.2f} | Classification: {t[4]} | Transfer: {t[5]}")

# Now check what the filtered total should be
print("\n=== RECALCULATING FILTERED TOTAL ===")

cursor.execute("""
    SELECT classification_id, exclude_from_expense_calc
    FROM transaction_classifications
    WHERE exclude_from_expense_calc = 1
""")
excluded_ids = [row[0] for row in cursor.fetchall()]
print(f"Excluded classification IDs: {excluded_ids}")

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

print(f"\n=== NEW FILTERED TOTAL (WHAT TOOL WILL SHOW) ===")
print(f"Count: {result[0]}")
print(f"Total: ${result[1]:,.2f}")

print(f"\n=== COMPARISON ===")
print(f"Your Excel (after removing 5 reinvestments): $26,240.31")
print(f"Database (after fixing 3 transactions):       ${result[1]:,.2f}")
print(f"Difference:                                    ${26240.31 - result[1]:,.2f}")

conn.close()

print("\n✓ Successfully updated 3 transactions!")
print("Please refresh your tool to see the updated totals.")
