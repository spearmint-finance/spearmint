import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT
        SUM(amount) as total,
        COUNT(*) as count,
        MIN(amount) as min_amt,
        MAX(amount) as max_amt,
        SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) as total_expenses,
        SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as total_income
    FROM transactions
    WHERE classification_id = 22
""")

row = cursor.fetchone()
print(f"""
Capital Expense Transactions (classification_id = 22):
=======================================================
Total Count: {row[1]}
Total Net Amount: ${row[0]:,.2f}
Total Expenses (negative): ${row[4]:,.2f}
Total Income (positive): ${row[5]:,.2f}
Min Amount: ${row[2]:,.2f}
Max Amount: ${row[3]:,.2f}
""")

conn.close()
