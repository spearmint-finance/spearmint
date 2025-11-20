"""
Test script to verify that credit card receipts are excluded from income
even when using WITH_CAPITAL mode.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.financial_analysis.services.analysis_service import AnalysisService, AnalysisMode
from src.financial_analysis.database.models import Transaction, TransactionClassification


def test_income_with_capital_mode():
    """Test that credit card receipts are excluded from income in WITH_CAPITAL mode."""
    
    # Connect to database
    engine = create_engine('sqlite:///financial_analysis.db')
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        print("=" * 80)
        print("Testing Income Analysis with WITH_CAPITAL Mode")
        print("=" * 80)
        
        # Get Credit Card Receipt classification
        cc_receipt = db.query(TransactionClassification).filter(
            TransactionClassification.classification_code == 'CC_RECEIPT'
        ).first()
        
        if cc_receipt:
            print(f"\n📋 Credit Card Receipt Classification (ID: {cc_receipt.classification_id})")
            print(f"   - exclude_from_income_calc: {cc_receipt.exclude_from_income_calc}")
            print(f"   - exclude_from_expense_calc: {cc_receipt.exclude_from_expense_calc}")
            print(f"   - exclude_from_cashflow_calc: {cc_receipt.exclude_from_cashflow_calc}")
        
        # Count transactions with CC_RECEIPT classification
        cc_receipt_count = db.query(Transaction).filter(
            Transaction.classification_id == cc_receipt.classification_id,
            Transaction.transaction_type == 'Income'
        ).count()
        
        print(f"\n📊 Found {cc_receipt_count} income transactions with CC_RECEIPT classification")
        
        # Run income analysis in WITH_CAPITAL mode
        service = AnalysisService(db)

        print("\n🔍 Running income analysis in WITH_CAPITAL mode...")
        result = service.analyze_income(mode=AnalysisMode.WITH_CAPITAL)
        
        print(f"\n✅ Income Analysis Results (WITH_CAPITAL mode):")
        print(f"   - Total Income: ${result.total_income:,.2f}")
        print(f"   - Transaction Count: {result.transaction_count}")
        print(f"   - Average Transaction: ${result.average_transaction:,.2f}")
        
        # Check if any CC_RECEIPT transactions are in the breakdown
        print(f"\n📋 Category Breakdown:")
        for category_name, data in result.breakdown_by_category.items():
            print(f"   - {category_name}: ${data['total']:,.2f} ({data['count']} transactions)")
        
        # Verify CC_RECEIPT transactions are excluded
        print("\n🔍 Verifying CC_RECEIPT transactions are excluded...")
        
        # Get all income transactions that should be included
        included_transactions = db.query(Transaction).filter(
            Transaction.transaction_type == 'Income',
            Transaction.include_in_analysis == True,
            Transaction.is_transfer == False
        ).outerjoin(
            TransactionClassification,
            Transaction.classification_id == TransactionClassification.classification_id
        ).filter(
            (TransactionClassification.exclude_from_income_calc == 0) |
            (TransactionClassification.exclude_from_income_calc == None)
        ).all()
        
        cc_receipt_in_results = [t for t in included_transactions if t.classification_id == cc_receipt.classification_id]
        
        if cc_receipt_in_results:
            print(f"   ❌ ERROR: Found {len(cc_receipt_in_results)} CC_RECEIPT transactions in results!")
            print(f"   These should have been excluded!")
            for t in cc_receipt_in_results[:5]:  # Show first 5
                print(f"      - Transaction {t.transaction_id}: ${t.amount} on {t.transaction_date}")
        else:
            print(f"   ✅ SUCCESS: No CC_RECEIPT transactions found in results!")
            print(f"   All {cc_receipt_count} CC_RECEIPT transactions were properly excluded.")
        
        print("\n" + "=" * 80)
        print("Test Complete")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_income_with_capital_mode()

