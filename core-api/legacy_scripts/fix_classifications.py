"""
Fix Classification Issues
This script fixes incorrect settings and removes duplicates
"""

import sqlite3

def fix_classifications():
    # Connect to database
    conn = sqlite3.connect('financial_analysis.db')
    cursor = conn.cursor()

    print("=" * 80)
    print("FIXING CLASSIFICATION ISSUES")
    print("=" * 80)

    # 1. Fix Insurance Reimbursement - should NOT exclude from cash flow
    print("\n1. Fixing Insurance Reimbursement cash flow setting...")
    cursor.execute("""
        UPDATE transaction_classifications
        SET exclude_from_cashflow_calc = 0
        WHERE classification_code = 'INSURANCE_REIMBURSEMENT'
    """)
    print(f"   Updated {cursor.rowcount} row(s)")

    # 2. Delete duplicate "Standard Transaction" (keep "Regular Transaction")
    print("\n2. Deleting duplicate 'Standard Transaction'...")
    cursor.execute("""
        DELETE FROM transaction_classifications
        WHERE classification_code = 'STANDARD'
    """)
    print(f"   Deleted {cursor.rowcount} row(s)")

    # 3. Delete old "Reimbursement Received" (keep "Work Reimbursement")
    print("\n3. Deleting old 'Reimbursement Received'...")
    cursor.execute("""
        DELETE FROM transaction_classifications
        WHERE classification_code = 'REIMB_RECEIVED'
    """)
    print(f"   Deleted {cursor.rowcount} row(s)")

    # 4. Delete old "Reimbursement Paid" (keep "Reimbursable Expense")
    print("\n4. Deleting old 'Reimbursement Paid'...")
    cursor.execute("""
        DELETE FROM transaction_classifications
        WHERE classification_code = 'REIMB_PAID'
    """)
    print(f"   Deleted {cursor.rowcount} row(s)")

    # Commit changes
    conn.commit()

    # 5. Display final system classifications
    print("\n" + "=" * 80)
    print("FINAL SYSTEM CLASSIFICATIONS")
    print("=" * 80)

    cursor.execute("""
        SELECT
            classification_id,
            classification_name,
            classification_code,
            CASE WHEN exclude_from_income_calc = 1 THEN 'YES' ELSE 'NO' END as excl_income,
            CASE WHEN exclude_from_expense_calc = 1 THEN 'YES' ELSE 'NO' END as excl_expense,
            CASE WHEN exclude_from_cashflow_calc = 1 THEN 'YES' ELSE 'NO' END as excl_cashflow
        FROM transaction_classifications
        WHERE is_system_classification = 1
        ORDER BY classification_name
    """)

    results = cursor.fetchall()
    print(f"\nFound {len(results)} system classifications:\n")
    print(f"{'ID':<4} {'Name':<30} {'Code':<25} {'Ex.Inc':<8} {'Ex.Exp':<8} {'Ex.CF':<8}")
    print("-" * 95)
    for row in results:
        print(f"{row[0]:<4} {row[1]:<30} {row[2]:<25} {row[3]:<8} {row[4]:<8} {row[5]:<8}")

    conn.close()
    print("\n✅ Classification fixes completed successfully!")

if __name__ == "__main__":
    fix_classifications()
