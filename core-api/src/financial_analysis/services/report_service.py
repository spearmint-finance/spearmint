"""
Report Service for generating financial reports and exports.
"""

from datetime import date, timedelta
from typing import Dict, List, Optional, Any
from decimal import Decimal
from enum import Enum
import csv
import io

from sqlalchemy.orm import Session
from sqlalchemy import func

from sqlalchemy import select

from .analysis_service import AnalysisService, AnalysisMode, DateRange
from ..database.models import Transaction, Category, Account, TransactionRelationship, Tag, TransactionTag


class ReportFormat(str, Enum):
    """Report export formats."""
    JSON = "json"
    CSV = "csv"
    # EXCEL = "excel"  # Future: requires openpyxl
    # PDF = "pdf"      # Future: requires reportlab


class ReportType(str, Enum):
    """Types of reports available."""
    SUMMARY = "summary"
    INCOME_DETAIL = "income_detail"
    EXPENSE_DETAIL = "expense_detail"
    CASHFLOW = "cashflow"
    CATEGORY_BREAKDOWN = "category_breakdown"
    RECONCILIATION = "reconciliation"
    BALANCE = "balance"


class ReportService:
    """Service for generating financial reports and exports."""
    
    def __init__(self, db: Session):
        """Initialize report service."""
        self.db = db
        self.analysis_service = AnalysisService(db)
    
    def generate_balance_report(self) -> Dict[str, Any]:
        """
        Generate a balance report showing net worth and account statuses.
        Based on check_account_balances.py logic.
        """
        accounts = self.db.query(Account).order_by(Account.account_name).all()
        
        total_assets = Decimal(0)
        total_liabilities = Decimal(0)
        account_details = []
        potential_issues = []

        for account in accounts:
            balance = account.current_balance or Decimal(0)
            
            # Calculate transaction totals
            income_sum = self.db.query(func.sum(Transaction.amount)).filter(
                Transaction.account_id == account.account_id,
                Transaction.transaction_type == 'Income'
            ).scalar() or 0
            
            expense_sum = self.db.query(func.sum(Transaction.amount)).filter(
                Transaction.account_id == account.account_id,
                Transaction.transaction_type == 'Expense'
            ).scalar() or 0
            
            transaction_count = self.db.query(func.count(Transaction.transaction_id)).filter(
                Transaction.account_id == account.account_id
            ).scalar() or 0

            # Classify Asset vs Liability
            if account.account_type in ['checking', 'savings', 'brokerage', '401k', 'investment']:
                total_assets += balance
            elif account.account_type in ['credit_card', 'loan']:
                total_liabilities += balance
            
            account_details.append({
                "account_name": account.account_name,
                "account_type": account.account_type,
                "balance": float(balance),
                "transaction_count": transaction_count,
                "income_sum": float(income_sum),
                "expense_sum": float(expense_sum)
            })
            
            # Check for potential issues (Logic from legacy script)
            if account.account_type in ['credit_card'] and balance > 0:
                potential_issues.append(f"{account.account_name} has positive balance (usually Credit Cards are negative)")

        return {
            "report_type": "balance",
            "summary": {
                "total_assets": float(total_assets),
                "total_liabilities": float(total_liabilities),
                "net_worth": float(total_assets + total_liabilities)
            },
            "accounts": account_details,
            "potential_issues": potential_issues
        }

    def generate_summary_report(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        mode: AnalysisMode = AnalysisMode.ANALYSIS
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive financial summary report.
        
        Args:
            start_date: Start of reporting period (default: 1 month ago)
            end_date: End of reporting period (default: today)
            mode: Analysis mode (analysis or complete)
            
        Returns:
            Dictionary containing summary report data
        """
        # Set default dates
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        date_range = DateRange(start_date=start_date, end_date=end_date)
        
        # Get analysis data
        income_data = self.analysis_service.analyze_income(date_range=date_range, mode=mode)
        expense_data = self.analysis_service.analyze_expenses(date_range=date_range, mode=mode)
        cashflow_data = self.analysis_service.analyze_cash_flow(date_range=date_range, mode=mode)
        health_data = self.analysis_service.get_financial_health_indicators(date_range=date_range)

        # Get total CapEx for the period
        total_capex = self.get_total_capex(start_date=start_date, end_date=end_date)

        # Get total outstanding receivables
        total_receivables = self.get_total_receivables(start_date=start_date, end_date=end_date)

        return {
            "report_type": "summary",
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": (end_date - start_date).days + 1
            },
            "mode": mode.value,
            "income": {
                "total": float(income_data.total_income),
                "transaction_count": income_data.transaction_count,
                "average_transaction": float(income_data.average_transaction),
                "top_categories": [
                    {
                        "category": cat_name,
                        "amount": float(cat_data["total"]),
                        "percentage": cat_data["percentage"]
                    }
                    for cat_name, cat_data in sorted(
                        income_data.breakdown_by_category.items(),
                        key=lambda x: x[1]["total"],
                        reverse=True
                    )[:5]
                ]
            },
            "expenses": {
                "total": float(expense_data.total_expenses),
                "transaction_count": expense_data.transaction_count,
                "average_transaction": float(expense_data.average_transaction),
                "top_categories": [
                    {
                        "category": cat["category"],
                        "amount": float(cat["amount"]),
                        "percentage": cat["percentage"]
                    }
                    for cat in expense_data.top_categories[:5]
                ]
            },
            "cashflow": {
                "net_cashflow": float(cashflow_data.net_cash_flow),
                "total_income": float(cashflow_data.total_income),
                "total_expenses": float(cashflow_data.total_expenses)
            },
            "health_indicators": {
                "income_to_expense_ratio": health_data.income_to_expense_ratio,
                "savings_rate": health_data.savings_rate,
                "average_daily_income": float(health_data.average_daily_income),
                "average_daily_expense": float(health_data.average_daily_expense),
                "average_daily_cashflow": float(health_data.net_daily_cash_flow)
            },
            "total_capex": total_capex,
            "total_receivables": total_receivables
        }
    
    def generate_income_detail_report(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        mode: AnalysisMode = AnalysisMode.ANALYSIS
    ) -> Dict[str, Any]:
        """Generate detailed income report with all categories."""
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        date_range = DateRange(start_date=start_date, end_date=end_date)
        income_data = self.analysis_service.analyze_income(date_range=date_range, mode=mode)
        
        return {
            "report_type": "income_detail",
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": (end_date - start_date).days + 1
            },
            "mode": mode.value,
            "total_income": float(income_data.total_income),
            "transaction_count": income_data.transaction_count,
            "average_transaction": float(income_data.average_transaction),
            "categories": [
                {
                    "category": cat_name,
                    "total": float(cat_data["total"]),
                    "count": cat_data["count"],
                    "average": float(cat_data["average"]),
                    "percentage": cat_data["percentage"]
                }
                for cat_name, cat_data in sorted(
                    income_data.breakdown_by_category.items(),
                    key=lambda x: x[1]["total"],
                    reverse=True
                )
            ]
        }
    
    def generate_expense_detail_report(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        mode: AnalysisMode = AnalysisMode.ANALYSIS
    ) -> Dict[str, Any]:
        """Generate detailed expense report with all categories."""
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        date_range = DateRange(start_date=start_date, end_date=end_date)
        expense_data = self.analysis_service.analyze_expenses(date_range=date_range, mode=mode)
        
        return {
            "report_type": "expense_detail",
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": (end_date - start_date).days + 1
            },
            "mode": mode.value,
            "total_expenses": float(expense_data.total_expenses),
            "transaction_count": expense_data.transaction_count,
            "average_transaction": float(expense_data.average_transaction),
            "categories": [
                {
                    "category": cat_name,
                    "total": float(cat_data["total"]),
                    "count": cat_data["count"],
                    "average": float(cat_data["average"]),
                    "percentage": cat_data["percentage"]
                }
                for cat_name, cat_data in sorted(
                    expense_data.breakdown_by_category.items(),
                    key=lambda x: x[1]["total"],
                    reverse=True
                )
            ]
        }
    
    def generate_reconciliation_report(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Generate reconciliation report showing all transactions including transfers.
        
        This report uses COMPLETE mode to show all transactions for reconciliation purposes.
        """
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        date_range = DateRange(start_date=start_date, end_date=end_date)
        
        # Use COMPLETE mode to include all transactions
        income_data = self.analysis_service.analyze_income(date_range=date_range, mode=AnalysisMode.COMPLETE)
        expense_data = self.analysis_service.analyze_expenses(date_range=date_range, mode=AnalysisMode.COMPLETE)
        cashflow_data = self.analysis_service.analyze_cash_flow(date_range=date_range, mode=AnalysisMode.COMPLETE)
        
        # Get all transactions for the period
        transactions = self.db.query(Transaction).filter(
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).order_by(Transaction.transaction_date.desc()).all()
        
        return {
            "report_type": "reconciliation",
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": (end_date - start_date).days + 1
            },
            "mode": "complete",
            "summary": {
                "total_income": float(income_data.total_income),
                "total_expenses": float(expense_data.total_expenses),
                "net_cashflow": float(cashflow_data.net_cash_flow),
                "transaction_count": len(transactions)
            },
            "transactions": [
                {
                    "date": tx.transaction_date.isoformat(),
                    "description": tx.description,
                    "category": tx.category.category_name if tx.category else "Uncategorized",
                    "type": tx.transaction_type,
                    "amount": float(tx.amount),
                    "classification": ", ".join(t.tag_name for t in tx.tags) if tx.tags else "Standard",
                    "source": tx.source
                }
                for tx in transactions
            ]
        }
    
    def generate_capex_report(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Generate a Capital Expense (CapEx) report.

        CapEx transactions are identified by:
        - Classification code containing 'CAPEX' or 'CAPITAL_EXPENSE'
        - OR classification name = 'Capital Expense'

        Args:
            start_date: Start of reporting period (default: 1 year ago)
            end_date: End of reporting period (default: today)

        Returns:
            Dictionary containing CapEx report data
        """
        # Set default dates (1 year for CapEx since they're less frequent)
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=365)

        # Query CapEx transactions - find transactions tagged 'capital-expense'
        capex_subq = (
            select(TransactionTag.transaction_id)
            .join(Tag, TransactionTag.tag_id == Tag.tag_id)
            .where(Tag.tag_name == 'capital-expense')
            .subquery()
        )
        query = self.db.query(Transaction).outerjoin(
            Category,
            Transaction.category_id == Category.category_id
        ).filter(
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date,
            Transaction.transaction_id.in_(select(capex_subq))
        ).order_by(Transaction.transaction_date.desc())

        transactions = query.all()

        # Calculate totals
        total_capex = sum(abs(tx.amount) for tx in transactions)
        transaction_count = len(transactions)
        average_transaction = total_capex / transaction_count if transaction_count > 0 else Decimal(0)

        # Group by category
        category_totals: Dict[str, Dict[str, Any]] = {}
        for tx in transactions:
            cat_name = tx.category.category_name if tx.category else "Uncategorized"
            if cat_name not in category_totals:
                category_totals[cat_name] = {"total": Decimal(0), "count": 0}
            category_totals[cat_name]["total"] += abs(tx.amount)
            category_totals[cat_name]["count"] += 1

        # Build category summary with percentages
        by_category = []
        for cat_name, data in sorted(category_totals.items(), key=lambda x: x[1]["total"], reverse=True):
            percentage = (float(data["total"]) / float(total_capex) * 100) if total_capex > 0 else 0
            by_category.append({
                "category": cat_name,
                "total": float(data["total"]),
                "count": data["count"],
                "percentage": round(percentage, 2)
            })

        # Build transaction list
        tx_list = [
            {
                "transaction_id": tx.transaction_id,
                "date": tx.transaction_date.isoformat(),
                "description": tx.description,
                "amount": float(tx.amount),
                "category": tx.category.category_name if tx.category else "Uncategorized",
                "classification": ", ".join(t.tag_name for t in tx.tags) if tx.tags else "capital-expense",
                "notes": tx.notes
            }
            for tx in transactions
        ]

        return {
            "report_type": "capex",
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": (end_date - start_date).days + 1
            },
            "summary": {
                "total_capex": float(total_capex),
                "transaction_count": transaction_count,
                "average_transaction": float(average_transaction)
            },
            "by_category": by_category,
            "transactions": tx_list
        }

    def get_total_capex(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> float:
        """
        Get the total capital expenditure for a period.

        This is a lightweight method for use in summary reports.

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            Total CapEx amount as float
        """
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=30)

        capex_subq = (
            select(TransactionTag.transaction_id)
            .join(Tag, TransactionTag.tag_id == Tag.tag_id)
            .where(Tag.tag_name == 'capital-expense')
            .subquery()
        )
        result = self.db.query(func.sum(func.abs(Transaction.amount))).filter(
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date,
            Transaction.transaction_id.in_(select(capex_subq))
        ).scalar()

        return float(result) if result else 0.0

    def generate_receivables_report(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        include_reimbursed: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a Receivables report for reimbursement tracking.

        Receivables are transactions classified as REIMB_PAID that are awaiting
        reimbursement. The report tracks:
        - Outstanding receivables (not yet reimbursed)
        - Recently reimbursed transactions
        - Aging information

        Args:
            start_date: Start of reporting period (default: 90 days ago)
            end_date: End of reporting period (default: today)
            include_reimbursed: Include recently reimbursed transactions

        Returns:
            Dictionary containing receivables report data
        """
        # Set default dates (90 days for receivables tracking)
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=90)

        # Find transactions tagged 'reimbursable'
        reimbursable_subq = (
            select(TransactionTag.transaction_id)
            .join(Tag, TransactionTag.tag_id == Tag.tag_id)
            .where(Tag.tag_name == 'reimbursable')
            .subquery()
        )

        # Query all reimbursable transactions in the period
        expense_query = self.db.query(Transaction).outerjoin(
            Category,
            Transaction.category_id == Category.category_id
        ).filter(
            Transaction.transaction_id.in_(select(reimbursable_subq)),
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).order_by(Transaction.transaction_date.desc())

        expenses = expense_query.all()

        # Get all reimbursement relationships for these expenses
        expense_ids = [tx.transaction_id for tx in expenses]

        # Find linked reimbursements via TransactionRelationship
        reimbursement_links = {}
        if expense_ids:
            relationships = self.db.query(TransactionRelationship).filter(
                TransactionRelationship.relationship_type == 'REIMBURSEMENT_PAIR',
                (TransactionRelationship.transaction_id_1.in_(expense_ids)) |
                (TransactionRelationship.transaction_id_2.in_(expense_ids))
            ).all()

            for rel in relationships:
                # Determine which is the expense and which is the reimbursement
                if rel.transaction_id_1 in expense_ids:
                    reimbursement_links[rel.transaction_id_1] = rel.transaction_id_2
                else:
                    reimbursement_links[rel.transaction_id_2] = rel.transaction_id_1

        # Separate into outstanding and reimbursed
        outstanding = []
        recently_reimbursed = []
        total_outstanding = Decimal(0)
        total_reimbursed = Decimal(0)
        days_outstanding_sum = 0
        oldest_outstanding_days = 0

        today = date.today()

        for tx in expenses:
            days_since = (today - tx.transaction_date).days
            is_reimbursed = tx.transaction_id in reimbursement_links

            tx_data = {
                "transaction_id": tx.transaction_id,
                "date": tx.transaction_date.isoformat(),
                "description": tx.description,
                "amount": float(tx.amount),
                "category": tx.category.category_name if tx.category else "Uncategorized",
                "classification": ", ".join(t.tag_name for t in tx.tags) if tx.tags else "reimbursable",
                "days_outstanding": days_since,
                "is_reimbursed": is_reimbursed,
                "reimbursement_id": reimbursement_links.get(tx.transaction_id),
                "notes": tx.notes
            }

            if is_reimbursed:
                recently_reimbursed.append(tx_data)
                total_reimbursed += abs(tx.amount)
            else:
                outstanding.append(tx_data)
                total_outstanding += abs(tx.amount)
                days_outstanding_sum += days_since
                if days_since > oldest_outstanding_days:
                    oldest_outstanding_days = days_since

        outstanding_count = len(outstanding)
        reimbursed_count = len(recently_reimbursed)
        avg_days_outstanding = days_outstanding_sum / outstanding_count if outstanding_count > 0 else 0

        # Group outstanding by category
        category_totals: Dict[str, Dict[str, Any]] = {}
        for tx in outstanding:
            cat_name = tx["category"]
            if cat_name not in category_totals:
                category_totals[cat_name] = {"total": 0.0, "count": 0}
            category_totals[cat_name]["total"] += abs(tx["amount"])
            category_totals[cat_name]["count"] += 1

        # Build category summary with percentages
        by_category = []
        for cat_name, data in sorted(category_totals.items(), key=lambda x: x[1]["total"], reverse=True):
            percentage = (data["total"] / float(total_outstanding) * 100) if total_outstanding > 0 else 0
            by_category.append({
                "category": cat_name,
                "total": data["total"],
                "count": data["count"],
                "percentage": round(percentage, 2)
            })

        return {
            "report_type": "receivables",
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": (end_date - start_date).days + 1
            },
            "summary": {
                "total_outstanding": float(total_outstanding),
                "total_reimbursed": float(total_reimbursed),
                "outstanding_count": outstanding_count,
                "reimbursed_count": reimbursed_count,
                "average_days_outstanding": round(avg_days_outstanding, 1),
                "oldest_outstanding_days": oldest_outstanding_days
            },
            "by_category": by_category,
            "outstanding": outstanding,
            "recently_reimbursed": recently_reimbursed if include_reimbursed else []
        }

    def _empty_receivables_report(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Return an empty receivables report structure."""
        return {
            "report_type": "receivables",
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": (end_date - start_date).days + 1
            },
            "summary": {
                "total_outstanding": 0.0,
                "total_reimbursed": 0.0,
                "outstanding_count": 0,
                "reimbursed_count": 0,
                "average_days_outstanding": 0.0,
                "oldest_outstanding_days": 0
            },
            "by_category": [],
            "outstanding": [],
            "recently_reimbursed": []
        }

    def get_total_receivables(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> float:
        """
        Get the total outstanding receivables amount.

        This is a lightweight method for use in summary reports.

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            Total outstanding receivables amount as float
        """
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=90)

        # Find transactions tagged 'reimbursable'
        reimbursable_subq = (
            select(TransactionTag.transaction_id)
            .join(Tag, TransactionTag.tag_id == Tag.tag_id)
            .where(Tag.tag_name == 'reimbursable')
            .subquery()
        )

        # Get all reimbursable expense IDs
        expenses = self.db.query(Transaction.transaction_id, Transaction.amount).filter(
            Transaction.transaction_id.in_(select(reimbursable_subq)),
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).all()

        if not expenses:
            return 0.0

        expense_ids = [e.transaction_id for e in expenses]

        # Find which ones are already linked
        linked_ids = set()
        relationships = self.db.query(TransactionRelationship).filter(
            TransactionRelationship.relationship_type == 'REIMBURSEMENT_PAIR',
            (TransactionRelationship.transaction_id_1.in_(expense_ids)) |
            (TransactionRelationship.transaction_id_2.in_(expense_ids))
        ).all()

        for rel in relationships:
            linked_ids.add(rel.transaction_id_1)
            linked_ids.add(rel.transaction_id_2)

        # Sum only unlinked (outstanding) expenses
        total = sum(abs(e.amount) for e in expenses if e.transaction_id not in linked_ids)
        return float(total)

    def export_to_csv(self, report_data: Dict[str, Any]) -> str:
        """
        Export report data to CSV format.

        Args:
            report_data: Report data dictionary

        Returns:
            CSV string
        """
        output = io.StringIO()
        
        report_type = report_data.get("report_type", "unknown")
        
        if report_type == "reconciliation":
            # Export transactions as CSV
            writer = csv.DictWriter(
                output,
                fieldnames=["date", "description", "category", "type", "amount", "classification", "source"]
            )
            writer.writeheader()
            writer.writerows(report_data["transactions"])
        
        elif report_type in ["income_detail", "expense_detail"]:
            # Export category breakdown as CSV
            writer = csv.DictWriter(
                output,
                fieldnames=["category", "total", "count", "average", "percentage"]
            )
            writer.writeheader()
            writer.writerows(report_data["categories"])

        elif report_type == "capex":
            # Export CapEx transactions as CSV
            writer = csv.DictWriter(
                output,
                fieldnames=["transaction_id", "date", "description", "amount", "category", "classification", "notes"]
            )
            writer.writeheader()
            writer.writerows(report_data["transactions"])

        elif report_type == "receivables":
            # Export receivables (outstanding) as CSV
            writer = csv.DictWriter(
                output,
                fieldnames=["transaction_id", "date", "description", "amount", "category", "classification",
                           "days_outstanding", "is_reimbursed", "reimbursement_id", "notes"]
            )
            writer.writeheader()
            writer.writerows(report_data["outstanding"])

        else:
            # For summary and other reports, create a simple key-value CSV
            writer = csv.writer(output)
            writer.writerow(["Report Type", report_type])
            writer.writerow(["Period", f"{report_data['period']['start_date']} to {report_data['period']['end_date']}"])
            writer.writerow([])
            
            # Flatten the report data
            for key, value in report_data.items():
                if key not in ["report_type", "period"]:
                    writer.writerow([key, str(value)])
        
        return output.getvalue()

