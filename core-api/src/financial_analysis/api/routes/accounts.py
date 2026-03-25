"""
API routes for account management.

Provides endpoints for:
- Account CRUD operations
- Balance tracking
- Investment holdings
- Reconciliation
- Net worth calculations
"""

import logging
from datetime import date
from typing import List, Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from ..dependencies import get_db
from ...services.account_service import AccountService
from ..schemas.account import (
    AccountCreate,
    AccountUpdate,
    AccountResponse,
    AccountSummary,
    BalanceCreate,
    BalanceResponse,
    BalanceHistory,
    HoldingCreate,
    HoldingUpdate,
    HoldingResponse,
    PortfolioSummary,
    ReconciliationCreate,
    ReconciliationComplete,
    ReconciliationResponse,
    NetWorthResponse,
    AccountFilterParams,
    TransactionClearRequest,
    CalculatedBalance
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


# ==================== Net Worth & Analytics (Must be before /{account_id}) ====================

@router.get("/net-worth", response_model=NetWorthResponse)
def get_net_worth(
    as_of_date: Optional[date] = Query(None, description="Calculate as of this date"),
    entity_id: Optional[int] = Query(None, gt=0, description="Filter by entity ID"),
    db: Session = Depends(get_db)
):
    """Get total net worth across all accounts, optionally filtered by entity."""
    service = AccountService(db)
    effective_date = as_of_date or date.today()
    net_worth = service.get_net_worth(as_of_date, entity_id=entity_id)

    # Add account breakdown (respecting the same date and entity filter)
    account_breakdown = {}
    accounts = service.get_accounts(is_active=True, entity_id=entity_id)

    for account in accounts:
        balance = service.get_current_balance(account.account_id)
        if balance and balance.balance_date <= effective_date:
            if account.account_type not in account_breakdown:
                account_breakdown[account.account_type] = Decimal('0')
            account_breakdown[account.account_type] += balance.total_balance

    return NetWorthResponse(
        assets=net_worth['assets'],
        liabilities=net_worth['liabilities'],
        net_worth=net_worth['net_worth'],
        liquid_assets=net_worth['liquid_assets'],
        investments=net_worth['investments'],
        as_of_date=net_worth['as_of_date'],
        account_breakdown=account_breakdown
    )


@router.get("/summary", response_model=List[AccountSummary])
def get_account_summary(
    entity_id: Optional[int] = Query(None, gt=0, description="Filter by entity ID"),
    db: Session = Depends(get_db)
):
    """Get summary of all accounts with current balances, optionally filtered by entity."""
    service = AccountService(db)
    summaries = service.get_account_summary(entity_id=entity_id)
    return [AccountSummary(**summary) for summary in summaries]


# ==================== Account Management ====================

@router.get("", response_model=List[AccountResponse])
def list_accounts(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    account_type: Optional[str] = Query(None, description="Filter by account type"),
    entity_id: Optional[int] = Query(None, gt=0, description="Filter by entity ID"),
    db: Session = Depends(get_db)
):
    """Get all accounts with optional filtering."""
    service = AccountService(db)
    accounts = service.get_accounts(is_active=is_active, account_type=account_type, entity_id=entity_id)

    # Add current balance to each account
    result = []
    for account in accounts:
        account_dict = {
            "account_id": account.account_id,
            "account_name": account.account_name,
            "account_type": account.account_type,
            "account_subtype": account.account_subtype,
            "institution_name": account.institution_name,
            "account_number_last4": account.account_number_last4,
            "currency": account.currency,
            "is_active": account.is_active,
            "has_cash_component": account.has_cash_component,
            "has_investment_component": account.has_investment_component,
            "opening_balance": account.opening_balance,
            "opening_balance_date": account.opening_balance_date,
            "entity_ids": [e.entity_id for e in account.entities],
            "notes": account.notes,
            "created_at": account.created_at,
            "updated_at": account.updated_at,
            "property_value": account.property_value,
            "property_type": account.property_type,
            "linked_mortgage_account_id": account.linked_mortgage_account_id,
        }

        # Get current balance
        balance = service.get_current_balance(account.account_id)
        if balance:
            account_dict["current_balance"] = balance.total_balance
            account_dict["current_balance_date"] = balance.balance_date
            account_dict["cash_balance"] = balance.cash_balance
            account_dict["investment_value"] = balance.investment_value

        result.append(AccountResponse(**account_dict))

    return result


@router.post("", response_model=AccountResponse)
def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db)
):
    """Create a new account."""
    service = AccountService(db)

    try:
        new_account = service.create_account(
            account_name=account.account_name,
            account_type=account.account_type,
            institution_name=account.institution_name,
            account_number_last4=account.account_number_last4,
            account_subtype=account.account_subtype,
            currency=account.currency,
            opening_balance=account.opening_balance,
            opening_balance_date=account.opening_balance_date,
            entity_ids=account.entity_ids,
            notes=account.notes,
            property_value=account.property_value,
            property_type=account.property_type,
            linked_mortgage_account_id=account.linked_mortgage_account_id,
        )

        # Build response
        response = AccountResponse(
            account_id=new_account.account_id,
            account_name=new_account.account_name,
            account_type=new_account.account_type,
            account_subtype=new_account.account_subtype,
            institution_name=new_account.institution_name,
            account_number_last4=new_account.account_number_last4,
            currency=new_account.currency,
            is_active=new_account.is_active,
            has_cash_component=new_account.has_cash_component,
            has_investment_component=new_account.has_investment_component,
            opening_balance=new_account.opening_balance,
            opening_balance_date=new_account.opening_balance_date,
            notes=new_account.notes,
            created_at=new_account.created_at,
            updated_at=new_account.updated_at,
            property_value=new_account.property_value,
            property_type=new_account.property_type,
            linked_mortgage_account_id=new_account.linked_mortgage_account_id,
        )

        if account.opening_balance != 0:
            response.current_balance = account.opening_balance
            response.current_balance_date = account.opening_balance_date

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError as e:
        logger.warning("Account creation conflict: %s", e)
        raise HTTPException(status_code=409, detail="An account with these details already exists")
    except Exception as e:
        logger.error("Unexpected error creating account: %s", e)
        raise HTTPException(status_code=500, detail="Failed to create account")


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int = Path(..., description="Account ID"),
    db: Session = Depends(get_db)
):
    """Get a specific account by ID."""
    service = AccountService(db)
    account = service.get_account(account_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Build response with current balance
    response_dict = {
        "account_id": account.account_id,
        "account_name": account.account_name,
        "account_type": account.account_type,
        "account_subtype": account.account_subtype,
        "institution_name": account.institution_name,
        "account_number_last4": account.account_number_last4,
        "currency": account.currency,
        "is_active": account.is_active,
        "has_cash_component": account.has_cash_component,
        "has_investment_component": account.has_investment_component,
        "opening_balance": account.opening_balance,
        "opening_balance_date": account.opening_balance_date,
        "notes": account.notes,
        "entity_ids": [e.entity_id for e in account.entities],
        "created_at": account.created_at,
        "updated_at": account.updated_at,
        "property_value": account.property_value,
        "property_type": account.property_type,
        "linked_mortgage_account_id": account.linked_mortgage_account_id,
    }

    # Get current balance
    balance = service.get_current_balance(account_id)
    if balance:
        response_dict["current_balance"] = balance.total_balance
        response_dict["current_balance_date"] = balance.balance_date
        response_dict["cash_balance"] = balance.cash_balance
        response_dict["investment_value"] = balance.investment_value

    return AccountResponse(**response_dict)


@router.put("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int = Path(..., description="Account ID"),
    account_update: AccountUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update an account."""
    service = AccountService(db)

    # Get update fields
    update_data = account_update.model_dump(exclude_unset=True)

    updated_account = service.update_account(account_id, **update_data)

    if not updated_account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Build response
    response_dict = {
        "account_id": updated_account.account_id,
        "account_name": updated_account.account_name,
        "account_type": updated_account.account_type,
        "account_subtype": updated_account.account_subtype,
        "institution_name": updated_account.institution_name,
        "account_number_last4": updated_account.account_number_last4,
        "currency": updated_account.currency,
        "is_active": updated_account.is_active,
        "has_cash_component": updated_account.has_cash_component,
        "has_investment_component": updated_account.has_investment_component,
        "opening_balance": updated_account.opening_balance,
        "opening_balance_date": updated_account.opening_balance_date,
        "notes": updated_account.notes,
        "entity_ids": [e.entity_id for e in updated_account.entities],
        "created_at": updated_account.created_at,
        "updated_at": updated_account.updated_at
    }

    return AccountResponse(**response_dict)


@router.delete("/{account_id}")
def delete_account(
    account_id: int = Path(..., description="Account ID"),
    db: Session = Depends(get_db)
):
    """Deactivate an account (soft delete)."""
    service = AccountService(db)
    success = service.deactivate_account(account_id)

    if not success:
        raise HTTPException(status_code=404, detail="Account not found")

    return {"message": "Account deactivated successfully"}


# ==================== Balance Management ====================

@router.get("/{account_id}/balances", response_model=BalanceHistory)
def get_balance_history(
    account_id: int = Path(..., description="Account ID"),
    start_date: Optional[date] = Query(None, description="Start date"),
    end_date: Optional[date] = Query(None, description="End date"),
    balance_type: Optional[str] = Query(None, description="Balance type filter"),
    db: Session = Depends(get_db)
):
    """Get balance history for an account."""
    service = AccountService(db)

    # Verify account exists
    account = service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=422,
            detail="start_date must be before or equal to end_date"
        )

    balances = service.get_balance_history(
        account_id=account_id,
        start_date=start_date,
        end_date=end_date,
        balance_type=balance_type
    )

    return BalanceHistory(
        account_id=account_id,
        account_name=account.account_name,
        balances=[BalanceResponse.model_validate(b) for b in balances],
        start_date=start_date,
        end_date=end_date
    )


@router.post("/{account_id}/balances", response_model=BalanceResponse)
def add_balance_snapshot(
    account_id: int = Path(..., description="Account ID"),
    balance: BalanceCreate = ...,
    db: Session = Depends(get_db)
):
    """Add a balance snapshot for an account."""
    service = AccountService(db)

    # Verify account exists
    account = service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    new_balance = service.add_balance_snapshot(
        account_id=account_id,
        balance_date=balance.balance_date,
        total_balance=balance.total_balance,
        balance_type=balance.balance_type,
        cash_balance=balance.cash_balance,
        investment_value=balance.investment_value,
        notes=balance.notes
    )

    return BalanceResponse.model_validate(new_balance)


@router.get("/{account_id}/current-balance", response_model=BalanceResponse)
def get_current_balance(
    account_id: int = Path(..., description="Account ID"),
    db: Session = Depends(get_db)
):
    """Get the current balance for an account."""
    service = AccountService(db)

    balance = service.get_current_balance(account_id)
    if not balance:
        raise HTTPException(status_code=404, detail="No balance found for this account")

    return BalanceResponse.model_validate(balance)


@router.get("/{account_id}/calculated-balance", response_model=CalculatedBalance)
def get_calculated_balance(
    account_id: int = Path(..., description="Account ID"),
    as_of_date: date = Query(date.today(), description="Calculate balance as of this date"),
    db: Session = Depends(get_db)
):
    """Calculate account balance from transactions."""
    service = AccountService(db)

    # Verify account exists
    account = service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    result = service.calculate_balance_from_transactions(account_id, as_of_date)

    # Count transactions
    from ...database.models import Transaction
    tx_count = db.query(Transaction).filter(
        Transaction.account_id == account_id,
        Transaction.transaction_date <= as_of_date
    ).count()

    return CalculatedBalance(
        account_id=account_id,
        as_of_date=as_of_date,
        total=result['total'],
        cash=result.get('cash'),
        investments=result.get('investments'),
        based_on_transactions=tx_count
    )


# ==================== Investment Holdings ====================

@router.get("/{account_id}/holdings", response_model=List[HoldingResponse])
def get_holdings(
    account_id: int = Path(..., description="Account ID"),
    db: Session = Depends(get_db)
):
    """Get current investment holdings for an account."""
    service = AccountService(db)

    # Verify account exists
    account = service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    holdings = service.get_current_holdings(account_id)

    # Calculate gain/loss for each holding
    result = []
    for holding in holdings:
        holding_dict = {
            "holding_id": holding.holding_id,
            "account_id": holding.account_id,
            "symbol": holding.symbol,
            "description": holding.description,
            "quantity": holding.quantity,
            "cost_basis": holding.cost_basis,
            "current_value": holding.current_value,
            "as_of_date": holding.as_of_date,
            "asset_class": holding.asset_class,
            "sector": holding.sector,
            "created_at": holding.created_at,
            "updated_at": holding.updated_at
        }

        # Calculate gain/loss if we have both values
        if holding.cost_basis is not None and holding.current_value is not None:
            holding_dict["gain_loss"] = holding.current_value - holding.cost_basis
            if holding.cost_basis != 0:
                holding_dict["gain_loss_percent"] = float(
                    ((holding.current_value - holding.cost_basis) / holding.cost_basis) * 100
                )

        result.append(HoldingResponse(**holding_dict))

    return result


@router.post("/{account_id}/holdings", response_model=HoldingResponse)
def add_holding(
    account_id: int = Path(..., description="Account ID"),
    holding: HoldingCreate = ...,
    db: Session = Depends(get_db)
):
    """Add or update an investment holding."""
    service = AccountService(db)

    # Verify account exists
    account = service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if not account.has_investment_component:
        raise HTTPException(
            status_code=400,
            detail="This account type does not support investment holdings"
        )

    new_holding = service.add_holding(
        account_id=account_id,
        symbol=holding.symbol,
        quantity=holding.quantity,
        as_of_date=holding.as_of_date,
        description=holding.description,
        cost_basis=holding.cost_basis,
        current_value=holding.current_value,
        asset_class=holding.asset_class,
        sector=holding.sector
    )

    return HoldingResponse.model_validate(new_holding)


@router.put("/holdings/{holding_id}", response_model=HoldingResponse)
def update_holding(
    holding_id: int = Path(..., description="Holding ID"),
    holding: HoldingUpdate = ...,
    db: Session = Depends(get_db)
):
    """Update an investment holding."""
    service = AccountService(db)
    updates = holding.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    updated = service.update_holding(holding_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Holding not found")

    result = {
        "holding_id": updated.holding_id,
        "account_id": updated.account_id,
        "symbol": updated.symbol,
        "description": updated.description,
        "quantity": updated.quantity,
        "cost_basis": updated.cost_basis,
        "current_value": updated.current_value,
        "as_of_date": updated.as_of_date,
        "asset_class": updated.asset_class,
        "sector": updated.sector,
        "created_at": updated.created_at,
        "updated_at": updated.updated_at
    }

    if updated.cost_basis is not None and updated.current_value is not None:
        result["gain_loss"] = float(updated.current_value - updated.cost_basis)
        result["gain_loss_percent"] = (
            float((updated.current_value - updated.cost_basis) / updated.cost_basis * 100)
            if updated.cost_basis != 0 else 0.0
        )

    return result


@router.delete("/holdings/{holding_id}")
def delete_holding(
    holding_id: int = Path(..., description="Holding ID"),
    db: Session = Depends(get_db)
):
    """Delete an investment holding."""
    service = AccountService(db)
    deleted = service.delete_holding(holding_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Holding not found")
    return {"message": f"Holding {holding_id} deleted"}


@router.get("/{account_id}/portfolio", response_model=PortfolioSummary)
def get_portfolio_summary(
    account_id: int = Path(..., description="Account ID"),
    db: Session = Depends(get_db)
):
    """Get portfolio summary for an account."""
    service = AccountService(db)

    # Verify account exists
    account = service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    holdings = service.get_current_holdings(account_id)

    # Calculate totals
    total_value = Decimal('0')
    total_cost_basis = Decimal('0')
    as_of_date = date.today()

    holding_responses = []
    for holding in holdings:
        if holding.current_value:
            total_value += holding.current_value
        if holding.cost_basis:
            total_cost_basis += holding.cost_basis
        if holding.as_of_date:
            as_of_date = holding.as_of_date

        holding_dict = {
            "holding_id": holding.holding_id,
            "account_id": holding.account_id,
            "symbol": holding.symbol,
            "description": holding.description,
            "quantity": holding.quantity,
            "cost_basis": holding.cost_basis,
            "current_value": holding.current_value,
            "as_of_date": holding.as_of_date,
            "asset_class": holding.asset_class,
            "sector": holding.sector,
            "created_at": holding.created_at,
            "updated_at": holding.updated_at
        }

        if holding.cost_basis is not None and holding.current_value is not None:
            holding_dict["gain_loss"] = holding.current_value - holding.cost_basis
            if holding.cost_basis != 0:
                holding_dict["gain_loss_percent"] = float(
                    ((holding.current_value - holding.cost_basis) / holding.cost_basis) * 100
                )

        holding_responses.append(HoldingResponse(**holding_dict))

    total_gain_loss = total_value - total_cost_basis if total_cost_basis > 0 else None

    return PortfolioSummary(
        account_id=account_id,
        account_name=account.account_name,
        total_value=total_value,
        total_cost_basis=total_cost_basis if total_cost_basis > 0 else None,
        total_gain_loss=total_gain_loss,
        holdings=holding_responses,
        as_of_date=as_of_date
    )


# ==================== Reconciliation ====================

@router.post("/{account_id}/reconcile", response_model=ReconciliationResponse)
def create_reconciliation(
    account_id: int = Path(..., description="Account ID"),
    reconciliation: ReconciliationCreate = ...,
    db: Session = Depends(get_db)
):
    """Start a new reconciliation for an account."""
    service = AccountService(db)

    # Verify account exists
    account = service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    new_reconciliation = service.create_reconciliation(
        account_id=account_id,
        statement_date=reconciliation.statement_date,
        statement_balance=reconciliation.statement_balance,
        statement_cash_balance=reconciliation.statement_cash_balance,
        statement_investment_value=reconciliation.statement_investment_value,
        notes=reconciliation.notes
    )

    return ReconciliationResponse.model_validate(new_reconciliation)


@router.get("/{account_id}/reconciliations", response_model=List[ReconciliationResponse])
def get_reconciliations(
    account_id: int = Path(..., description="Account ID"),
    is_reconciled: Optional[bool] = Query(None, description="Filter by reconciliation status"),
    db: Session = Depends(get_db)
):
    """Get reconciliation history for an account."""
    service = AccountService(db)

    # Verify account exists
    account = service.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    reconciliations = service.get_reconciliations(account_id, is_reconciled)

    return [ReconciliationResponse.model_validate(r) for r in reconciliations]


@router.put("/reconciliations/{reconciliation_id}/complete", response_model=ReconciliationResponse)
def complete_reconciliation(
    reconciliation_id: int = Path(..., description="Reconciliation ID"),
    completion: ReconciliationComplete = ...,
    db: Session = Depends(get_db)
):
    """Mark a reconciliation as complete."""
    service = AccountService(db)

    # Clear transactions if provided
    if completion.cleared_transaction_ids:
        service.clear_transactions_batch(
            completion.cleared_transaction_ids,
            cleared_date=date.today()
        )

    success = service.complete_reconciliation(
        reconciliation_id,
        reconciled_by=completion.reconciled_by
    )

    if not success:
        raise HTTPException(status_code=404, detail="Reconciliation not found")

    # Get the updated reconciliation
    from ...database.models import Reconciliation
    reconciliation = db.query(Reconciliation).filter(
        Reconciliation.reconciliation_id == reconciliation_id
    ).first()

    return ReconciliationResponse.model_validate(reconciliation)


@router.post("/transactions/clear", response_model=dict)
def clear_transactions(
    request: TransactionClearRequest,
    db: Session = Depends(get_db)
):
    """Mark transactions as cleared."""
    service = AccountService(db)

    count = service.clear_transactions_batch(
        request.transaction_ids,
        request.cleared_date
    )

    return {
        "message": f"Cleared {count} transactions",
        "cleared_count": count
    }


