"""
Fix Reimbursement Classification Logic

Key insight:
- Reimbursable Expense = EXPENSE transaction (money going OUT, will be reimbursed)
- Work Reimbursement = INCOME transaction (money coming IN from employer)
- Insurance Reimbursement = INCOME transaction (money coming IN from insurance)
- Refund = INCOME transaction (money coming IN from store)

The flags control whether to COUNT them in totals, not the transaction direction.
"""

import sqlite3

def fix_reimbursements():
    conn = sqlite3.connect('financial_analysis.db')
    cursor = conn.cursor()

    print("=" * 80)
    print("FIXING REIMBURSEMENT CLASSIFICATIONS")
    print("=" * 80)

    # Fix Reimbursable Expense
    # This is an EXPENSE transaction, but shouldn't count as personal expense
    print("\n1. Fixing Reimbursable Expense...")
    print("   Transaction type: EXPENSE (money going OUT)")
    print("   Should: Exclude Income (it's an expense), Exclude Expense (will be reimbursed), Include Cash Flow")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_income_calc = 1,
            exclude_from_expense_calc = 1,
            exclude_from_cashflow_calc = 0
        WHERE classification_code = 'REIMBURSABLE_EXPENSE'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    # Fix Work Reimbursement
    # This is an INCOME transaction, but not earned income
    print("\n2. Fixing Work Reimbursement...")
    print("   Transaction type: INCOME (money coming IN)")
    print("   Should: Exclude Income (not earned), Exclude Expense (not an expense!), Include Cash Flow")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_income_calc = 1,
            exclude_from_expense_calc = 1,
            exclude_from_cashflow_calc = 0
        WHERE classification_code = 'REIMBURSEMENT'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    # Fix Insurance Reimbursement
    # This is an INCOME transaction, but not earned income
    print("\n3. Fixing Insurance Reimbursement...")
    print("   Transaction type: INCOME (money coming IN)")
    print("   Should: Exclude Income (not earned), Exclude Expense (not an expense!), Include Cash Flow")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_income_calc = 1,
            exclude_from_expense_calc = 1,
            exclude_from_cashflow_calc = 0
        WHERE classification_code = 'INSURANCE_REIMBURSEMENT'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    # Fix Refund
    # This is an INCOME transaction, but not earned income
    print("\n4. Fixing Refund...")
    print("   Transaction type: INCOME (money coming IN)")
    print("   Should: Exclude Income (not earned), Exclude Expense (not an expense!), Include Cash Flow")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_income_calc = 1,
            exclude_from_expense_calc = 1,
            exclude_from_cashflow_calc = 0
        WHERE classification_code = 'REFUND'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    conn.commit()

    # Display results
    print("\n" + "=" * 80)
    print("FINAL REIMBURSEMENT CLASSIFICATIONS")
    print("=" * 80)

    cursor.execute("""
        SELECT
            classification_name,
            CASE WHEN exclude_from_income_calc = 0 THEN 'Include' ELSE 'Exclude' END as income,
            CASE WHEN exclude_from_expense_calc = 0 THEN 'Include' ELSE 'Exclude' END as expense,
            CASE WHEN exclude_from_cashflow_calc = 0 THEN 'Include' ELSE 'Exclude' END as cashflow
        FROM transaction_classifications
        WHERE classification_code IN ('REIMBURSEMENT', 'REIMBURSABLE_EXPENSE', 'INSURANCE_REIMBURSEMENT', 'REFUND')
        ORDER BY classification_name
    """)

    results = cursor.fetchall()
    for row in results:
        print(f"\n{row[0]}:")
        print(f"  Income: {row[1]:<8} | Expense: {row[2]:<8} | Cash Flow: {row[3]}")

    print("\n" + "=" * 80)
    print("EXAMPLE SCENARIO:")
    print("=" * 80)
    print("\n1. Pay work hotel: $200 EXPENSE with REIMBURSABLE_EXPENSE classification")
    print("   - Not counted in personal expenses (will be reimbursed)")
    print("   - Shows in cash flow OUT")
    print("\n2. Receive reimbursement: $200 INCOME with REIMBURSEMENT classification")
    print("   - Not counted in personal income (just getting your money back)")
    print("   - Shows in cash flow IN")
    print("\nNet result: $0 impact on income/expenses, cash flow shows the timing")

    conn.close()
    print("\nReimbursement classifications fixed!")

if __name__ == "__main__":
    fix_reimbursements()
