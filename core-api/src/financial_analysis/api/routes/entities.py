"""Entity API endpoints."""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ...services.entity_service import EntityService
from ..schemas.entity import (
    EntityCreate, EntityUpdate, EntityResponse,
    PnlResponse, CashFlowResponse,
)

router = APIRouter(prefix="/entities", tags=["entities"])


@router.post("/", response_model=EntityResponse, status_code=201)
def create_entity(entity: EntityCreate, db: Session = Depends(get_db)):
    """Create a new entity (business, rental property, etc.)."""
    service = EntityService(db)
    created = service.create_entity(
        entity_name=entity.entity_name,
        entity_type=entity.entity_type,
        tax_id=entity.tax_id,
        address=entity.address,
        fiscal_year_start_month=entity.fiscal_year_start_month,
        is_default=entity.is_default,
        notes=entity.notes,
    )
    return _to_response(created, service)


@router.get("/", response_model=List[EntityResponse])
def list_entities(db: Session = Depends(get_db)):
    """List all entities."""
    service = EntityService(db)
    entities = service.list_entities()
    return [_to_response(e, service) for e in entities]


@router.get("/{entity_id}", response_model=EntityResponse)
def get_entity(entity_id: int, db: Session = Depends(get_db)):
    """Get entity by ID."""
    service = EntityService(db)
    entity = service.get_entity(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found")
    return _to_response(entity, service)


@router.put("/{entity_id}", response_model=EntityResponse)
def update_entity(
    entity_id: int, entity: EntityUpdate, db: Session = Depends(get_db)
):
    """Update an entity."""
    service = EntityService(db)
    updates = entity.model_dump(exclude_unset=True)
    updated = service.update_entity(entity_id, **updates)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found")
    return _to_response(updated, service)


@router.delete("/{entity_id}")
def delete_entity(entity_id: int, db: Session = Depends(get_db)):
    """Delete an entity. Fails if accounts are still assigned."""
    service = EntityService(db)
    try:
        deleted = service.delete_entity(entity_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found")
    return {"message": f"Entity {entity_id} deleted"}


@router.get("/{entity_id}/pnl", response_model=PnlResponse)
def get_entity_pnl(
    entity_id: int,
    start_date: date = Query(..., description="Period start date"),
    end_date: date = Query(..., description="Period end date"),
    db: Session = Depends(get_db),
):
    """Generate a Profit & Loss statement for an entity."""
    if start_date > end_date:
        raise HTTPException(status_code=422, detail="start_date must be before or equal to end_date")
    service = EntityService(db)
    try:
        return service.get_pnl(entity_id, start_date, end_date)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{entity_id}/cashflow", response_model=CashFlowResponse)
def get_entity_cashflow(
    entity_id: int,
    start_date: date = Query(..., description="Period start date"),
    end_date: date = Query(..., description="Period end date"),
    db: Session = Depends(get_db),
):
    """Generate a Cash Flow statement for an entity."""
    if start_date > end_date:
        raise HTTPException(status_code=422, detail="start_date must be before or equal to end_date")
    service = EntityService(db)
    try:
        return service.get_cashflow(entity_id, start_date, end_date)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


def _to_response(entity, service: EntityService) -> EntityResponse:
    """Convert Entity model to response with account count."""
    return EntityResponse(
        entity_id=entity.entity_id,
        entity_name=entity.entity_name,
        entity_type=entity.entity_type,
        tax_id=entity.tax_id,
        address=entity.address,
        fiscal_year_start_month=entity.fiscal_year_start_month,
        is_default=entity.is_default,
        notes=entity.notes,
        account_count=service.get_account_count(entity.entity_id),
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
