import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

# Check the data type and values of exclude_from_expense_calc
cursor.execute("""
    SELECT
        classification_id,
        classification_name,
        exclude_from_expense_calc,
        typeof(exclude_from_expense_calc) as data_type
    FROM transaction_classifications
    WHERE classification_id = 22
""")

row = cursor.fetchone()
print("Capital Expense Classification:")
print(f"  ID: {row[0]}")
print(f"  Name: {row[1]}")
print(f"  exclude_from_expense_calc: {row[2]}")
print(f"  Data Type: {row[3]}")
print(f"  Comparing to False: {row[2] == False}")
print(f"  Comparing to 0: {row[2] == 0}")
print(f"  Comparing to 1: {row[2] == 1}")

conn.close()
