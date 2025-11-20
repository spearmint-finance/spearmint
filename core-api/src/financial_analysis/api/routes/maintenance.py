"""
API routes for system maintenance and data fix tasks.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel

from ..dependencies import get_db

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

class FixResult(BaseModel):
    task_name: str
    status: str
    details: dict
    rows_affected: int

@router.post(
    "/fix/classifications",
    response_model=FixResult,
    summary="Fix System Classifications",
    description="""
    Repair incorrect system classifications.
    - Fixes 'Insurance Reimbursement' cash flow settings
    - Removes duplicate/legacy classifications ('STANDARD', 'REIMB_RECEIVED')
    """
)
def fix_classifications(db: Session = Depends(get_db)):
    """Run the classification fix logic."""
    total_affected = 0
    details = {}

    try:
        # 1. Fix Insurance Reimbursement
        result = db.execute(text("""
            UPDATE transaction_classifications
            SET exclude_from_cashflow_calc = 0
            WHERE classification_code = 'INSURANCE_REIMBURSEMENT'
        """))
        details['insurance_reimbursement_updated'] = result.rowcount
        total_affected += result.rowcount

        # 2. Delete duplicate "Standard Transaction"
        result = db.execute(text("""
            DELETE FROM transaction_classifications
            WHERE classification_code = 'STANDARD'
        """))
        details['legacy_standard_deleted'] = result.rowcount
        total_affected += result.rowcount

        # 3. Delete old "Reimbursement Received"
        result = db.execute(text("""
            DELETE FROM transaction_classifications
            WHERE classification_code = 'REIMB_RECEIVED'
        """))
        details['legacy_reimb_received_deleted'] = result.rowcount
        total_affected += result.rowcount

        # 4. Delete old "Reimbursement Paid"
        result = db.execute(text("""
            DELETE FROM transaction_classifications
            WHERE classification_code = 'REIMB_PAID'
        """))
        details['legacy_reimb_paid_deleted'] = result.rowcount
        total_affected += result.rowcount

        db.commit()

        return FixResult(
            task_name="fix_classifications",
            status="success",
            details=details,
            rows_affected=total_affected
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/fix/transfers",
    response_model=FixResult,
    summary="Fix Transfer Links",
    description="Attempts to link orphaned transfers based on amount and date proximity."
)
def fix_transfers(db: Session = Depends(get_db)):
    """Run the transfer linking logic (placeholder for complex logic)."""
    # Logic from fix_transfers.py would go here.
    # For now, we'll just implement a basic query or placeholder
    # as the original script logic involves complex iteration.
    
    # Example placeholder implementation
    return FixResult(
        task_name="fix_transfers",
        status="not_implemented",
        details={"message": "Transfer fixing logic needs to be ported from legacy scripts"},
        rows_affected=0
    )

@router.post(
    "/fix/reimbursements",
    response_model=FixResult,
    summary="Fix Reimbursement Links",
    description="Links reimbursement expenses to income."
)
def fix_reimbursements(db: Session = Depends(get_db)):
    """Run reimbursement linking logic."""
    return FixResult(
        task_name="fix_reimbursements",
        status="not_implemented", 
        details={"message": "Reimbursement logic needs to be ported"},
        rows_affected=0
    )
