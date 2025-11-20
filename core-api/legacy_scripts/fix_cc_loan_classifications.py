"""
Fix Credit Card and Loan Classification Settings
These were incorrectly configured
"""

import sqlite3

def fix_classifications():
    conn = sqlite3.connect('financial_analysis.db')
    cursor = conn.cursor()

    print("=" * 80)
    print("FIXING CREDIT CARD AND LOAN CLASSIFICATIONS")
    print("=" * 80)

    # Fix Credit Card Payment
    # Should exclude from ALL calculations (it's an internal transfer)
    print("\n1. Fixing Credit Card Payment...")
    print("   Should: Exclude from Income (not income), Exclude from Expense (already recorded), Exclude from Cash Flow (transfer)")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_income_calc = 1,
            exclude_from_expense_calc = 1,
            exclude_from_cashflow_calc = 1
        WHERE classification_code = 'CC_PAYMENT'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    # Fix Credit Card Receipt
    # Should exclude from ALL calculations (other side of internal transfer)
    print("\n2. Fixing Credit Card Receipt...")
    print("   Should: Exclude from Income (not income), Exclude from Expense (already recorded), Exclude from Cash Flow (transfer)")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_income_calc = 1,
            exclude_from_expense_calc = 1,
            exclude_from_cashflow_calc = 1
        WHERE classification_code = 'CC_RECEIPT'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    # Fix Loan Disbursement
    # Should exclude from income (borrowed money) but INCLUDE in cash flow (you receive it)
    print("\n3. Fixing Loan Disbursement...")
    print("   Should: Exclude from Income (borrowed, not earned), Include in Expense, INCLUDE in Cash Flow (real cash in)")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_income_calc = 1,
            exclude_from_expense_calc = 0,
            exclude_from_cashflow_calc = 0
        WHERE classification_code = 'LOAN_DISB'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    # Fix Loan Payment - Principal
    # Should exclude from expense (paying back borrowed money) but INCLUDE in cash flow
    print("\n4. Fixing Loan Payment - Principal...")
    print("   Should: Include in Income, Exclude from Expense (paying back loan), INCLUDE in Cash Flow (real cash out)")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_income_calc = 0,
            exclude_from_expense_calc = 1,
            exclude_from_cashflow_calc = 0
        WHERE classification_code = 'LOAN_PRINCIPAL'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    # Loan Payment - Interest is already correct (include in all)

    conn.commit()

    # Display results
    print("\n" + "=" * 80)
    print("FINAL CREDIT CARD & LOAN CLASSIFICATIONS")
    print("=" * 80)

    cursor.execute("""
        SELECT
            classification_name,
            classification_code,
            CASE WHEN exclude_from_income_calc = 0 THEN 'YES' ELSE 'NO' END as incl_income,
            CASE WHEN exclude_from_expense_calc = 0 THEN 'YES' ELSE 'NO' END as incl_expense,
            CASE WHEN exclude_from_cashflow_calc = 0 THEN 'YES' ELSE 'NO' END as incl_cashflow
        FROM transaction_classifications
        WHERE classification_code IN ('CC_PAYMENT', 'CC_RECEIPT', 'LOAN_DISB', 'LOAN_PRINCIPAL', 'LOAN_INTEREST')
        ORDER BY classification_name
    """)

    results = cursor.fetchall()
    print(f"\n{'Name':<30} {'Code':<20} {'Inc':<5} {'Exp':<5} {'CF':<5}")
    print("-" * 70)
    for row in results:
        print(f"{row[0]:<30} {row[1]:<20} {row[2]:<5} {row[3]:<5} {row[4]:<5}")

    conn.close()
    print("\nClassification fixes completed successfully!")

if __name__ == "__main__":
    fix_classifications()
