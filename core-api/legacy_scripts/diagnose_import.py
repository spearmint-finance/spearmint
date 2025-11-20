"""Diagnostic script to check why import is failing."""

import pandas as pd

# Read the Excel file
excel_file = 'D:/CodingProjects/financial-analysis/data/transactions.xlsx'

print("=" * 80)
print("IMPORT DIAGNOSTIC TOOL")
print("=" * 80)
print()

# Read first few rows
print("Reading Excel file...")
df = pd.read_excel(excel_file, sheet_name='transaction-clean', nrows=5)

print(f"✅ Successfully read {len(df)} rows")
print()

print("=" * 80)
print("COLUMN ANALYSIS")
print("=" * 80)
print()

print("Columns in Excel file:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. '{col}'")
print()

# Check column mapping
print("=" * 80)
print("COLUMN MAPPING TEST")
print("=" * 80)
print()

COLUMN_MAPPINGS = {
    'date': ['date', 'transaction_date', 'trans_date'],
    'amount': ['amount', 'value', 'transaction_amount'],
    'type': ['type', 'transaction_type', 'trans_type'],
    'category': ['category', 'category_name'],
    'source': ['source', 'account', 'from_account'],
    'description': ['full description', 'description', 'desc', 'memo'],
    'payment_method': ['payment_method', 'payment', 'method', 'institution'],
}

df_columns_lower = {col.lower().strip(): col for col in df.columns}

print("Column mapping results:")
for standard_name, variations in COLUMN_MAPPINGS.items():
    found = False
    for variation in variations:
        if variation in df_columns_lower:
            print(f"  ✅ {standard_name:20} <- '{df_columns_lower[variation]}'")
            found = True
            break
    if not found:
        print(f"  ❌ {standard_name:20} <- NOT FOUND")
print()

# Check first row data
print("=" * 80)
print("FIRST ROW DATA")
print("=" * 80)
print()

row = df.iloc[0]
print("Raw data:")
for col in df.columns:
    value = row[col]
    print(f"  {col:25} = {value}")
print()

# Try to validate first row
print("=" * 80)
print("VALIDATION TEST")
print("=" * 80)
print()

# Normalize columns
column_map = {}
for standard_name, variations in COLUMN_MAPPINGS.items():
    for variation in variations:
        if variation in df_columns_lower:
            column_map[df_columns_lower[variation]] = standard_name
            break

df_normalized = df.rename(columns=column_map)
print("Normalized columns:")
for col in df_normalized.columns:
    print(f"  - {col}")
print()

# Check required fields
row_normalized = df_normalized.iloc[0]
print("Required field check:")
print(f"  date:     {row_normalized.get('date')} (type: {type(row_normalized.get('date'))})")
print(f"  amount:   {row_normalized.get('amount')} (type: {type(row_normalized.get('amount'))})")
print(f"  category: {row_normalized.get('category')} (type: {type(row_normalized.get('category'))})")
print()

# Check for NaN values
print("NaN check:")
print(f"  date is NaN:     {pd.isna(row_normalized.get('date'))}")
print(f"  amount is NaN:   {pd.isna(row_normalized.get('amount'))}")
print(f"  category is NaN: {pd.isna(row_normalized.get('category'))}")
print()

# Try actual import with detailed error reporting
print("=" * 80)
print("ACTUAL IMPORT TEST (First 5 rows)")
print("=" * 80)
print()

db = SessionLocal()
try:
    service = ImportService(db)
    
    # Create a temp file with just first 5 rows
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False, mode='wb') as tmp:
        df.to_excel(tmp.name, index=False, sheet_name='transaction-clean')
        tmp_path = tmp.name
    
    print(f"Created temp file: {tmp_path}")
    print()
    
    result = service.import_from_excel(tmp_path, mode='incremental', skip_duplicates=False)
    
    print(f"Import Result:")
    print(f"  Success: {result.success}")
    print(f"  Total rows: {result.total_rows}")
    print(f"  Successful: {result.successful_rows}")
    print(f"  Failed: {result.failed_rows}")
    print()
    
    if result.errors:
        print(f"Errors ({len(result.errors)}):")
        for error in result.errors:
            print(f"  Row {error.row_number}: [{error.error_type}] {error.error_message}")
    
    if result.warnings:
        print(f"Warnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  Row {warning.row_number}: {warning.warning_message}")
    
    # Clean up
    import os
    os.unlink(tmp_path)
    
finally:
    db.close()

print()
print("=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)

