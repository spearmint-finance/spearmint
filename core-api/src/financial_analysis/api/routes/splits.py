"""Transaction Splits API routes — category-based line-item splits."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from ..dependencies import get_db
from ...database.models import Transaction, TransactionSplit
from ..schemas.split import TransactionSplitCreate, TransactionSplitResponse

router = APIRouter(prefix="/transactions", tags=["splits"])


@router.get("/{transaction_id}/splits", response_model=List[TransactionSplitResponse])
def get_transaction_splits(transaction_id: int, db: Session = Depends(get_db)):
    """Get all splits for a transaction."""
    tx = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    splits = db.query(TransactionSplit).options(
        joinedload(TransactionSplit.category),
        joinedload(TransactionSplit.entity)
    ).filter(TransactionSplit.transaction_id == transaction_id).all()
    # Attach category_name for response
    result = []
    for s in splits:
        s.category_name = s.category.category_name if s.category else None
        result.append(s)
    return result


@router.put("/{transaction_id}/splits", response_model=List[TransactionSplitResponse], status_code=200)
def set_transaction_splits(
    transaction_id: int,
    splits: List[TransactionSplitCreate],
    db: Session = Depends(get_db)
):
    """Replace all splits for a transaction. Send empty list to remove all splits."""
    tx = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Validate split amounts sum to transaction amount
    if splits:
        total = sum(abs(float(s.amount)) for s in splits)
        tx_amount = abs(float(tx.amount))
        if abs(total - tx_amount) > 0.01:
            raise HTTPException(
                status_code=400,
                detail=f"Split amounts ({total:.2f}) must sum to transaction amount ({tx_amount:.2f})"
            )

    # Replace all existing splits
    db.query(TransactionSplit).filter(
        TransactionSplit.transaction_id == transaction_id
    ).delete()

    result = []
    for s in splits:
        split = TransactionSplit(
            transaction_id=transaction_id,
            amount=s.amount,
            category_id=s.category_id,
            entity_id=s.entity_id,
            description=s.description,
            notes=s.notes,
        )
        db.add(split)
        db.flush()
        db.refresh(split)
        # Attach category_name
        from ...database.models import Category
        cat = db.query(Category).filter(Category.category_id == split.category_id).first()
        split.category_name = cat.category_name if cat else None
        result.append(split)

    db.commit()
    return result
