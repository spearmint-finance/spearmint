"""
Integration tests for end-to-end workflows.

Tests complete user workflows from data import through analysis,
projections, and reporting.
"""

import pytest
from decimal import Decimal
from datetime import date, timedelta


class TestCompleteUserWorkflow:
    """Test complete user workflow from start to finish."""
    
    def test_complete_workflow_import_to_report(self, client, sample_categories):
        """
        Test complete workflow:
        1. Import transactions
        2. Classify transactions
        3. Analyze income/expenses
        4. Generate projections
        5. Create reports
        """
        # Step 1: Create transactions
        today = date.today()
        transactions = []
        
        for i in range(10):
            transaction_data = {
                "transaction_date": (today - timedelta(days=i*3)).isoformat(),
                "description": f"Transaction {i}",
                "amount": 100.00 * (i + 1),
                "transaction_type": "Income" if i % 2 == 0 else "Expense",
                "category_id": 1 if i % 2 == 0 else 2
            }
            
            response = client.post("/api/transactions", json=transaction_data)
            assert response.status_code == 201
            transactions.append(response.json())
        
        # Step 2: Analyze income
        income_response = client.get("/api/analysis/income", params={"mode": "analysis"})
        assert income_response.status_code == 200
        income_data = income_response.json()
        assert income_data["transaction_count"] == 5  # Half are income
        
        # Step 3: Analyze expenses
        expense_response = client.get("/api/analysis/expenses", params={"mode": "analysis"})
        assert expense_response.status_code == 200
        expense_data = expense_response.json()
        assert expense_data["transaction_count"] == 5  # Half are expenses
        
        # Step 4: Get cash flow
        cashflow_response = client.get("/api/analysis/cashflow", params={"mode": "analysis"})
        assert cashflow_response.status_code == 200
        cashflow_data = cashflow_response.json()
        # Verify cashflow is calculated (Income: 2500, Expense: 3000, Net: -500)
        assert Decimal(str(cashflow_data["net_cash_flow"])) == Decimal("-500.00")
        
        # Step 5: Generate income projection
        projection_response = client.get(
            "/api/projections/income",
            params={
                "projection_days": 3,
                "method": "linear_regression"
            }
        )
        assert projection_response.status_code == 200
        projection_data = projection_response.json()
        # Verify projection response has required fields
        assert "projected_total" in projection_data
        assert "daily_projections" in projection_data
        
        # Step 6: Generate summary report
        report_response = client.get("/api/reports/summary")
        assert report_response.status_code == 200
        report_data = report_response.json()
        assert "income" in report_data
        assert "expenses" in report_data
        assert "cashflow" in report_data
        assert "health_indicators" in report_data


class TestImportAnalyzeWorkflow:
    """Test import and analyze workflow."""
    
    def test_import_and_immediate_analysis(self, client, sample_categories, tmp_path):
        """Test importing data and immediately analyzing it."""
        # Create transactions via API (simulating import)
        transactions_data = [
            {"transaction_date": "2025-01-01", "description": "Salary", "amount": "5000.00", "transaction_type": "Income", "category_id": 1},
            {"transaction_date": "2025-01-05", "description": "Groceries", "amount": "150.00", "transaction_type": "Expense", "category_id": 2},
            {"transaction_date": "2025-01-10", "description": "Electric Bill", "amount": "100.00", "transaction_type": "Expense", "category_id": 3},
            {"transaction_date": "2025-01-15", "description": "Bonus", "amount": "1000.00", "transaction_type": "Income", "category_id": 1},
            {"transaction_date": "2025-01-20", "description": "Movie Tickets", "amount": "50.00", "transaction_type": "Expense", "category_id": 4},
        ]

        # Create all transactions
        for transaction_data in transactions_data:
            response = client.post("/api/transactions", json=transaction_data)
            assert response.status_code == 201
        
        # Immediately analyze income
        income_response = client.get("/api/analysis/income", params={"mode": "analysis"})
        assert income_response.status_code == 200
        income_data = income_response.json()
        assert Decimal(str(income_data["total_income"])) == Decimal("6000.00")
        
        # Analyze expenses
        expense_response = client.get("/api/analysis/expenses", params={"mode": "analysis"})
        assert expense_response.status_code == 200
        expense_data = expense_response.json()
        assert Decimal(str(expense_data["total_expenses"])) == Decimal("300.00")


