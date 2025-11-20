import sqlite3

conn = sqlite3.connect('financial_analysis.db')
cursor = conn.cursor()

# Check sample data
cursor.execute('''
    SELECT source, transfer_account_from, transfer_account_to, payment_method
    FROM transactions
    WHERE source IS NOT NULL
       OR transfer_account_from IS NOT NULL
       OR transfer_account_to IS NOT NULL
       OR payment_method IS NOT NULL
    LIMIT 10
''')
rows = cursor.fetchall()

print('Sample transactions with institution/account data:')
print('source | transfer_from | transfer_to | payment_method')
print('-' * 80)
for row in rows:
    print(f'{row[0] or "NULL"} | {row[1] or "NULL"} | {row[2] or "NULL"} | {row[3] or "NULL"}')

# Get counts
cursor.execute('SELECT COUNT(*) FROM transactions WHERE source IS NOT NULL')
source_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM transactions WHERE transfer_account_from IS NOT NULL')
from_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM transactions WHERE transfer_account_to IS NOT NULL')
to_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM transactions WHERE payment_method IS NOT NULL')
payment_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM transactions')
total_count = cursor.fetchone()[0]

print(f'\nTotal transactions: {total_count}')
print(f'Total with source: {source_count} ({source_count/total_count*100:.1f}%)')
print(f'Total with transfer_account_from: {from_count} ({from_count/total_count*100:.1f}%)')
print(f'Total with transfer_account_to: {to_count} ({to_count/total_count*100:.1f}%)')
print(f'Total with payment_method: {payment_count} ({payment_count/total_count*100:.1f}%)')

conn.close()
