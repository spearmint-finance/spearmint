"""
Update all classification descriptions with better formatting and clearer language
"""

import sqlite3

def update_all_descriptions():
    conn = sqlite3.connect('financial_analysis.db')
    cursor = conn.cursor()

    print("=" * 80)
    print("UPDATING DESCRIPTIONS WITH PROPER FORMATTING")
    print("=" * 80)

    descriptions = {
        'REGULAR': """What it is: Normal income or expense

When to use: Any regular transaction (salary, groceries, bills, etc.)

Include in Income: YES (earned income counts)
Include in Expense: YES (real expenses count)
Include in Cash Flow: YES (money actually moves)""",

        'TRANSFER': """What it is: Moving money between your own accounts

When to use: Transfers between checking/savings, paying credit card from checking

Include in Income: NO (not earned income)
Include in Expense: NO (just moving money, not spending)
Include in Cash Flow: NO (money stays yours, no net change)""",

        'REFUND': """What it is: Getting money back from a previous purchase

When to use: When recording the refund as an INCOME transaction

Include in Income: NO (not earned, just getting YOUR money back)
Include in Expense: NO (money coming IN, not going out)
Include in Cash Flow: YES (real money entering your account)""",

        'CREDIT_CARD_REWARD': """What it is: Cashback or points redemption from credit card

When to use: When recording statement credit or cashback as an INCOME transaction

Include in Income: NO (reward/rebate, not earned income)
Include in Expense: NO (money coming IN, not going out)
Include in Cash Flow: YES (reduces what you have to pay)""",

        'REIMBURSEMENT': """What it is: Employer paying you back for work expenses

When to use: When recording employer reimbursement as an INCOME transaction

Include in Income: NO (getting YOUR money back, not getting paid)
Include in Expense: NO (money coming IN, not going out)
Include in Cash Flow: YES (real money entering your account)""",

        'INSURANCE_REIMBURSEMENT': """What it is: Insurance paying you back for medical/other expenses

When to use: When recording insurance payment as an INCOME transaction

Include in Income: NO (getting money back for expenses, not earned)
Include in Expense: NO (money coming IN, not going out)
Include in Cash Flow: YES (real money entering your account)""",

        'INVESTMENT_DISTRIBUTION': """What it is: Dividends or capital gains from investments

When to use: When recording investment returns as an INCOME transaction

Include in Income: YES (this IS taxable income)
Include in Expense: NO (money coming IN, not going out)
Include in Cash Flow: YES (real money you receive)""",

        'REIMBURSABLE_EXPENSE': """What it is: Expense that employer will reimburse

When to use: When recording a work expense as an EXPENSE transaction (that you'll be reimbursed for)

Include in Income: NO (money going OUT, not coming in)
Include in Expense: NO (will be reimbursed, not personal expense)
Include in Cash Flow: YES (money temporarily leaving your account)""",

        'CC_PAYMENT': """What it is: Paying your credit card bill from bank account

When to use: When recording the payment as an EXPENSE transaction in your checking account

Include in Income: NO (money going OUT, not coming in)
Include in Expense: NO (purchases already recorded when you used card)
Include in Cash Flow: NO (internal transfer, not real spending)""",

        'CC_RECEIPT': """What it is: Credit card company receiving your payment

When to use: When recording the payment as an INCOME transaction in your credit card account

Include in Income: NO (not income for you)
Include in Expense: NO (not expense for you)
Include in Cash Flow: NO (other side of credit card payment transfer)""",

        'LOAN_DISB': """What it is: Receiving loan money (mortgage, personal loan, etc.)

When to use: When recording loan proceeds as an INCOME transaction

Include in Income: NO (borrowed money you must repay, not earned)
Include in Expense: NO (money coming IN, not going out)
Include in Cash Flow: YES (real money entering your account)""",

        'LOAN_PRINCIPAL': """What it is: Principal portion of loan payment

When to use: When recording the principal part of your loan payment as an EXPENSE transaction

Include in Income: NO (money going OUT, not coming in)
Include in Expense: NO (returning borrowed money, not buying goods/services)
Include in Cash Flow: YES (real money leaving your account)""",

        'LOAN_INTEREST': """What it is: Interest portion of loan payment

When to use: When recording the interest part of your loan payment as an EXPENSE transaction

Include in Income: NO (money going OUT, not coming in)
Include in Expense: YES (real expense - cost of borrowing, tax deductible)
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

    # Display a few examples
    print("\n" + "=" * 80)
    print("EXAMPLE DESCRIPTIONS:")
    print("=" * 80)

    cursor.execute("""
        SELECT classification_name, description
        FROM transaction_classifications
        WHERE classification_code IN ('CC_PAYMENT', 'LOAN_PRINCIPAL')
        ORDER BY classification_name
    """)

    for row in cursor.fetchall():
        print(f"\n{row[0]}:")
        print("-" * 80)
        print(row[1])

    print("\n" + "=" * 80)
    print("All descriptions updated!")
    print("=" * 80)

    conn.close()

if __name__ == "__main__":
    update_all_descriptions()
