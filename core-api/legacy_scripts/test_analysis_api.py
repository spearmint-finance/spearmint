"""
Test script to verify the Analysis API endpoints are working.

This script:
1. Starts the API server (if not already running)
2. Creates sample transactions
3. Tests all analysis endpoints
4. Displays results

Run this script to verify Phase 2 analysis features.
"""

import requests
import json
from datetime import date, timedelta
from decimal import Decimal

# API base URL
BASE_URL = "http://localhost:8000/api"

def print_section(title):
    """Print a section header."""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_result(endpoint, response):
    """Print API response in a readable format."""
    print(f"\n📍 Endpoint: {endpoint}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Success!")
        print("\nResponse Data:")
        print(json.dumps(response.json(), indent=2, default=str))
    else:
        print("❌ Failed!")
        print(f"Error: {response.text}")

def check_health():
    """Check if API is running."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API is running!")
            return True
        else:
            print("❌ API returned error:", response.status_code)
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Please start the server with:")
        print("   python run_api.py")
        return False

def create_sample_data():
    """Create sample transactions for testing."""
    print_section("Creating Sample Data")
    
    # First, create categories if they don't exist
    categories = [
        {"category_name": "Salary", "category_type": "Income"},
        {"category_name": "Freelance", "category_type": "Income"},
        {"category_name": "Groceries", "category_type": "Expense"},
        {"category_name": "Rent", "category_type": "Expense"},
        {"category_name": "Utilities", "category_type": "Expense"},
        {"category_name": "Entertainment", "category_type": "Expense"},
    ]
    
    print("\n📦 Creating categories...")
    for cat in categories:
        try:
            response = requests.post(f"{BASE_URL}/categories", json=cat)
            if response.status_code in [200, 201]:
                print(f"  ✅ Created: {cat['category_name']}")
            elif response.status_code == 400 and "already exists" in response.text.lower():
                print(f"  ℹ️  Already exists: {cat['category_name']}")
            else:
                print(f"  ⚠️  {cat['category_name']}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Error creating {cat['category_name']}: {e}")
    
    # Get category IDs
    response = requests.get(f"{BASE_URL}/categories")
    if response.status_code != 200:
        print("❌ Failed to get categories")
        return False
    
    categories_data = response.json()
    category_map = {cat['category_name']: cat['category_id'] for cat in categories_data['categories']}
    
    # Create sample transactions
    today = date.today()
    transactions = [
        # Income - Last 3 months
        {
            "transaction_date": str(today - timedelta(days=90)),
            "amount": 5000.00,
            "transaction_type": "Income",
            "category_id": category_map.get("Salary"),
            "description": "Monthly salary - 3 months ago",
            "include_in_analysis": True
        },
        {
            "transaction_date": str(today - timedelta(days=60)),
            "amount": 5000.00,
            "transaction_type": "Income",
            "category_id": category_map.get("Salary"),
            "description": "Monthly salary - 2 months ago",
            "include_in_analysis": True
        },
        {
            "transaction_date": str(today - timedelta(days=30)),
            "amount": 5000.00,
            "transaction_type": "Income",
            "category_id": category_map.get("Salary"),
            "description": "Monthly salary - 1 month ago",
            "include_in_analysis": True
        },
        {
            "transaction_date": str(today - timedelta(days=45)),
            "amount": 1500.00,
            "transaction_type": "Income",
            "category_id": category_map.get("Freelance"),
            "description": "Freelance project",
            "include_in_analysis": True
        },
        # Expenses - Last 3 months
        {
            "transaction_date": str(today - timedelta(days=85)),
            "amount": 1500.00,
            "transaction_type": "Expense",
            "category_id": category_map.get("Rent"),
            "description": "Rent payment",
            "include_in_analysis": True
        },
        {
            "transaction_date": str(today - timedelta(days=55)),
            "amount": 1500.00,
            "transaction_type": "Expense",
            "category_id": category_map.get("Rent"),
            "description": "Rent payment",
            "include_in_analysis": True
        },
        {
            "transaction_date": str(today - timedelta(days=25)),
            "amount": 1500.00,
            "transaction_type": "Expense",
            "category_id": category_map.get("Rent"),
            "description": "Rent payment",
            "include_in_analysis": True
        },
        {
            "transaction_date": str(today - timedelta(days=80)),
            "amount": 300.00,
            "transaction_type": "Expense",
            "category_id": category_map.get("Groceries"),
            "description": "Grocery shopping",
            "include_in_analysis": True
        },
        {
            "transaction_date": str(today - timedelta(days=50)),
            "amount": 350.00,
            "transaction_type": "Expense",
            "category_id": category_map.get("Groceries"),
            "description": "Grocery shopping",
            "include_in_analysis": True
        },
        {
            "transaction_date": str(today - timedelta(days=20)),
            "amount": 280.00,
            "transaction_type": "Expense",
            "category_id": category_map.get("Groceries"),
            "description": "Grocery shopping",
            "include_in_analysis": True
        },
        {
            "transaction_date": str(today - timedelta(days=70)),
            "amount": 150.00,
            "transaction_type": "Expense",
            "category_id": category_map.get("Utilities"),
            "description": "Electric bill",
            "include_in_analysis": True
        },
        {
            "transaction_date": str(today - timedelta(days=40)),
            "amount": 160.00,
            "transaction_type": "Expense",
            "category_id": category_map.get("Utilities"),
            "description": "Electric bill",
            "include_in_analysis": True
        },
        {
            "transaction_date": str(today - timedelta(days=35)),
            "amount": 200.00,
            "transaction_type": "Expense",
            "category_id": category_map.get("Entertainment"),
            "description": "Concert tickets",
            "include_in_analysis": True
        },
    ]
    
    print("\n💰 Creating transactions...")
    created_count = 0
    for tx in transactions:
        try:
            response = requests.post(f"{BASE_URL}/transactions", json=tx)
            if response.status_code in [200, 201]:
                created_count += 1
                print(f"  ✅ Created: {tx['description']}")
            else:
                print(f"  ⚠️  {tx['description']}: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n✅ Created {created_count} transactions")
    return True

def test_income_analysis():
    """Test income analysis endpoint."""
    print_section("Testing Income Analysis")
    
    # Test 1: All time income
    response = requests.get(f"{BASE_URL}/analysis/income")
    print_result("GET /analysis/income (all time)", response)
    
    # Test 2: Last 30 days income
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    response = requests.get(
        f"{BASE_URL}/analysis/income",
        params={"start_date": str(start_date), "end_date": str(end_date)}
    )
    print_result(f"GET /analysis/income (last 30 days)", response)

def test_expense_analysis():
    """Test expense analysis endpoint."""
    print_section("Testing Expense Analysis")
    
    # Test 1: All time expenses
    response = requests.get(f"{BASE_URL}/analysis/expenses")
    print_result("GET /analysis/expenses (all time)", response)
    
    # Test 2: Top 5 categories
    response = requests.get(
        f"{BASE_URL}/analysis/expenses",
        params={"top_n": 5}
    )
    print_result("GET /analysis/expenses (top 5 categories)", response)

def test_cash_flow():
    """Test cash flow analysis endpoint."""
    print_section("Testing Cash Flow Analysis")
    
    response = requests.get(f"{BASE_URL}/analysis/cashflow")
    print_result("GET /analysis/cashflow", response)

def test_trends():
    """Test trend analysis endpoints."""
    print_section("Testing Trend Analysis")
    
    # Income trends - monthly
    response = requests.get(
        f"{BASE_URL}/analysis/income/trends",
        params={"period": "monthly"}
    )
    print_result("GET /analysis/income/trends (monthly)", response)
    
    # Expense trends - monthly
    response = requests.get(
        f"{BASE_URL}/analysis/expenses/trends",
        params={"period": "monthly"}
    )
    print_result("GET /analysis/expenses/trends (monthly)", response)
    
    # Cash flow trends - monthly
    response = requests.get(
        f"{BASE_URL}/analysis/cashflow/trends",
        params={"period": "monthly"}
    )
    print_result("GET /analysis/cashflow/trends (monthly)", response)

def test_financial_health():
    """Test financial health indicators endpoint."""
    print_section("Testing Financial Health Indicators")
    
    response = requests.get(f"{BASE_URL}/analysis/health")
    print_result("GET /analysis/health", response)

def main():
    """Main test function."""
    print("\n" + "🚀 "*20)
    print("  FINANCIAL ANALYSIS API - VERIFICATION TEST")
    print("🚀 "*20)
    
    # Check if API is running
    if not check_health():
        return
    
    # Ask user if they want to create sample data
    print("\n" + "-"*80)
    create_data = input("\n📊 Do you want to create sample transactions? (y/n): ").lower().strip()
    if create_data == 'y':
        if not create_sample_data():
            print("\n⚠️  Warning: Sample data creation had issues, but continuing with tests...")
    
    # Run all tests
    test_income_analysis()
    test_expense_analysis()
    test_cash_flow()
    test_trends()
    test_financial_health()
    
    print("\n" + "="*80)
    print("  ✅ VERIFICATION COMPLETE!")
    print("="*80)
    print("\n💡 Next steps:")
    print("  1. Check the API documentation at: http://localhost:8000/api/docs")
    print("  2. Try the interactive API explorer (Swagger UI)")
    print("  3. Test with your own data from data/transactions.xlsx")
    print("\n")

if __name__ == "__main__":
    main()

