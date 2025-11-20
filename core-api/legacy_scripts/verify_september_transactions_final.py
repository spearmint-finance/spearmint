"""
Script to verify September 2025 transactions between Excel file and database.
Compares transactions excluding income, capital expenses, and transfers.
"""

import pandas as pd
import sqlite3

# Read Excel file from Sept sheet
excel_file = r"C:\Users\harry\Downloads\transactions-sept.xlsx"
print(f"Reading Excel file: {excel_file}")
df_excel = pd.read_excel(excel_file, sheet_name='Sept')

print(f"\n=== EXCEL FILE ANALYSIS ===")
print(f"Total rows in Excel: {len(df_excel)}")

# Filter to only rows with amounts
df_excel_clean = df_excel.dropna(subset=['Amount'])
excel_total_abs = df_excel_clean['Amount'].abs().sum()
excel_count = len(df_excel_clean)

print(f"Transaction Count: {excel_count}")
print(f"Total (absolute): ${excel_total_abs:,.2f}")

# Connect to database
print(f"\n=== DATABASE ANALYSIS ===")
conn = sqlite3.connect('financial_analysis.db')

# Query transaction_classifications table with correct column names
query_classifications = """
SELECT classification_id, classification_name,
       exclude_from_expense_calc, exclude_from_income_calc
FROM transaction_classifications
"""
df_classifications = pd.read_sql_query(query_classifications, conn)
print(f"\n=== CLASSIFICATION TYPES ===")
print(df_classifications.to_string(index=False))

# Get excluded classification IDs
excluded_classification_ids = df_classifications[
    df_classifications['exclude_from_expense_calc'] == 1
]['classification_id'].tolist()

print(f"\nClassifications excluded from expense analysis (IDs): {excluded_classification_ids}")
excluded_names = df_classifications[
    df_classifications['exclude_from_expense_calc'] == 1
]['classification_name'].tolist()
print(f"Excluded classification names: {excluded_names}")

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
print(f"Count: {len(df_db_all)}")
print(f"Total (absolute): ${df_db_all['amount'].abs().sum():,.2f}")

# Show breakdown by classification
print(f"\n=== BREAKDOWN BY CLASSIFICATION ===")
classification_summary = df_db_all.groupby('classification_id', dropna=False).agg({
    'transaction_id': 'count',
    'amount': lambda x: abs(x).sum()
}).rename(columns={'transaction_id': 'count', 'amount': 'total'})

# Add classification names
classification_summary['name'] = ''
classification_summary['excluded'] = 0
for idx in classification_summary.index:
    if pd.notna(idx):
        class_info = df_classifications[df_classifications['classification_id'] == idx]
        if len(class_info) > 0:
            classification_summary.loc[idx, 'name'] = class_info['classification_name'].values[0]
            classification_summary.loc[idx, 'excluded'] = class_info['exclude_from_expense_calc'].values[0]
    else:
        classification_summary.loc[idx, 'name'] = 'Unclassified'
        classification_summary.loc[idx, 'excluded'] = 0

print(classification_summary[['name', 'count', 'total', 'excluded']].to_string())

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
print(f"\n=== FILTERED DATABASE RESULTS (WHAT TOOL SHOULD SHOW) ===")
print(f"(Excluding transfers and classifications with exclude_from_expense_calc=1)")
print(f"Count: {len(df_db_filtered)}")
print(f"Total (absolute): ${df_db_filtered['amount'].abs().sum():,.2f}")

# Show what was excluded
df_excluded = df_db_all[
    (df_db_all['is_transfer'] == 1) |
    (df_db_all['classification_id'].isin(excluded_classification_ids))
]
print(f"\n=== EXCLUDED TRANSACTIONS ===")
print(f"Count: {len(df_excluded)}")
print(f"Total (absolute): ${df_excluded['amount'].abs().sum():,.2f}")

