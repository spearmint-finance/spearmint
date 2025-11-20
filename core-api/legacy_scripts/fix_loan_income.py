"""
Fix Loan Payment Income Classification
Loan payments are NOT income - they're money going OUT
"""

import sqlite3

def fix_loan_payments():
    conn = sqlite3.connect('financial_analysis.db')
    cursor = conn.cursor()

    print("=" * 80)
    print("FIXING LOAN PAYMENT INCOME CLASSIFICATION")
    print("=" * 80)

    # Fix Loan Payment - Principal
    # Should EXCLUDE from income (you're paying OUT, not receiving)
    print("\n1. Fixing Loan Payment - Principal...")
    print("   Should: EXCLUDE from Income (paying out, not receiving)")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_income_calc = 1
        WHERE classification_code = 'LOAN_PRINCIPAL'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    # Fix Loan Payment - Interest
    # Should EXCLUDE from income (you're paying OUT, not receiving)
    print("\n2. Fixing Loan Payment - Interest...")
    print("   Should: EXCLUDE from Income (paying out, not receiving)")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_income_calc = 1
        WHERE classification_code = 'LOAN_INTEREST'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    conn.commit()

    # Display all loan-related classifications
    print("\n" + "=" * 80)
    print("FINAL LOAN CLASSIFICATIONS")
    print("=" * 80)

    cursor.execute("""
        SELECT
            classification_name,
            classification_code,
            CASE WHEN exclude_from_income_calc = 0 THEN 'YES' ELSE 'NO' END as incl_income,
            CASE WHEN exclude_from_expense_calc = 0 THEN 'YES' ELSE 'NO' END as incl_expense,
            CASE WHEN exclude_from_cashflow_calc = 0 THEN 'YES' ELSE 'NO' END as incl_cashflow,
            description
        FROM transaction_classifications
        WHERE classification_code LIKE 'LOAN_%'
        ORDER BY classification_name
    """)

    results = cursor.fetchall()
    print(f"\n{'Name':<30} {'Inc':<5} {'Exp':<5} {'CF':<5}")
    print("-" * 50)
    for row in results:
        print(f"{row[0]:<30} {row[2]:<5} {row[3]:<5} {row[4]:<5}")
        print(f"  → {row[5]}")
        print()

    print("\nExplanation:")
    print("  - Loan Disbursement: You receive money (cash flow IN) but it's borrowed, not income")
    print("  - Loan Principal: You pay back borrowed money (cash flow OUT, not an expense)")
    print("  - Loan Interest: Cost of borrowing (real expense, cash flow OUT)")

    conn.close()
    print("\nLoan payment income classification fixed!")

if __name__ == "__main__":
    fix_loan_payments()
