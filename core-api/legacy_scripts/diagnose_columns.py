"""Diagnostic script to check Excel column detection."""
import pandas as pd
import sys

if len(sys.argv) < 2:
    print("Usage: python diagnose_columns.py <excel_file>")
    sys.exit(1)

file_path = sys.argv[1]

# Read Excel file
df = pd.read_excel(file_path)

print("=" * 80)
print("EXCEL COLUMN ANALYSIS")
print("=" * 80)
print(f"\nFile: {file_path}")
print(f"Total rows (including header): {len(df) + 1}")
print(f"Total columns: {len(df.columns)}")

print("\n" + "-" * 80)
print("ORIGINAL COLUMN NAMES:")
print("-" * 80)
for i, col in enumerate(df.columns, 1):
    print(f"{i}. '{col}' (type: {type(col).__name__}, repr: {repr(col)})")

print("\n" + "-" * 80)
print("LOWERCASE COLUMN NAMES:")
print("-" * 80)
for i, col in enumerate(df.columns, 1):
    lower_col = col.lower().strip()
    print(f"{i}. '{lower_col}' (original: '{col}')")

print("\n" + "-" * 80)
print("COLUMN MAPPING DETECTION:")
print("-" * 80)

COLUMN_MAPPINGS = {
    'date': ['date', 'transaction date', 'trans_date', 'transaction_date', 'post date', 'posting date', 'posted date', 'date added'],
    'amount': ['amount', 'value', 'transaction_amount', 'transaction amount'],
    'category': ['category', 'category_name'],
    'description': ['full description', 'description', 'desc', 'memo'],
}

df_columns_lower = {col.lower().strip(): col for col in df.columns}

for standard_name, variations in COLUMN_MAPPINGS.items():
    matched = None
    for variation in variations:
        if variation in df_columns_lower:
            matched = df_columns_lower[variation]
            break

    if matched:
        print(f"✓ {standard_name:15} -> '{matched}'")
    else:
        print(f"✗ {standard_name:15} -> NOT FOUND (looking for: {variations})")

print("\n" + "-" * 80)
print("SAMPLE DATA (First 3 rows):")
print("-" * 80)
print(df.head(3).to_string())

print("\n" + "-" * 80)
print("COLUMN DATA TYPES:")
print("-" * 80)
for col in df.columns:
    print(f"'{col}': {df[col].dtype}")

print("\n" + "-" * 80)
print("NULL/NA VALUES PER COLUMN:")
print("-" * 80)
for col in df.columns:
    null_count = df[col].isna().sum()
    print(f"'{col}': {null_count} null values")

print("\n" + "=" * 80)
