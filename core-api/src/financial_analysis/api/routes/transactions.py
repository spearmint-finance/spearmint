"""Transaction API endpoints."""

import asyncio
from typing import Optional, List
from datetime import date
from decimal import Decimal
from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
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


# NOTE: These static routes MUST be before /transactions/{transaction_id} to avoid route collision
@router.get("/transactions/uncategorized-descriptions")
def get_uncategorized_descriptions(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get unique uncategorized descriptions sorted by frequency."""
    from ...services.auto_categorize_service import AutoCategorizeService
    service = AutoCategorizeService(db)
    desc_map = service.get_uncategorized_descriptions()
    items = sorted(desc_map.values(), key=lambda d: d["count"], reverse=True)
    total = len(items)
    page = items[offset:offset + limit]
    return {
        "total": total,
        "total_transactions": sum(d["count"] for d in items),
        "offset": offset,
        "limit": limit,
        "descriptions": page,
    }


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

    # When filtering by entity, adjust transactions that have entity-scoped
    # splits: show only this entity's split portion amount.
    if entity_id:
        for tx in transactions:
            # Check if this transaction has splits with entity assignments
            splits = tx.splits or []
            entity_assigned_splits = [s for s in splits if s.entity_id is not None]
            if not entity_assigned_splits:
                # No entity-scoped splits — show the full transaction as-is
                continue
            # Transaction has entity-scoped splits — show only this entity's portion
            matching_splits = [s for s in splits if s.entity_id == entity_id]
            if matching_splits:
                split_total = sum(s.amount for s in matching_splits)
                tx.amount = split_total if tx.amount >= 0 else -abs(split_total)
                tx.entity_id = entity_id
                tx.split_portion = True
                # Use the first matching split's category if available
                if matching_splits[0].category_id and matching_splits[0].category:
                    tx.category_id = matching_splits[0].category_id
                    tx.category = matching_splits[0].category

    # Get total count and summary via SQL aggregation (single query, no row fetching)
    stats = service.count_and_summarize(filters)
    total = stats['total']

    # When entity-filtered, recalculate summary from adjusted transaction amounts
    # (split portions may differ from raw SQL aggregation)
    total_income = stats['total_income']
    total_expenses = stats['total_expenses']
    if entity_id:
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


# ==================== Smart Auto-Categorization ====================


class ClassifyBatchRequest(BaseModel):
    """Request to classify a specific list of descriptions."""
    descriptions: List[str] = Field(..., description="List of descriptions to classify")
    mode: str = Field(default="apply", description="'preview' or 'apply'")
    create_rules: bool = Field(default=True)


@router.post("/transactions/classify-batch")
def classify_batch(
    request: ClassifyBatchRequest,
    db: Session = Depends(get_db),
):
    """
    Classify a small batch of specific descriptions using LLM.
    Designed for interactive use — pass 10-20 descriptions at a time.
    """
    from ...services.auto_categorize_service import AutoCategorizeService
    service = AutoCategorizeService(db)
    categories = service.get_existing_categories()

    # Build description dicts from the requested descriptions
    desc_map = service.get_uncategorized_descriptions()
    batch = []
    for desc_text in request.descriptions:
        if desc_text in desc_map:
            batch.append(desc_map[desc_text])
        else:
            batch.append({"description": desc_text, "transaction_type": "Expense", "sample_amount": 0, "count": 0})

    if not batch:
        return {"results": [], "rules_created": 0, "categories_created": 0}

    try:
        classifications = asyncio.run(service.classify_batch(batch, categories))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

    # Build category lookup
    cat_name_to_id = {c["category_name"].lower(): c["category_id"] for c in categories}
    rules_created = 0
    categories_created = 0

    results = []
    for c in classifications:
        desc = c.get("description", "")
        cat_id = c.get("category_id")
        suggested_cat = c.get("suggested_category", "")
        confidence = c.get("confidence", 0.0)
        count = desc_map.get(desc, {}).get("count", 0)

        if cat_id is None and suggested_cat:
            cat_id = cat_name_to_id.get(suggested_cat.lower())

        # Apply if mode == "apply" and we have a category
        if request.mode == "apply" and cat_id and confidence >= 0.5:
            from ...database.models import Transaction as TxModel, Category as CatModel
            from sqlalchemy import or_
            nan_cat = db.query(CatModel).filter(CatModel.category_name == "nan").first()
            cat_conditions = []
            if nan_cat:
                cat_conditions.append(TxModel.category_id == nan_cat.category_id)
            cat_conditions.append(TxModel.category_id.is_(None))

            updated = db.query(TxModel).filter(
                TxModel.description == desc,
                or_(*cat_conditions),
            ).update(
                {TxModel.category_id: cat_id},
                synchronize_session="fetch",
            )

            # Create rule
            if request.create_rules and c.get("suggested_pattern"):
                from ...database.models import CategoryRule
                existing = db.query(CategoryRule).filter(
                    CategoryRule.description_pattern == c["suggested_pattern"]
                ).first()
                if not existing:
                    db.add(CategoryRule(
                        rule_name=f"Auto: {c.get('merchant_name', desc[:30])}",
                        description_pattern=c["suggested_pattern"],
                        category_id=cat_id,
                        rule_priority=5,
                        is_active=True,
                    ))
                    rules_created += 1

        results.append({
            **c,
            "category_id": cat_id,
            "transaction_count": count,
        })

    if request.mode == "apply":
        db.commit()

    return {
        "results": results,
        "rules_created": rules_created,
        "categories_created": categories_created,
    }


class ApplyCategoryAssignment(BaseModel):
    description: str
    category_id: int
    suggested_pattern: Optional[str] = None
    rule_name: Optional[str] = None


class ApplyCategoriesRequest(BaseModel):
    """Apply pre-approved category assignments without calling LLM."""
    assignments: List[ApplyCategoryAssignment]
    create_rules: bool = Field(default=True)


@router.post("/transactions/apply-categories")
def apply_categories(
    request: ApplyCategoriesRequest,
    db: Session = Depends(get_db),
):
    """
    Apply user-approved category assignments directly.
    No LLM call — just updates transactions and optionally creates rules.
    """
    from ...database.models import Transaction as TxModel, Category as CatModel, CategoryRule
    from sqlalchemy import or_

    nan_cat = db.query(CatModel).filter(CatModel.category_name == "nan").first()
    rules_created = 0
    total_updated = 0

    for a in request.assignments:
        cat_conditions = []
        if nan_cat:
            cat_conditions.append(TxModel.category_id == nan_cat.category_id)
        cat_conditions.append(TxModel.category_id.is_(None))

        updated = db.query(TxModel).filter(
            TxModel.description == a.description,
            or_(*cat_conditions),
        ).update(
            {TxModel.category_id: a.category_id},
            synchronize_session="fetch",
        )
        total_updated += updated

        if request.create_rules and a.suggested_pattern:
            existing = db.query(CategoryRule).filter(
                CategoryRule.description_pattern == a.suggested_pattern
            ).first()
            if not existing:
                db.add(CategoryRule(
                    rule_name=a.rule_name or f"Auto: {a.description[:30]}",
                    description_pattern=a.suggested_pattern,
                    category_id=a.category_id,
                    rule_priority=5,
                    is_active=True,
                ))
                rules_created += 1

    db.commit()

    return {
        "total_updated": total_updated,
        "rules_created": rules_created,
        "assignments_processed": len(request.assignments),
    }

