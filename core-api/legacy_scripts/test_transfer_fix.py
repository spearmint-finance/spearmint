"""Quick test to verify transfer filtering works."""
import sys
sys.path.insert(0, '.')

from src.financial_analysis.database.base import get_db
from src.financial_analysis.database.models import Transaction
from src.financial_analysis.services.analysis_service import AnalysisService, AnalysisMode

# Get database session
db = next(get_db())

# Count income transactions marked as transfers
income_transfers = db.query(Transaction).filter(
    Transaction.transaction_type == 'Income',
    Transaction.is_transfer == True
).count()

print(f"\nDatabase Check:")
print(f"  Income transactions marked as transfers: {income_transfers}")

# Test the analysis service
service = AnalysisService(db)

# Test in ANALYSIS mode (should exclude transfers)
result_analysis = service.analyze_income(mode=AnalysisMode.ANALYSIS)
print(f"\nAnalysis Mode (should exclude transfers):")
print(f"  Total Income: ${result_analysis.total_income}")
print(f"  Transaction Count: {result_analysis.transaction_count}")
print(f"  'Credit Card Payment' in categories: {'Credit Card Payment' in result_analysis.breakdown_by_category}")

# Test in COMPLETE mode (should include transfers)
result_complete = service.analyze_income(mode=AnalysisMode.COMPLETE)
print(f"\nComplete Mode (includes transfers):")
print(f"  Total Income: ${result_complete.total_income}")
print(f"  Transaction Count: {result_complete.transaction_count}")
print(f"  'Credit Card Payment' in categories: {'Credit Card Payment' in result_complete.breakdown_by_category}")

print(f"\nDifference: {result_complete.transaction_count - result_analysis.transaction_count} transactions excluded")

db.close()
