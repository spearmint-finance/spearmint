"""
Calculate exact total of September 2025 expenses excluding transfers and capital expenses
"""

import pandas as pd
import sqlite3

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

print(f"Excluded classification IDs: {excluded_classification_ids}")
print(f"\nExcluded classifications:")
for idx in excluded_classification_ids:
    class_info = df_classifications[df_classifications['classification_id'] == idx]
    if len(class_info) > 0:
        print(f"  ID {idx}: {class_info['classification_name'].values[0]}")

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
ORDER BY amount
"""

df_db_all = pd.read_sql_query(query_all, conn)
df_db_all['amount_abs'] = df_db_all['amount'].abs()

print(f"\n=== ALL SEPTEMBER 2025 EXPENSES ===")
print(f"Count: {len(df_db_all)}")
print(f"Total: ${df_db_all['amount_abs'].sum():,.2f}")

# Filter to exclude transfers and excluded classifications
df_db_filtered = df_db_all[
    ((df_db_all['is_transfer'] == 0) | (df_db_all['is_transfer'].isna())) &
    ((~df_db_all['classification_id'].isin(excluded_classification_ids)) | (df_db_all['classification_id'].isna()))
].copy()

filtered_total = df_db_filtered['amount_abs'].sum()

print(f"\n=== FILTERED (EXCLUDING TRANSFERS & CAPITAL EXPENSES) ===")
print(f"Count: {len(df_db_filtered)}")
print(f"Total: ${filtered_total:,.2f}")

# Show what was excluded
df_excluded = df_db_all[
    (df_db_all['is_transfer'] == 1) |
    (df_db_all['classification_id'].isin(excluded_classification_ids))
]

print(f"\n=== EXCLUDED TRANSACTIONS ===")
print(f"Count: {len(df_excluded)}")
print(f"Total: ${df_excluded['amount_abs'].sum():,.2f}")

# Break down excluded by type
print(f"\n=== BREAKDOWN OF EXCLUDED ===")

# Transfers
df_transfers_only = df_excluded[
    (df_excluded['is_transfer'] == 1) &
    (~df_excluded['classification_id'].isin(excluded_classification_ids) | df_excluded['classification_id'].isna())
]
print(f"Transfers (is_transfer=1): {len(df_transfers_only)} transactions, ${df_transfers_only['amount_abs'].sum():,.2f}")

# Capital expenses
capital_expense_id = df_classifications[df_classifications['classification_name'] == 'Capital Expense']['classification_id'].values
if len(capital_expense_id) > 0:
    capital_expense_id = capital_expense_id[0]
    df_capital = df_db_all[df_db_all['classification_id'] == capital_expense_id]
    print(f"Capital Expenses: {len(df_capital)} transactions, ${df_capital['amount_abs'].sum():,.2f}")

# Other excluded classifications
df_other_excluded = df_excluded[
    (df_excluded['classification_id'].isin(excluded_classification_ids)) &
    (df_excluded['classification_id'] != capital_expense_id) &
    ((df_excluded['is_transfer'] == 0) | df_excluded['is_transfer'].isna())
]
print(f"Other excluded classifications: {len(df_other_excluded)} transactions, ${df_other_excluded['amount_abs'].sum():,.2f}")

if len(df_other_excluded) > 0:
    other_breakdown = df_other_excluded.groupby('classification_id').agg({
        'transaction_id': 'count',
        'amount_abs': 'sum'
    }).rename(columns={'transaction_id': 'count', 'amount_abs': 'total'})

    for idx in other_breakdown.index:
        class_name = df_classifications[df_classifications['classification_id'] == idx]['classification_name'].values[0]
        other_breakdown.loc[idx, 'name'] = class_name

    print(f"\n  Details:")
    print(other_breakdown[['name', 'count', 'total']].to_string())

print(f"\n" + "="*80)
print(f"ANSWER: Database total excluding transfers and capital expenses")
print(f"        {len(df_db_filtered)} transactions, ${filtered_total:,.2f}")
print(f"="*80)

conn.close()
