"""
API routes for report generation and export.
"""

from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, timedelta
import io

from ..dependencies import get_db
from ...services.report_service import ReportService, ReportFormat, AnalysisMode
from ..schemas.report import (
    ReportRequest,
    ReportFormatEnum,
    ReportModeEnum,
    SummaryReportResponse,
    IncomeDetailReportResponse,
    ExpenseDetailReportResponse,
    ReconciliationReportResponse,
    BalanceReportResponse,
    CapExReportResponse,
    ReceivablesReportResponse
)

router = APIRouter()


@router.get(
    "/reports/balances",
    response_model=BalanceReportResponse,
    summary="Generate Balance Sheet / Net Worth Report",
    description="""
    Generate a report of all account balances and net worth.
    """
)
def get_balance_report(db: Session = Depends(get_db)):
    """Generate balance sheet report."""
    service = ReportService(db)
    return service.generate_balance_report()


@router.get(
    "/reports/summary",
    response_model=SummaryReportResponse,
    summary="Generate Summary Report",
    description="""
    Generate a comprehensive financial summary report including:
    - Income summary with top categories
    - Expense summary with top categories
    - Cash flow summary
    - Financial health indicators
    
    The report can be generated in JSON or CSV format.
    """
)
def get_summary_report(
    start_date: Optional[date] = Query(None, description="Start date (default: 30 days ago)"),
    end_date: Optional[date] = Query(None, description="End date (default: today)"),
    mode: ReportModeEnum = Query(
        ReportModeEnum.ANALYSIS,
        description="Analysis mode: 'analysis' excludes transfers, 'complete' includes all"
    ),
    format: ReportFormatEnum = Query(
        ReportFormatEnum.JSON,
        description="Export format: 'json' or 'csv'"
    ),
    db: Session = Depends(get_db)
):
    """Generate a summary financial report."""
    service = ReportService(db)
    
    # Convert enum to service enum
    analysis_mode = AnalysisMode.ANALYSIS if mode == ReportModeEnum.ANALYSIS else AnalysisMode.COMPLETE
    
    # Generate report
    report_data = service.generate_summary_report(
        start_date=start_date,
        end_date=end_date,
        mode=analysis_mode
    )
    
    # Handle CSV export
    if format == ReportFormatEnum.CSV:
        csv_data = service.export_to_csv(report_data)
        return StreamingResponse(
            io.StringIO(csv_data),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=summary_report.csv"}
        )
    
    return report_data


@router.get(
    "/reports/income",
    response_model=IncomeDetailReportResponse,
    summary="Generate Income Detail Report",
    description="""
    Generate a detailed income report showing:
    - Total income for the period
    - Transaction count and averages
    - Complete breakdown by category with percentages
    
    Useful for understanding income sources and patterns.
    """
)
def get_income_detail_report(
    start_date: Optional[date] = Query(None, description="Start date (default: 30 days ago)"),
    end_date: Optional[date] = Query(None, description="End date (default: today)"),
    mode: ReportModeEnum = Query(
        ReportModeEnum.ANALYSIS,
        description="Analysis mode: 'analysis' excludes transfers, 'complete' includes all"
    ),
    format: ReportFormatEnum = Query(
        ReportFormatEnum.JSON,
        description="Export format: 'json' or 'csv'"
    ),
    db: Session = Depends(get_db)
):
    """Generate a detailed income report."""
    service = ReportService(db)
    
    analysis_mode = AnalysisMode.ANALYSIS if mode == ReportModeEnum.ANALYSIS else AnalysisMode.COMPLETE
    
    report_data = service.generate_income_detail_report(
        start_date=start_date,
        end_date=end_date,
        mode=analysis_mode
    )
    
    if format == ReportFormatEnum.CSV:
        csv_data = service.export_to_csv(report_data)
        return StreamingResponse(
            io.StringIO(csv_data),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=income_detail_report.csv"}
        )
    
    return report_data


@router.get(
    "/reports/expenses",
    response_model=ExpenseDetailReportResponse,
    summary="Generate Expense Detail Report",
    description="""
    Generate a detailed expense report showing:
    - Total expenses for the period
    - Transaction count and averages
    - Complete breakdown by category with percentages
    
    Useful for understanding spending patterns and identifying areas for optimization.
    """
)
def get_expense_detail_report(
    start_date: Optional[date] = Query(None, description="Start date (default: 30 days ago)"),
    end_date: Optional[date] = Query(None, description="End date (default: today)"),
    mode: ReportModeEnum = Query(
        ReportModeEnum.ANALYSIS,
        description="Analysis mode: 'analysis' excludes transfers, 'complete' includes all"
    ),
    format: ReportFormatEnum = Query(
        ReportFormatEnum.JSON,
        description="Export format: 'json' or 'csv'"
    ),
    db: Session = Depends(get_db)
):
    """Generate a detailed expense report."""
    service = ReportService(db)
    
    analysis_mode = AnalysisMode.ANALYSIS if mode == ReportModeEnum.ANALYSIS else AnalysisMode.COMPLETE
    
    report_data = service.generate_expense_detail_report(
        start_date=start_date,
        end_date=end_date,
        mode=analysis_mode
    )
    
    if format == ReportFormatEnum.CSV:
        csv_data = service.export_to_csv(report_data)
        return StreamingResponse(
            io.StringIO(csv_data),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=expense_detail_report.csv"}
        )
    
    return report_data


