"""
Budget management API routes.

Provides CRUD operations for budgets and a summary endpoint
that calculates actual spending vs. budgeted amounts.
"""

from datetime import date
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from ...database.base import get_db
from ...database.models import Budget, Category, Transaction, Entity

router = APIRouter()


# =============================================================================
# Pydantic Schemas
# =============================================================================

class BudgetCreate(BaseModel):
    category_id: int
    budget_amount: float = Field(gt=0)
    period_type: str = "Monthly"
    start_date: str  # YYYY-MM-DD
    end_date: Optional[str] = None
    entity_id: Optional[int] = None
    notes: Optional[str] = None


class BudgetUpdate(BaseModel):
    budget_amount: Optional[float] = Field(None, gt=0)
    period_type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    entity_id: Optional[int] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class BudgetResponse(BaseModel):
    budget_id: int
    category_id: int
    category_name: Optional[str] = None
    budget_amount: float
    period_type: str
    start_date: str
    end_date: Optional[str] = None
    entity_id: Optional[int] = None
    is_active: bool
    notes: Optional[str] = None

    model_config = {"from_attributes": True}


class BudgetSummaryItem(BaseModel):
    budget_id: int
    category_id: int
    category_name: str
    budget_amount: float
    actual_spent: float
    remaining: float
    percentage_used: float
    status: str  # "on_track", "warning", "over_budget"


class BudgetSummaryResponse(BaseModel):
    period: str  # "2026-03"
    total_budgeted: float
    total_spent: float
    budgets: list[BudgetSummaryItem]


# =============================================================================
# CRUD Endpoints
# =============================================================================

