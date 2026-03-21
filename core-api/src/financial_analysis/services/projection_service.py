"""
Projection Service for Financial Analysis Tool.

Provides income, expense, and cash flow forecasting using statistical methods.
Supports multiple projection algorithms and scenario analysis.
"""

from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from enum import Enum

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session

from ..database.models import Transaction
from .analysis_service import AnalysisService, AnalysisMode, DateRange


class ProjectionMethod(str, Enum):
    """Projection algorithm methods."""
    LINEAR_REGRESSION = "linear_regression"
    MOVING_AVERAGE = "moving_average"
    EXPONENTIAL_SMOOTHING = "exponential_smoothing"
    WEIGHTED_AVERAGE = "weighted_average"


class ScenarioType(str, Enum):
    """Scenario analysis types."""
    BEST_CASE = "best_case"
    EXPECTED = "expected"
    WORST_CASE = "worst_case"


class ProjectionService:
    """Service for financial projections and forecasting."""

    def __init__(self, db: Session):
        """
        Initialize projection service.

        Args:
            db: Database session
        """
        self.db = db
        self.analysis_service = AnalysisService(db)

    def project_income(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        projection_days: int = 90,
        method: ProjectionMethod = ProjectionMethod.LINEAR_REGRESSION,
        confidence_level: float = 0.95
    ) -> Dict:
        """
        Project future income based on historical data.

        Args:
            start_date: Start of historical period (default: 1 year ago)
            end_date: End of historical period (default: today)
            projection_days: Number of days to project forward
            method: Projection algorithm to use
            confidence_level: Confidence level for intervals (0-1)

        Returns:
            Dictionary with projections, confidence intervals, and metadata
        """
        # Get historical data
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=365)

        # Create date range
        date_range = DateRange(start_date=start_date, end_date=end_date)

        # Get income analysis
        income_data = self.analysis_service.analyze_income(
            date_range=date_range,
            mode=AnalysisMode.ANALYSIS
        )

        # Get daily income trends
        trends = self.analysis_service.get_income_trends(
            date_range=date_range,
            period='daily',
            mode=AnalysisMode.ANALYSIS
        )

        # Convert to DataFrame for analysis
        if not trends:
            return self._empty_projection_result("income", projection_days, start_date, end_date, method, confidence_level)

        # Convert TrendDataPoint objects to dict
        trend_data = [{'period': t.period, 'value': float(t.value)} for t in trends]
        df = pd.DataFrame(trend_data)

        df['date'] = pd.to_datetime(df['period'])
        df = df.sort_values('date')

        # CRITICAL FIX: Fill in missing dates with zero values
        # The trends only include days with transactions, but we need ALL calendar days
        # for accurate projections (otherwise moving average uses wrong window)
        df = self._fill_missing_dates(df, start_date, end_date)

        # Generate projections
        projections = self._generate_projections(
            df=df,
            value_column='value',
            projection_days=projection_days,
            method=method,
            confidence_level=confidence_level
        )

        return {
            "projection_type": "income",
            "historical_period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": (end_date - start_date).days,
                "total_income": float(income_data.total_income),
                "average_daily": float(income_data.total_income) / max((end_date - start_date).days, 1)
            },
            "projection_period": {
                "start_date": (end_date + timedelta(days=1)).isoformat(),
                "end_date": (end_date + timedelta(days=projection_days)).isoformat(),
                "days": projection_days
            },
            "method": method,
            "confidence_level": confidence_level,
            **projections
        }

    def project_expenses(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        projection_days: int = 90,
        method: ProjectionMethod = ProjectionMethod.LINEAR_REGRESSION,
        confidence_level: float = 0.95
    ) -> Dict:
        """
        Project future expenses based on historical data.

        Args:
            start_date: Start of historical period (default: 1 year ago)
            end_date: End of historical period (default: today)
            projection_days: Number of days to project forward
            method: Projection algorithm to use
            confidence_level: Confidence level for intervals (0-1)

        Returns:
            Dictionary with projections, confidence intervals, and metadata
        """
        # Get historical data
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=365)

        # Create date range
        date_range = DateRange(start_date=start_date, end_date=end_date)

        # Get expense analysis
        expense_data = self.analysis_service.analyze_expenses(
            date_range=date_range,
            mode=AnalysisMode.ANALYSIS
        )

        # Get daily expense trends
        trends = self.analysis_service.get_expense_trends(
            date_range=date_range,
            period='daily',
            mode=AnalysisMode.ANALYSIS
        )

        # Convert to DataFrame for analysis
        if not trends:
            return self._empty_projection_result("expenses", projection_days, start_date, end_date, method, confidence_level)

        # Convert TrendDataPoint objects to dict
        trend_data = [{'period': t.period, 'value': float(t.value)} for t in trends]
        df = pd.DataFrame(trend_data)

        df['date'] = pd.to_datetime(df['period'])
        df = df.sort_values('date')

        # CRITICAL FIX: Fill in missing dates with zero values
        # The trends only include days with transactions, but we need ALL calendar days
        # for accurate projections (otherwise moving average uses wrong window)
        df = self._fill_missing_dates(df, start_date, end_date)

        # Generate projections
        projections = self._generate_projections(
            df=df,
            value_column='value',
            projection_days=projection_days,
            method=method,
            confidence_level=confidence_level
        )

        return {
            "projection_type": "expenses",
            "historical_period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": (end_date - start_date).days,
                "total_expenses": float(expense_data.total_expenses),
                "average_daily": float(expense_data.total_expenses) / max((end_date - start_date).days, 1)
            },
            "projection_period": {
                "start_date": (end_date + timedelta(days=1)).isoformat(),
                "end_date": (end_date + timedelta(days=projection_days)).isoformat(),
                "days": projection_days
            },
            "method": method,
            "confidence_level": confidence_level,
            **projections
        }

    def project_cashflow(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        projection_days: int = 90,
        method: ProjectionMethod = ProjectionMethod.LINEAR_REGRESSION,
        confidence_level: float = 0.95,
        include_scenarios: bool = True
    ) -> Dict:
        """
        Project future cash flow based on historical data.

        Args:
            start_date: Start of historical period (default: 1 year ago)
            end_date: End of historical period (default: today)
            projection_days: Number of days to project forward
            method: Projection algorithm to use
            confidence_level: Confidence level for intervals (0-1)
            include_scenarios: Include best/worst case scenarios

        Returns:
            Dictionary with cash flow projections and scenarios
        """
        # Get income and expense projections
        income_proj = self.project_income(
            start_date=start_date,
            end_date=end_date,
            projection_days=projection_days,
            method=method,
            confidence_level=confidence_level
        )

        expense_proj = self.project_expenses(
            start_date=start_date,
            end_date=end_date,
            projection_days=projection_days,
            method=method,
            confidence_level=confidence_level
        )

        # Calculate net cash flow projections
        # Note: expenses are stored as positive values, so we SUBTRACT them to get net cash flow
        # Net Cash Flow = Income - Expenses
        # Example: $1000 income - $800 expenses = $200 net cash flow
        projected_income = income_proj['projected_total']
        projected_expenses = expense_proj['projected_total']
        projected_cashflow = projected_income - projected_expenses

        # Calculate confidence intervals for cash flow
        income_lower = income_proj['confidence_interval']['lower']
        income_upper = income_proj['confidence_interval']['upper']
        expense_lower = expense_proj['confidence_interval']['lower']
        expense_upper = expense_proj['confidence_interval']['upper']

        # Cash flow confidence interval (income - expenses)
        # Best case: high income, low expenses
        # Worst case: low income, high expenses
        cashflow_lower = income_lower - expense_upper
        cashflow_upper = income_upper - expense_lower

        result = {
            "projection_type": "cashflow",
            "historical_period": income_proj['historical_period'],
            "projection_period": income_proj['projection_period'],
            "method": method,
            "confidence_level": confidence_level,
            "projected_income": projected_income,
            "projected_expenses": projected_expenses,
            "projected_cashflow": projected_cashflow,
            "confidence_interval": {
                "lower": cashflow_lower,
                "upper": cashflow_upper,
                "range": cashflow_upper - cashflow_lower
            },
            "daily_projections": self._combine_daily_projections(
                income_proj['daily_projections'],
                expense_proj['daily_projections']
            )
        }

        # Add scenario analysis if requested
        if include_scenarios:
            result['scenarios'] = self._generate_scenarios(
                income_proj=income_proj,
                expense_proj=expense_proj
            )

        return result

    def _generate_projections(
        self,
        df: pd.DataFrame,
        value_column: str,
        projection_days: int,
        method: ProjectionMethod,
        confidence_level: float
    ) -> Dict:
        """Generate projections using specified method."""
        if method == ProjectionMethod.LINEAR_REGRESSION:
            return self._linear_regression_projection(df, value_column, projection_days, confidence_level)
        elif method == ProjectionMethod.MOVING_AVERAGE:
            return self._moving_average_projection(df, value_column, projection_days, confidence_level)
        elif method == ProjectionMethod.EXPONENTIAL_SMOOTHING:
            return self._exponential_smoothing_projection(df, value_column, projection_days, confidence_level)
        elif method == ProjectionMethod.WEIGHTED_AVERAGE:
            return self._weighted_average_projection(df, value_column, projection_days, confidence_level)
        else:
            raise ValueError(f"Unknown projection method: {method}")

    def _linear_regression_projection(
        self,
        df: pd.DataFrame,
        value_column: str,
        projection_days: int,
        confidence_level: float
    ) -> Dict:
        """Project using linear regression."""
        # Prepare data
        df = df.copy()
        df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
        X = df['days_since_start'].values.reshape(-1, 1)
        y = df[value_column].values

        # Fit linear regression
        model = LinearRegression()
        model.fit(X, y)

        # Generate future dates
        last_day = df['days_since_start'].max()
        future_days = np.arange(last_day + 1, last_day + projection_days + 1).reshape(-1, 1)

        # Predict
        predictions = model.predict(future_days)

        # Calculate prediction intervals
        residuals = y - model.predict(X)
        mse = np.mean(residuals ** 2)
        std_error = np.sqrt(mse)

        # t-statistic for confidence interval
        t_stat = stats.t.ppf((1 + confidence_level) / 2, len(y) - 2)
        margin = t_stat * std_error

        # Calculate total projection
        projected_total = float(np.sum(predictions))
        lower_bound = float(np.sum(predictions - margin))
        upper_bound = float(np.sum(predictions + margin))

        # Generate daily projections
        start_date = df['date'].max() + timedelta(days=1)
        daily_projections = []
        for i, pred in enumerate(predictions.flatten()):
            proj_date = start_date + timedelta(days=i)
            daily_projections.append({
                "date": proj_date.isoformat(),
                "projected_value": float(pred),
                "lower_bound": float(pred - margin),
                "upper_bound": float(pred + margin)
            })

        return {
            "projected_total": projected_total,
            "confidence_interval": {
                "lower": lower_bound,
                "upper": upper_bound,
                "range": upper_bound - lower_bound
            },
            "daily_projections": daily_projections,
            "model_metrics": {
                "r_squared": float(model.score(X, y)),
                "slope": float(model.coef_[0]),
                "intercept": float(model.intercept_),
                "std_error": float(std_error)
            }
        }

    def _moving_average_projection(
        self,
        df: pd.DataFrame,
        value_column: str,
        projection_days: int,
        confidence_level: float,
        window: int = 30
    ) -> Dict:
        """Project using moving average."""
        # Calculate moving average
        values = df[value_column].values
        if len(values) < window:
            window = max(len(values) // 2, 1)

        moving_avg = np.mean(values[-window:])
        std_dev = np.std(values[-window:])

        # Calculate confidence interval
        z_score = stats.norm.ppf((1 + confidence_level) / 2)
        margin = z_score * std_dev / np.sqrt(window)

        # Project forward
        projected_total = float(moving_avg * projection_days)
        lower_bound = float((moving_avg - margin) * projection_days)
        upper_bound = float((moving_avg + margin) * projection_days)

        # Generate daily projections
        start_date = df['date'].max() + timedelta(days=1)
        daily_projections = []
        for i in range(projection_days):
            proj_date = start_date + timedelta(days=i)
            daily_projections.append({
                "date": proj_date.isoformat(),
                "projected_value": float(moving_avg),
                "lower_bound": float(moving_avg - margin),
                "upper_bound": float(moving_avg + margin)
            })

        return {
            "projected_total": projected_total,
            "confidence_interval": {
                "lower": lower_bound,
                "upper": upper_bound,
                "range": upper_bound - lower_bound
            },
            "daily_projections": daily_projections,
            "model_metrics": {
                "moving_average": float(moving_avg),
                "std_deviation": float(std_dev),
                "window_size": window
            }
        }

    def _exponential_smoothing_projection(
        self,
        df: pd.DataFrame,
        value_column: str,
        projection_days: int,
        confidence_level: float,
        alpha: float = 0.3
    ) -> Dict:
        """Project using exponential smoothing."""
        values = df[value_column].values

        # Apply exponential smoothing
        smoothed = [values[0]]
        for i in range(1, len(values)):
            smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[i-1])

        # Use last smoothed value for projection
        projected_value = smoothed[-1]

        # Calculate residuals for confidence interval
        residuals = values - np.array(smoothed)
        std_error = np.std(residuals)

        z_score = stats.norm.ppf((1 + confidence_level) / 2)
        margin = z_score * std_error

        # Project forward
        projected_total = float(projected_value * projection_days)
        lower_bound = float((projected_value - margin) * projection_days)
        upper_bound = float((projected_value + margin) * projection_days)

        # Generate daily projections
        start_date = df['date'].max() + timedelta(days=1)
        daily_projections = []
        for i in range(projection_days):
            proj_date = start_date + timedelta(days=i)
            daily_projections.append({
                "date": proj_date.isoformat(),
                "projected_value": float(projected_value),
                "lower_bound": float(projected_value - margin),
                "upper_bound": float(projected_value + margin)
            })

        return {
            "projected_total": projected_total,
            "confidence_interval": {
                "lower": lower_bound,
                "upper": upper_bound,
                "range": upper_bound - lower_bound
            },
            "daily_projections": daily_projections,
            "model_metrics": {
                "smoothed_value": float(projected_value),
                "alpha": alpha,
                "std_error": float(std_error)
            }
        }

    def _weighted_average_projection(
        self,
        df: pd.DataFrame,
        value_column: str,
        projection_days: int,
        confidence_level: float
    ) -> Dict:
        """Project using weighted average (more weight to recent data)."""
        values = df[value_column].values
        n = len(values)

        # Create weights (linear increase, more weight to recent)
        weights = np.arange(1, n + 1)
        weights = weights / weights.sum()

        # Calculate weighted average
        weighted_avg = np.sum(values * weights)

        # Calculate weighted standard deviation
        weighted_var = np.sum(weights * (values - weighted_avg) ** 2)
        weighted_std = np.sqrt(weighted_var)

        # Confidence interval
        z_score = stats.norm.ppf((1 + confidence_level) / 2)
        margin = z_score * weighted_std

        # Project forward
        projected_total = float(weighted_avg * projection_days)
        lower_bound = float((weighted_avg - margin) * projection_days)
        upper_bound = float((weighted_avg + margin) * projection_days)

        # Generate daily projections
        start_date = df['date'].max() + timedelta(days=1)
        daily_projections = []
        for i in range(projection_days):
            proj_date = start_date + timedelta(days=i)
            daily_projections.append({
                "date": proj_date.isoformat(),
                "projected_value": float(weighted_avg),
                "lower_bound": float(weighted_avg - margin),
                "upper_bound": float(weighted_avg + margin)
            })

        return {
            "projected_total": projected_total,
            "confidence_interval": {
                "lower": lower_bound,
                "upper": upper_bound,
                "range": upper_bound - lower_bound
            },
            "daily_projections": daily_projections,
            "model_metrics": {
                "weighted_average": float(weighted_avg),
                "weighted_std": float(weighted_std),
                "sample_size": n
            }
        }

    def _combine_daily_projections(
        self,
        income_projections: List[Dict],
        expense_projections: List[Dict]
    ) -> List[Dict]:
        """
        Combine income and expense projections into cash flow projections.

        Note: Expenses are stored as positive values, so we SUBTRACT them from income
        to get the net cash flow (profit/loss).
        """
        combined = []
        for inc, exp in zip(income_projections, expense_projections):
            combined.append({
                "date": inc['date'],
                "projected_income": inc['projected_value'],
                "projected_expenses": exp['projected_value'],
                "projected_cashflow": inc['projected_value'] - exp['projected_value'],
                "cashflow_lower": inc['lower_bound'] - exp['upper_bound'],
                "cashflow_upper": inc['upper_bound'] - exp['lower_bound']
            })
        return combined

    def _generate_scenarios(
        self,
        income_proj: Dict,
        expense_proj: Dict
    ) -> Dict:
        """
        Generate best/worst/expected case scenarios.

        Note: Expenses are stored as positive values, so we SUBTRACT them from income
        to get the net cash flow (profit/loss).
        """
        # Expected case: use projected values
        expected_income = income_proj['projected_total']
        expected_expenses = expense_proj['projected_total']
        expected_cashflow = expected_income - expected_expenses

        # Best case: upper bound income, lower bound expenses
        best_income = income_proj['confidence_interval']['upper']
        best_expenses = expense_proj['confidence_interval']['lower']
        best_cashflow = best_income - best_expenses

        # Worst case: lower bound income, upper bound expenses
        worst_income = income_proj['confidence_interval']['lower']
        worst_expenses = expense_proj['confidence_interval']['upper']
        worst_cashflow = worst_income - worst_expenses

        return {
            "expected": {
                "income": expected_income,
                "expenses": expected_expenses,
                "cashflow": expected_cashflow,
                "description": "Most likely outcome based on historical trends"
            },
            "best_case": {
                "income": best_income,
                "expenses": best_expenses,
                "cashflow": best_cashflow,
                "description": "Optimistic scenario with high income and low expenses"
            },
            "worst_case": {
                "income": worst_income,
                "expenses": worst_expenses,
                "cashflow": worst_cashflow,
                "description": "Conservative scenario with low income and high expenses"
            },
            "range": {
                "cashflow_range": best_cashflow - worst_cashflow,
                "income_range": best_income - worst_income,
                "expense_range": best_expenses - worst_expenses
            }
        }

    def _empty_projection_result(
        self,
        projection_type: str,
        projection_days: int,
        start_date: date,
        end_date: date,
        method: ProjectionMethod,
        confidence_level: float
    ) -> Dict:
        """Return empty projection result when no historical data available."""
        return {
            "projection_type": projection_type,
            "historical_period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": (end_date - start_date).days,
                "total_income": 0.0 if projection_type == "income" else None,
                "total_expenses": 0.0 if projection_type == "expenses" else None,
                "average_daily": 0.0
            },
            "projection_period": {
                "start_date": (end_date + timedelta(days=1)).isoformat(),
                "end_date": (end_date + timedelta(days=projection_days)).isoformat(),
                "days": projection_days
            },
            "method": method.value if hasattr(method, 'value') else str(method),
            "confidence_level": confidence_level,
            "projected_total": 0.0,
            "confidence_interval": {
                "lower": 0.0,
                "upper": 0.0,
                "range": 0.0
            },
            "daily_projections": [],
            "model_metrics": {}
        }

    def calculate_accuracy_metrics(
        self,
        actual_values: List[float],
        predicted_values: List[float]
    ) -> Dict:
        """
        Calculate projection accuracy metrics.

        Args:
            actual_values: Actual observed values
            predicted_values: Predicted values

        Returns:
            Dictionary with MAPE, RMSE, and other accuracy metrics
        """
        actual = np.array(actual_values)
        predicted = np.array(predicted_values)

        # Mean Absolute Percentage Error (MAPE)
        mape = np.mean(np.abs((actual - predicted) / np.maximum(actual, 1e-10))) * 100

        # Root Mean Squared Error (RMSE)
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))

        # Mean Absolute Error (MAE)
        mae = np.mean(np.abs(actual - predicted))

        # R-squared
        ss_res = np.sum((actual - predicted) ** 2)
        ss_tot = np.sum((actual - np.mean(actual)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        return {
            "mape": float(mape),
            "rmse": float(rmse),
            "mae": float(mae),
            "r_squared": float(r_squared),
            "sample_size": len(actual),
            "accuracy_grade": self._get_accuracy_grade(mape)
        }

    def _get_accuracy_grade(self, mape: float) -> str:
        """Get accuracy grade based on MAPE."""
        if mape < 10:
            return "Excellent"
        elif mape < 20:
            return "Good"
        elif mape < 30:
            return "Acceptable"
        elif mape < 50:
            return "Poor"
        else:
            return "Very Poor"

    def _fill_missing_dates(self, df: pd.DataFrame, start_date: date, end_date: date) -> pd.DataFrame:
        """
        Fill in missing dates with zero values.

        The trend data only includes days with transactions, but for accurate projections
        we need ALL calendar days (including days with zero income/expenses).

        Otherwise, moving average and other methods will use the wrong window size.
        For example, if we want the last 30 days but only 10 days had transactions,
        we'd be averaging over 90+ calendar days instead of 30.

        Args:
            df: DataFrame with 'date' and 'value' columns (sparse - only days with transactions)
            start_date: Start of the historical period
            end_date: End of the historical period

        Returns:
            DataFrame with all calendar days filled in (zero for missing days)
        """
        # Create a complete date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')

        # Create a DataFrame with all dates
        complete_df = pd.DataFrame({'date': date_range})

        # Merge with existing data, filling missing values with 0
        result = complete_df.merge(df, on='date', how='left')
        result['value'] = result['value'].fillna(0)

        # Sort by date
        result = result.sort_values('date').reset_index(drop=True)

        return result

