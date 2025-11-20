"""
Fix Credit Card Payment and Receipt classifications to exclude from all calculations.

This script updates the Credit Card Payment and Credit Card Receipt classifications
to exclude from income, expense, AND cashflow calculations to prevent double-counting.

Background:
- Credit card payments are transfers between accounts, not actual expenses
- The actual expenses were already recorded when the credit card purchases were made
- Including these in calculations causes double-counting
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.financial_analysis.database.models import TransactionClassification
from src.financial_analysis.database.base import Base


def fix_credit_card_classifications():
    """Update credit card classifications to exclude from all calculations."""
    
    # Connect to database
    engine = create_engine('sqlite:///financial_analysis.db')
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        print("=" * 80)
        print("Fixing Credit Card Classifications")
        print("=" * 80)
        
        # Get Credit Card Payment classification
        cc_payment = db.query(TransactionClassification).filter(
            TransactionClassification.classification_code == 'CC_PAYMENT'
        ).first()
        
        if cc_payment:
            print(f"\n📋 Credit Card Payment (ID: {cc_payment.classification_id})")
            print(f"   Current settings:")
            print(f"   - exclude_from_income_calc: {cc_payment.exclude_from_income_calc}")
            print(f"   - exclude_from_expense_calc: {cc_payment.exclude_from_expense_calc}")
            print(f"   - exclude_from_cashflow_calc: {cc_payment.exclude_from_cashflow_calc}")
            
            # Update to exclude from all calculations
            cc_payment.exclude_from_income_calc = True
            cc_payment.exclude_from_expense_calc = True
            cc_payment.exclude_from_cashflow_calc = True
            cc_payment.description = "Payment to credit card (excluded from all calculations to prevent double-counting)"
            
            print(f"\n   ✅ Updated to:")
            print(f"   - exclude_from_income_calc: True")
            print(f"   - exclude_from_expense_calc: True")
            print(f"   - exclude_from_cashflow_calc: True")
        else:
            print("\n⚠️  Credit Card Payment classification not found!")
        
        # Get Credit Card Receipt classification
        cc_receipt = db.query(TransactionClassification).filter(
            TransactionClassification.classification_code == 'CC_RECEIPT'
        ).first()
        
        if cc_receipt:
            print(f"\n📋 Credit Card Receipt (ID: {cc_receipt.classification_id})")
            print(f"   Current settings:")
            print(f"   - exclude_from_income_calc: {cc_receipt.exclude_from_income_calc}")
            print(f"   - exclude_from_expense_calc: {cc_receipt.exclude_from_expense_calc}")
            print(f"   - exclude_from_cashflow_calc: {cc_receipt.exclude_from_cashflow_calc}")
            
            # Update to exclude from all calculations
            cc_receipt.exclude_from_income_calc = True
            cc_receipt.exclude_from_expense_calc = True
            cc_receipt.exclude_from_cashflow_calc = True
            cc_receipt.description = "Credit card company receiving payment (excluded from all calculations to prevent double-counting)"
            
            print(f"\n   ✅ Updated to:")
            print(f"   - exclude_from_income_calc: True")
            print(f"   - exclude_from_expense_calc: True")
            print(f"   - exclude_from_cashflow_calc: True")
        else:
            print("\n⚠️  Credit Card Receipt classification not found!")
        
        # Commit changes
        db.commit()
        
        print("\n" + "=" * 80)
        print("✅ Credit card classifications updated successfully!")
        print("=" * 80)
        
        print("\n📊 Impact:")
        print("   - Credit card payments will now be excluded from all financial calculations")
        print("   - This prevents double-counting of expenses")
        print("   - The actual expenses are counted when credit card purchases are made")
        print("   - Paying the credit card bill is just a transfer between accounts")
        
        print("\n💡 Next Steps:")
        print("   1. Refresh the Classifications page in the UI to see the changes")
        print("   2. Re-run any financial analysis to get accurate calculations")
        print("   3. Consider re-applying classification rules if needed")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    fix_credit_card_classifications()

