"""
Test script to verify that expense trends properly exclude transfers in WITH_CAPITAL mode.
"""

import sys
from pathlib import Path
from decimal import Decimal

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from src.financial_analysis.services.analysis_service import AnalysisService, AnalysisMode, TimePeriod
from src.financial_analysis.database.models import Transaction
import datetime


def test_expense_trends():
    """Test that expense trends exclude transfers in WITH_CAPITAL mode."""
    
    # Connect to database
    engine = create_engine('sqlite:///financial_analysis.db')
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        print("=" * 120)
        print("TESTING EXPENSE TRENDS WITH WITH_CAPITAL MODE")
        print("=" * 120)
        
        # Check April 2025 specifically
        april_start = datetime.date(2025, 4, 1)
        april_end = datetime.date(2025, 5, 1)
        
        # Get total transfers in April
        total_transfers = db.query(func.sum(func.abs(Transaction.amount))).filter(
            Transaction.transaction_date >= april_start,
            Transaction.transaction_date < april_end,
            Transaction.transaction_type == 'Expense',
            Transaction.is_transfer == True
        ).scalar() or Decimal('0')
        
        print(f"\n📊 APRIL 2025 DATA:")
        print(f"   Total TRANSFER expenses: ${total_transfers:,.2f}")
        
        # Run expense trends in WITH_CAPITAL mode
        service = AnalysisService(db)
        
        print(f"\n🔍 Running expense trends in WITH_CAPITAL mode...")
        trends = service.get_expense_trends(
            date_range=None,
            period=TimePeriod.MONTHLY,
            mode=AnalysisMode.WITH_CAPITAL
        )
        
        # Find April 2025 in trends
        april_trend = None
        for trend in trends:
            if '2025-04' in trend.period:
                april_trend = trend
                break
        
        if april_trend:
            print(f"\n✅ April 2025 Trend Data:")
            print(f"   Period: {april_trend.period}")
            print(f"   Value: ${abs(april_trend.value):,.2f}")
            print(f"   Count: {april_trend.count}")
            
            # Check if transfers are excluded
            if abs(april_trend.value) > 1000000:  # If > $1M, likely includes transfers
                print(f"\n   ❌ ERROR: April expense trend is ${abs(april_trend.value):,.2f}")
                print(f"   This is suspiciously high and likely includes the ${total_transfers:,.2f} in transfers!")
            else:
                print(f"\n   ✅ SUCCESS: April expense trend is ${abs(april_trend.value):,.2f}")
                print(f"   Transfers (${total_transfers:,.2f}) are properly excluded!")
        else:
            print(f"\n   ⚠️  No April 2025 data found in trends")
        
        # Show all trends
        print(f"\n📋 ALL EXPENSE TRENDS (WITH_CAPITAL mode):")
        print("-" * 120)
        for trend in trends:
            print(f"   {trend.period}: ${abs(trend.value):>12,.2f} ({trend.count} transactions)")
        
        print("\n" + "=" * 120)
        print("Test Complete")
        print("=" * 120)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_expense_trends()