@router.get(
    "/reports/reconciliation",
    response_model=ReconciliationReportResponse,
    summary="Generate Reconciliation Report",
    description="""
    Generate a reconciliation report showing ALL transactions including transfers.
    
    This report uses COMPLETE mode to show:
    - All transactions in the period (including transfers, credit card payments, etc.)
    - Complete transaction details for reconciliation
    - Summary statistics
    
    Useful for:
    - Bank reconciliation
    - Verifying all transactions are accounted for
    - Auditing purposes
    - Complete financial picture
    """
)
def get_reconciliation_report(
    start_date: Optional[date] = Query(None, description="Start date (default: 30 days ago)"),
    end_date: Optional[date] = Query(None, description="End date (default: today)"),
    format: ReportFormatEnum = Query(
        ReportFormatEnum.JSON,
        description="Export format: 'json' or 'csv'"
    ),
    db: Session = Depends(get_db)
):
    """Generate a reconciliation report (always uses COMPLETE mode)."""
    service = ReportService(db)
    
    report_data = service.generate_reconciliation_report(
        start_date=start_date,
        end_date=end_date
    )
    
    if format == ReportFormatEnum.CSV:
        csv_data = service.export_to_csv(report_data)
        return StreamingResponse(
            io.StringIO(csv_data),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=reconciliation_report.csv"}
        )

    return report_data


@router.get(
    "/reports/capex",
    response_model=CapExReportResponse,
    summary="Generate Capital Expense (CapEx) Report",
    description="""
    Generate a report of all capital expense transactions.

    Capital expenses are large asset purchases (vehicles, property improvements, equipment)
    that are tracked separately from regular operating expenses.

    This report includes:
    - Total CapEx for the period
    - Breakdown by category (Vehicle, Equipment, Home Improvement, etc.)
    - Full list of CapEx transactions

    CapEx transactions are identified by their classification code (CAPEX, CAPITAL_EXPENSE, etc.)
    or classification name containing 'Capital Expense'.
    """
)
def get_capex_report(
    start_date: Optional[date] = Query(None, description="Start date (default: 1 year ago)"),
    end_date: Optional[date] = Query(None, description="End date (default: today)"),
    format: ReportFormatEnum = Query(
        ReportFormatEnum.JSON,
        description="Export format: 'json' or 'csv'"
    ),
    db: Session = Depends(get_db)
):
    """Generate a capital expense report."""
    service = ReportService(db)

    report_data = service.generate_capex_report(
        start_date=start_date,
        end_date=end_date
    )

    if format == ReportFormatEnum.CSV:
        csv_data = service.export_to_csv(report_data)
        return StreamingResponse(
            io.StringIO(csv_data),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=capex_report.csv"}
        )

    return report_data


@router.get(
    "/reports/receivables",
    response_model=ReceivablesReportResponse,
    summary="Generate Receivables (Reimbursement Tracking) Report",
    description="""
    Generate a report for tracking reimbursable expenses and their status.

    This report helps you track:
    - **Outstanding receivables**: Expenses paid that haven't been reimbursed yet
    - **Recently reimbursed**: Expenses that have been successfully reimbursed
    - **Aging information**: How long receivables have been outstanding

    Receivables are identified by their classification:
    - `REIMB_PAID`: Expense paid that will be reimbursed
    - Linked via `REIMBURSEMENT_PAIR` relationship when reimbursement is received

    Use this report to:
    - Follow up on outstanding expense reports
    - Track reimbursement turnaround time
    - Identify stale receivables that need attention
    """
)
def get_receivables_report(
    start_date: Optional[date] = Query(None, description="Start date (default: 90 days ago)"),
    end_date: Optional[date] = Query(None, description="End date (default: today)"),
    include_reimbursed: bool = Query(
        True,
        description="Include recently reimbursed transactions in the response"
    ),
    format: ReportFormatEnum = Query(
        ReportFormatEnum.JSON,
        description="Export format: 'json' or 'csv'"
    ),
    db: Session = Depends(get_db)
):
    """Generate a receivables (reimbursement tracking) report."""
    service = ReportService(db)

    report_data = service.generate_receivables_report(
        start_date=start_date,
        end_date=end_date,
        include_reimbursed=include_reimbursed
    )

    if format == ReportFormatEnum.CSV:
        csv_data = service.export_to_csv(report_data)
        return StreamingResponse(
            io.StringIO(csv_data),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=receivables_report.csv"}
        )

    return report_data
