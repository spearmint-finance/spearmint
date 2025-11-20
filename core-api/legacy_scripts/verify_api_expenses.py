import requests
import json

# Test the actual API endpoint to see what expenses are being returned
base_url = "http://localhost:8000/api"

# Get expenses in ANALYSIS mode (operating only - should exclude capital)
print("=" * 80)
print("TESTING EXPENSE API IN ANALYSIS MODE (Operating Expenses)")
print("=" * 80)

response = requests.get(
    f"{base_url}/analysis/expenses",
    params={
        "analysis_mode": "ANALYSIS",
        "start_date": "2020-01-01",
        "end_date": "2025-12-31"
    }
)

analysis_total = None
if response.status_code == 200:
    data = response.json()
    analysis_total = float(data['total_expenses'])
    print(f"\nTotal Expenses: ${analysis_total:,.2f}")
    print(f"Transaction Count: {data['transaction_count']}")

    if 'categories' in data:
        print("\n\nTop 5 Categories:")
        for cat in data['categories'][:5]:
            print(f"  {cat['category_name']}: ${float(cat['total']):,.2f} ({cat['count']} transactions)")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

print("\n" + "=" * 80)
print("TESTING EXPENSE API IN WITH_CAPITAL MODE")
print("=" * 80)

response = requests.get(
    f"{base_url}/analysis/expenses",
    params={
        "analysis_mode": "WITH_CAPITAL",
        "start_date": "2020-01-01",
        "end_date": "2025-12-31"
    }
)

with_capital_total = None
if response.status_code == 200:
    data = response.json()
    with_capital_total = float(data['total_expenses'])
    print(f"\nTotal Expenses: ${with_capital_total:,.2f}")
    print(f"Transaction Count: {data['transaction_count']}")

    if 'categories' in data:
        print("\n\nTop 5 Categories:")
        for cat in data['categories'][:5]:
            print(f"  {cat['category_name']}: ${float(cat['total']):,.2f} ({cat['count']} transactions)")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Calculate difference
print("\n" + "=" * 80)
print("COMPARISON")
print("=" * 80)
print(f"ANALYSIS mode total (operating only): ${analysis_total:,.2f}" if analysis_total else "N/A")
print(f"WITH_CAPITAL mode total: ${with_capital_total:,.2f}" if with_capital_total else "N/A")

if analysis_total and with_capital_total:
    difference = with_capital_total - analysis_total
    print(f"\nDifference (capital expenses): ${difference:,.2f}")
    print(f"\nExpected difference from database check: $6,746.66")

    if abs(difference - (-6746.66)) < 1:
        print("\n✓ MATCH! Capital expenses are being correctly excluded from ANALYSIS mode")
    else:
        print(f"\n✗ MISMATCH! Expected -$6,746.66 but got ${difference:,.2f}")
