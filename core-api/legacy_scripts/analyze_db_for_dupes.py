"""Analyze database to understand what would be considered duplicates."""
from pathlib import Path
from sqlalchemy import create_engine, text
from hashlib import md5

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/financial_analysis.db"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Get all transactions
    result = conn.execute(text("""
        SELECT transaction_id, transaction_date, amount, description
        FROM transactions
        ORDER BY transaction_date DESC, amount
        LIMIT 100
    """))

    transactions = result.fetchall()

    print("=" * 120)
    print("ANALYZING TRANSACTIONS FOR POTENTIAL DUPLICATES")
    print("=" * 120)

    # Group by date and amount (common duplicate indicators)
    print("\nTransactions with same DATE and AMOUNT (potential duplicates if description also matches):")
    print("-" * 120)

    date_amount_groups = {}
    for tx in transactions:
        key = (tx[1], tx[2])  # date, amount
        if key not in date_amount_groups:
            date_amount_groups[key] = []
        date_amount_groups[key].append(tx)

    found_potential_dupes = False
    for (date, amount), txs in date_amount_groups.items():
        if len(txs) > 1:
            found_potential_dupes = True
            print(f"\nDate: {date}, Amount: ${amount:.2f} - {len(txs)} transactions:")
            for tx in txs[:5]:  # Show max 5
                print(f"  ID: {tx[0]:6} | {tx[3][:80]}")

    if not found_potential_dupes:
        print("No transactions with same date+amount found in sample")

    # Check what the duplicate detection algorithm would flag
    print("\n" + "=" * 120)
    print("SIMULATING DUPLICATE DETECTION ALGORITHM")
    print("=" * 120)

    result = conn.execute(text("""
        SELECT transaction_date, amount, description, COUNT(*) as cnt
        FROM transactions
        GROUP BY transaction_date, amount, description
        HAVING COUNT(*) > 1
    """))

    exact_dupes = result.fetchall()
    if exact_dupes:
        print(f"\nFound {len(exact_dupes)} sets of transactions with EXACT same date+amount+description:")
        for d in exact_dupes[:10]:
            print(f"  Date: {d[0]}, Amount: ${d[1]:.2f}, Count: {d[3]}, Desc: {d[2][:70]}")
    else:
        print("\nNo exact duplicates (same date+amount+description) found")

    # Show some examples of similar-looking transactions
    print("\n" + "=" * 120)
    print("SAMPLE TRANSACTIONS (to understand your data)")
    print("=" * 120)

    result = conn.execute(text("""
        SELECT transaction_date, amount, description
        FROM transactions
        ORDER BY transaction_date DESC
        LIMIT 20
    """))

    print(f"\n{'Date':<12} | {'Amount':>10} | Description")
    print("-" * 120)
    for row in result:
        desc = row[2][:80] if row[2] else ''
        print(f"{row[0]} | ${row[1]:>9.2f} | {desc}")
