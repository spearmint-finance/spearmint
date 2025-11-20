import pandas as pd
import requests
from datetime import datetime

# Read Excel file
excel_file = r'C:\Users\harry\Downloads\transactions-sept.xlsx'
df_excel = pd.read_excel(excel_file, sheet_name='Sept')

# Create match keys for Excel (date + amount)
df_excel['Date'] = pd.to_datetime(df_excel['Date'])
df_excel['match_key'] = df_excel['Date'].dt.strftime('%Y-%m-%d') + '_' + df_excel['Amount'].abs().round(2).astype(str)

excel_keys = set(df_excel['match_key'].values)

print(f"Excel transactions: {len(df_excel)}")
print(f"Unique match keys in Excel: {len(excel_keys)}")

# Get API transactions (filtered - no capital expenses or transfers)
url = "http://localhost:8000/api/transactions?start_date=2025-09-01&end_date=2025-09-30&transaction_type=Expense&include_capital_expenses=false&include_transfers=false&limit=999&sort_by=transaction_date&sort_order=asc"
response = requests.get(url)
data = response.json()

api_transactions = data['transactions']
print(f"\nAPI transactions: {len(api_transactions)}")

# Create match keys for API transactions
api_data = []
for t in api_transactions:
    date = t['transaction_date']
    amount = abs(float(t['amount']))
    match_key = f"{date}_{amount:.2f}"
    api_data.append({
        'transaction_id': t['transaction_id'],
        'date': date,
        'amount': amount,
        'description': t['description'],
        'classification_id': t['classification_id'],
        'is_transfer': t['is_transfer'],
        'match_key': match_key
    })

df_api = pd.DataFrame(api_data)
api_keys = set(df_api['match_key'].values)

print(f"Unique match keys in API: {len(api_keys)}")

# Find transactions in API but not in Excel
in_api_not_excel = api_keys - excel_keys
in_excel_not_api = excel_keys - api_keys

print(f"\n=== TRANSACTIONS IN API BUT NOT IN EXCEL ({len(in_api_not_excel)}) ===")
if in_api_not_excel:
    for key in sorted(in_api_not_excel):
        row = df_api[df_api['match_key'] == key].iloc[0]
        print(f"\n  {row['date']} | ${row['amount']:>10,.2f} | ID: {row['transaction_id']}")
        print(f"    {row['description'][:70]}")
        print(f"    Classification: {row['classification_id']}, Transfer: {row['is_transfer']}")

print(f"\n=== TRANSACTIONS IN EXCEL BUT NOT IN API ({len(in_excel_not_api)}) ===")
if in_excel_not_api:
    for key in sorted(in_excel_not_api):
        row = df_excel[df_excel['match_key'] == key].iloc[0]
        print(f"\n  {row['Date'].strftime('%Y-%m-%d')} | ${abs(row['Amount']):>10,.2f}")
        print(f"    {row['Description'][:70]}")

# Check for duplicate match keys
excel_dupes = df_excel[df_excel.duplicated(subset=['match_key'], keep=False)]
api_dupes = df_api[df_api.duplicated(subset=['match_key'], keep=False)]

if len(excel_dupes) > 0:
    print(f"\n=== DUPLICATE MATCH KEYS IN EXCEL ({len(excel_dupes)}) ===")
    print(excel_dupes[['Date', 'Amount', 'Description', 'match_key']])

if len(api_dupes) > 0:
    print(f"\n=== DUPLICATE MATCH KEYS IN API ({len(api_dupes)}) ===")
    print(api_dupes[['date', 'amount', 'description', 'match_key']])
