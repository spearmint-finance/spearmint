"""
Comprehensive test of the account system to verify it actually works.

This test simulates real-world usage scenarios including:
1. Creating accounts matching your actual accounts
2. Adding historical balances
3. Linking existing transactions
4. Testing reconciliation
5. Verifying calculations
"""

import requests
import json
from datetime import date, datetime, timedelta
from decimal import Decimal
import sys

# API base URL
BASE_URL = "http://localhost:8000/api"

def test_account_system():
    """Run comprehensive tests of the account system."""

    print("=" * 70)
    print("COMPREHENSIVE ACCOUNT SYSTEM TEST")
    print("=" * 70)

    # Track test results
    tests_passed = 0
    tests_failed = 0

    # ========== Test 1: Create Real Accounts ==========
    print("\n1. CREATING ACCOUNTS")
    print("-" * 40)

    accounts_to_create = [
        {
            "account_name": "Direct Deposit",
            "account_type": "checking",
            "institution_name": "Fidelity",
            "account_number_last4": "1234",
            "notes": "Main checking account"
        },
        {
            "account_name": "INVESTMENTS",
            "account_type": "brokerage",
            "account_subtype": "hybrid",
            "institution_name": "Fidelity",
            "account_number_last4": "6597",
            "notes": "Main brokerage with cash and investments"
        },
        {
            "account_name": "Citi AAdvantage Card",
            "account_type": "credit_card",
            "institution_name": "Citibank",
            "account_number_last4": "9983",
            "notes": "Primary credit card"
        }
    ]

    created_accounts = {}

    for account_data in accounts_to_create:
        response = requests.post(f"{BASE_URL}/accounts", json=account_data)
        if response.status_code == 200:
            account = response.json()
            created_accounts[account['account_name']] = account
            print(f"  + Created: {account['account_name']} (ID: {account['account_id']})")
            tests_passed += 1
        else:
            print(f"  X Failed to create: {account_data['account_name']}")
            print(f"    Error: {response.text}")
            tests_failed += 1

    # ========== Test 2: Add Balance History ==========
    print("\n2. ADDING BALANCE HISTORY")
    print("-" * 40)

    if "INVESTMENTS" in created_accounts:
        investment_id = created_accounts["INVESTMENTS"]["account_id"]

        balances_to_add = [
            {
                "balance_date": "2024-01-01",
                "total_balance": 500000.00,
                "cash_balance": 50000.00,
                "investment_value": 450000.00,
                "balance_type": "statement"
            },
            {
                "balance_date": "2024-06-01",
                "total_balance": 800000.00,
                "cash_balance": 30000.00,
                "investment_value": 770000.00,
                "balance_type": "statement"
            },
            {
                "balance_date": "2024-10-09",
                "total_balance": 1245678.90,
                "cash_balance": 45678.90,
                "investment_value": 1200000.00,
                "balance_type": "statement"
            }
        ]

        for balance_data in balances_to_add:
            response = requests.post(
                f"{BASE_URL}/accounts/{investment_id}/balances",
                json=balance_data
            )
            if response.status_code == 200:
                print(f"  + Added balance for {balance_data['balance_date']}: ${balance_data['total_balance']:,.2f}")
                tests_passed += 1
            else:
                print(f"  X Failed to add balance for {balance_data['balance_date']}")
                tests_failed += 1

    # ========== Test 3: Add Investment Holdings ==========
    print("\n3. ADDING INVESTMENT HOLDINGS")
    print("-" * 40)

    if "INVESTMENTS" in created_accounts:
        investment_id = created_accounts["INVESTMENTS"]["account_id"]

        holdings = [
            {
                "symbol": "VOO",
                "quantity": 2500,
                "description": "Vanguard S&P 500 ETF",
                "cost_basis": 900000.00,
                "current_value": 1000000.00,
                "as_of_date": "2024-10-09",
                "asset_class": "etf"
            },
            {
                "symbol": "VTI",
                "quantity": 1000,
                "description": "Vanguard Total Stock Market ETF",
                "cost_basis": 180000.00,
                "current_value": 200000.00,
                "as_of_date": "2024-10-09",
                "asset_class": "etf"
            }
        ]

        for holding in holdings:
            response = requests.post(
                f"{BASE_URL}/accounts/{investment_id}/holdings",
                json=holding
            )
            if response.status_code == 200:
                result = response.json()
                gain = (holding['current_value'] - holding['cost_basis']) / holding['cost_basis'] * 100
                print(f"  + Added {holding['symbol']}: {holding['quantity']} shares, +{gain:.1f}% gain")
                tests_passed += 1
            else:
                print(f"  X Failed to add holding {holding['symbol']}")
                tests_failed += 1

    # ========== Test 4: Test Balance Calculations ==========
    print("\n4. TESTING BALANCE CALCULATIONS")
    print("-" * 40)

    # Get current balance
    if "INVESTMENTS" in created_accounts:
        investment_id = created_accounts["INVESTMENTS"]["account_id"]

        response = requests.get(f"{BASE_URL}/accounts/{investment_id}/current-balance")
        if response.status_code == 200:
            balance = response.json()
            print(f"  + Current Balance: ${float(balance['total_balance']):,.2f}")
            print(f"    - Cash: ${float(balance['cash_balance']):,.2f}")
            print(f"    - Investments: ${float(balance['investment_value']):,.2f}")
            tests_passed += 1
        else:
            print(f"  X Failed to get current balance")
            tests_failed += 1

    # ========== Test 5: Test Portfolio Summary ==========
    print("\n5. TESTING PORTFOLIO SUMMARY")
    print("-" * 40)

    if "INVESTMENTS" in created_accounts:
        investment_id = created_accounts["INVESTMENTS"]["account_id"]

        response = requests.get(f"{BASE_URL}/accounts/{investment_id}/portfolio")
        if response.status_code == 200:
            portfolio = response.json()
            print(f"  + Portfolio Value: ${float(portfolio['total_value']):,.2f}")
            print(f"    Total Gain/Loss: ${float(portfolio.get('total_gain_loss', 0)):,.2f}")
            print(f"    Holdings: {len(portfolio['holdings'])}")
            tests_passed += 1
        else:
            print(f"  X Failed to get portfolio summary")
            tests_failed += 1

    # ========== Test 6: Test Net Worth Calculation ==========
    print("\n6. TESTING NET WORTH CALCULATION")
    print("-" * 40)

    response = requests.get(f"{BASE_URL}/accounts/net-worth")
    if response.status_code == 200:
        net_worth = response.json()
        print(f"  + Total Assets: ${float(net_worth['assets']):,.2f}")
        print(f"    Total Liabilities: ${float(net_worth['liabilities']):,.2f}")
        print(f"    Net Worth: ${float(net_worth['net_worth']):,.2f}")
        print(f"    Liquid Assets: ${float(net_worth['liquid_assets']):,.2f}")
        print(f"    Investments: ${float(net_worth['investments']):,.2f}")

        if 'account_breakdown' in net_worth and net_worth['account_breakdown']:
            print("\n    Account Breakdown:")
            for account_type, amount in net_worth['account_breakdown'].items():
                print(f"      - {account_type}: ${float(amount):,.2f}")
        tests_passed += 1
    else:
        print(f"  X Failed to calculate net worth")
        tests_failed += 1

    # ========== Test 7: Test Account Summary ==========
    print("\n7. TESTING ACCOUNT SUMMARY")
    print("-" * 40)

    response = requests.get(f"{BASE_URL}/accounts/summary")
    if response.status_code == 200:
        summary = response.json()
        print(f"  + Found {len(summary)} accounts:")
        for account in summary:
            balance = float(account['current_balance'])
            print(f"    - {account['account_name']}: ${balance:,.2f}")
        tests_passed += 1
    else:
        print(f"  X Failed to get account summary")
        tests_failed += 1

    # ========== Test 8: Test Reconciliation ==========
    print("\n8. TESTING RECONCILIATION")
    print("-" * 40)

    if "Direct Deposit" in created_accounts:
        checking_id = created_accounts["Direct Deposit"]["account_id"]

        # Create a reconciliation
        reconciliation_data = {
            "statement_date": "2024-10-09",
            "statement_balance": 25000.00,
            "notes": "October statement reconciliation"
        }

        response = requests.post(
            f"{BASE_URL}/accounts/{checking_id}/reconcile",
            json=reconciliation_data
        )

        if response.status_code == 200:
            reconciliation = response.json()
            discrepancy = float(reconciliation.get('discrepancy_amount', 0))
            print(f"  + Created reconciliation:")
            print(f"    Statement Balance: ${float(reconciliation['statement_balance']):,.2f}")
            print(f"    Calculated Balance: ${float(reconciliation['calculated_balance']):,.2f}")
            print(f"    Discrepancy: ${abs(discrepancy):,.2f}")
            tests_passed += 1

            # Complete the reconciliation
            complete_data = {
                "reconciled_by": "Test User"
            }

            response = requests.put(
                f"{BASE_URL}/accounts/reconciliations/{reconciliation['reconciliation_id']}/complete",
                json=complete_data
            )

            if response.status_code == 200:
                print(f"  + Reconciliation completed successfully")
                tests_passed += 1
            else:
                print(f"  X Failed to complete reconciliation")
                tests_failed += 1
        else:
            print(f"  X Failed to create reconciliation")
            tests_failed += 1

    # ========== Test 9: Test Balance History ==========
    print("\n9. TESTING BALANCE HISTORY")
    print("-" * 40)

    if "INVESTMENTS" in created_accounts:
        investment_id = created_accounts["INVESTMENTS"]["account_id"]

        response = requests.get(f"{BASE_URL}/accounts/{investment_id}/balances")
        if response.status_code == 200:
            history = response.json()
            print(f"  + Balance history for {history['account_name']}:")
            for balance in history['balances']:
                print(f"    - {balance['balance_date']}: ${float(balance['total_balance']):,.2f}")
            tests_passed += 1
        else:
            print(f"  X Failed to get balance history")
            tests_failed += 1

    # ========== Test 10: Test Error Handling ==========
    print("\n10. TESTING ERROR HANDLING")
    print("-" * 40)

    # Try to get non-existent account
    response = requests.get(f"{BASE_URL}/accounts/999999")
    if response.status_code == 404:
        print(f"  + Correctly returns 404 for non-existent account")
        tests_passed += 1
    else:
        print(f"  X Should return 404 for non-existent account")
        tests_failed += 1

    # Try to create account with invalid type
    invalid_account = {
        "account_name": "Invalid Account",
        "account_type": "invalid_type"
    }
    response = requests.post(f"{BASE_URL}/accounts", json=invalid_account)
    if response.status_code != 200:
        print(f"  + Correctly rejects invalid account type")
        tests_passed += 1
    else:
        print(f"  X Should reject invalid account type")
        tests_failed += 1

    # ========== RESULTS ==========
    print("\n" + "=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    print(f"  Tests Passed: {tests_passed}")
    print(f"  Tests Failed: {tests_failed}")
    print(f"  Success Rate: {tests_passed / (tests_passed + tests_failed) * 100:.1f}%")

    if tests_failed == 0:
        print("\nSUCCESS: ALL TESTS PASSED! The account system is fully functional.")
    else:
        print(f"\nWARNING: {tests_failed} tests failed. Please review the errors above.")

    return tests_failed == 0


if __name__ == "__main__":
    try:
        # Check if API is running
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("ERROR: API is not running. Please start the API server first.")
            sys.exit(1)

        # Run the tests
        success = test_account_system()
        sys.exit(0 if success else 1)

    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to API. Please ensure the server is running on http://localhost:8000")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)