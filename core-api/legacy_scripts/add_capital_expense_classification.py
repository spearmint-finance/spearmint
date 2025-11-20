#!/usr/bin/env python3
"""
Script to add Capital Expense classification types to the database.

This script adds classification types for tracking capital expenses (CapEx)
which are large asset purchases that should be excluded from regular expense
analysis but included in cash flow analysis.

Usage:
    python add_capital_expense_classification.py [--simple|--advanced]

Options:
    --simple    : Add single "Capital Expense" classification (default)
    --advanced  : Add multiple classifications (Property, Vehicle, Equipment)
"""

import sqlite3
import sys
from datetime import datetime


def add_simple_classification(conn):
    """Add a single Capital Expense classification."""
    cursor = conn.cursor()

    classification = {
        'classification_name': 'Capital Expense',
        'classification_code': 'CAPITAL_EXPENSE',
        'description': '''What it is: Large purchase of assets with multi-year lifespan (vehicles, equipment, property improvements, major appliances)

When to use: For significant asset purchases typically >$500-1000 that provide value for multiple years (not regular monthly expenses)

Include/Exclude logic:
- Income calculation: EXCLUDED (capital purchases are not income)
- Expense calculation: EXCLUDED (tracked separately as CapEx, not operating expenses)
- Cash flow calculation: INCLUDED (real cash outflow that impacts your bank balance)

Examples:
- Vehicle purchase ($20,000 car)
- Home improvements (new roof $10,000, HVAC $8,000)
- Business equipment (computer $2,000, desk $800)
- Major appliances (refrigerator $1,500, washer/dryer $1,200)
- Property investments (down payment, closing costs)

NOT capital expenses (use Regular Transaction):
- Vehicle maintenance/repairs (<$1,000)
- Small tools or supplies
- Monthly subscriptions or utilities
- Regular home/office maintenance''',
        'exclude_from_income_calc': True,   # Not income
        'exclude_from_expense_calc': True,  # Separate from operating expenses
        'exclude_from_cashflow_calc': False, # Real cash outflow
        'is_system_classification': False,  # User-created
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }

    try:
        cursor.execute('''
            INSERT INTO transaction_classifications (
                classification_name,
                classification_code,
                description,
                exclude_from_income_calc,
                exclude_from_expense_calc,
                exclude_from_cashflow_calc,
                is_system_classification,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            classification['classification_name'],
            classification['classification_code'],
            classification['description'],
            classification['exclude_from_income_calc'],
            classification['exclude_from_expense_calc'],
            classification['exclude_from_cashflow_calc'],
            classification['is_system_classification'],
            classification['created_at'],
            classification['updated_at']
        ))

        conn.commit()
        print(f"✅ Successfully added: {classification['classification_name']}")
        print(f"   Code: {classification['classification_code']}")
        print(f"   ID: {cursor.lastrowid}")

    except sqlite3.IntegrityError:
        print(f"⚠️  Classification '{classification['classification_code']}' already exists")
        conn.rollback()


def add_advanced_classifications(conn):
    """Add multiple specialized Capital Expense classifications."""
    cursor = conn.cursor()

    classifications = [
        {
            'classification_name': 'Property Capital Expense',
            'classification_code': 'PROPERTY_CAPEX',
            'description': '''What it is: Real estate purchases and major property improvements

When to use: For property-related capital investments

Include/Exclude logic:
- Income calculation: EXCLUDED
- Expense calculation: EXCLUDED
- Cash flow calculation: INCLUDED

Examples:
- Property purchase/down payment
- Major renovations (kitchen, bathroom)
- Structural improvements (roof, foundation, HVAC)
- Property additions (garage, deck, room addition)
- Rental property improvements''',
            'exclude_from_income_calc': True,
            'exclude_from_expense_calc': True,
            'exclude_from_cashflow_calc': False,
            'is_system_classification': False
        },
        {
            'classification_name': 'Vehicle Capital Expense',
            'classification_code': 'VEHICLE_CAPEX',
            'description': '''What it is: Vehicle purchases and major repairs/upgrades

When to use: For vehicle acquisitions and significant improvements

Include/Exclude logic:
- Income calculation: EXCLUDED
- Expense calculation: EXCLUDED
- Cash flow calculation: INCLUDED

Examples:
- Vehicle purchase
- Down payment on vehicle
- Major repairs/upgrades (engine replacement, transmission)
- Vehicle modifications for business use

NOT this classification:
- Regular maintenance (oil changes, tire rotation)
- Minor repairs (<$1,000)
- Gas and insurance (use Regular Transaction)''',
            'exclude_from_income_calc': True,
            'exclude_from_expense_calc': True,
            'exclude_from_cashflow_calc': False,
            'is_system_classification': False
        },
        {
            'classification_name': 'Equipment Capital Expense',
            'classification_code': 'EQUIPMENT_CAPEX',
            'description': '''What it is: Business equipment, computers, machinery, tools, furniture

When to use: For equipment and technology asset purchases

Include/Exclude logic:
- Income calculation: EXCLUDED
- Expense calculation: EXCLUDED
- Cash flow calculation: INCLUDED

Examples:
- Computers and laptops
- Office furniture (desks, chairs)
- Business machinery
- Professional tools and equipment
- Cameras and recording equipment
- Servers and networking equipment

NOT this classification:
- Software subscriptions (use Regular Transaction)
- Small office supplies (<$500)
- Consumables and accessories''',
            'exclude_from_income_calc': True,
            'exclude_from_expense_calc': True,
            'exclude_from_cashflow_calc': False,
            'is_system_classification': False
        }
    ]

    added_count = 0
    skipped_count = 0

    for classification in classifications:
        try:
            cursor.execute('''
                INSERT INTO transaction_classifications (
                    classification_name,
                    classification_code,
                    description,
                    exclude_from_income_calc,
                    exclude_from_expense_calc,
                    exclude_from_cashflow_calc,
                    is_system_classification,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                classification['classification_name'],
                classification['classification_code'],
                classification['description'],
                classification['exclude_from_income_calc'],
                classification['exclude_from_expense_calc'],
                classification['exclude_from_cashflow_calc'],
                classification['is_system_classification'],
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))

            print(f"✅ Successfully added: {classification['classification_name']}")
            print(f"   Code: {classification['classification_code']}")
            print(f"   ID: {cursor.lastrowid}")
            added_count += 1

        except sqlite3.IntegrityError:
            print(f"⚠️  Classification '{classification['classification_code']}' already exists")
            skipped_count += 1

    if added_count > 0:
        conn.commit()
        print(f"\n✅ Successfully added {added_count} classification(s)")

    if skipped_count > 0:
        print(f"⚠️  Skipped {skipped_count} existing classification(s)")


