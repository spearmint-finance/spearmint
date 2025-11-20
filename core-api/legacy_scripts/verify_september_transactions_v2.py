"""
Script to verify September 2025 transactions between Excel file and database.
Compares transactions excluding income, capital expenses, and transfers.
"""

import pandas as pd
import sqlite3
from datetime import datetime

# Read Excel file from Sept sheet
excel_file = r"C:\Users\harry\Downloads\transactions-sept.xlsx"
print(f"Reading Excel file: {excel_file}")
df_excel = pd.read_excel(excel_file, sheet_name='Sept')

print(f"\n=== EXCEL FILE ANALYSIS ===")
print(f"Total rows in Excel: {len(df_excel)}")
print(f"Columns: {df_excel.columns.tolist()}")

# Display first few rows to understand structure
print(f"\nFirst 10 rows:")
print(df_excel.head(10))

# Look for key columns - try common names
date_col = None
amount_col = None
desc_col = None

for col in df_excel.columns:
    col_lower = str(col).lower()
    if 'date' in col_lower and date_col is None:
        date_col = col
    if 'amount' in col_lower and amount_col is None:
        amount_col = col
    if 'description' in col_lower and desc_col is None:
        desc_col = col

print(f"\nIdentified columns:")
print(f"  Date column: {date_col}")
print(f"  Amount column: {amount_col}")
print(f"  Description column: {desc_col}")

# Filter to only expense rows (amount should be negative or marked as expense)
if amount_col:
    # Remove NaN rows
    df_excel_clean = df_excel.dropna(subset=[amount_col])

    # Show info about the data
    print(f"\nRows with amounts: {len(df_excel_clean)}")
    print(f"\nAmount column statistics:")
    print(df_excel_clean[amount_col].describe())

    # Calculate totals
    excel_total_abs = df_excel_clean[amount_col].abs().sum()
    excel_count = len(df_excel_clean)

    print(f"\n=== EXCEL SUMMARY ===")
    print(f"  Transaction Count: {excel_count}")
    print(f"  Total (absolute): ${excel_total_abs:,.2f}")

    # Show sample transactions
    print(f"\nSample transactions from Excel:")
    if desc_col and date_col:
        print(df_excel_clean[[date_col, desc_col, amount_col]].head(10).to_string(index=False))
    else:
        print(df_excel_clean.head(10))

# Connect to database
print(f"\n=== DATABASE ANALYSIS ===")
conn = sqlite3.connect('financial_analysis.db')

# First, check classification types
query_classifications = """
SELECT classification_id, name, exclude_from_expense_analysis
FROM classification_types
"""
df_classifications = pd.read_sql_query(query_classifications, conn)
print(f"\n=== CLASSIFICATION TYPES ===")
print(df_classifications.to_string(index=False))

# Get excluded classification IDs
excluded_classification_ids = df_classifications[
    df_classifications['exclude_from_expense_analysis'] == 1
]['classification_id'].tolist()

print(f"\nClassifications excluded from expense analysis: {excluded_classification_ids}")

