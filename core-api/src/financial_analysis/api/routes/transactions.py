"""Transaction API endpoints."""

from typing import Optional, List
from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionListResponse
)
from ..schemas.split import TransactionSplitCreate, TransactionSplitResponse
from ..schemas.common import SuccessResponse, PaginationParams
from ...services.transaction_service import TransactionService, TransactionFilter
from ...utils.validators import ValidationError

router = APIRouter()


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new transaction.
    
    Args:
        transaction: Transaction data
        db: Database session
        
    Returns:
        TransactionResponse: Created transaction
    """
    service = TransactionService(db)
    
    try:
        created = service.create_transaction(
            transaction_date=transaction.transaction_date,
            amount=transaction.amount,
            transaction_type=transaction.transaction_type,
            category_id=transaction.category_id,
            source=transaction.source,
            description=transaction.description,
            payment_method=transaction.payment_method,
            include_in_analysis=transaction.include_in_analysis,
            transfer_account_from=transaction.transfer_account_from,
            transfer_account_to=transaction.transfer_account_to,
            notes=transaction.notes,
            tag_names=transaction.tag_names,
            account_id=transaction.account_id,
            entity_id=transaction.entity_id,
            is_capital_expense=transaction.is_capital_expense or False,
            is_tax_deductible=transaction.is_tax_deductible or False,
            is_recurring=transaction.is_recurring or False,
            is_reimbursable=transaction.is_reimbursable or False,
            exclude_from_income=transaction.exclude_from_income or False,
            exclude_from_expenses=transaction.exclude_from_expenses or False,
            splits=transaction.splits,
        )
        return created
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create transaction: {str(e)}")


@router.put("/transactions/bulk-update")
def bulk_update_transactions(
    updates: dict,
    db: Session = Depends(get_db)
):
    """
    Bulk update transactions. Accepts a list of transaction IDs and fields to update.

    Body: { "transaction_ids": [1, 2, 3], "updates": { "entity_id": 1 } }
    """
    service = TransactionService(db)
    transaction_ids = updates.get("transaction_ids", [])
    field_updates = updates.get("updates", {})

    if not transaction_ids:
        raise HTTPException(status_code=400, detail="transaction_ids is required")
    if not field_updates:
        raise HTTPException(status_code=400, detail="updates is required")

    updated_count = 0
    failed = []
    for tid in transaction_ids:
        try:
            result = service.update_transaction(tid, **field_updates)
            if result:
                updated_count += 1
            else:
                failed.append({"id": tid, "error": "Transaction not found"})
        except Exception as e:
            failed.append({"id": tid, "error": str(e)})

    return {"updated": updated_count, "total": len(transaction_ids), "failed": failed}


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    """
    Get transaction by ID.
    
    Args:
        transaction_id: Transaction ID
        db: Database session
        
    Returns:
        TransactionResponse: Transaction data
    """
    service = TransactionService(db)
    transaction = service.get_transaction(transaction_id)

    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction {transaction_id} not found")

    # Compute is_transfer from category for backward-compat response field
    if hasattr(transaction, 'category') and transaction.category:
        transaction.is_transfer = transaction.category.category_type == 'Transfer'
    else:
        transaction.is_transfer = False

    return transaction


@router.get("/transactions", response_model=TransactionListResponse)
def list_transactions(
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    transaction_type: Optional[str] = Query(None, pattern="^(Income|Expense)$", description="Filter by transaction type: 'Income' or 'Expense'"),
    category_id: Optional[int] = Query(None, gt=0, description="Filter by category ID"),
    include_in_analysis: Optional[bool] = Query(None, description="Filter to include/exclude transactions marked for analysis"),
    is_transfer: Optional[bool] = Query(None, description="Filter by transfer status (derived from category type): true for transfers only, false to exclude transfers"),
    min_amount: Optional[Decimal] = Query(None, gt=0, description="Minimum amount filter"),
    max_amount: Optional[Decimal] = Query(None, gt=0, description="Maximum amount filter"),
    search_text: Optional[str] = Query(None, description="Search in description, source, notes"),
    account_id: Optional[int] = Query(None, gt=0, description="Filter by account ID"),
    tag_ids: Optional[List[int]] = Query(None, description="Filter by tag IDs (transactions matching any of the given tags)"),
    entity_id: Optional[int] = Query(None, gt=0, description="Filter by entity ID (via account)"),
    include_capital_expenses: bool = Query(True, description="Include non-operating expenses (capital, refunds, reimbursements, etc.) in results"),
    include_transfers: bool = Query(True, description="Include transfers in results"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    sort_by: str = Query("transaction_date", description="Field to sort by"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """
    List transactions with optional filters.

    Args:
        Various filter parameters
        db: Database session

    Returns:
        TransactionListResponse: List of transactions
    """
    service = TransactionService(db)

    # Resolve transfer filtering precedence:
    # - If include_transfers is False, exclude transfers by default (is_transfer=False)
    # - Otherwise honor the explicit is_transfer filter (if provided)
    resolved_is_transfer = (is_transfer if include_transfers else False)

    filters = TransactionFilter(
        start_date=start_date,
        end_date=end_date,
        transaction_type=transaction_type,
        category_id=category_id,
        include_in_analysis=include_in_analysis,
        is_transfer=resolved_is_transfer,
        min_amount=min_amount,
        max_amount=max_amount,
        search_text=search_text,
        account_id=account_id,
        tag_ids=tag_ids,
        entity_id=entity_id,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order
    )

    transactions = service.list_transactions(filters)

    # Compute is_transfer from category for backward-compat response field
    for tx in transactions:
        if hasattr(tx, 'category') and tx.category:
            tx.is_transfer = tx.category.category_type == 'Transfer'
        else:
            tx.is_transfer = False

    # When filtering by entity, adjust transactions that were included via
    # split entity match: show the split's amount/entity/category instead of
    # the parent transaction's values.
    summary_adjustment = Decimal('0')  # track amount adjustments for summary
    if entity_id:
        for tx in transactions:
            # Skip if the transaction itself belongs to this entity
            if tx.entity_id == entity_id:
                continue
            # Check if inherited from account
            if tx.entity_id is None and tx.account_id:
                from sqlalchemy import exists as sa_exists
                from ..dependencies import get_db as _  # already have db
                from ...database.models import account_entities
                inherited = db.query(
                    sa_exists().where(
                        (account_entities.c.account_id == tx.account_id) &
                        (account_entities.c.entity_id == entity_id)
                    )
                ).scalar()
                if inherited:
                    continue
            # This transaction was included via split match — find the matching splits
            matching_splits = [s for s in (tx.splits or []) if s.entity_id == entity_id]
            if matching_splits:
                original_amount = tx.amount
                split_total = sum(s.amount for s in matching_splits)
                # Override display values with split portion
                tx.amount = split_total if tx.amount >= 0 else -abs(split_total)
                tx.entity_id = entity_id
                # Use the first matching split's category if available
                if matching_splits[0].category_id:
                    tx.category_id = matching_splits[0].category_id
                    # Update category relationship for display
                    if matching_splits[0].category:
                        tx.category = matching_splits[0].category
                # Track the difference for summary adjustment
                summary_adjustment += tx.amount - original_amount

    # Get total count and summary via SQL aggregation (single query, no row fetching)
    stats = service.count_and_summarize(filters)
    total = stats['total']

    # Adjust summary stats to reflect split-based amounts
    total_income = stats['total_income']
    total_expenses = stats['total_expenses']
    if entity_id and summary_adjustment != 0:
        # Recalculate from the adjusted transactions for accuracy
        total_income = sum(
            tx.amount for tx in transactions if tx.transaction_type == 'Income'
        )
        total_expenses = sum(
            abs(tx.amount) for tx in transactions if tx.transaction_type == 'Expense'
        )

    summary = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_income": total_income - total_expenses,
        "transaction_count": total
    }

    return TransactionListResponse(
        transactions=transactions,
        total=total,
        limit=limit,
        offset=offset,
        summary=summary
    )


@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update transaction.
    
    Args:
        transaction_id: Transaction ID
        transaction: Updated transaction data
        db: Database session
        
    Returns:
        TransactionResponse: Updated transaction
    """
    service = TransactionService(db)
    
    try:
        # Convert to dict and remove None values
        updates = transaction.model_dump(exclude_unset=True)

        updated = service.update_transaction(transaction_id, **updates)

        if not updated:
            raise HTTPException(status_code=404, detail=f"Transaction {transaction_id} not found")

        return updated
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update transaction: {str(e)}")


@router.put("/transactions/{transaction_id}/splits", response_model=TransactionResponse)
def set_transaction_splits(
    transaction_id: int,
    splits: List[TransactionSplitCreate],
    db: Session = Depends(get_db)
):
    """
    Replace all splits for a transaction.

    Passing an empty list removes all splits.

    Args:
        transaction_id: Transaction ID
        splits: New splits to set
        db: Database session

    Returns:
        TransactionResponse: Updated transaction with new splits
    """
    service = TransactionService(db)

    try:
        updated = service.update_transaction(transaction_id, splits=splits)

        if not updated:
            raise HTTPException(status_code=404, detail=f"Transaction {transaction_id} not found")

        return updated
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set splits: {str(e)}")


@router.delete("/transactions/{transaction_id}", response_model=SuccessResponse)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete transaction.
    
    Args:
        transaction_id: Transaction ID
        db: Database session
        
    Returns:
        SuccessResponse: Success message
    """
    service = TransactionService(db)
    
    deleted = service.delete_transaction(transaction_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Transaction {transaction_id} not found")
    
    return SuccessResponse(message=f"Transaction {transaction_id} deleted successfully")

