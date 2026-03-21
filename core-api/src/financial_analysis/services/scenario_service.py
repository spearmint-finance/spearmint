"""ScenarioService: deterministic scenario planning engine (Phase 1).

Builds a baseline monthly series from historical data (excludes transfers per Analysis discipline),
optionally attributes by person using TransactionSplit records, applies adjusters, and computes KPIs.
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any
from calendar import monthrange

from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from sqlalchemy import select

from ..database.models import Transaction, TransactionSplit, Category, Tag, TransactionTag
from ..api.schemas.scenario import (
    ScenarioPreviewRequest,
    ScenarioPreviewResponse,
    SeriesPoint,
    ScenarioKPIs,
)


class ScenarioService:
    """Service to simulate person-aware scenarios."""

    def __init__(self, db: Session):
        self.db = db

    # ---------------- Public API ----------------
    def preview(self, payload: ScenarioPreviewRequest) -> ScenarioPreviewResponse:
        horizon_months = payload.horizon_months
        today = date.today()
        start_month = date(today.year, today.month, 1)

        # 1) Build baseline averages by month and by person
        baseline_monthly_by_person = self._baseline_monthly_by_person()

        # Expand into monthly series for horizon
        baseline_series = self._expand_series(start_month, horizon_months, baseline_monthly_by_person)

        # 2) Apply adjusters to build scenario
        scenario_series = self._apply_adjusters(
            start_month,
            baseline_series,
            payload.adjusters,
            default_split_strategy=payload.shared_expense_strategy,
        )

        # 3) Compute KPIs
        kpis = self._compute_kpis(
            baseline_series=baseline_series,
            scenario_series=scenario_series,
            starting_balance=payload.starting_balance or Decimal("0"),
        )

        # 4) Deltas
        deltas = {
            "income": sum(p.income for p in scenario_series) - sum(p.income for p in baseline_series),
            "expenses": sum(p.expenses for p in scenario_series) - sum(p.expenses for p in baseline_series),
            "net_cf": sum(p.net_cf for p in scenario_series) - sum(p.net_cf for p in baseline_series),
        }

        return ScenarioPreviewResponse(
            baseline_series=baseline_series,
            scenario_series=scenario_series,
            kpis=kpis,
            deltas=deltas,
            generated_at=datetime.utcnow(),
        )

    # ---------------- Baseline ----------------
    def _baseline_monthly_by_person(self) -> Dict[Optional[int], Dict[str, Decimal]]:
        """
        Produce baseline average monthly income/expenses by person from recent history.

        Returns a mapping: {person_id_or_None: {"income": Decimal, "expenses": Decimal}}
        Where person_id=None represents "Household" share for any unassigned amount.
        """
        # Define lookback window (last 6 months)
        today = date.today()
        lookback_start = date(today.year - (1 if today.month <= 6 else 0), (today.month - 6) % 12 or 12, 1)

        # Base filters: exclude transfers; include only include_in_analysis
        base_q = self.db.query(Transaction).filter(
            Transaction.include_in_analysis == True,
            # Transfers excluded via include_in_analysis=False
            Transaction.transaction_date >= lookback_start,
        )

        # Tag-based exclusion subqueries
        exclude_income_subq = (
            select(TransactionTag.transaction_id)
            .join(Tag, TransactionTag.tag_id == Tag.tag_id)
            .where(Tag.tag_name == 'exclude-from-income')
            .subquery()
        )
        exclude_expense_subq = (
            select(TransactionTag.transaction_id)
            .join(Tag, TransactionTag.tag_id == Tag.tag_id)
            .where(Tag.tag_name == 'exclude-from-expenses')
            .subquery()
        )

        # For income: exclude transactions tagged exclude-from-income
        inc_q = base_q.filter(
            Transaction.transaction_type == "Income",
            ~Transaction.transaction_id.in_(select(exclude_income_subq))
        )
        # For expenses: exclude transactions tagged exclude-from-expenses
        exp_q = base_q.filter(
            Transaction.transaction_type == "Expense",
            ~Transaction.transaction_id.in_(select(exclude_expense_subq))
        )

        # Fetch transactions and any splits
        income_tx = inc_q.all()
        expense_tx = exp_q.all()

        # Group amounts by person via splits; any remainder goes to None (household)
        per_person: Dict[Optional[int], Dict[str, Decimal]] = {}

        def add_amt(pid: Optional[int], key: str, amt: Decimal):
            bucket = per_person.setdefault(pid, {"income": Decimal("0"), "expenses": Decimal("0")})
            bucket[key] += Decimal(amt)

        # Helper to sum splits for tx; return dict person_id->amount
        def get_splits_for_tx(tx: Transaction) -> Dict[int, Decimal]:
            return {s.person_id: s.amount for s in getattr(tx, "splits", [])}

        # Process income
        for tx in income_tx:
            splits = get_splits_for_tx(tx)
            assigned_total = sum(splits.values(), Decimal("0")) if splits else Decimal("0")
            if splits:
                for pid, amt in splits.items():
                    add_amt(pid, "income", amt)
            # Assign remainder to household
            remainder = Decimal(tx.amount) - assigned_total
            if remainder != 0:
                add_amt(None, "income", remainder)

        # Process expenses (amounts are negative in DB by convention)
        for tx in expense_tx:
            splits = get_splits_for_tx(tx)
            assigned_total = sum(splits.values(), Decimal("0")) if splits else Decimal("0")
            if splits:
                for pid, amt in splits.items():
                    add_amt(pid, "expenses", amt)
            remainder = Decimal(tx.amount) - assigned_total
            if remainder != 0:
                add_amt(None, "expenses", remainder)

        # Convert totals to average monthly figures over the observed months
        # Count distinct months in window with data to avoid dividing by zero
        months_count = self._months_in_range(lookback_start, today)
        for pid, vals in per_person.items():
            vals["income"] = (vals.get("income", Decimal("0")) / months_count).quantize(Decimal("0.01"))
            vals["expenses"] = (vals.get("expenses", Decimal("0")) / months_count).quantize(Decimal("0.01"))
        return per_person

    def _expand_series(
        self,
        start_month: date,
        horizon_months: int,
        monthly_by_person: Dict[Optional[int], Dict[str, Decimal]],
    ) -> List[SeriesPoint]:
        """Repeat the monthly baseline amounts across the horizon and aggregate."""
        series: List[SeriesPoint] = []
        for i in range(horizon_months):
            y, m = self._add_months(start_month.year, start_month.month, i)
            d = date(y, m, 1)
            # Sum across persons
            income = sum(vals.get("income", Decimal("0")) for vals in monthly_by_person.values())
            expenses = sum(vals.get("expenses", Decimal("0")) for vals in monthly_by_person.values())
            net_cf = income + expenses  # expenses negative
            series.append(SeriesPoint(date=d, income=income, expenses=expenses, net_cf=net_cf, by_person=None))
        return series

    # ---------------- Adjusters ----------------
    def _apply_adjusters(
        self,
        start_month: date,
        baseline_series: List[SeriesPoint],
        adjusters: List[Any],
        default_split_strategy: str = "equal_split",
    ) -> List[SeriesPoint]:
        """Apply adjusters on top of baseline to produce scenario series."""
        # Copy baseline
        scenario = [SeriesPoint(**p.model_dump()) for p in baseline_series]

        for adj in adjusters or []:
            adj_type = adj.type
            target_pid = getattr(adj, "target_person_id", None)
            start_dt = adj.start_date or start_month
            # Find the month index from which to apply
            start_idx = self._month_index(start_month, start_dt)

            if adj_type == "job_loss":
                # Zero out income for target person from start_idx onward
                for idx in range(start_idx, len(scenario)):
                    # For now, without per-person breakdown in series points, approximate by reducing total income
                    # by that person's share from baseline monthly_by_person
                    # We assume baseline was uniform; so compute per-person income share once
                    # For simplicity, reduce income by 50% if no person provided (household reduction)
                    reduction = self._estimate_person_income_share(target_pid)
                    scenario[idx].income = (scenario[idx].income - reduction).quantize(Decimal("0.01"))
                    scenario[idx].net_cf = scenario[idx].income + scenario[idx].expenses

            elif adj_type == "income_reduction":
                pct = Decimal(str(adj.params.get("percent", 0)))  # e.g., 20 for 20%
                pct = pct / Decimal("100") if pct > 1 else pct
                months = int(adj.params.get("months", 0))
                end_idx = min(len(scenario), start_idx + months) if months > 0 else len(scenario)
                for idx in range(start_idx, end_idx):
                    reduction = (scenario[idx].income * pct).quantize(Decimal("0.01"))
                    scenario[idx].income = scenario[idx].income - reduction
                    scenario[idx].net_cf = scenario[idx].income + scenario[idx].expenses

            elif adj_type == "expense_change":
                pct = Decimal(str(adj.params.get("percent", 0)))
                pct = pct / Decimal("100") if pct > 1 else pct
                months = int(adj.params.get("months", 0))
                end_idx = min(len(scenario), start_idx + months) if months > 0 else len(scenario)
                for idx in range(start_idx, end_idx):
                    change = (scenario[idx].expenses * pct).quantize(Decimal("0.01"))
                    scenario[idx].expenses = scenario[idx].expenses + change
                    scenario[idx].net_cf = scenario[idx].income + scenario[idx].expenses

            elif adj_type == "one_time":
                amt = Decimal(str(adj.params.get("amount", 0)))
                idx = min(start_idx, len(scenario) - 1)
                # If positive => inflow; negative => outflow
                if amt >= 0:
                    scenario[idx].income = scenario[idx].income + amt
                else:
                    scenario[idx].expenses = scenario[idx].expenses + amt
                scenario[idx].net_cf = scenario[idx].income + scenario[idx].expenses

        return scenario

    def _estimate_person_income_share(self, person_id: Optional[int]) -> Decimal:
        """Estimate a single person's monthly income share from recent history (fallback if no split granularity)."""
        # Simple estimate using last 3 months, splits if present, else equal share among observed earners
        today = date.today()
        lookback_start = date(today.year - (1 if today.month <= 3 else 0), (today.month - 3) % 12 or 12, 1)
        q = self.db.query(Transaction).filter(
            Transaction.include_in_analysis == True,
            # Transfers excluded via include_in_analysis=False
            Transaction.transaction_type == "Income",
            Transaction.transaction_date >= lookback_start,
        )
        txs = q.all()
        per_person: Dict[Optional[int], Decimal] = {}
        for tx in txs:
            splits = getattr(tx, "splits", [])
            if splits:
                for s in splits:
                    per_person[s.person_id] = per_person.get(s.person_id, Decimal("0")) + Decimal(s.amount)
            else:
                per_person[None] = per_person.get(None, Decimal("0")) + Decimal(tx.amount)
        months = self._months_in_range(lookback_start, today)
        if not per_person:
            return Decimal("0")
        # If specific person
        if person_id in per_person:
            return (per_person[person_id] / months).quantize(Decimal("0.01"))
        # Fallback: equal split of household income across observed earners
        earners = [pid for pid in per_person.keys() if pid is not None]
        if earners:
            share = (sum(per_person.get(None, Decimal("0")) for _ in earners) / (months * max(len(earners), 1))).quantize(Decimal("0.01"))
            return share
        return (per_person.get(None, Decimal("0")) / months).quantize(Decimal("0.01"))

    # ---------------- KPIs ----------------
    def _compute_kpis(
        self,
        baseline_series: List[SeriesPoint],
        scenario_series: List[SeriesPoint],
        starting_balance: Decimal,
    ) -> ScenarioKPIs:
        # Runway months from starting balance and scenario CF
        balance = starting_balance
        runway_months: Optional[float] = None
        min_balance = balance
        for i, pt in enumerate(scenario_series, start=1):
            balance += pt.net_cf
            if balance < min_balance:
                min_balance = balance
            if runway_months is None and balance <= 0:
                runway_months = float(i)
        # Coverage by person (approximate: use baseline averages; in future, compute per person series)
        coverage_by_person: Dict[int, float] = {}
        # Use fixed obligation categories to estimate fixed_expenses by person (based on historical splits)
        fixed_by_person = self._fixed_obligations_by_person()
        income_by_person = self._income_by_person_monthly()
        for pid, fixed_amt in fixed_by_person.items():
            inc = income_by_person.get(pid, Decimal("0"))
            coverage_by_person[int(pid)] = float((inc / abs(fixed_amt)).quantize(Decimal("0.01"))) if fixed_amt != 0 else float("inf")

        return ScenarioKPIs(
            runway_months=runway_months,
            min_balance=min_balance.quantize(Decimal("0.01")),
            coverage_by_person=coverage_by_person,
            monthly_shortfall_by_person=None,
        )

    def _fixed_obligations_by_person(self) -> Dict[int, Decimal]:
        today = date.today()
        lookback_start = date(today.year - (1 if today.month <= 6 else 0), (today.month - 6) % 12 or 12, 1)
        q = (
            self.db.query(Transaction)
            .join(Category, Transaction.category_id == Category.category_id)
            .filter(
                Transaction.transaction_type == "Expense",
                Transaction.include_in_analysis == True,
                # Transfers excluded via include_in_analysis=False
                Category.is_fixed_obligation == True,
                Transaction.transaction_date >= lookback_start,
            )
        )
        txs = q.all()
        per_person: Dict[int, Decimal] = {}
        for tx in txs:
            splits = getattr(tx, "splits", [])
            if splits:
                for s in splits:
                    per_person[s.person_id] = per_person.get(s.person_id, Decimal("0")) + Decimal(s.amount)
        # Convert to average monthly
        months = self._months_in_range(lookback_start, today)
        return {pid: (amt / months).quantize(Decimal("0.01")) for pid, amt in per_person.items()}

    def _income_by_person_monthly(self) -> Dict[int, Decimal]:
        today = date.today()
        lookback_start = date(today.year - (1 if today.month <= 6 else 0), (today.month - 6) % 12 or 12, 1)
        q = (
            self.db.query(Transaction)
            .filter(
                Transaction.transaction_type == "Income",
                Transaction.include_in_analysis == True,
                # Transfers excluded via include_in_analysis=False
                Transaction.transaction_date >= lookback_start,
            )
        )
        txs = q.all()
        per_person: Dict[int, Decimal] = {}
        for tx in txs:
            splits = getattr(tx, "splits", [])
            for s in splits or []:
                per_person[s.person_id] = per_person.get(s.person_id, Decimal("0")) + Decimal(s.amount)
        months = self._months_in_range(lookback_start, today)
        return {pid: (amt / months).quantize(Decimal("0.01")) for pid, amt in per_person.items()}

    # ---------------- Utilities ----------------
    @staticmethod
    def _add_months(year: int, month: int, add: int) -> (int, int):
        m = month + add
        y = year + (m - 1) // 12
        m = (m - 1) % 12 + 1
        return y, m

    @staticmethod
    def _month_index(start_month: date, dt: date) -> int:
        return (dt.year - start_month.year) * 12 + (dt.month - start_month.month)

    @staticmethod
    def _months_in_range(start: date, end: date) -> int:
        return max((end.year - start.year) * 12 + (end.month - start.month) + 1, 1)

