"""
Check database schema and Excel file structure
"""

import pandas as pd
import sqlite3

# Check database schema
print("=== DATABASE SCHEMA ===")
conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"Tables: {[t[0] for t in tables]}")

cursor.execute("PRAGMA table_info(transactions);")
columns = cursor.fetchall()
print(f"\nTransactions table columns:")
for col in columns:
    print(f"  {col[1]}: {col[2]}")

conn.close()

# Check Excel file with different reading options
print(f"\n=== EXCEL FILE ANALYSIS ===")
excel_file = r"C:\Users\harry\Downloads\transactions-sept.xlsx"

# Try reading without headers first
df = pd.read_excel(excel_file, header=None)
print(f"\nExcel shape (no header): {df.shape}")
print(f"\nFirst 10 rows:")
print(df.head(10))

# Try reading with header
df_with_header = pd.read_excel(excel_file)
print(f"\nExcel shape (with header): {df_with_header.shape}")
print(f"\nColumns: {df_with_header.columns.tolist()}")
print(f"\nFirst 10 rows (with header):")
print(df_with_header.head(10))

# Check all sheets
xl_file = pd.ExcelFile(excel_file)
print(f"\nSheet names: {xl_file.sheet_names}")
