"""
Investigate the large expense spike in April 2025.
"""

import sys
from pathlib import Path
from decimal import Decimal

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from src.financial_analysis.database.models import Transaction, TransactionClassification, Category
import datetime


def investigate_april_expenses():
    """Investigate April 2025 expense transactions."""
    
    # Connect to database
    engine = create_engine('sqlite:///financial_analysis.db')
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        print("=" * 120)
        print("INVESTIGATING APRIL 2025 EXPENSE SPIKE")
        print("=" * 120)
        
        # Get all April 2025 expense transactions
        april_start = datetime.date(2025, 4, 1)
        april_end = datetime.date(2025, 5, 1)
        
        # Total expenses
        total_all = db.query(func.sum(func.abs(Transaction.amount))).filter(
            Transaction.transaction_date >= april_start,
            Transaction.transaction_date < april_end,
            Transaction.transaction_type == 'Expense'
        ).scalar() or Decimal('0')
        
        # Transfer expenses
        total_transfers = db.query(func.sum(func.abs(Transaction.amount))).filter(
            Transaction.transaction_date >= april_start,
            Transaction.transaction_date < april_end,
            Transaction.transaction_type == 'Expense',
            Transaction.is_transfer == True
        ).scalar() or Decimal('0')
        
        # Non-transfer expenses
        total_non_transfers = total_all - total_transfers
        
        print(f"\n📊 APRIL 2025 EXPENSE SUMMARY:")
        print(f"   Total ALL expenses:          ${total_all:>15,.2f}")
        print(f"   Total TRANSFER expenses:     ${total_transfers:>15,.2f}")
        print(f"   Total NON-TRANSFER expenses: ${total_non_transfers:>15,.2f}")
        
        # Get top 10 largest transactions
        print(f"\n📋 TOP 10 LARGEST EXPENSE TRANSACTIONS:")
        print("-" * 120)
        
        april_txns = db.query(Transaction).filter(
            Transaction.transaction_date >= april_start,
            Transaction.transaction_date < april_end,
            Transaction.transaction_type == 'Expense'
        ).order_by(Transaction.amount.desc()).limit(10).all()
        
        for t in april_txns:
            classification = db.query(TransactionClassification).filter(
                TransactionClassification.classification_id == t.classification_id
            ).first()
            
            category = db.query(Category).filter(
                Category.category_id == t.category_id
            ).first()
            
            class_name = classification.classification_name if classification else "None"
            cat_name = category.category_name if category else "None"
            
            print(f"ID: {t.transaction_id:5d} | {t.transaction_date} | ${abs(t.amount):>12,.2f} | "
                  f"Transfer: {str(t.is_transfer):5s} | {class_name:30s} | {cat_name}")
        
        # Count transactions by classification
        print(f"\n📊 TRANSACTIONS BY CLASSIFICATION:")
        print("-" * 120)
        
        classification_summary = db.query(
            TransactionClassification.classification_name,
            func.count(Transaction.transaction_id).label('count'),
            func.sum(func.abs(Transaction.amount)).label('total')
        ).outerjoin(
            Transaction,
            Transaction.classification_id == TransactionClassification.classification_id
        ).filter(
            Transaction.transaction_date >= april_start,
            Transaction.transaction_date < april_end,
            Transaction.transaction_type == 'Expense'
        ).group_by(
            TransactionClassification.classification_name
        ).order_by(
            func.sum(func.abs(Transaction.amount)).desc()
        ).all()
        
        for row in classification_summary:
            print(f"{row.classification_name:40s} | Count: {row.count:4d} | Total: ${row.total:>15,.2f}")
        
        # Check if transfers are being excluded in WITH_CAPITAL mode
        print(f"\n🔍 CHECKING EXPENSE ANALYSIS FILTERING:")
        print("-" * 120)
        
        # Simulate WITH_CAPITAL mode query
        from src.financial_analysis.services.analysis_service import AnalysisService, AnalysisMode
        
        service = AnalysisService(db)
        result = service.analyze_expenses(
            date_range=None,
            mode=AnalysisMode.WITH_CAPITAL
        )
        
        print(f"WITH_CAPITAL mode expense analysis:")
        print(f"   Total Expenses: ${result.total_expenses:,.2f}")
        print(f"   Transaction Count: {result.transaction_count}")
        
        # Now check what SHOULD be included
        should_be_included = db.query(func.sum(func.abs(Transaction.amount))).filter(
            Transaction.transaction_type == 'Expense',
            Transaction.include_in_analysis == True,
            Transaction.is_transfer == False
        ).outerjoin(
            TransactionClassification,
            Transaction.classification_id == TransactionClassification.classification_id
        ).filter(
            (TransactionClassification.exclude_from_expense_calc == 0) |
            (TransactionClassification.exclude_from_expense_calc == None)
        ).scalar() or Decimal('0')
        
        print(f"\n   Expected (transfers excluded): ${should_be_included:,.2f}")
        
        if abs(result.total_expenses - should_be_included) > Decimal('0.01'):
            print(f"   ❌ MISMATCH! Difference: ${abs(result.total_expenses - should_be_included):,.2f}")
        else:
            print(f"   ✅ MATCH! Transfers are being properly excluded.")
        
        print("\n" + "=" * 120)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    investigate_april_expenses()