def main():
    """Main execution function."""
    # Parse command line arguments
    mode = 'simple'
    if len(sys.argv) > 1:
        if sys.argv[1] == '--advanced':
            mode = 'advanced'
        elif sys.argv[1] == '--simple':
            mode = 'simple'
        elif sys.argv[1] in ['-h', '--help']:
            print(__doc__)
            return

    print("=" * 70)
    print("Capital Expense Classification Setup")
    print("=" * 70)
    print(f"Mode: {mode.upper()}")
    print()

    # Connect to database
    try:
        conn = sqlite3.connect('financial_analysis.db')
        print("✅ Connected to database: financial_analysis.db\n")
    except sqlite3.Error as e:
        print(f"❌ Error connecting to database: {e}")
        return

    try:
        if mode == 'simple':
            print("Adding single Capital Expense classification...\n")
            add_simple_classification(conn)
        else:
            print("Adding advanced Capital Expense classifications...\n")
            add_advanced_classifications(conn)

        print("\n" + "=" * 70)
        print("Setup Complete!")
        print("=" * 70)
        print("\nNext Steps:")
        print("1. Go to /classifications in the web UI to view your new classifications")
        print("2. Create categories for your assets (Vehicle Purchase, Equipment, etc.)")
        print("3. Set up classification rules to auto-classify capital expenses")
        print("4. Reclassify any existing capital expense transactions")
        print("5. Check expense analysis - capital expenses should be excluded")
        print("6. Check cash flow analysis - capital expenses should be included")
        print("\nSee capital-expenses-guide.md for detailed usage instructions.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    main()
