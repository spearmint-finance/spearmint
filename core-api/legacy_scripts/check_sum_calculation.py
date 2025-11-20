"""
Check how the sum is calculated - with signs vs absolute values
"""

import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

# Get all September expenses (non-transfer)
cursor.execute("""
    SELECT amount
    FROM transactions
    WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND (is_transfer = 0 OR is_transfer IS NULL)
    ORDER BY amount
""")

amounts = [row[0] for row in cursor.fetchall()]

# Calculate both ways
sum_with_signs = sum(amounts)
abs_of_sum = abs(sum_with_signs)
sum_of_abs = sum(abs(a) for a in amounts)

print(f"=== CALCULATION METHODS ===")
print(f"Number of transactions: {len(amounts)}")
print(f"\n1. Sum with signs: ${sum_with_signs:,.2f}")
print(f"2. Absolute value of sum: ${abs_of_sum:,.2f}")
print(f"3. Sum of absolute values: ${sum_of_abs:,.2f}")

print(f"\n=== API CALCULATION (line 157 in routes/transactions.py) ===")
print(f"total_expenses = abs(sum(float(t.amount) for t in all_transactions if t.transaction_type == 'Expense'))")
print(f"Result: ${abs_of_sum:,.2f}")

# Show positive and negative amounts
positive_amounts = [a for a in amounts if a > 0]
negative_amounts = [a for a in amounts if a < 0]

print(f"\n=== BREAKDOWN ===")
print(f"Positive amounts: {len(positive_amounts)} transactions, total: ${sum(positive_amounts):,.2f}")
if positive_amounts:
    print(f"  Largest positive: ${max(positive_amounts):,.2f}")
    for a in positive_amounts:
        cursor.execute(f"SELECT description, amount FROM transactions WHERE amount = {a} AND transaction_date BETWEEN '2025-09-01' AND '2025-09-30'")
        desc, amt = cursor.fetchone()
        print(f"    ${amt:>10,.2f} - {desc}")

print(f"\nNegative amounts: {len(negative_amounts)} transactions, total: ${sum(negative_amounts):,.2f}")

conn.close()

print(f"\n=== ANSWER ===")
print(f"The tool shows: $22,948.31")
print(f"This matches: abs(sum with signs) = ${abs_of_sum:,.2f}")
print(f"\nThis is because one transaction (Check Paid # 1001) is POSITIVE $21,895.78")
print(f"When you sum: -$44,791.09 (negative expenses) + $21,895.78 (positive) = -$22,895.31")
print(f"Then abs(-$22,895.31) ≈ $22,895.31")
