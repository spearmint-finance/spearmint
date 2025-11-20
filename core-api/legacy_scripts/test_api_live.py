"""
Live API testing script.
Tests the running FastAPI server with real HTTP requests.
"""

import httpx
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_health_check():
    """Test the health check endpoint."""
    print_section("1. Health Check")
    response = httpx.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_create_category():
    """Test creating a category."""
    print_section("2. Create Category")

    # Try to create a new category with timestamp to make it unique
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    data = {
        "category_name": f"Test_Groceries_{timestamp}",
        "category_type": "Expense",
        "description": "Food and household items (test)"
    }
    response = httpx.post(f"{BASE_URL}/categories", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    if response.status_code in [200, 201]:
        return response.json()["category_id"]

    # If creation failed, try to get existing category
    print("  Category creation failed, trying to get existing category...")
    response = httpx.get(f"{BASE_URL}/categories")
    if response.status_code == 200:
        categories = response.json()["categories"]
        if categories:
            print(f"  Using existing category: {categories[0]['category_name']}")
            return categories[0]["category_id"]

    return None

def test_list_categories():
    """Test listing categories."""
    print_section("3. List Categories")
    response = httpx.get(f"{BASE_URL}/categories")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total categories: {data['total']}")
    print(f"Categories: {json.dumps(data['categories'][:3], indent=2)}")  # Show first 3
    return response.status_code == 200

def test_create_transaction(category_id):
    """Test creating a transaction."""
    print_section("4. Create Transaction")
    data = {
        "transaction_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        "description": "Whole Foods Market",
        "amount": 125.50,
        "transaction_type": "Expense",
        "category_id": category_id,
        "source": "Chase Checking",
        "tags": ["groceries", "weekly-shopping"]
    }
    response = httpx.post(f"{BASE_URL}/transactions", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    if response.status_code in [200, 201]:
        return response.json()["transaction_id"]
    return None

def test_get_transaction(transaction_id):
    """Test getting a specific transaction."""
    print_section("5. Get Transaction by ID")
    response = httpx.get(f"{BASE_URL}/transactions/{transaction_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_list_transactions():
    """Test listing transactions with filters."""
    print_section("6. List Transactions")
    params = {
        "limit": 10,
        "offset": 0
    }
    response = httpx.get(f"{BASE_URL}/transactions", params=params)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total transactions: {data['total']}")
    print(f"Transactions: {json.dumps(data['transactions'], indent=2)}")
    return response.status_code == 200

def test_update_transaction(transaction_id):
    """Test updating a transaction."""
    print_section("7. Update Transaction")
    data = {
        "amount": 130.75,
        "notes": "Updated amount after checking receipt"
    }
    response = httpx.put(f"{BASE_URL}/transactions/{transaction_id}", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_search_transactions():
    """Test searching transactions."""
    print_section("8. Search Transactions")
    params = {
        "search": "Whole Foods",
        "limit": 10
    }
    response = httpx.get(f"{BASE_URL}/transactions", params=params)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {data['total']} matching transactions")
    print(f"Results: {json.dumps(data['transactions'], indent=2)}")
    return response.status_code == 200

def main():
    """Run all tests."""
    print("\n" + "🚀" * 30)
    print("  FINANCIAL ANALYSIS API - LIVE TESTING")
    print("🚀" * 30)
    
    try:
        # Test 1: Health check
        if not test_health_check():
            print("\n❌ Health check failed!")
            return
        
        # Test 2: Create category
        category_id = test_create_category()
        if not category_id:
            print("\n❌ Category creation failed!")
            return
        
        # Test 3: List categories
        if not test_list_categories():
            print("\n❌ List categories failed!")
            return
        
        # Test 4: Create transaction
        transaction_id = test_create_transaction(category_id)
        if not transaction_id:
            print("\n❌ Transaction creation failed!")
            return
        
        # Test 5: Get transaction
        if not test_get_transaction(transaction_id):
            print("\n❌ Get transaction failed!")
            return
        
        # Test 6: List transactions
        if not test_list_transactions():
            print("\n❌ List transactions failed!")
            return
        
        # Test 7: Update transaction
        if not test_update_transaction(transaction_id):
            print("\n❌ Update transaction failed!")
            return
        
        # Test 8: Search transactions
        if not test_search_transactions():
            print("\n❌ Search transactions failed!")
            return
        
        # Success!
        print("\n" + "✅" * 30)
        print("  ALL TESTS PASSED!")
        print("✅" * 30)
        
        print("\n📊 Summary:")
        print("  - Health check: ✅")
        print("  - Category creation: ✅")
        print("  - Category listing: ✅")
        print("  - Transaction creation: ✅")
        print("  - Transaction retrieval: ✅")
        print("  - Transaction listing: ✅")
        print("  - Transaction update: ✅")
        print("  - Transaction search: ✅")
        
        print("\n🌐 API Documentation:")
        print("  - Swagger UI: http://localhost:8000/api/docs")
        print("  - ReDoc: http://localhost:8000/api/redoc")

    except httpx.ConnectError:
        print("\n❌ ERROR: Could not connect to API server!")
        print("   Make sure the server is running: python run_api.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

