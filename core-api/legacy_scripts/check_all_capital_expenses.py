import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

# First, let's see what the Capital Expense classification rule actually matches
print("=" * 80)
print("CAPITAL EXPENSE CLASSIFICATION RULE")
print("=" * 80)

cursor.execute("""
    SELECT
        rule_id,
        rule_name,
        description_pattern,
        category_pattern,
        classification_id
    FROM classification_rules
    WHERE classification_id = 22
""")

rule = cursor.fetchone()
if rule:
    print(f"Rule ID: {rule[0]}")
    print(f"Rule Name: {rule[1]}")
    print(f"Description Pattern: {rule[2]}")
    print(f"Category Pattern: {rule[3]}")
    print(f"Classification ID: {rule[4]}")

# Now check all transactions that SHOULD match this rule
print("\n" + "=" * 80)
print("TRANSACTIONS MATCHING THE RULE PATTERN")
print("=" * 80)

cursor.execute("""
    SELECT
        t.transaction_id,
        t.transaction_date,
        t.description,
        c.category_name,
        t.amount,
        t.classification_id,
        tc.classification_name
    FROM transactions t
    LEFT JOIN categories c ON t.category_id = c.category_id
    LEFT JOIN transaction_classifications tc ON t.classification_id = tc.classification_id
    WHERE t.description LIKE '%capital%'
       OR c.category_name LIKE '%capital%'
    ORDER BY t.transaction_date DESC
""")

transactions = cursor.fetchall()
total_capital = 0
classified_count = 0
unclassified_count = 0

print(f"\nFound {len(transactions)} transactions matching capital pattern:\n")
for t in transactions[:10]:  # Show first 10
    print(f"  {t[1]} | {t[3]:30s} | ${float(t[4]):>10,.2f} | {t[6] if t[6] else 'UNCLASSIFIED'}")
    total_capital += float(t[4])
    if t[5] == 22:
        classified_count += 1
    else:
        unclassified_count += 1

if len(transactions) > 10:
    print(f"  ... and {len(transactions) - 10} more transactions")
    for t in transactions[10:]:
        total_capital += float(t[4])
        if t[5] == 22:
            classified_count += 1
        else:
            unclassified_count += 1

print(f"\nTotal matching pattern: {len(transactions)}")
print(f"Already classified as Capital Expense: {classified_count}")
print(f"Not yet classified: {unclassified_count}")
print(f"Total amount: ${total_capital:,.2f}")

# Now check ONLY transactions already classified as Capital Expense
print("\n" + "=" * 80)
print("TRANSACTIONS ALREADY CLASSIFIED AS CAPITAL EXPENSE (ID=22)")
print("=" * 80)

cursor.execute("""
    SELECT
        COUNT(*) as count,
        SUM(amount) as total
    FROM transactions
    WHERE classification_id = 22
""")

result = cursor.fetchone()
print(f"Count: {result[0]}")
print(f"Total: ${float(result[1]) if result[1] else 0:,.2f}")

# Check all expenses (for comparison)
print("\n" + "=" * 80)
print("ALL EXPENSES (for comparison)")
print("=" * 80)

cursor.execute("""
    SELECT
        COUNT(*) as count,
        SUM(amount) as total
    FROM transactions
    WHERE transaction_type = 'Expense'
""")

result = cursor.fetchone()
all_expense_count = result[0]
all_expense_total = float(result[1]) if result[1] else 0

print(f"Total Expense Count: {all_expense_count}")
print(f"Total Expense Amount: ${all_expense_total:,.2f}")

# Calculate what should be excluded
print("\n" + "=" * 80)
print("EXPECTED TOTALS")
print("=" * 80)
print(f"WITH capital expenses: ${all_expense_total:,.2f}")
print(f"Capital expenses only: ${total_capital:,.2f}")
print(f"WITHOUT capital (operating only): ${all_expense_total - total_capital:,.2f}")

conn.close()
