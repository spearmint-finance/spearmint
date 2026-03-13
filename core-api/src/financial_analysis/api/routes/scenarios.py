"""Scenarios API routes (Phase 1: preview only)."""

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas.scenario import ScenarioPreviewRequest, ScenarioPreviewResponse

# ScenarioService will be implemented in services; import when available
try:
    from ...services.scenario_service import ScenarioService
except Exception:  # pragma: no cover - during initial wiring before service exists
    ScenarioService = None  # type: ignore

router = APIRouter(prefix="/scenarios", tags=["scenarios"]) 


@router.post("/preview", response_model=ScenarioPreviewResponse)
def preview_scenario(payload: ScenarioPreviewRequest, db: Session = Depends(get_db)):
    """Simulate a scenario without saving it (deterministic, fast preview)."""
    if ScenarioService is None:
        # Temporary stub until ScenarioService is implemented
        # Return a minimal, empty structure to keep API wiring valid
        now = datetime.utcnow()
        return ScenarioPreviewResponse(
            baseline_series=[],
            scenario_series=[],
            kpis={"runway_months": None, "min_balance": 0, "coverage_by_person": {}},
            deltas={"income": 0, "expenses": 0, "net_cf": 0},
            generated_at=now,
        )

    service = ScenarioService(db)
    return service.preview(payload)

