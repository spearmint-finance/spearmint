import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

# Check the Capital Expense classification settings
cursor.execute("""
    SELECT classification_id, classification_name, classification_code,
           exclude_from_income_calc, exclude_from_expense_calc, exclude_from_cashflow_calc
    FROM transaction_classifications
    WHERE classification_code = 'CAPITAL_EXPENSE'
""")

classification = cursor.fetchone()
if classification:
    print("\n=== Capital Expense Classification ===")
    print(f"ID: {classification[0]}")
    print(f"Name: {classification[1]}")
    print(f"Code: {classification[2]}")
    print(f"Exclude from income calc: {classification[3]}")
    print(f"Exclude from expense calc: {classification[4]}")
    print(f"Exclude from cashflow calc: {classification[5]}")

    # Count transactions with this classification
    cursor.execute("""
        SELECT COUNT(*) FROM transactions WHERE classification_id = ?
    """, (classification[0],))
    count = cursor.fetchone()[0]
    print(f"\nTotal transactions classified as Capital Expense: {count}")

    # Show sample transactions
    cursor.execute("""
        SELECT t.transaction_id, t.transaction_date, t.description, t.amount, c.category_name
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.category_id
        WHERE t.classification_id = ?
        ORDER BY t.transaction_date DESC
        LIMIT 5
    """, (classification[0],))

    print("\n=== Sample Capital Expense Transactions ===")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Date: {row[1]}, Amount: ${row[3]:,.2f}, Category: {row[4]}, Desc: {row[2][:50]}")

else:
    print("Capital Expense classification not found!")

conn.close()