# Query all September 2025 expenses
query_all = """
SELECT
    transaction_id,
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
print(f"\n=== ALL SEPTEMBER 2025 EXPENSES IN DATABASE ===")
print(f"  Count: {len(df_db_all)}")
print(f"  Total (absolute): ${df_db_all['amount'].abs().sum():,.2f}")

# Show breakdown by classification
print(f"\n=== BREAKDOWN BY CLASSIFICATION ===")
classification_summary = df_db_all.groupby('classification_id', dropna=False).agg({
    'transaction_id': 'count',
    'amount': lambda x: abs(x).sum()
}).rename(columns={'transaction_id': 'count', 'amount': 'total'})

# Add classification names
for idx in classification_summary.index:
    if pd.notna(idx):
        class_name = df_classifications[df_classifications['classification_id'] == idx]['name'].values
        if len(class_name) > 0:
            classification_summary.loc[idx, 'name'] = class_name[0]
    else:
        classification_summary.loc[idx, 'name'] = 'Unclassified'

print(classification_summary.to_string())

# Show breakdown by is_transfer
print(f"\n=== BREAKDOWN BY IS_TRANSFER ===")
transfer_summary = df_db_all.groupby('is_transfer', dropna=False).agg({
    'transaction_id': 'count',
    'amount': lambda x: abs(x).sum()
}).rename(columns={'transaction_id': 'count', 'amount': 'total'})
print(transfer_summary.to_string())

# Query expenses EXCLUDING transfers and excluded classifications
# This should match what the tool shows
where_conditions = [
    "transaction_date BETWEEN '2025-09-01' AND '2025-09-30'",
    "transaction_type = 'Expense'",
    "(is_transfer = 0 OR is_transfer IS NULL)"
]

if excluded_classification_ids:
    excluded_ids_str = ','.join(map(str, excluded_classification_ids))
    where_conditions.append(f"(classification_id NOT IN ({excluded_ids_str}) OR classification_id IS NULL)")

query_filtered = f"""
SELECT
    transaction_id,
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
WHERE {' AND '.join(where_conditions)}
ORDER BY transaction_date, description
"""

df_db_filtered = pd.read_sql_query(query_filtered, conn)
print(f"\n=== FILTERED DATABASE RESULTS ===")
print(f"(Excluding transfers and classifications with exclude_from_expense_analysis=1)")
print(f"  Count: {len(df_db_filtered)}")
print(f"  Total (absolute): ${df_db_filtered['amount'].abs().sum():,.2f}")

# Show what was excluded
df_excluded = df_db_all[
    (df_db_all['is_transfer'] == 1) |
    (df_db_all['classification_id'].isin(excluded_classification_ids))
]
print(f"\n=== EXCLUDED TRANSACTIONS ===")
print(f"  Count: {len(df_excluded)}")
print(f"  Total (absolute): ${df_excluded['amount'].abs().sum():,.2f}")

if len(df_excluded) > 0:
    print("\nExcluded transactions breakdown:")
    excluded_breakdown = df_excluded.groupby(['is_transfer', 'classification_id'], dropna=False).agg({
        'transaction_id': 'count',
        'amount': lambda x: abs(x).sum()
    }).rename(columns={'transaction_id': 'count', 'amount': 'total'})
    print(excluded_breakdown.to_string())

    print("\nSample excluded transactions:")
    print(df_excluded[['transaction_date', 'description', 'amount', 'classification_id', 'is_transfer']].head(20).to_string(index=False))

# Compare counts
print(f"\n=== COMPARISON ===")
if amount_col:
    print(f"Excel file (Sept sheet): {excel_count} transactions, ${excel_total_abs:,.2f}")
    print(f"Database (filtered): {len(df_db_filtered)} transactions, ${df_db_filtered['amount'].abs().sum():,.2f}")
    print(f"Difference: {excel_count - len(df_db_filtered)} transactions, ${excel_total_abs - df_db_filtered['amount'].abs().sum():,.2f}")
else:
    print("Could not analyze Excel file - amount column not found")

# Save results for manual comparison
df_db_filtered.to_csv('database_filtered_sept_expenses.csv', index=False)
print(f"\nFiltered database results saved to: database_filtered_sept_expenses.csv")

df_db_all.to_csv('database_all_sept_expenses.csv', index=False)
print(f"All database results saved to: database_all_sept_expenses.csv")

if amount_col and desc_col:
    df_excel_clean.to_csv('excel_sept_expenses.csv', index=False)
    print(f"Excel data saved to: excel_sept_expenses.csv")

conn.close()

print(f"\n=== NEXT STEPS ===")
print("1. Review the CSV files to identify missing transactions")
print("2. Check if Excel transactions are using different descriptions")
print("3. Verify date formats match between Excel and database")
