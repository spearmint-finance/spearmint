"""Debug Excel file import"""
import pandas as pd
import sys

# Path to your Excel file (you'll need to update this with the actual path)
file_path = input("Enter the full path to your Excel file: ")

try:
    # Read the Excel file
    with pd.ExcelFile(file_path) as xl_file:
        print(f"\nAvailable sheets: {xl_file.sheet_names}")

        # Try to find 'import' sheet first
        sheet_to_use = None
        for sheet in xl_file.sheet_names:
            if sheet.lower().strip() == 'import':
                sheet_to_use = sheet
                break

        # Default to first sheet if 'import' not found
        if not sheet_to_use:
            sheet_to_use = 0

        print(f"Using sheet: {sheet_to_use}")

        # Read the sheet
        df = pd.read_excel(xl_file, sheet_name=sheet_to_use)

        print(f"\nDataFrame shape: {df.shape}")
        print(f"\nColumn names: {list(df.columns)}")
        print(f"\nColumn data types:")
        print(df.dtypes)

        print(f"\nFirst 5 rows:")
        print(df.head())

        # Check if Date column exists
        if 'Date' in df.columns:
            print(f"\nDate column found!")
            print(f"First few date values:")
            print(df['Date'].head(10))
            print(f"Date column type: {df['Date'].dtype}")
        else:
            print(f"\nWARNING: No 'Date' column found!")
            print("Looking for columns that might contain dates...")
            for col in df.columns:
                if 'date' in col.lower() or 'month' in col.lower():
                    print(f"  Found potential date column: {col}")
                    print(f"  First few values: {df[col].head(5).tolist()}")

        # Check for unnamed columns
        unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col)]
        if unnamed_cols:
            print(f"\nFound unnamed columns: {unnamed_cols}")
            for col in unnamed_cols:
                print(f"\n{col} first few values:")
                print(df[col].head(5))

except Exception as e:
    print(f"Error reading Excel file: {e}")
    import traceback
    traceback.print_exc()