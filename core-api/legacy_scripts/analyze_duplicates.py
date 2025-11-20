"""Analyze duplicate detection to see what was skipped."""
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from hashlib import md5

# Find the Excel file - try multiple locations
possible_locations = [
    Path("C:/Users/harry/Downloads/transactions.xlsx"),
    Path.home() / "Downloads" / "transactions.xlsx",
    Path("D:/CodingProjects/financial-analysis/data/temp/transactions.xlsx"),
    Path("D:/CodingProjects/financial-analysis/transactions.xlsx"),
]

excel_file = None
for loc in possible_locations:
    if loc.exists():
        excel_file = loc
        break

if not excel_file:
    print("ERROR: Could not find transactions.xlsx file")
    print("\nSearched in:")
    for loc in possible_locations:
        print(f"  - {loc}")
    print("\nPlease copy the file to one of these locations or update the script")
    exit(1)

print(f"Reading Excel file: {excel_file}")

# Read Excel file
with pd.ExcelFile(excel_file) as xl_file:
    # Look for 'import' sheet
    sheet_names = xl_file.sheet_names
    print(f"Available sheets: {sheet_names}")

    sheet_to_use = None
    for sheet in sheet_names:
        if sheet.lower().strip() == 'import':
            sheet_to_use = sheet
            break

    if not sheet_to_use:
        sheet_to_use = 0

    print(f"Using sheet: '{sheet_to_use}'")
    df = pd.read_excel(xl_file, sheet_name=sheet_to_use)

print(f"\nTotal rows in Excel: {len(df)}")

# Check for exact duplicates in Excel
exact_dupes = df.duplicated(keep=False)
print(f"Exact duplicate rows in Excel: {exact_dupes.sum()}")

# Simulate the duplicate detection algorithm
def generate_duplicate_key(date, amount, description):
    """Generate duplicate detection key (same as DuplicateDetector)."""
    key_parts = [
        str(date).split()[0] if pd.notna(date) else '',
        f"{float(amount):.2f}" if pd.notna(amount) else '',
        str(description).strip().lower()[:100] if pd.notna(description) else ''
    ]
    key_string = '|'.join(key_parts)
    return md5(key_string.encode()).hexdigest()

# Normalize column names (simulate the import process)
column_map = {}
df_columns_lower = {col.lower().strip(): col for col in df.columns}

COLUMN_MAPPINGS = {
    'date': ['date', 'transaction date', 'trans_date', 'transaction_date', 'post date', 'posting date', 'posted date', 'date added'],
    'amount': ['amount', 'value', 'transaction_amount', 'transaction amount'],
    'description': ['full description', 'description', 'desc', 'memo'],
}

for standard_name, variations in COLUMN_MAPPINGS.items():
    for variation in variations:
        if variation in df_columns_lower:
            column_map[df_columns_lower[variation]] = standard_name
            break

df_normalized = df.rename(columns=column_map)

print(f"\nColumn mapping: {column_map}")

# Check if required columns exist
if 'date' not in df_normalized.columns:
    print("ERROR: 'date' column not found after normalization")
    print(f"Available columns: {list(df_normalized.columns)}")
    exit(1)

if 'amount' not in df_normalized.columns:
    print("ERROR: 'amount' column not found after normalization")
    exit(1)

# Generate duplicate keys for all rows
print("\nGenerating duplicate keys...")
duplicate_keys = []
for idx, row in df_normalized.iterrows():
    key = generate_duplicate_key(
        row.get('date'),
        row.get('amount'),
        row.get('description')
    )
    duplicate_keys.append(key)

df_normalized['dup_key'] = duplicate_keys

# Find duplicates based on our algorithm
dup_counts = df_normalized['dup_key'].value_counts()
duplicates_in_file = dup_counts[dup_counts > 1]

print(f"\nDuplicates found using duplicate detection algorithm:")
print(f"  Unique transactions: {len(dup_counts)}")
print(f"  Duplicate groups: {len(duplicates_in_file)}")
print(f"  Total duplicate rows: {(dup_counts - 1).sum()}")

if len(duplicates_in_file) > 0:
    print(f"\nTop 10 duplicate groups:")
    print("-" * 100)
    for i, (key, count) in enumerate(duplicates_in_file.head(10).items(), 1):
        matching_rows = df_normalized[df_normalized['dup_key'] == key]
        first_row = matching_rows.iloc[0]
        print(f"{i}. Count: {count} | Date: {first_row.get('date')} | Amount: ${first_row.get('amount')} | Desc: {str(first_row.get('description'))[:60]}")

# Check database
BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/financial_analysis.db"
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    db_count = conn.execute(text("SELECT COUNT(*) FROM transactions")).scalar()
    print(f"\n" + "=" * 100)
    print(f"Summary:")
    print(f"  Excel rows: {len(df)}")
    print(f"  Unique in Excel (by our algorithm): {len(dup_counts)}")
    print(f"  Database count: {db_count}")
    print(f"  Expected skipped: {len(df) - db_count}")
    print("=" * 100)
