import requests
import json

# Get expense data
response = requests.get('http://127.0.0.1:8000/api/analysis/expenses?start_date=2024-10-03&end_date=2025-10-03&mode=analysis')
data = response.json()

print(f"Total Expenses: {data['total_expenses']}")
print(f"Transaction Count: {data['transaction_count']}")
print(f"Average per transaction: {data['average_transaction']}")
print()

# Sort categories by total (most negative first)
categories = []
for cat_name, cat_data in data['breakdown_by_category'].items():
    categories.append({
        'name': cat_name,
        'total': float(cat_data['total']),
        'count': cat_data['count'],
        'average': float(cat_data['average'])
    })

categories.sort(key=lambda x: x['total'])

print("Top 20 Expense Categories:")
print(f"{'Category':<40} {'Total':>15} {'Count':>8} {'Avg/Transaction':>15}")
print("=" * 85)

for cat in categories[:20]:
    print(f"{cat['name']:<40} ${cat['total']:>14,.2f} {cat['count']:>8} ${cat['average']:>14,.2f}")

print()
print(f"Top 20 total: ${sum(c['total'] for c in categories[:20]):,.2f}")
print(f"All expenses: ${sum(c['total'] for c in categories):,.2f}")

