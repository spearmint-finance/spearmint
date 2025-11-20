"""
Fix transfer transactions in the database.

This script:
1. Finds transactions with "Transfer" in the description
2. Sets is_transfer=True
3. Sets classification_id=2 (Transfer classification)
4. Sets include_in_analysis=False
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from financial_analysis.database.base import SessionLocal
from financial_analysis.database.models import Transaction, TransactionClassification

def fix_transfer_transactions():
    """Fix transfer transactions in the database."""
    db = SessionLocal()
    
    try:
        # Get Transfer classification
        transfer_classification = db.query(TransactionClassification).filter(
            TransactionClassification.classification_code == "TRANSFER"
        ).first()
        
        if not transfer_classification:
            print("❌ Transfer classification not found!")
            print("Creating Transfer classification...")
            transfer_classification = TransactionClassification(
                classification_name="Transfer",
                classification_code="TRANSFER",
                description="Transfer between accounts",
                is_system_classification=True,
                exclude_from_income_calc=True,
                exclude_from_expense_calc=True,
                exclude_from_cashflow_calc=True
            )
            db.add(transfer_classification)
            db.commit()
            db.refresh(transfer_classification)
            print(f"✅ Created Transfer classification (ID: {transfer_classification.classification_id})")
        
        # Find all transactions with "Transfer" in description
        transfer_transactions = db.query(Transaction).filter(
            Transaction.description.like("%Transfer%")
        ).all()
        
        print(f"\n📊 Found {len(transfer_transactions)} transfer transactions:")
        print("-" * 80)
        
        for tx in transfer_transactions:
            print(f"\nID: {tx.transaction_id}")
            print(f"  Description: {tx.description}")
            print(f"  Type: {tx.transaction_type}")
            print(f"  Amount: ${tx.amount}")
            print(f"  is_transfer (before): {tx.is_transfer}")
            print(f"  classification_id (before): {tx.classification_id}")
            print(f"  include_in_analysis (before): {tx.include_in_analysis}")
            
            # Update the transaction
            tx.is_transfer = True
            tx.classification_id = transfer_classification.classification_id
            tx.include_in_analysis = False
            
            # Set transfer account info if description contains clues
            if "from" in tx.description.lower():
                parts = tx.description.lower().split("from")
                if len(parts) > 1:
                    tx.transfer_account_from = parts[1].strip().title()
            if "to" in tx.description.lower():
                parts = tx.description.lower().split("to")
                if len(parts) > 1:
                    tx.transfer_account_to = parts[1].strip().title()
            
            print(f"  is_transfer (after): {tx.is_transfer}")
            print(f"  classification_id (after): {tx.classification_id}")
            print(f"  include_in_analysis (after): {tx.include_in_analysis}")
            print(f"  transfer_account_from: {tx.transfer_account_from}")
            print(f"  transfer_account_to: {tx.transfer_account_to}")
        
        # Commit changes
        db.commit()
        
        print("\n" + "=" * 80)
        print(f"✅ Successfully updated {len(transfer_transactions)} transfer transactions!")
        print("=" * 80)
        
        # Verify the changes
        print("\n🔍 Verification:")
        transfers = db.query(Transaction).filter(
            Transaction.is_transfer == True
        ).all()
        print(f"Total transfers in database: {len(transfers)}")
        
        for tx in transfers:
            print(f"  - {tx.description}: Type={tx.transaction_type}, Amount=${tx.amount}")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Fixing Transfer Transactions")
    print("=" * 80)
    fix_transfer_transactions()