@router.get("/budgets", response_model=list[BudgetResponse])
def list_budgets(
    entity_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    """List all budgets, optionally filtered by entity and active status."""
    query = db.query(Budget)
    if entity_id is not None:
        query = query.filter(Budget.entity_id == entity_id)
    if is_active is not None:
        query = query.filter(Budget.is_active == is_active)

    budgets = query.all()
    result = []
    for b in budgets:
        cat_name = b.category.category_name if b.category else None
        result.append(BudgetResponse(
            budget_id=b.budget_id,
            category_id=b.category_id,
            category_name=cat_name,
            budget_amount=float(b.budget_amount),
            period_type=b.period_type,
            start_date=str(b.start_date),
            end_date=str(b.end_date) if b.end_date else None,
            entity_id=b.entity_id,
            is_active=b.is_active,
            notes=b.notes,
        ))
    return result


@router.post("/budgets", response_model=BudgetResponse, status_code=201)
def create_budget(budget_data: BudgetCreate, db: Session = Depends(get_db)):
    """Create a new budget for a category."""
    # Validate category exists
    category = db.query(Category).filter_by(category_id=budget_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category {budget_data.category_id} not found")

    # Validate entity if provided
    if budget_data.entity_id:
        entity = db.query(Entity).filter_by(entity_id=budget_data.entity_id).first()
        if not entity:
            raise HTTPException(status_code=404, detail=f"Entity {budget_data.entity_id} not found")

    budget = Budget(
        category_id=budget_data.category_id,
        budget_amount=Decimal(str(budget_data.budget_amount)),
        period_type=budget_data.period_type,
        start_date=date.fromisoformat(budget_data.start_date),
        end_date=date.fromisoformat(budget_data.end_date) if budget_data.end_date else None,
        entity_id=budget_data.entity_id,
        notes=budget_data.notes,
        is_active=True,
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)

    return BudgetResponse(
        budget_id=budget.budget_id,
        category_id=budget.category_id,
        category_name=category.category_name,
        budget_amount=float(budget.budget_amount),
        period_type=budget.period_type,
        start_date=str(budget.start_date),
        end_date=str(budget.end_date) if budget.end_date else None,
        entity_id=budget.entity_id,
        is_active=budget.is_active,
        notes=budget.notes,
    )


@router.put("/budgets/{budget_id}", response_model=BudgetResponse)
def update_budget(budget_id: int, budget_data: BudgetUpdate, db: Session = Depends(get_db)):
    """Update an existing budget."""
    budget = db.query(Budget).filter_by(budget_id=budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail=f"Budget {budget_id} not found")

    if budget_data.budget_amount is not None:
        budget.budget_amount = Decimal(str(budget_data.budget_amount))
    if budget_data.period_type is not None:
        budget.period_type = budget_data.period_type
    if budget_data.start_date is not None:
        budget.start_date = date.fromisoformat(budget_data.start_date)
    if budget_data.end_date is not None:
        budget.end_date = date.fromisoformat(budget_data.end_date)
    if budget_data.entity_id is not None:
        budget.entity_id = budget_data.entity_id
    if budget_data.is_active is not None:
        budget.is_active = budget_data.is_active
    if budget_data.notes is not None:
        budget.notes = budget_data.notes

    db.commit()
    db.refresh(budget)

    cat_name = budget.category.category_name if budget.category else None
    return BudgetResponse(
        budget_id=budget.budget_id,
        category_id=budget.category_id,
        category_name=cat_name,
        budget_amount=float(budget.budget_amount),
        period_type=budget.period_type,
        start_date=str(budget.start_date),
        end_date=str(budget.end_date) if budget.end_date else None,
        entity_id=budget.entity_id,
        is_active=budget.is_active,
        notes=budget.notes,
    )


@router.delete("/budgets/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    """Delete a budget."""
    budget = db.query(Budget).filter_by(budget_id=budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail=f"Budget {budget_id} not found")

    db.delete(budget)
    db.commit()
    return {"success": True, "message": f"Budget {budget_id} deleted"}


# =============================================================================
# Summary Endpoint
# =============================================================================

@router.get("/budgets/summary", response_model=BudgetSummaryResponse)
def get_budget_summary(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    entity_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Get budget vs. actual spending summary for a given month.
    Calculates actual spending from expense transactions per category.
    """
    # Get active budgets
    query = db.query(Budget).filter(Budget.is_active == True)
    if entity_id is not None:
        query = query.filter(Budget.entity_id == entity_id)

    budgets = query.all()

    if not budgets:
        return BudgetSummaryResponse(
            period=f"{year}-{month:02d}",
            total_budgeted=0,
            total_spent=0,
            budgets=[],
        )

    # Calculate actual spending per category for the month
    spending_query = (
        db.query(
            Transaction.category_id,
            func.sum(Transaction.amount).label("total_spent"),
        )
        .filter(
            Transaction.transaction_type == "Expense",
            extract("year", Transaction.transaction_date) == year,
            extract("month", Transaction.transaction_date) == month,
        )
    )
    if entity_id is not None:
        spending_query = spending_query.filter(Transaction.entity_id == entity_id)

    spending_query = spending_query.group_by(Transaction.category_id)
    spending_map = {row.category_id: float(row.total_spent or 0) for row in spending_query.all()}

    items = []
    total_budgeted = 0.0
    total_spent = 0.0

    for b in budgets:
        cat_name = b.category.category_name if b.category else f"Category {b.category_id}"
        budget_amt = float(b.budget_amount)
        actual = spending_map.get(b.category_id, 0.0)
        remaining = budget_amt - actual
        pct = (actual / budget_amt * 100) if budget_amt > 0 else 0

        if pct > 100:
            status = "over_budget"
        elif pct >= 75:
            status = "warning"
        else:
            status = "on_track"

        items.append(BudgetSummaryItem(
            budget_id=b.budget_id,
            category_id=b.category_id,
            category_name=cat_name,
            budget_amount=budget_amt,
            actual_spent=actual,
            remaining=remaining,
            percentage_used=round(pct, 1),
            status=status,
        ))

        total_budgeted += budget_amt
        total_spent += actual

    # Sort by percentage used (descending) so most urgent budgets appear first
    items.sort(key=lambda x: x.percentage_used, reverse=True)

    return BudgetSummaryResponse(
        period=f"{year}-{month:02d}",
        total_budgeted=total_budgeted,
        total_spent=total_spent,
        budgets=items,
    )
