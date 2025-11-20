import pandas as pd

# Read Excel file
excel_file = r'C:\Users\harry\Downloads\transactions-sept.xlsx'
df = pd.read_excel(excel_file, sheet_name='Sept')

print(f"Total rows in Excel: {len(df)}")
print(f"\nColumn names: {list(df.columns)}")

# Calculate totals
sum_total = df['Amount'].sum()
abs_total = df['Amount'].abs().sum()

print(f"\n=== EXCEL TOTALS ===")
print(f"Sum of amounts: ${sum_total:,.2f}")
print(f"Sum of absolute values: ${abs_total:,.2f}")

# Show largest expenses
print(f"\n=== TOP 10 LARGEST EXPENSES ===")
largest = df.nsmallest(10, 'Amount')[['Date', 'Description', 'Amount', 'Category']]
for idx, row in largest.iterrows():
    print(f"${abs(row['Amount']):>10,.2f} - {row['Description'][:50]}")

print(f"\n=== SUMMARY ===")
print(f"Min amount: ${df['Amount'].min():,.2f}")
print(f"Max amount: ${df['Amount'].max():,.2f}")
print(f"Mean amount: ${df['Amount'].mean():,.2f}")
