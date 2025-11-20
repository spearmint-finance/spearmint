"""Check import history details."""
from pathlib import Path
from sqlalchemy import create_engine, text

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/financial_analysis.db"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Get latest import
    result = conn.execute(text("""
        SELECT
            import_id,
            file_name,
            import_date,
            total_rows,
            successful_rows,
            failed_rows,
            classified_rows,
            import_mode,
            error_log
        FROM import_history
        ORDER BY import_date DESC
        LIMIT 1
    """))

    row = result.fetchone()

    if row:
        print("=" * 100)
        print("LATEST IMPORT DETAILS")
        print("=" * 100)
        print(f"Import ID: {row[0]}")
        print(f"File Name: {row[1]}")
        print(f"Import Date: {row[2]}")
        print(f"Total Rows: {row[3]}")
        print(f"Successful: {row[4]}")
        print(f"Failed: {row[5]}")
        print(f"Classified: {row[6]}")
        print(f"Mode: {row[7]}")
        print(f"\nSkipped (duplicates): {row[3] - row[4] - row[5]}")

        if row[8]:  # error_log
            print(f"\nError Log:")
            print("-" * 100)
            print(row[8])
        else:
            print("\nNo errors logged")
        print("=" * 100)
    else:
        print("No import history found")

    # Check for actual duplicates in database
    print("\nChecking for duplicates in database...")
    dup_check = conn.execute(text("""
        SELECT
            transaction_date,
            amount,
            description,
            COUNT(*) as count
        FROM transactions
        GROUP BY transaction_date, amount, description
        HAVING COUNT(*) > 1
        LIMIT 10
    """))

    dupes = dup_check.fetchall()
    if dupes:
        print(f"\nFound {len(dupes)} duplicate groups in database:")
        print("-" * 100)
        for d in dupes:
            print(f"Date: {d[0]}, Amount: ${d[1]:.2f}, Description: {d[2][:60]}, Count: {d[3]}")
    else:
        print("\nNo duplicates found in database (good!)")
