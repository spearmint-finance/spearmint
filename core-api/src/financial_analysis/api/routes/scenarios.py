"""Scenarios API routes (Phase 1: preview only, Phase 2: templates)."""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas.scenario import (
    ScenarioPreviewRequest,
    ScenarioPreviewResponse,
    ScenarioTemplate,
    ScenarioTemplateListResponse,
    TemplateAdjuster,
)

# ScenarioService will be implemented in services; import when available
try:
    from ...services.scenario_service import ScenarioService
except Exception:  # pragma: no cover - during initial wiring before service exists
    ScenarioService = None  # type: ignore

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


# --- Scenario Templates (seed data) ---

SCENARIO_TEMPLATES = [
    ScenarioTemplate(
        id="stpl_having-a-baby",
        name="Having a Baby",
        description="Model the financial impact of expanding your family — parental leave, childcare, medical costs, and increased insurance.",
        adjusters=[
            TemplateAdjuster(type="percentage", key="income_reduction_leave", label="Income reduction during leave", default=-1.0, min=-1, max=0),
            TemplateAdjuster(type="fixed", key="childcare_monthly", label="Monthly childcare cost", default=1800, min=0, max=5000),
            TemplateAdjuster(type="fixed", key="supplies_monthly", label="Monthly baby supplies", default=250, min=0, max=1000),
            TemplateAdjuster(type="fixed", key="hospital_one_time", label="Hospital / delivery costs", default=5000, min=0, max=30000),
            TemplateAdjuster(type="percentage", key="insurance_increase", label="Insurance premium increase", default=0.4, min=0, max=2),
        ],
    ),
    ScenarioTemplate(
        id="stpl_buying-a-home",
        name="Buying a Home",
        description="Model the shift from renting to owning — mortgage, property tax, insurance, maintenance, and upfront closing costs.",
        adjusters=[
            TemplateAdjuster(type="fixed", key="mortgage_monthly", label="Monthly mortgage payment", default=2200, min=0, max=10000),
            TemplateAdjuster(type="fixed", key="property_tax_monthly", label="Monthly property tax", default=400, min=0, max=3000),
            TemplateAdjuster(type="fixed", key="home_insurance_monthly", label="Monthly home insurance", default=150, min=0, max=1000),
            TemplateAdjuster(type="fixed", key="maintenance_monthly", label="Monthly maintenance reserve", default=200, min=0, max=2000),
            TemplateAdjuster(type="fixed", key="down_payment_closing", label="Down payment + closing costs", default=60000, min=0, max=500000),
            TemplateAdjuster(type="percentage", key="rent_removal", label="Rent removal (savings)", default=-1.0, min=-1, max=0),
        ],
    ),
    ScenarioTemplate(
        id="stpl_job-change",
        name="Job Change",
        description="Model a career move — new salary, changes to commute costs, and benefits adjustments.",
        adjusters=[
            TemplateAdjuster(type="percentage", key="salary_change", label="Salary change", default=0.15, min=-1, max=2),
            TemplateAdjuster(type="fixed", key="commute_change_monthly", label="Monthly commute cost change", default=-100, min=-2000, max=2000),
            TemplateAdjuster(type="fixed", key="benefits_change_monthly", label="Monthly benefits / insurance change", default=50, min=-1000, max=1000),
        ],
    ),
    ScenarioTemplate(
        id="stpl_tax-increase",
        name="Tax Increase",
        description="Model the impact of a higher effective tax rate on your take-home pay.",
        adjusters=[
            TemplateAdjuster(type="percentage", key="effective_rate_change", label="Effective tax rate increase", default=0.02, min=0, max=0.2),
        ],
    ),
    ScenarioTemplate(
        id="stpl_early-retirement",
        name="Early Retirement",
        description="Model leaving the workforce early — loss of salary, private insurance costs, and retirement withdrawals.",
        adjusters=[
            TemplateAdjuster(type="percentage", key="salary_reduction", label="Salary reduction", default=-1.0, min=-1, max=0),
            TemplateAdjuster(type="fixed", key="health_insurance_monthly", label="Monthly private health insurance", default=600, min=0, max=3000),
            TemplateAdjuster(type="fixed", key="retirement_withdrawal_monthly", label="Monthly retirement withdrawal", default=4000, min=0, max=20000),
        ],
    ),
    ScenarioTemplate(
        id="stpl_starting-a-business",
        name="Starting a Business",
        description="Model the financial transition from employment to entrepreneurship — reduced salary, startup costs, and projected revenue.",
        adjusters=[
            TemplateAdjuster(type="percentage", key="salary_reduction", label="Salary reduction", default=-1.0, min=-1, max=0),
            TemplateAdjuster(type="fixed", key="startup_costs", label="One-time startup costs", default=15000, min=0, max=200000),
            TemplateAdjuster(type="fixed", key="operating_costs_monthly", label="Monthly operating costs", default=2000, min=0, max=20000),
            TemplateAdjuster(type="fixed", key="projected_revenue_monthly", label="Monthly projected revenue (delayed start)", default=3000, min=0, max=50000),
        ],
    ),
]


@router.get("/templates", response_model=ScenarioTemplateListResponse)
def list_scenario_templates(
    page: int = Query(default=1, ge=1, description="Page number"),
    pageSize: int = Query(default=20, ge=1, le=100, alias="pageSize", description="Items per page"),
):
    """List available scenario templates for the create-from-template workflow.

    Returns a paginated list of pre-configured scenario templates that users
    can select, customize, and preview before saving.
    """
    total = len(SCENARIO_TEMPLATES)
    start = (page - 1) * pageSize
    end = start + pageSize
    items = SCENARIO_TEMPLATES[start:end]

    return ScenarioTemplateListResponse(
        items=items,
        page=page,
        pageSize=pageSize,
        total=total,
    )


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

