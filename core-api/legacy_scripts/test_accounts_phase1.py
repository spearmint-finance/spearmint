"""
Test script for Phase 1 of the Account Balance Tracking feature.

This script tests the database models and service layer for:
- Account management
- Balance tracking
- Investment holdings
- Reconciliations
"""

import sys
from pathlib import Path
from datetime import date, datetime
from decimal import Decimal

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from financial_analysis.database.base import Base
from financial_analysis.database.models import (
    Account, AccountBalance, InvestmentHolding, Reconciliation, Transaction
)
from financial_analysis.services.account_service import AccountService


def test_phase1():
    """Test Phase 1 implementation."""

    print("=" * 60)
    print("Testing Phase 1: Account System Backend")
    print("=" * 60)

    # Create test database
    print("\n1. Creating test database...")
    engine = create_engine('sqlite:///test_accounts.db')
    Base.metadata.create_all(engine)
    print("   + Test database created")

    # Create session
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    service = AccountService(db)

    try:
        # Test 1: Create accounts
        print("\n2. Testing Account Creation...")

        # Create a checking account
        checking = service.create_account(
            account_name="Chase Checking",
            account_type="checking",
            institution_name="Chase Bank",
            account_number_last4="1234",
            opening_balance=Decimal("5000.00"),
            opening_balance_date=date(2024, 1, 1)
        )
        print(f"   + Created: {checking.account_name} (ID: {checking.account_id})")

        # Create a brokerage account (hybrid with cash and investments)
        brokerage = service.create_account(
            account_name="Fidelity Investments",
            account_type="brokerage",
            institution_name="Fidelity",
            account_number_last4="6597",
            opening_balance=Decimal("10000.00"),
            notes="Main investment account with cash and securities"
        )
        print(f"   + Created: {brokerage.account_name} (ID: {brokerage.account_id})")
        print(f"     - Has cash: {brokerage.has_cash_component}")
        print(f"     - Has investments: {brokerage.has_investment_component}")

        # Create a credit card account
        credit_card = service.create_account(
            account_name="Chase Sapphire",
            account_type="credit_card",
            institution_name="Chase Bank",
            account_number_last4="5678"
        )
        print(f"   + Created: {credit_card.account_name} (ID: {credit_card.account_id})")

        # Test 2: Add balance snapshots
        print("\n3. Testing Balance Tracking...")

        # Add balance for checking account
        balance1 = service.add_balance_snapshot(
            account_id=checking.account_id,
            balance_date=date(2024, 10, 1),
            total_balance=Decimal("5234.67"),
            balance_type="statement"
        )
        print(f"   + Added balance: ${balance1.total_balance} on {balance1.balance_date}")

        # Add balance for brokerage with cash/investment split
        balance2 = service.add_balance_snapshot(
            account_id=brokerage.account_id,
            balance_date=date(2024, 10, 1),
            total_balance=Decimal("1245678.90"),
            cash_balance=Decimal("45678.90"),
            investment_value=Decimal("1200000.00"),
            balance_type="statement"
        )
        print(f"   + Added brokerage balance:")
        print(f"     - Total: ${balance2.total_balance}")
        print(f"     - Cash: ${balance2.cash_balance}")
        print(f"     - Investments: ${balance2.investment_value}")

        # Test 3: Add investment holdings
        print("\n4. Testing Investment Holdings...")

        # Add VOO holding
        holding1 = service.add_holding(
            account_id=brokerage.account_id,
            symbol="VOO",
            quantity=Decimal("2500"),
            as_of_date=date(2024, 10, 1),
            description="Vanguard S&P 500 ETF",
            cost_basis=Decimal("900000.00"),
            current_value=Decimal("1000000.00"),
            asset_class="etf",
            sector="broad_market"
        )
        print(f"   + Added holding: {holding1.symbol} - {holding1.quantity} shares")

        # Add VTI holding
        holding2 = service.add_holding(
            account_id=brokerage.account_id,
            symbol="VTI",
            quantity=Decimal("1000"),
            as_of_date=date(2024, 10, 1),
            description="Vanguard Total Stock Market ETF",
            cost_basis=Decimal("180000.00"),
            current_value=Decimal("200000.00"),
            asset_class="etf",
            sector="broad_market"
        )
        print(f"   + Added holding: {holding2.symbol} - {holding2.quantity} shares")

        # Test 4: Create reconciliation
        print("\n5. Testing Reconciliation...")

        reconciliation = service.create_reconciliation(
            account_id=checking.account_id,
            statement_date=date(2024, 10, 1),
            statement_balance=Decimal("5234.67"),
            notes="October statement reconciliation"
        )
        print(f"   + Created reconciliation:")
        print(f"     - Statement balance: ${reconciliation.statement_balance}")
        print(f"     - Calculated balance: ${reconciliation.calculated_balance}")
        print(f"     - Discrepancy: ${reconciliation.discrepancy_amount}")

        # Test 5: Get account summary
        print("\n6. Testing Account Summary...")

        summary = service.get_account_summary()
        for acc in summary:
            print(f"   + {acc['account_name']}:")
            print(f"     - Type: {acc['account_type']}")
            print(f"     - Balance: ${acc['current_balance']}")
            if acc.get('cash_balance') is not None:
                print(f"     - Cash: ${acc['cash_balance']}")
                print(f"     - Investments: ${acc['investment_value']}")

        # Test 6: Calculate net worth
        print("\n7. Testing Net Worth Calculation...")

        net_worth = service.get_net_worth()
        print(f"   + Total Assets: ${net_worth['assets']}")
        print(f"   + Total Liabilities: ${net_worth['liabilities']}")
        print(f"   + Net Worth: ${net_worth['net_worth']}")
        print(f"   + Liquid Assets: ${net_worth['liquid_assets']}")
        print(f"   + Investments: ${net_worth['investments']}")

        print("\n" + "=" * 60)
        print("Phase 1 Testing Complete - All Tests Passed!")
        print("=" * 60)

    except Exception as e:
        print(f"\nERROR: Test failed - {e}")
        import traceback
        traceback.print_exc()

    finally:
        db.close()


if __name__ == "__main__":
    test_phase1()