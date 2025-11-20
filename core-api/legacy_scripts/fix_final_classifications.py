"""
Final Classification Fixes
Fix 3 remaining incorrect classifications and update ALL descriptions
"""

import sqlite3

def fix_and_update_all():
    conn = sqlite3.connect('financial_analysis.db')
    cursor = conn.cursor()

    print("=" * 80)
    print("FINAL CLASSIFICATION FIXES & DESCRIPTION UPDATES")
    print("=" * 80)

    # FIX 1: Credit Card Reward
    print("\n1. Fixing Credit Card Reward...")
    print("   Was: Exclude Income, INCLUDE Expense (WRONG), Include Cash Flow")
    print("   Now: Exclude Income, EXCLUDE Expense (CORRECT), Include Cash Flow")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_expense_calc = 1,
            description = 'Credit card cashback or points redemption. Apply to INCOME transactions. Not earned income (reward/rebate), not an expense (money coming IN). Shows in cash flow.'
        WHERE classification_code = 'CREDIT_CARD_REWARD'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    # FIX 2: Investment Distribution
    print("\n2. Fixing Investment Distribution...")
    print("   Was: Include Income, INCLUDE Expense (WRONG), Include Cash Flow")
    print("   Now: Include Income, EXCLUDE Expense (CORRECT), Include Cash Flow")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_expense_calc = 1,
            description = 'Dividend or capital gains distribution from investments. Apply to INCOME transactions. This IS taxable income. Not an expense (money coming IN). Shows in cash flow.'
        WHERE classification_code = 'INVESTMENT_DISTRIBUTION'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    # FIX 3: Loan Disbursement
    print("\n3. Fixing Loan Disbursement...")
    print("   Was: Exclude Income, INCLUDE Expense (WRONG), Include Cash Flow")
    print("   Now: Exclude Income, EXCLUDE Expense (CORRECT), Include Cash Flow")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_expense_calc = 1,
            description = 'Loan amount received. Apply to INCOME transactions. Not earned income (borrowed money you must repay). Not an expense (money coming IN). Shows in cash flow.'
        WHERE classification_code = 'LOAN_DISB'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    print("\n" + "=" * 80)
    print("UPDATING ALL OTHER DESCRIPTIONS")
    print("=" * 80)

    # Update all other descriptions (no setting changes, just better descriptions)

    updates = [
        ('REGULAR', 'Normal income or expense transaction. Counted in all financial calculations.'),
        ('TRANSFER', 'Transfer between your own accounts. Moving money around is not income or expense. Excluded from all calculations.'),
        ('REFUND', 'Refund of a previous purchase. Apply to INCOME transactions when you receive money back. Not counted as earned income (getting your money back). Shows in cash flow.'),
        ('REIMBURSEMENT', 'Employer reimbursement for work expenses. Apply to INCOME transactions. Not counted as earned income (getting your money back). Shows in cash flow.'),
        ('INSURANCE_REIMBURSEMENT', 'Insurance reimbursement for medical/other expenses. Apply to INCOME transactions. Not counted as earned income (getting money back). Shows in cash flow.'),
        ('REIMBURSABLE_EXPENSE', 'Expense that will be reimbursed by employer. Apply to EXPENSE transactions. Not counted as personal expense (you will get the money back). Shows in cash flow temporarily.'),
        ('CC_PAYMENT', 'Payment to credit card from bank account. Apply to EXPENSE transactions. Not an expense (purchases already recorded). Internal transfer. Excluded from all calculations.'),
        ('CC_RECEIPT', 'Credit card company receiving your payment. Apply to INCOME transactions on credit card account. Other side of CC_PAYMENT. Excluded from all calculations.'),
        ('LOAN_PRINCIPAL', 'Principal portion of loan payment. Apply to EXPENSE transactions. Not an expense (returning borrowed money, not buying goods/services). Shows in cash flow out.'),
        ('LOAN_INTEREST', 'Interest portion of loan payment. Apply to EXPENSE transactions. This IS a real expense (cost of borrowing, tax deductible). Shows in cash flow out.'),
    ]

    for code, desc in updates:
        cursor.execute("""
            UPDATE transaction_classifications
            SET description = ?
            WHERE classification_code = ?
        """, (desc, code))
        print(f"   Updated description for {code}")

    conn.commit()

    # Display final results
    print("\n" + "=" * 80)
    print("FINAL CLASSIFICATION TABLE")
    print("=" * 80)

    cursor.execute("""
        SELECT
            classification_name,
            classification_code,
            CASE WHEN exclude_from_income_calc = 0 THEN 'YES' ELSE 'NO' END as inc,
            CASE WHEN exclude_from_expense_calc = 0 THEN 'YES' ELSE 'NO' END as exp,
            CASE WHEN exclude_from_cashflow_calc = 0 THEN 'YES' ELSE 'NO' END as cf
        FROM transaction_classifications
        WHERE is_system_classification = 1
        ORDER BY classification_name
    """)

    print(f"\n{'Name':<32} {'Code':<26} {'Inc':<4} {'Exp':<4} {'CF':<4}")
    print("-" * 80)
    for row in cursor.fetchall():
        print(f"{row[0]:<32} {row[1]:<26} {row[2]:<4} {row[3]:<4} {row[4]:<4}")

    print("\n" + "=" * 80)
    print("All classifications fixed and descriptions updated!")
    print("=" * 80)

    conn.close()

if __name__ == "__main__":
    fix_and_update_all()