if len(df_excluded) > 0:
    print("\nExcluded transactions by reason:")

    # Transfers
    df_transfers = df_excluded[df_excluded['is_transfer'] == 1]
    if len(df_transfers) > 0:
        print(f"\nTransfers (is_transfer=1): {len(df_transfers)} transactions, ${df_transfers['amount'].abs().sum():,.2f}")
        print("Sample transfers:")
        print(df_transfers[['transaction_date', 'description', 'amount']].head(10).to_string(index=False))

    # Excluded classifications
    df_excluded_class = df_excluded[df_excluded['classification_id'].isin(excluded_classification_ids)]
    if len(df_excluded_class) > 0:
        print(f"\nExcluded by classification: {len(df_excluded_class)} transactions, ${df_excluded_class['amount'].abs().sum():,.2f}")
        excluded_class_breakdown = df_excluded_class.groupby('classification_id').agg({
            'transaction_id': 'count',
            'amount': lambda x: abs(x).sum()
        }).rename(columns={'transaction_id': 'count', 'amount': 'total'})

        for idx in excluded_class_breakdown.index:
            class_name = df_classifications[df_classifications['classification_id'] == idx]['classification_name'].values[0]
            excluded_class_breakdown.loc[idx, 'name'] = class_name

        print(excluded_class_breakdown[['name', 'count', 'total']].to_string())

        print("\nSample excluded classification transactions:")
        print(df_excluded_class[['transaction_date', 'description', 'amount', 'classification_id']].head(10).to_string(index=False))

# Compare counts
print(f"\n" + "="*70)
print(f"=== FINAL COMPARISON ===")
print(f"="*70)
print(f"Excel file (Sept sheet):        {excel_count:3d} transactions, ${excel_total_abs:>10,.2f}")
print(f"Database (all Sept expenses):   {len(df_db_all):3d} transactions, ${df_db_all['amount'].abs().sum():>10,.2f}")
print(f"Database (filtered, tool view): {len(df_db_filtered):3d} transactions, ${df_db_filtered['amount'].abs().sum():>10,.2f}")
print(f"-"*70)
print(f"Difference (Excel vs Tool):     {excel_count - len(df_db_filtered):3d} transactions, ${excel_total_abs - df_db_filtered['amount'].abs().sum():>10,.2f}")
print(f"Difference (All DB vs Tool):    {len(df_db_all) - len(df_db_filtered):3d} transactions, ${df_db_all['amount'].abs().sum() - df_db_filtered['amount'].abs().sum():>10,.2f}")
print(f"="*70)

# Save results for manual comparison
df_db_filtered.to_csv('database_filtered_sept_expenses.csv', index=False)
print(f"\nFiltered database results saved to: database_filtered_sept_expenses.csv")

df_db_all.to_csv('database_all_sept_expenses.csv', index=False)
print(f"All database results saved to: database_all_sept_expenses.csv")

df_excel_clean.to_csv('excel_sept_expenses.csv', index=False)
print(f"Excel data saved to: excel_sept_expenses.csv")

# Try to find missing transactions by comparing descriptions
print(f"\n=== LOOKING FOR MISSING TRANSACTIONS ===")
# Normalize descriptions for comparison
df_excel_clean['desc_normalized'] = df_excel_clean['Description'].str.lower().str.strip()
df_db_all['desc_normalized'] = df_db_all['description'].str.lower().str.strip()

excel_descriptions = set(df_excel_clean['desc_normalized'].values)
db_descriptions = set(df_db_all['desc_normalized'].values)

in_excel_not_db = excel_descriptions - db_descriptions
in_db_not_excel = db_descriptions - excel_descriptions

if in_excel_not_db:
    print(f"\nDescriptions in Excel but NOT in database ({len(in_excel_not_db)}):")
    for desc in list(in_excel_not_db)[:10]:
        matching_rows = df_excel_clean[df_excel_clean['desc_normalized'] == desc]
        if len(matching_rows) > 0:
            row = matching_rows.iloc[0]
            print(f"  {row['Date']} | {row['Description'][:50]:50s} | ${row['Amount']:>10.2f}")

if in_db_not_excel:
    print(f"\nDescriptions in database but NOT in Excel ({len(in_db_not_excel)}):")
    for desc in list(in_db_not_excel)[:10]:
        matching_rows = df_db_all[df_db_all['desc_normalized'] == desc]
        if len(matching_rows) > 0:
            row = matching_rows.iloc[0]
            print(f"  {row['transaction_date']} | {row['description'][:50]:50s} | ${row['amount']:>10.2f}")

conn.close()

print(f"\n=== SUMMARY ===")
print(f"✓ Excel file contains {excel_count} expense transactions totaling ${excel_total_abs:,.2f}")
print(f"✓ Database contains {len(df_db_all)} September 2025 expense transactions totaling ${df_db_all['amount'].abs().sum():,.2f}")
print(f"✓ After filtering (excluding transfers & excluded classifications), tool should show:")
print(f"  {len(df_db_filtered)} transactions totaling ${df_db_filtered['amount'].abs().sum():,.2f}")
print(f"\nReview the CSV files to identify specific transaction differences.")