class TestProjectionWorkflow:
    """Test projection workflow."""
    
    def test_analyze_and_project(self, client, sample_transactions):
        """Test analyzing historical data and generating projections."""
        # Get historical income trends
        trends_response = client.get(
            "/api/analysis/income/trends",
            params={"period": "monthly", "mode": "analysis"}
        )
        assert trends_response.status_code == 200
        
        # Generate income projection
        projection_response = client.get(
            "/api/projections/income",
            params={
                "projection_days": 6,
                "method": "linear_regression"
            }
        )
        assert projection_response.status_code == 200
        projection_data = projection_response.json()

        # Verify projection response has required fields
        assert "projected_total" in projection_data
        assert "daily_projections" in projection_data
        assert "method" in projection_data
        assert projection_data["method"] == "linear_regression"
    
    def test_scenario_analysis_workflow(self, client, sample_transactions):
        """Test scenario analysis workflow."""
        # Generate scenarios
        scenario_response = client.get(
            "/api/projections/scenarios",
            params={"projection_days": 3}
        )
        assert scenario_response.status_code == 200
        scenario_data = scenario_response.json()

        # Scenarios are nested under the "scenarios" field
        assert "scenarios" in scenario_data
        assert "best_case" in scenario_data["scenarios"]
        assert "worst_case" in scenario_data["scenarios"]
        assert "expected" in scenario_data["scenarios"]


class TestReportingWorkflow:
    """Test reporting workflow."""
    
    def test_generate_all_reports(self, client, sample_transactions):
        """Test generating all report types."""
        # Summary report
        summary_response = client.get("/api/reports/summary")
        assert summary_response.status_code == 200
        summary_data = summary_response.json()
        assert "income" in summary_data
        assert "expenses" in summary_data
        assert "cashflow" in summary_data
        
        # Income detail report
        income_report_response = client.get("/api/reports/income")
        assert income_report_response.status_code == 200
        income_report_data = income_report_response.json()
        assert "total_income" in income_report_data
        
        # Expense detail report
        expense_report_response = client.get("/api/reports/expenses")
        assert expense_report_response.status_code == 200
        expense_report_data = expense_report_response.json()
        assert "total_expenses" in expense_report_data
        
        # Reconciliation report
        recon_response = client.get("/api/reports/reconciliation")
        assert recon_response.status_code == 200
        recon_data = recon_response.json()
        assert "transactions" in recon_data
    
    def test_export_report_to_csv(self, client, sample_transactions):
        """Test exporting report to CSV format."""
        response = client.get(
            "/api/reports/summary",
            params={"format": "csv"}
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"


class TestRelationshipWorkflow:
    """Test relationship detection workflow."""
    
    def test_detect_and_analyze_relationships(self, client, sample_transactions):
        """Test detecting relationships and analyzing their impact."""
        # Detect transfer pairs
        transfer_response = client.post("/api/relationships/detect/transfers")
        assert transfer_response.status_code == 200
        transfer_data = transfer_response.json()

        # Response has "count" field, not "pairs_detected"
        assert "count" in transfer_data
        assert "pairs" in transfer_data

        # Get related transactions if any pairs were detected
        if transfer_data["count"] > 0:
            # Get the first pair's transaction ID
            first_pair = transfer_data["pairs"][0]
            tx_id = first_pair["transaction_1"]["transaction_id"]

            related_response = client.get(f"/api/transactions/{tx_id}/relationships")
            assert related_response.status_code == 200
            related_data = related_response.json()
            assert "related_transactions" in related_data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

