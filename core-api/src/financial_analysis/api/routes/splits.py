"""Transaction Splits API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..dependencies import get_db
from ...database.models import Transaction, TransactionSplit, Person
from ..schemas.split import TransactionSplitCreate, TransactionSplitRead

router = APIRouter(prefix="/transactions", tags=["splits"])


@router.get("/{transaction_id}/splits", response_model=List[TransactionSplitRead])
def get_transaction_splits(transaction_id: int, db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db.query(TransactionSplit).filter(TransactionSplit.transaction_id == transaction_id).all()


@router.post("/{transaction_id}/splits", response_model=TransactionSplitRead, status_code=status.HTTP_201_CREATED)
def create_transaction_split(transaction_id: int, payload: TransactionSplitCreate, db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    person = db.query(Person).filter(Person.person_id == payload.person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    # Enforce single split per person per transaction
    existing = db.query(TransactionSplit).filter(
        TransactionSplit.transaction_id == transaction_id,
        TransactionSplit.person_id == payload.person_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Split for this person already exists for the transaction")

    split = TransactionSplit(
        transaction_id=transaction_id,
        person_id=payload.person_id,
        amount=payload.amount,
    )
    db.add(split)
    db.commit()
    db.refresh(split)
    return split

