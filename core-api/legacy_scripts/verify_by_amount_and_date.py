"""
Compare Excel and database transactions by matching amount and date
"""

import pandas as pd
import sqlite3
from datetime import datetime

# Read Excel file from Sept sheet
excel_file = r"C:\Users\harry\Downloads\transactions-sept.xlsx"
print(f"Reading Excel file: {excel_file}")
df_excel = pd.read_excel(excel_file, sheet_name='Sept')

# Clean Excel data
df_excel_clean = df_excel.dropna(subset=['Amount'])
df_excel_clean['Date'] = pd.to_datetime(df_excel_clean['Date'])
df_excel_clean['amount_abs'] = df_excel_clean['Amount'].abs()

print(f"\n=== EXCEL FILE ===")
print(f"Transactions: {len(df_excel_clean)}")
print(f"Total: ${df_excel_clean['amount_abs'].sum():,.2f}")

# Connect to database
conn = sqlite3.connect('financial_analysis.db')

# Get classifications
df_classifications = pd.read_sql_query(
    "SELECT classification_id, classification_name, exclude_from_expense_calc FROM transaction_classifications",
    conn
)

excluded_classification_ids = df_classifications[
    df_classifications['exclude_from_expense_calc'] == 1
]['classification_id'].tolist()

print(f"\nExcluded classification IDs: {excluded_classification_ids}")

# Get all September expenses from database
query_all = """
SELECT
    transaction_id,
    transaction_date,
    description,
    amount,
    classification_id,
    is_transfer
FROM transactions
WHERE transaction_date BETWEEN '2025-09-01' AND '2025-09-30'
    AND transaction_type = 'Expense'
"""

df_db_all = pd.read_sql_query(query_all, conn)
df_db_all['transaction_date'] = pd.to_datetime(df_db_all['transaction_date'])
df_db_all['amount_abs'] = df_db_all['amount'].abs()

print(f"\n=== ALL DATABASE SEPTEMBER EXPENSES ===")
print(f"Transactions: {len(df_db_all)}")
print(f"Total: ${df_db_all['amount_abs'].sum():,.2f}")

# Filter database to match tool's logic
df_db_filtered = df_db_all[
    ((df_db_all['is_transfer'] == 0) | (df_db_all['is_transfer'].isna())) &
    ((~df_db_all['classification_id'].isin(excluded_classification_ids)) | (df_db_all['classification_id'].isna()))
].copy()

print(f"\n=== FILTERED DATABASE (WHAT TOOL SHOWS) ===")
print(f"Transactions: {len(df_db_filtered)}")
print(f"Total: ${df_db_filtered['amount_abs'].sum():,.2f}")

# Create matching keys
df_excel_clean['match_key'] = df_excel_clean['Date'].dt.strftime('%Y-%m-%d') + '_' + df_excel_clean['amount_abs'].round(2).astype(str)
df_db_all['match_key'] = df_db_all['transaction_date'].dt.strftime('%Y-%m-%d') + '_' + df_db_all['amount_abs'].round(2).astype(str)
df_db_filtered['match_key'] = df_db_filtered['transaction_date'].dt.strftime('%Y-%m-%d') + '_' + df_db_filtered['amount_abs'].round(2).astype(str)

# Find transactions in Excel but not in database
excel_keys = set(df_excel_clean['match_key'].values)
db_all_keys = set(df_db_all['match_key'].values)
db_filtered_keys = set(df_db_filtered['match_key'].values)

in_excel_not_in_db = excel_keys - db_all_keys
in_excel_but_filtered_out = excel_keys & db_all_keys - db_filtered_keys
in_db_not_in_excel = db_filtered_keys - excel_keys

print(f"\n=== MATCHING ANALYSIS ===")
print(f"Transactions in Excel NOT in database at all: {len(in_excel_not_in_db)}")
print(f"Transactions in Excel but filtered out by tool: {len(in_excel_but_filtered_out)}")
print(f"Transactions in database (filtered) NOT in Excel: {len(in_db_not_in_excel)}")

# Show missing transactions
if in_excel_not_in_db:
    print(f"\n=== TRANSACTIONS IN EXCEL BUT NOT IN DATABASE ===")
    for key in sorted(in_excel_not_in_db)[:20]:
        match = df_excel_clean[df_excel_clean['match_key'] == key].iloc[0]
        print(f"{match['Date'].strftime('%Y-%m-%d')} | ${match['amount_abs']:>10.2f} | {match['Description'][:60]}")

if in_excel_but_filtered_out:
    print(f"\n=== TRANSACTIONS IN EXCEL BUT FILTERED OUT BY TOOL ===")
    for key in sorted(in_excel_but_filtered_out)[:20]:
        excel_match = df_excel_clean[df_excel_clean['match_key'] == key].iloc[0]
        db_match = df_db_all[df_db_all['match_key'] == key].iloc[0]

        # Get classification name
        class_name = "Unclassified"
        if pd.notna(db_match['classification_id']):
            class_info = df_classifications[df_classifications['classification_id'] == db_match['classification_id']]
            if len(class_info) > 0:
                class_name = class_info['classification_name'].values[0]

        is_transfer_str = "Yes" if db_match['is_transfer'] == 1 else "No"

        print(f"{excel_match['Date'].strftime('%Y-%m-%d')} | ${excel_match['amount_abs']:>10.2f} | Transfer: {is_transfer_str} | Classification: {class_name:30s} | {excel_match['Description'][:40]}")

if in_db_not_in_excel:
    print(f"\n=== TRANSACTIONS IN TOOL (FILTERED) BUT NOT IN EXCEL ===")
    for key in sorted(in_db_not_in_excel)[:20]:
        db_match = df_db_filtered[df_db_filtered['match_key'] == key].iloc[0]
        print(f"{db_match['transaction_date'].strftime('%Y-%m-%d')} | ${db_match['amount_abs']:>10.2f} | {db_match['description'][:60]}")

# Summary statistics
excel_total = df_excel_clean['amount_abs'].sum()
db_filtered_total = df_db_filtered['amount_abs'].sum()
difference = excel_total - db_filtered_total

print(f"\n" + "="*80)
print(f"=== FINAL SUMMARY ===")
print(f"="*80)
print(f"Excel file:                     {len(df_excel_clean):3d} transactions, ${excel_total:>12,.2f}")
print(f"Tool (filtered database):       {len(df_db_filtered):3d} transactions, ${db_filtered_total:>12,.2f}")
print(f"-"*80)
print(f"Difference:                     {len(df_excel_clean) - len(df_db_filtered):3d} transactions, ${difference:>12,.2f}")
print(f"="*80)

# What should the user expect to see in the tool?
print(f"\n=== WHAT THE TOOL SHOULD SHOW ===")
print(f"With filters:")
print(f"  - Date Range: 09/01/2025 to 09/30/2025")
print(f"  - Transaction Type: Expense")
print(f"  - Is Transfer: No")
print(f"  - (Classifications excluding capital expenses automatically)")
print(f"\nExpected result: {len(df_db_filtered)} transactions, ${db_filtered_total:,.2f}")

conn.close()
