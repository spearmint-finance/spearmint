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

from .analysis_service import AnalysisService, AnalysisMode, DateRange
from ..database.models import Transaction, Category, Account


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
            }
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
                    "classification": tx.classification.classification_name if tx.classification else "Standard",
                    "source": tx.source
                }
                for tx in transactions
            ]
        }
    
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

