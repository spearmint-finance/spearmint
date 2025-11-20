#!/usr/bin/env python3
"""
Script to view Capital Expense transactions and generate reports.

This script queries the database for all transactions classified as capital
expenses and displays them in a formatted report.

Usage:
    python view_capital_expenses.py [--year YYYY] [--category NAME] [--export]
"""

import sqlite3
import sys
from datetime import datetime
from typing import Optional


def format_currency(amount: float) -> str:
    """Format amount as currency."""
    return f"${abs(amount):,.2f}"


def get_capital_expenses(
    conn: sqlite3.Connection,
    year: Optional[int] = None,
    category: Optional[str] = None
) -> list:
    """Query capital expense transactions."""
    cursor = conn.cursor()

    query = """
        SELECT
            t.transaction_id,
            DATE(t.transaction_date) as date,
            t.description,
            t.amount,
            c.category_name,
            tc.classification_name,
            tc.classification_code,
            t.notes
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.category_id
        LEFT JOIN transaction_classifications tc ON t.classification_id = tc.classification_id
        WHERE tc.classification_code LIKE '%CAPEX%'
           OR tc.classification_code = 'CAPITAL_EXPENSE'
    """

    params = []

    if year:
        query += " AND strftime('%Y', t.transaction_date) = ?"
        params.append(str(year))

    if category:
        query += " AND c.category_name = ?"
        params.append(category)

    query += " ORDER BY t.transaction_date DESC"

    cursor.execute(query, params)
    return cursor.fetchall()


def print_summary_report(transactions: list):
    """Print a summary report of capital expenses."""
    if not transactions:
        print("No capital expense transactions found.")
        return

    # Calculate totals by year and category
    totals_by_year = {}
    totals_by_category = {}
    total_capex = 0

    for row in transactions:
        year = row[1][:4]  # Extract year from date
        category = row[4] or "Uncategorized"
        amount = abs(row[3])

        totals_by_year[year] = totals_by_year.get(year, 0) + amount
        totals_by_category[category] = totals_by_category.get(category, 0) + amount
        total_capex += amount

    print("\n" + "=" * 80)
    print("CAPITAL EXPENSES SUMMARY REPORT")
    print("=" * 80)
    print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Transactions: {len(transactions)}")
    print(f"Total Capital Expenses: {format_currency(total_capex)}")
    print("=" * 80)

    # Summary by Year
    print("\nSUMMARY BY YEAR:")
    print("-" * 40)
    for year in sorted(totals_by_year.keys(), reverse=True):
        print(f"  {year}: {format_currency(totals_by_year[year])}")

    # Summary by Category
    print("\nSUMMARY BY CATEGORY:")
    print("-" * 40)
    sorted_categories = sorted(
        totals_by_category.items(),
        key=lambda x: x[1],
        reverse=True
    )
    for category, amount in sorted_categories:
        percentage = (amount / total_capex) * 100
        print(f"  {category:<30} {format_currency(amount):>15}  ({percentage:>5.1f}%)")


def print_detailed_report(transactions: list):
    """Print a detailed transaction-by-transaction report."""
    if not transactions:
        return

    print("\n" + "=" * 80)
    print("DETAILED TRANSACTION LIST")
    print("=" * 80)
    print(f"{'Date':<12} {'Description':<30} {'Category':<20} {'Amount':>12}")
    print("-" * 80)

    current_year = None
    year_total = 0

    for row in transactions:
        trans_id, date, description, amount, category, classification, class_code, notes = row
        year = date[:4]

        # Print year header
        if year != current_year:
            if current_year is not None:
                print("-" * 80)
                print(f"{'Year Total:':<64} {format_currency(year_total):>12}")
                print("=" * 80)
            current_year = year
            year_total = 0
            print(f"\n{year}")
            print("-" * 80)

        # Print transaction
        desc_short = description[:28] + ".." if len(description) > 30 else description
        cat_short = (category or "None")[:18] + ".." if len(category or "") > 20 else (category or "None")
        print(f"{date:<12} {desc_short:<30} {cat_short:<20} {format_currency(amount):>12}")

        if notes:
            print(f"             Note: {notes[:60]}")

        year_total += abs(amount)

    # Print final year total
    if current_year:
        print("-" * 80)
        print(f"{'Year Total:':<64} {format_currency(year_total):>12}")
        print("=" * 80)


def export_to_csv(transactions: list, filename: str = "capital_expenses.csv"):
    """Export transactions to CSV file."""
    import csv

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Date',
            'Description',
            'Amount',
            'Category',
            'Classification',
            'Notes'
        ])

        for row in transactions:
            trans_id, date, description, amount, category, classification, class_code, notes = row
            writer.writerow([
                date,
                description,
                abs(amount),
                category or '',
                classification or '',
                notes or ''
            ])

    print(f"\n✅ Exported to {filename}")


def main():
    """Main execution function."""
    # Parse command line arguments
    year = None
    category = None
    export = False

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--year' and i + 1 < len(sys.argv):
            year = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--category' and i + 1 < len(sys.argv):
            category = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--export':
            export = True
            i += 1
        elif sys.argv[i] in ['-h', '--help']:
            print(__doc__)
            return
        else:
            i += 1

    # Connect to database
    try:
        conn = sqlite3.connect('financial_analysis.db')
    except sqlite3.Error as e:
        print(f"❌ Error connecting to database: {e}")
        return

    try:
        # Get transactions
        transactions = get_capital_expenses(conn, year, category)

        if not transactions:
            print("\n⚠️  No capital expense transactions found.")
            print("\nPossible reasons:")
            print("  1. No capital expense classifications exist")
            print("  2. No transactions have been classified as capital expenses")
            print("  3. Filters are too restrictive\n")
            print("To add capital expense classification, run:")
            print("  python add_capital_expense_classification.py\n")
            return

        # Print reports
        print_summary_report(transactions)
        print_detailed_report(transactions)

        # Export if requested
        if export:
            filename = f"capital_expenses_{year or 'all'}.csv"
            export_to_csv(transactions, filename)

        # Print footer
        print("\n" + "=" * 80)
        print("OPTIONS:")
        print("  --year YYYY      : Filter by year (e.g., --year 2025)")
        print("  --category NAME  : Filter by category (e.g., --category 'Vehicle Purchase')")
        print("  --export         : Export to CSV file")
        print("\nEXAMPLES:")
        print("  python view_capital_expenses.py --year 2025")
        print("  python view_capital_expenses.py --category 'Equipment' --export")
        print("  python view_capital_expenses.py --year 2024 --export")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()


if __name__ == '__main__':
    main()
