"""
Script to verify September 2025 transactions between Excel file and database.
Compares transactions excluding income, capital expenses, and transfers.
"""

import pandas as pd
import sqlite3
from datetime import datetime
from decimal import Decimal

# Read Excel file
excel_file = r"C:\Users\harry\Downloads\transactions-sept.xlsx"
print(f"Reading Excel file: {excel_file}")
df_excel = pd.read_excel(excel_file)

print(f"\n=== EXCEL FILE ANALYSIS ===")
print(f"Total rows in Excel: {len(df_excel)}")
print(f"Columns: {df_excel.columns.tolist()}")

# Display first few rows to understand structure
print(f"\nFirst 5 rows:")
print(df_excel.head())

# Calculate Excel totals
excel_count = len(df_excel)
# Try to find amount column (could be 'amount', 'Amount', 'Transaction Amount', etc.)
amount_col = None
for col in df_excel.columns:
    if 'amount' in col.lower():
        amount_col = col
        break

if amount_col:
    excel_total = df_excel[amount_col].abs().sum()
    print(f"\nExcel Summary:")
    print(f"  Count: {excel_count}")
    print(f"  Total (absolute): ${excel_total:,.2f}")
else:
    print("\nCould not find amount column in Excel file")
    print("Available columns:", df_excel.columns.tolist())

# Connect to database
print(f"\n=== DATABASE ANALYSIS ===")
conn = sqlite3.connect('financial_analysis.db')

# Query all September 2025 expenses
query_all = """
SELECT
    id,
    transaction_date,
    description,
    amount,
    transaction_type,
    category_id,
    classification_id,
    is_transfer,
    source,
    payment_method
FROM transactions
WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
ORDER BY transaction_date, description
"""

df_db_all = pd.read_sql_query(query_all, conn)
print(f"\nAll September 2025 Expenses in Database:")
print(f"  Count: {len(df_db_all)}")
print(f"  Total (absolute): ${df_db_all['amount'].abs().sum():,.2f}")

# Check classification types
query_classifications = """
SELECT id, name, exclude_from_expense_analysis
FROM classification_types
"""
df_classifications = pd.read_sql_query(query_classifications, conn)
print(f"\n=== CLASSIFICATION TYPES ===")
print(df_classifications.to_string(index=False))

# Find capital expense classification ID
capital_expense_ids = df_classifications[
    df_classifications['name'].str.contains('Capital', case=False, na=False)
]['id'].tolist()

print(f"\nCapital Expense Classification IDs: {capital_expense_ids}")

# Query expenses excluding transfers and capital expenses
excluded_classification_ids = df_classifications[
    df_classifications['exclude_from_expense_analysis'] == 1
]['id'].tolist()

print(f"All excluded classification IDs: {excluded_classification_ids}")

query_filtered = f"""
SELECT
    id,
    transaction_date,
    description,
    amount,
    transaction_type,
    category_id,
    classification_id,
    is_transfer,
    source,
    payment_method
FROM transactions
WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
    AND (is_transfer = 0 OR is_transfer IS NULL)
    AND (classification_id NOT IN ({','.join(map(str, excluded_classification_ids))}) OR classification_id IS NULL)
ORDER BY transaction_date, description
"""

df_db_filtered = pd.read_sql_query(query_filtered, conn)
print(f"\n=== FILTERED DATABASE RESULTS ===")
print(f"(Excluding transfers and capital expenses)")
print(f"  Count: {len(df_db_filtered)}")
print(f"  Total (absolute): ${df_db_filtered['amount'].abs().sum():,.2f}")

# Show breakdown by classification
print(f"\n=== BREAKDOWN BY CLASSIFICATION ===")
classification_breakdown = df_db_all.groupby('classification_id').agg({
    'id': 'count',
    'amount': lambda x: abs(x).sum()
}).rename(columns={'id': 'count', 'amount': 'total'})
print(classification_breakdown)

# Show what was excluded
df_excluded = df_db_all[
    (df_db_all['is_transfer'] == 1) |
    (df_db_all['classification_id'].isin(excluded_classification_ids))
]
print(f"\n=== EXCLUDED TRANSACTIONS ===")
print(f"Count: {len(df_excluded)}")
print(f"Total (absolute): ${df_excluded['amount'].abs().sum():,.2f}")
if len(df_excluded) > 0:
    print("\nSample excluded transactions:")
    print(df_excluded[['transaction_date', 'description', 'amount', 'classification_id', 'is_transfer']].head(10))

# Compare counts
print(f"\n=== COMPARISON ===")
print(f"Excel file: {excel_count} transactions, ${excel_total if amount_col else 'N/A'}")
print(f"Database (filtered): {len(df_db_filtered)} transactions, ${df_db_filtered['amount'].abs().sum():,.2f}")
print(f"Difference: {excel_count - len(df_db_filtered)} transactions, ${(excel_total - df_db_filtered['amount'].abs().sum()) if amount_col else 'N/A'}")

# Save filtered results to CSV for comparison
df_db_filtered.to_csv('database_filtered_sept_expenses.csv', index=False)
print(f"\nFiltered database results saved to: database_filtered_sept_expenses.csv")

# Save all database results to CSV
df_db_all.to_csv('database_all_sept_expenses.csv', index=False)
print(f"All database results saved to: database_all_sept_expenses.csv")

conn.close()
