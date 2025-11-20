import pandas as pd
import requests

# Read Excel file
excel_file = r'C:\Users\harry\Downloads\transactions-sept.xlsx'
df = pd.read_excel(excel_file, sheet_name='Sept')

excel_count = len(df)
excel_total = df['Amount'].abs().sum()

print("=" * 60)
print("SEPTEMBER 2025 EXPENSE COMPARISON")
print("=" * 60)

print(f"\nEXCEL FILE:")
print(f"   Transactions: {excel_count}")
print(f"   Total: ${excel_total:,.2f}")

# Get API results with filters OFF (exclude capital expenses & transfers)
url = "http://localhost:8000/api/transactions?start_date=2025-09-01&end_date=2025-09-30&transaction_type=Expense&include_capital_expenses=false&include_transfers=false&limit=1"
response = requests.get(url)
data = response.json()

api_count_filtered = data['summary']['transaction_count']
api_total_filtered = data['summary']['total_expenses']

print(f"\nAPI (Capital Expenses & Transfers EXCLUDED):")
print(f"   Transactions: {api_count_filtered}")
print(f"   Total: ${api_total_filtered:,.2f}")

print(f"\nDIFFERENCE:")
diff_count = api_count_filtered - excel_count
diff_total = api_total_filtered - excel_total
print(f"   Transactions: {diff_count:+d}")
print(f"   Total: ${diff_total:+,.2f}")

if abs(diff_count) <= 5 and abs(diff_total) <= 1000:
    print(f"\n>> CLOSE MATCH - Difference is within acceptable range")
else:
    print(f"\n>> SIGNIFICANT DIFFERENCE - Needs investigation")

# Also get API results with filters ON (include everything)
url_all = "http://localhost:8000/api/transactions?start_date=2025-09-01&end_date=2025-09-30&transaction_type=Expense&include_capital_expenses=true&include_transfers=true&limit=1"
response_all = requests.get(url_all)
data_all = response_all.json()

api_count_all = data_all['summary']['transaction_count']
api_total_all = data_all['summary']['total_expenses']

print(f"\nAPI (ALL EXPENSES - Capital & Transfers INCLUDED):")
print(f"   Transactions: {api_count_all}")
print(f"   Total: ${api_total_all:,.2f}")

print(f"\nCAPITAL EXPENSES + TRANSFERS:")
capital_transfer_count = api_count_all - api_count_filtered
capital_transfer_total = api_total_all - api_total_filtered
print(f"   Transactions: {capital_transfer_count}")
print(f"   Total: ${capital_transfer_total:,.2f}")

print("\n" + "=" * 60)
