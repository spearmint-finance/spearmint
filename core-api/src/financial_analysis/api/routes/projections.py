"""
API routes for financial projections.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from ..dependencies import get_db
from ...services.projection_service import ProjectionService, ProjectionMethod
from ..schemas.projection import (
    ProjectionRequest,
    CashflowProjectionRequest,
    IncomeProjectionResponse,
    ExpenseProjectionResponse,
    CashflowProjectionResponse,
    AccuracyMetrics,
    ValidationRequest,
    ProjectionMethodEnum
)

router = APIRouter()


@router.get(
    "/projections/income",
    response_model=IncomeProjectionResponse,
    summary="Project Future Income",
    description="Generate income projections based on historical data using statistical methods"
)
def project_income(
    start_date: Optional[date] = Query(None, description="Start of historical period (default: 1 year ago)"),
    end_date: Optional[date] = Query(None, description="End of historical period (default: today)"),
    projection_days: int = Query(90, ge=1, le=365, description="Number of days to project forward"),
    method: ProjectionMethodEnum = Query(
        ProjectionMethodEnum.LINEAR_REGRESSION,
        description="Projection algorithm to use"
    ),
    confidence_level: float = Query(0.95, ge=0.5, le=0.99, description="Confidence level for intervals"),
    db: Session = Depends(get_db)
):
    """
    Project future income based on historical transaction data.

    **Projection Methods:**
    - `linear_regression`: Trend-based projection using linear regression
    - `moving_average`: Simple moving average of recent data
    - `exponential_smoothing`: Exponentially weighted moving average
    - `weighted_average`: Weighted average with more weight on recent data

    **Returns:**
    - Total projected income for the period
    - Daily projections with confidence intervals
    - Model performance metrics
    - Historical period summary

    **Example:**
    ```
    GET /api/projections/income?projection_days=90&method=linear_regression&confidence_level=0.95
    ```
    """
    try:
        service = ProjectionService(db)
        result = service.project_income(
            start_date=start_date,
            end_date=end_date,
            projection_days=projection_days,
            method=ProjectionMethod(method.value),
            confidence_level=confidence_level
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating income projection: {str(e)}")


@router.get(
    "/projections/expenses",
    response_model=ExpenseProjectionResponse,
    summary="Project Future Expenses",
    description="Generate expense projections based on historical data using statistical methods"
)
def project_expenses(
    start_date: Optional[date] = Query(None, description="Start of historical period (default: 1 year ago)"),
    end_date: Optional[date] = Query(None, description="End of historical period (default: today)"),
    projection_days: int = Query(90, ge=1, le=365, description="Number of days to project forward"),
    method: ProjectionMethodEnum = Query(
        ProjectionMethodEnum.LINEAR_REGRESSION,
        description="Projection algorithm to use"
    ),
    confidence_level: float = Query(0.95, ge=0.5, le=0.99, description="Confidence level for intervals"),
    db: Session = Depends(get_db)
):
    """
    Project future expenses based on historical transaction data.

    **Projection Methods:**
    - `linear_regression`: Trend-based projection using linear regression
    - `moving_average`: Simple moving average of recent data
    - `exponential_smoothing`: Exponentially weighted moving average
    - `weighted_average`: Weighted average with more weight on recent data

    **Returns:**
    - Total projected expenses for the period
    - Daily projections with confidence intervals
    - Model performance metrics
    - Historical period summary

    **Example:**
    ```
    GET /api/projections/expenses?projection_days=90&method=moving_average
    ```
    """
    try:
        service = ProjectionService(db)
        result = service.project_expenses(
            start_date=start_date,
            end_date=end_date,
            projection_days=projection_days,
            method=ProjectionMethod(method.value),
            confidence_level=confidence_level
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating expense projection: {str(e)}")


@router.get(
    "/projections/cashflow",
    response_model=CashflowProjectionResponse,
    summary="Project Future Cash Flow",
    description="Generate cash flow projections with scenario analysis"
)
def project_cashflow(
    start_date: Optional[date] = Query(None, description="Start of historical period (default: 1 year ago)"),
    end_date: Optional[date] = Query(None, description="End of historical period (default: today)"),
    projection_days: int = Query(90, ge=1, le=365, description="Number of days to project forward"),
    method: ProjectionMethodEnum = Query(
        ProjectionMethodEnum.LINEAR_REGRESSION,
        description="Projection algorithm to use"
    ),
    confidence_level: float = Query(0.95, ge=0.5, le=0.99, description="Confidence level for intervals"),
    include_scenarios: bool = Query(True, description="Include best/worst case scenarios"),
    db: Session = Depends(get_db)
):
    """
    Project future cash flow (income - expenses) with scenario analysis.

    **Features:**
    - Combined income and expense projections
    - Net cash flow calculation
    - Confidence intervals for cash flow
    - Scenario analysis (best/expected/worst case)

    **Scenarios:**
    - **Expected**: Most likely outcome based on historical trends
    - **Best Case**: High income + low expenses (optimistic)
    - **Worst Case**: Low income + high expenses (conservative)

    **Returns:**
    - Projected income, expenses, and net cash flow
    - Daily cash flow projections
    - Scenario analysis with ranges
    - Confidence intervals

    **Example:**
    ```
    GET /api/projections/cashflow?projection_days=90&include_scenarios=true
    ```
    """
    try:
        service = ProjectionService(db)
        result = service.project_cashflow(
            start_date=start_date,
            end_date=end_date,
            projection_days=projection_days,
            method=ProjectionMethod(method.value),
            confidence_level=confidence_level,
            include_scenarios=include_scenarios
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating cash flow projection: {str(e)}")


@router.post(
    "/projections/validate",
    response_model=AccuracyMetrics,
    summary="Validate Projection Accuracy",
    description="Calculate accuracy metrics for projection validation"
)
def validate_projection(
    request: ValidationRequest,
    db: Session = Depends(get_db)
):
    """
    Validate projection accuracy by comparing actual vs. predicted values.

    **Metrics Calculated:**
    - **MAPE** (Mean Absolute Percentage Error): Average percentage error
    - **RMSE** (Root Mean Squared Error): Root of average squared errors
    - **MAE** (Mean Absolute Error): Average absolute error
    - **R-squared**: Proportion of variance explained
    - **Accuracy Grade**: Qualitative assessment (Excellent/Good/Acceptable/Poor/Very Poor)

    **Accuracy Grades:**
    - Excellent: MAPE < 10%
    - Good: MAPE < 20%
    - Acceptable: MAPE < 30%
    - Poor: MAPE < 50%
    - Very Poor: MAPE >= 50%

    **Example Request:**
    ```json
    {
      "actual_values": [100.0, 105.0, 110.0, 108.0, 115.0],
      "predicted_values": [98.0, 107.0, 109.0, 110.0, 113.0]
    }
    ```

    **Example Response:**
    ```json
    {
      "mape": 2.5,
      "rmse": 2.8,
      "mae": 2.2,
      "r_squared": 0.95,
      "sample_size": 5,
      "accuracy_grade": "Excellent"
    }
    ```
    """
    try:
        service = ProjectionService(db)
        
        # Validate that lists have same length
        if len(request.actual_values) != len(request.predicted_values):
            raise HTTPException(
                status_code=400,
                detail="Actual and predicted values must have the same length"
            )
        
        metrics = service.calculate_accuracy_metrics(
            actual_values=request.actual_values,
            predicted_values=request.predicted_values
        )
        return metrics
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating accuracy metrics: {str(e)}")


@router.get(
    "/projections/scenarios",
    response_model=CashflowProjectionResponse,
    summary="Get Scenario Analysis",
    description="Get detailed scenario analysis for cash flow projections"
)
def get_scenarios(
    start_date: Optional[date] = Query(None, description="Start of historical period"),
    end_date: Optional[date] = Query(None, description="End of historical period"),
    projection_days: int = Query(90, ge=1, le=365, description="Number of days to project"),
    method: ProjectionMethodEnum = Query(ProjectionMethodEnum.LINEAR_REGRESSION, description="Projection method"),
    db: Session = Depends(get_db)
):
    """
    Get detailed scenario analysis for financial planning.

    This endpoint is similar to `/projections/cashflow` but always includes
    scenario analysis and is optimized for scenario planning use cases.

    **Use Cases:**
    - Financial planning and budgeting
    - Risk assessment
    - What-if analysis
    - Emergency fund planning

    **Returns:**
    - Expected, best case, and worst case scenarios
    - Range of possible outcomes
    - Confidence intervals
    - Daily projections for each scenario

    **Example:**
    ```
    GET /api/projections/scenarios?projection_days=180&method=linear_regression
    ```
    """
    try:
        service = ProjectionService(db)
        result = service.project_cashflow(
            start_date=start_date,
            end_date=end_date,
            projection_days=projection_days,
            method=ProjectionMethod(method.value),
            confidence_level=0.95,
            include_scenarios=True  # Always include scenarios
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating scenario analysis: {str(e)}")

