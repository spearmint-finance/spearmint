"""
Update all classification descriptions with detailed logical explanations
"""

import sqlite3

def update_all_descriptions():
    conn = sqlite3.connect('financial_analysis.db')
    cursor = conn.cursor()

    print("=" * 80)
    print("UPDATING ALL DESCRIPTIONS WITH DETAILED LOGIC")
    print("=" * 80)

    descriptions = {
        'REGULAR': """What it is: Normal income or expense
Include in Income: YES (earned income counts)
Include in Expense: YES (real expenses count)
Include in Cash Flow: YES (money actually moves)""",

        'TRANSFER': """What it is: Moving money between your own accounts
Include in Income: NO (not earned income)
Include in Expense: NO (just moving money, not spending)
Include in Cash Flow: NO (money stays yours, no net change)""",

        'REFUND': """What it is: Getting money back from a previous purchase
Apply to: INCOME transactions (money coming back to you)
Include in Income: NO (not earned income, just getting YOUR money back)
Include in Expense: NO (it's money coming IN, not an expense)
Include in Cash Flow: YES (real money entering your account)""",

        'CREDIT_CARD_REWARD': """What it is: Cashback or points redemption from credit card
Apply to: INCOME transactions (statement credit)
Include in Income: NO (it's a reward/rebate, not earned income)
Include in Expense: NO (money coming IN, not an expense)
Include in Cash Flow: YES (reduces what you have to pay)""",

        'REIMBURSEMENT': """What it is: Employer paying you back for work expenses
Apply to: INCOME transactions (money coming from employer)
Include in Income: NO (getting YOUR money back, not getting paid)
Include in Expense: NO (money coming IN, not an expense)
Include in Cash Flow: YES (real money entering your account)""",

        'INSURANCE_REIMBURSEMENT': """What it is: Insurance paying you back for medical/other expenses
Apply to: INCOME transactions (insurance payment to you)
Include in Income: NO (getting money back for expenses, not earned income)
Include in Expense: NO (money coming IN, not an expense)
Include in Cash Flow: YES (real money entering your account)""",

        'INVESTMENT_DISTRIBUTION': """What it is: Dividends or capital gains from investments
Apply to: INCOME transactions (investment returns)
Include in Income: YES (this IS taxable income)
Include in Expense: NO (money coming IN, not an expense)
Include in Cash Flow: YES (real money you receive)""",

        'REIMBURSABLE_EXPENSE': """What it is: Expense that employer will reimburse
Apply to: EXPENSE transactions (you paying for work)
Include in Income: NO (you're paying OUT, not receiving)
Include in Expense: NO (will be reimbursed, not personal expense)
Include in Cash Flow: YES (money temporarily leaving your account)""",

        'CC_PAYMENT': """What it is: Paying your credit card bill from bank account
Apply to: EXPENSE transactions (money leaving checking account)
Include in Income: NO (you're paying OUT, not receiving)
Include in Expense: NO (purchases already recorded when you used card)
Include in Cash Flow: NO (internal transfer from checking to credit card)""",

        'CC_RECEIPT': """What it is: Credit card company receiving your payment
Apply to: INCOME transactions (on credit card account side)
Include in Income: NO (not your income)
Include in Expense: NO (not your expense)
Include in Cash Flow: NO (other side of CC_PAYMENT transfer)""",

        'LOAN_DISB': """What it is: Receiving loan money (mortgage, personal loan, etc.)
Apply to: INCOME transactions (money coming to you)
Include in Income: NO (borrowed money you must repay, not earned)
Include in Expense: NO (money coming IN, not an expense)
Include in Cash Flow: YES (real money entering your account)""",

        'LOAN_PRINCIPAL': """What it is: Principal portion of loan payment
Apply to: EXPENSE transactions (paying back the loan)
Include in Income: NO (you're paying OUT, not receiving)
Include in Expense: NO (returning borrowed money, not buying goods/services)
Include in Cash Flow: YES (real money leaving your account)""",

        'LOAN_INTEREST': """What it is: Interest portion of loan payment
Apply to: EXPENSE transactions (cost of borrowing)
Include in Income: NO (you're paying OUT, not receiving)
Include in Expense: YES (real expense, cost of borrowing, tax deductible)
Include in Cash Flow: YES (real money leaving your account)""",
    }

    for code, description in descriptions.items():
        cursor.execute("""
            UPDATE transaction_classifications
            SET description = ?
            WHERE classification_code = ?
        """, (description, code))
        print(f"Updated: {code}")

    conn.commit()

    # Display one example
    print("\n" + "=" * 80)
    print("EXAMPLE - LOAN_PRINCIPAL:")
    print("=" * 80)
    cursor.execute("""
        SELECT description
        FROM transaction_classifications
        WHERE classification_code = 'LOAN_PRINCIPAL'
    """)
    result = cursor.fetchone()
    if result:
        print(result[0])

    print("\n" + "=" * 80)
    print("All descriptions updated with detailed logic!")
    print("=" * 80)

    conn.close()

if __name__ == "__main__":
    update_all_descriptions()
