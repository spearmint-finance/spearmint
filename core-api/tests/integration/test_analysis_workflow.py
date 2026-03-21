"""
Integration tests for analysis workflow.

Tests the complete analysis workflow including income, expense,
cash flow, and health indicator analysis.
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal


class TestAnalysisWorkflow:
    """Test complete analysis workflow."""

    def test_api_can_see_transactions(self, client, sample_transactions):
        """Test that API can see transactions via /api/transactions endpoint."""
        # Try to get all transactions via API
        response = client.get("/api/transactions")
        assert response.status_code == 200
        data = response.json()

        print(f"\n=== API Transactions Response ===")
        print(f"Total: {data.get('total', 0)}")
        print(f"Transactions: {len(data.get('transactions', []))}")

        # Should see all 7 transactions
        assert data.get('total', 0) == 7

    def test_income_analysis_workflow(self, client, sample_transactions, test_db_session):
        """Test complete income analysis workflow."""
        # Get income analysis
        response = client.get("/api/analysis/income", params={"mode": "analysis"})

        assert response.status_code == 200
        data = response.json()

        # Debug: print the response
        print(f"\n=== Income Analysis Response ===")
        print(f"Total Income: {data['total_income']}")
        print(f"Transaction Count: {data['transaction_count']}")
        print(f"Breakdown: {data.get('breakdown_by_category', {})}")

        # Verify income totals (excludes transfers)
        assert Decimal(str(data["total_income"])) == Decimal("6000.00")  # 5000 + 1000
        assert data["transaction_count"] == 2
        assert Decimal(str(data["average_transaction"])) == Decimal("3000.00")
        
        # Verify category breakdown
        assert "Salary" in data["breakdown_by_category"]
        salary_breakdown = data["breakdown_by_category"]["Salary"]
        assert Decimal(str(salary_breakdown["total"])) == Decimal("6000.00")
        assert salary_breakdown["count"] == 2
        assert salary_breakdown["percentage"] == 100.0
    
    def test_expense_analysis_workflow(self, client, sample_transactions):
        """Test complete expense analysis workflow."""
        # Get expense analysis
        response = client.get("/api/analysis/expenses", params={"mode": "analysis"})
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify expense totals (excludes transfers)
        assert Decimal(str(data["total_expenses"])) == Decimal("300.00")  # 150 + 100 + 50
        assert data["transaction_count"] == 3
        assert Decimal(str(data["average_transaction"])) == Decimal("100.00")
        
        # Verify category breakdown
        assert len(data["breakdown_by_category"]) == 3
        assert "Groceries" in data["breakdown_by_category"]
        assert "Utilities" in data["breakdown_by_category"]
        assert "Entertainment" in data["breakdown_by_category"]
    
    def test_cash_flow_analysis_workflow(self, client, sample_transactions):
        """Test complete cash flow analysis workflow."""
        # Get cash flow analysis
        response = client.get("/api/analysis/cashflow", params={"mode": "analysis"})

        assert response.status_code == 200
        data = response.json()

        # Verify cash flow (income - expenses, excludes transfers)
        assert Decimal(str(data["total_income"])) == Decimal("6000.00")
        assert Decimal(str(data["total_expenses"])) == Decimal("300.00")
        assert Decimal(str(data["net_cash_flow"])) == Decimal("5700.00")

        # Verify transaction counts
        assert data["income_count"] == 2
        assert data["expense_count"] == 3
    
    def test_financial_health_workflow(self, client, sample_transactions):
        """Test complete financial health analysis workflow."""
        # Get financial health indicators
        response = client.get("/api/analysis/health", params={"mode": "analysis"})

        assert response.status_code == 200
        data = response.json()

        # Verify health indicators
        assert "savings_rate" in data
        assert "income_to_expense_ratio" in data  # Correct field name
        assert "net_daily_cash_flow" in data

        # Verify calculations
        savings_rate = float(data["savings_rate"])
        assert savings_rate > 0  # Should be positive with more income than expenses

        income_ratio = float(data["income_to_expense_ratio"])
        assert income_ratio > 1  # Should be > 1 when income > expenses
    
    def test_income_trends_workflow(self, client, sample_transactions):
        """Test income trends analysis workflow."""
        # Get income trends
        response = client.get(
            "/api/analysis/income/trends",
            params={"period": "monthly", "mode": "analysis"}
        )

        assert response.status_code == 200
        data = response.json()

        # Verify trends data
        assert "trends" in data
        assert len(data["trends"]) > 0

        # Verify trend data points
        for trend in data["trends"]:
            assert "period" in trend
            assert "value" in trend  # Correct field name
            assert "count" in trend
    
    def test_expense_trends_workflow(self, client, sample_transactions):
        """Test expense trends analysis workflow."""
        # Get expense trends
        response = client.get(
            "/api/analysis/expenses/trends",
            params={"period": "monthly", "mode": "analysis"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify trends data
        assert "trends" in data
        assert len(data["trends"]) > 0
    
    def test_analysis_mode_switching(self, client, sample_transactions):
        """Test switching between analysis and complete modes."""
        # Get income in analysis mode (excludes transfers)
        response_analysis = client.get(
            "/api/analysis/income",
            params={"mode": "analysis"}
        )
        
        assert response_analysis.status_code == 200
        data_analysis = response_analysis.json()
        
        # Get income in complete mode (includes transfers)
        response_complete = client.get(
            "/api/analysis/income",
            params={"mode": "complete"}
        )
        
        assert response_complete.status_code == 200
        data_complete = response_complete.json()
        
        # Complete mode should include transfer (500.00 credit)
        assert Decimal(str(data_complete["total_income"])) > Decimal(str(data_analysis["total_income"]))
    
    def test_date_range_filtering(self, client, sample_transactions):
        """Test date range filtering in analysis."""
        today = date.today()
        start_date = (today - timedelta(days=20)).isoformat()
        end_date = today.isoformat()
        
        # Get income with date range
        response = client.get(
            "/api/analysis/income",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "mode": "analysis"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should only include transactions within date range
        assert data["period_start"] == start_date
        assert data["period_end"] == end_date
        
        # Should have fewer transactions than total
        assert data["transaction_count"] <= 2  # Only bonus within last 20 days


class TestAnalysisErrorHandling:
    """Test error handling in analysis endpoints."""
    
    def test_invalid_date_range(self, client, sample_transactions):
        """Test analysis with invalid date range."""
        # End date before start date
        response = client.get(
            "/api/analysis/income",
            params={
                "start_date": "2025-12-31",
                "end_date": "2025-01-01",
                "mode": "analysis"
            }
        )
        
        # Should handle gracefully (may return empty results or error)
        assert response.status_code in [200, 400]
    
    def test_invalid_mode(self, client, sample_transactions):
        """Test analysis with invalid mode."""
        response = client.get(
            "/api/analysis/income",
            params={"mode": "invalid"}
        )
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_invalid_period(self, client, sample_transactions):
        """Test trends with invalid period."""
        response = client.get(
            "/api/analysis/income/trends",
            params={"period": "invalid"}
        )
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_empty_dataset(self, client):
        """Test analysis with no transactions."""
        # Get income analysis with no data
        response = client.get("/api/analysis/income", params={"mode": "analysis"})
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return zero values
        assert Decimal(str(data["total_income"])) == Decimal("0.00")
        assert data["transaction_count"] == 0


class TestAnalysisPerformance:
    """Test analysis performance with larger datasets."""
    
    def test_analysis_with_many_transactions(self, client, sample_categories):
        """Test analysis performance with many transactions."""
        # Create many transactions
        today = date.today()

        for i in range(100):
            transaction_data = {
                "transaction_date": (today - timedelta(days=i)).isoformat(),
                "description": f"Transaction {i}",
                "amount": 100.00,
                "transaction_type": "Income" if i % 2 == 0 else "Expense",  # Correct values
                "category_id": 1 if i % 2 == 0 else 2
            }

            response = client.post("/api/transactions", json=transaction_data)
            assert response.status_code == 201
        
        # Get income analysis
        response = client.get("/api/analysis/income", params={"mode": "analysis"})
        
        assert response.status_code == 200
        data = response.json()
        
        # Should handle large dataset
        assert data["transaction_count"] == 50  # Half are income
        assert Decimal(str(data["total_income"])) == Decimal("5000.00")  # 50 * 100


class TestAnalysisIntegration:
    """Test integration between different analysis endpoints."""
    
    def test_analysis_consistency(self, client, sample_transactions):
        """Test consistency across different analysis endpoints."""
        # Get income, expense, and cash flow
        income_response = client.get("/api/analysis/income", params={"mode": "analysis"})
        expense_response = client.get("/api/analysis/expenses", params={"mode": "analysis"})
        cashflow_response = client.get("/api/analysis/cashflow", params={"mode": "analysis"})
        
        assert income_response.status_code == 200
        assert expense_response.status_code == 200
        assert cashflow_response.status_code == 200
        
        income_data = income_response.json()
        expense_data = expense_response.json()
        cashflow_data = cashflow_response.json()
        
        # Verify consistency
        assert Decimal(str(income_data["total_income"])) == Decimal(str(cashflow_data["total_income"]))
        assert Decimal(str(expense_data["total_expenses"])) == Decimal(str(cashflow_data["total_expenses"]))
        
        # Verify cash flow calculation
        expected_cashflow = Decimal(str(income_data["total_income"])) - Decimal(str(expense_data["total_expenses"]))
        assert Decimal(str(cashflow_data["net_cash_flow"])) == expected_cashflow


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

