"""
Tool Orchestrator for AI Assistant.

Executes tool calls, manages confirmations, and handles undo operations.
"""

from datetime import date, datetime, timezone
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from typing import Dict, Any, Optional, List, Tuple
from uuid import uuid4
import logging

from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from ...database.models import Transaction, Category, Account
from ...database.assistant_models import AssistantActionLog
from ..analysis_service import AnalysisService, DateRange, AnalysisMode
from ..transaction_service import TransactionService
from ..account_service import AccountService
from .tools import READ_ONLY_TOOLS, CONFIRMATION_REQUIRED_TOOLS

logger = logging.getLogger(__name__)


def _convert_decimals(obj: Any) -> Any:
    """Recursively convert Decimal values to float for JSON serialization."""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: _convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_decimals(item) for item in obj]
    return obj


class ToolOrchestrator:
    """
    Executes tool calls and manages action confirmations.

    Responsibilities:
    - Execute read-only query tools directly
    - Generate previews for action tools
    - Handle confirmation flow for modifications
    - Log actions for undo capability
    """

    def __init__(self, db: Session):
        """
        Initialize tool orchestrator.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.analysis_service = AnalysisService(db)
        self.transaction_service = TransactionService(db)
        self.account_service = AccountService(db)

    async def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool and return the result.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        logger.info(f"Executing tool: {tool_name} with args: {arguments}")

        # Route to appropriate handler
        handler = getattr(self, f"_execute_{tool_name}", None)
        if handler:
            try:
                return await handler(arguments)
            except Exception as e:
                logger.error(f"Tool execution error: {e}")
                return {"error": str(e)}
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    def _get_date_range(self, period: Optional[str], date_from: Optional[str] = None, date_to: Optional[str] = None) -> Tuple[date, date]:
        """Convert period string to date range."""
        today = date.today()

        if period == "this_month":
            start = today.replace(day=1)
            end = today
        elif period == "last_month":
            first_of_month = today.replace(day=1)
            end = first_of_month - relativedelta(days=1)
            start = end.replace(day=1)
        elif period == "this_quarter":
            quarter = (today.month - 1) // 3
            start = date(today.year, quarter * 3 + 1, 1)
            end = today
        elif period == "last_quarter":
            quarter = (today.month - 1) // 3
            if quarter == 0:
                start = date(today.year - 1, 10, 1)
                end = date(today.year - 1, 12, 31)
            else:
                start = date(today.year, (quarter - 1) * 3 + 1, 1)
                end_month = quarter * 3
                end = date(today.year, end_month, 1) - relativedelta(days=1)
        elif period == "this_year":
            start = date(today.year, 1, 1)
            end = today
        elif period == "last_year":
            start = date(today.year - 1, 1, 1)
            end = date(today.year - 1, 12, 31)
        elif period == "custom" and date_from and date_to:
            start = date.fromisoformat(date_from)
            end = date.fromisoformat(date_to)
        else:
            # Default to this month
            start = today.replace(day=1)
            end = today

        return start, end

    # ===== Query Tool Implementations =====

    async def _execute_get_spending_summary(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get spending summary for a period."""
        period = args.get("period", "this_month")
        category_name = args.get("category")
        date_from = args.get("date_from")
        date_to = args.get("date_to")

        start_date, end_date = self._get_date_range(period, date_from, date_to)

        # Get category ID if specified
        category_id = None
        if category_name:
            category = self.db.query(Category).filter(
                func.lower(Category.category_name) == category_name.lower()
            ).first()
            if category:
                category_id = category.category_id
            else:
                return {
                    "error": f"Category '{category_name}' not found",
                    "suggestion": "Try searching for transactions to see available categories"
                }

        # Query expenses
        result = self.analysis_service.analyze_expenses(
            date_range=DateRange(start_date=start_date, end_date=end_date),
            mode=AnalysisMode.ANALYSIS
        )

        return {
            "total": float(result.total_expenses),
            "count": result.transaction_count,
            "average": float(result.average_transaction),
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "label": period
            },
            "category": category_name,
            "breakdown": _convert_decimals(result.breakdown_by_category) if not category_name else None
        }

    async def _execute_get_income_summary(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get income summary for a period."""
        period = args.get("period", "this_month")
        category_name = args.get("category")
        date_from = args.get("date_from")
        date_to = args.get("date_to")

        start_date, end_date = self._get_date_range(period, date_from, date_to)

        # Get category ID if specified
        category_id = None
        if category_name:
            category = self.db.query(Category).filter(
                func.lower(Category.category_name) == category_name.lower()
            ).first()
            if category:
                category_id = category.category_id

        # Query income
        result = self.analysis_service.analyze_income(
            date_range=DateRange(start_date=start_date, end_date=end_date),
            mode=AnalysisMode.ANALYSIS
        )

        return {
            "total": float(result.total_income),
            "count": result.transaction_count,
            "average": float(result.average_transaction),
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "label": period
            },
            "category": category_name,
            "breakdown": _convert_decimals(result.breakdown_by_category) if not category_name else None
        }

    async def _execute_get_top_categories(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get top categories by spending or income."""
        category_type = args.get("type", "expense")
        limit = min(args.get("limit", 5), 10)
        period = args.get("period", "this_month")

        start_date, end_date = self._get_date_range(period)

        if category_type == "expense":
            result = self.analysis_service.analyze_expenses(
                date_range=DateRange(start_date=start_date, end_date=end_date),
                mode=AnalysisMode.ANALYSIS
            )
            categories = _convert_decimals(result.top_categories[:limit])
        else:
            result = self.analysis_service.analyze_income(
                date_range=DateRange(start_date=start_date, end_date=end_date),
                mode=AnalysisMode.ANALYSIS
            )
            # Convert breakdown to ranked list
            breakdown = _convert_decimals(result.breakdown_by_category)
            categories = sorted(
                [{"name": k, "total": v.get("total", 0), "count": v.get("count", 0)}
                 for k, v in breakdown.items()],
                key=lambda x: x["total"],
                reverse=True
            )[:limit]

        return {
            "type": category_type,
            "categories": categories,
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "label": period
            }
        }

    async def _execute_search_transactions(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search for transactions."""
        limit = min(args.get("limit", 20), 50)

        # Build query
        query = self.db.query(Transaction).join(Category, isouter=True)

        if args.get("merchant"):
            query = query.filter(
                Transaction.source.ilike(f"%{args['merchant']}%")
            )

        if args.get("description"):
            query = query.filter(
                Transaction.description.ilike(f"%{args['description']}%")
            )

        if args.get("category"):
            query = query.filter(
                func.lower(Category.category_name) == args["category"].lower()
            )

        if args.get("amount_min") is not None:
            query = query.filter(Transaction.amount >= args["amount_min"])

        if args.get("amount_max") is not None:
            query = query.filter(Transaction.amount <= args["amount_max"])

        if args.get("date_from"):
            query = query.filter(
                Transaction.transaction_date >= date.fromisoformat(args["date_from"])
            )

        if args.get("date_to"):
            query = query.filter(
                Transaction.transaction_date <= date.fromisoformat(args["date_to"])
            )

        if args.get("is_uncategorized"):
            # Find uncategorized category
            uncategorized = self.db.query(Category).filter(
                Category.category_name == "Uncategorized"
            ).first()
            if uncategorized:
                query = query.filter(
                    Transaction.category_id == uncategorized.category_id
                )

        # Execute query
        transactions = query.order_by(
            Transaction.transaction_date.desc()
        ).limit(limit).all()

        return {
            "transactions": [
                {
                    "id": t.transaction_id,
                    "date": t.transaction_date.isoformat(),
                    "amount": float(t.amount),
                    "type": t.transaction_type,
                    "source": t.source,
                    "description": t.description,
                    "category": t.category.category_name if t.category else None
                }
                for t in transactions
            ],
            "count": len(transactions),
            "limit": limit
        }

    def _get_account_balance_value(self, account_id: int) -> float:
        """Get the current balance for an account from the most recent snapshot."""
        balance = self.account_service.get_current_balance(account_id)
        if balance:
            return float(balance.total_balance)
        return 0.0

    async def _execute_get_account_balance(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get account balance(s)."""
        account_name = args.get("account_name")
        include_all = args.get("include_all", False)

        if include_all or not account_name:
            accounts = self.db.query(Account).filter(
                Account.is_active == True
            ).all()

            account_data = []
            total = 0.0
            for a in accounts:
                bal = self._get_account_balance_value(a.account_id)
                total += bal
                account_data.append({
                    "name": a.account_name,
                    "type": a.account_type,
                    "balance": bal,
                    "institution": a.institution_name,
                })

            return {
                "accounts": account_data,
                "total_balance": total,
            }
        else:
            account = self.db.query(Account).filter(
                func.lower(Account.account_name) == account_name.lower()
            ).first()

            if not account:
                return {"error": f"Account '{account_name}' not found"}

            return {
                "name": account.account_name,
                "type": account.account_type,
                "balance": self._get_account_balance_value(account.account_id),
                "institution": account.institution_name,
            }

    async def _execute_get_cash_flow(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get cash flow for a period."""
        period = args.get("period", "this_month")
        include_breakdown = args.get("include_breakdown", True)

        start_date, end_date = self._get_date_range(period)

        cash_flow = self.analysis_service.analyze_cash_flow(
            date_range=DateRange(start_date=start_date, end_date=end_date),
            mode=AnalysisMode.ANALYSIS
        )

        result = {
            "net_cash_flow": float(cash_flow.net_cash_flow),
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "label": period
            }
        }

        if include_breakdown:
            result["income"] = {
                "total": float(cash_flow.total_income),
                "count": cash_flow.income_count
            }
            result["expenses"] = {
                "total": float(cash_flow.total_expenses),
                "count": cash_flow.expense_count
            }

        return result

    async def _execute_compare_periods(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Compare metrics between two periods."""
        metric = args["metric"]
        category_name = args.get("category")
        period_1 = args["period_1"]
        period_2 = args["period_2"]

        start_1, end_1 = self._get_date_range(period_1)
        start_2, end_2 = self._get_date_range(period_2)

        # Get category ID if specified
        category_id = None
        if category_name:
            category = self.db.query(Category).filter(
                func.lower(Category.category_name) == category_name.lower()
            ).first()
            if category:
                category_id = category.category_id

        # Get values for each period
        if metric == "spending":
            result_1 = self.analysis_service.analyze_expenses(
                date_range=DateRange(start_date=start_1, end_date=end_1),
                mode=AnalysisMode.ANALYSIS
            )
            result_2 = self.analysis_service.analyze_expenses(
                date_range=DateRange(start_date=start_2, end_date=end_2),
                mode=AnalysisMode.ANALYSIS
            )
            value_1 = float(result_1.total_expenses)
            value_2 = float(result_2.total_expenses)
        elif metric == "income":
            result_1 = self.analysis_service.analyze_income(
                date_range=DateRange(start_date=start_1, end_date=end_1),
                mode=AnalysisMode.ANALYSIS
            )
            result_2 = self.analysis_service.analyze_income(
                date_range=DateRange(start_date=start_2, end_date=end_2),
                mode=AnalysisMode.ANALYSIS
            )
            value_1 = float(result_1.total_income)
            value_2 = float(result_2.total_income)
        else:  # net_cash_flow
            cf_1 = self.analysis_service.analyze_cash_flow(
                date_range=DateRange(start_date=start_1, end_date=end_1),
                mode=AnalysisMode.ANALYSIS
            )
            cf_2 = self.analysis_service.analyze_cash_flow(
                date_range=DateRange(start_date=start_2, end_date=end_2),
                mode=AnalysisMode.ANALYSIS
            )
            value_1 = float(cf_1.net_cash_flow)
            value_2 = float(cf_2.net_cash_flow)

        # Calculate difference
        difference = value_1 - value_2
        if value_2 != 0:
            percent_change = ((value_1 - value_2) / abs(value_2)) * 100
        else:
            percent_change = 100.0 if value_1 > 0 else -100.0 if value_1 < 0 else 0.0

        return {
            "metric": metric,
            "category": category_name,
            "period_1": {
                "label": period_1,
                "start": start_1.isoformat(),
                "end": end_1.isoformat(),
                "value": value_1
            },
            "period_2": {
                "label": period_2,
                "start": start_2.isoformat(),
                "end": end_2.isoformat(),
                "value": value_2
            },
            "difference": difference,
            "percent_change": round(percent_change, 1)
        }

    async def _execute_create_navigation_link(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a navigation link for the frontend."""
        page = args["page"]
        filters = args.get("filters", {})
        label = args.get("label", f"View {page}")

        # Build URL with query params
        url = f"/{page}"
        if filters:
            params = "&".join(f"{k}={v}" for k, v in filters.items() if v)
            if params:
                url += f"?{params}"

        return {
            "type": "navigation",
            "url": url,
            "label": label,
            "page": page,
            "filters": filters
        }

    # ===== Agent Tool Implementations =====

    async def _execute_get_budget_advice(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke the Budget Advisor A2A agent for spending analysis and advice."""
        from ...agents.registry import AgentRegistry

        months = min(args.get("months", 6), 12)
        top_categories = min(args.get("top_categories", 5), 10)

        agent = AgentRegistry.get("budget-advisor")
        if not agent:
            return {"error": "Budget Advisor agent is not registered"}

        try:
            result = await agent.invoke(
                "analyze-spending",
                {"months": months, "top_categories": top_categories},
                None,
                self.db,
            )
            return _convert_decimals(result)
        except Exception as e:
            logger.error(f"Budget Advisor error: {e}")
            return {"error": f"Budget Advisor failed: {str(e)}"}

    # ===== Action Tool Implementations (Phase 2) =====

    async def _execute_propose_categorization(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Propose categorizing transactions (requires confirmation)."""
        transaction_ids = args.get("transaction_ids", [])
        merchant_pattern = args.get("merchant_pattern")
        category_name = args["category_name"]

        # Find target category
        category = self.db.query(Category).filter(
            func.lower(Category.category_name) == category_name.lower()
        ).first()

        if not category:
            return {"error": f"Category '{category_name}' not found"}

        # Find transactions to update
        if transaction_ids:
            transactions = self.db.query(Transaction).filter(
                Transaction.transaction_id.in_(transaction_ids)
            ).all()
        elif merchant_pattern:
            transactions = self.db.query(Transaction).filter(
                Transaction.source.ilike(f"%{merchant_pattern}%")
            ).all()
        else:
            return {"error": "Must provide transaction_ids or merchant_pattern"}

        if not transactions:
            return {"error": "No matching transactions found"}

        return {
            "type": "action_proposal",
            "action": "categorize",
            "requires_confirmation": True,
            "preview": {
                "transaction_count": len(transactions),
                "category": category_name,
                "total_amount": sum(float(t.amount) for t in transactions),
                "transactions": [
                    {
                        "id": t.transaction_id,
                        "date": t.transaction_date.isoformat(),
                        "source": t.source,
                        "amount": float(t.amount),
                        "current_category": t.category.category_name if t.category else None
                    }
                    for t in transactions[:10]  # Show first 10
                ],
                "more_count": max(0, len(transactions) - 10)
            },
            "payload": {
                "transaction_ids": [t.transaction_id for t in transactions],
                "category_id": category.category_id,
                "category_name": category_name
            }
        }

    async def _execute_propose_category_rule(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Propose creating a category rule (requires confirmation)."""
        pattern = args["pattern"]
        pattern_type = args["pattern_type"]
        category_name = args["category_name"]
        rule_name = args.get("rule_name", f"Auto-categorize {pattern}")

        # Find target category
        category = self.db.query(Category).filter(
            func.lower(Category.category_name) == category_name.lower()
        ).first()

        if not category:
            return {"error": f"Category '{category_name}' not found"}

        # Count matching transactions
        if pattern_type == "contains":
            match_query = Transaction.source.ilike(f"%{pattern}%")
        elif pattern_type == "starts_with":
            match_query = Transaction.source.ilike(f"{pattern}%")
        elif pattern_type == "ends_with":
            match_query = Transaction.source.ilike(f"%{pattern}")
        elif pattern_type == "exact":
            match_query = func.lower(Transaction.source) == pattern.lower()
        else:
            match_query = Transaction.source.ilike(f"%{pattern}%")

        matching_count = self.db.query(Transaction).filter(match_query).count()

        return {
            "type": "action_proposal",
            "action": "create_rule",
            "requires_confirmation": True,
            "preview": {
                "rule_name": rule_name,
                "pattern": pattern,
                "pattern_type": pattern_type,
                "category": category_name,
                "matching_transactions": matching_count
            },
            "payload": {
                "pattern": pattern,
                "pattern_type": pattern_type,
                "category_id": category.category_id,
                "category_name": category_name,
                "rule_name": rule_name
            }
        }
