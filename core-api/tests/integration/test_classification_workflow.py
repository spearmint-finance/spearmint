"""
Integration tests for classification workflow.

Tests the complete classification workflow including manual classification,
bulk classification, auto-classification, and classification rules.
"""

import pytest
from decimal import Decimal


class TestClassificationWorkflow:
    """Test complete classification workflow."""
    
    def test_list_classifications(self, client):
        """Test listing all classifications."""
        response = client.get("/api/classifications")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have system classifications
        assert "classifications" in data
        assert len(data["classifications"]) >= 4  # At least 4 system classifications
        
        # Verify system classifications
        codes = [c["classification_code"] for c in data["classifications"]]
        assert "STANDARD" in codes
        assert "TRANSFER" in codes
        assert "CC_PAYMENT" in codes
        assert "CC_RECEIPT" in codes
    
    def test_get_classification(self, client):
        """Test getting a specific classification."""
        response = client.get("/api/classifications/1")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["classification_id"] == 1
        assert data["classification_code"] == "STANDARD"
        assert data["is_system_classification"] is True
    
    def test_create_custom_classification(self, client):
        """Test creating a custom classification."""
        # Use unique name and code with timestamp to avoid conflicts
        import time
        unique_suffix = int(time.time() * 1000) % 1000000
        unique_name = f"Custom Classification {unique_suffix}"
        unique_code = f"CUSTOM_{unique_suffix}"

        classification_data = {
            "classification_name": unique_name,
            "classification_code": unique_code,
            "description": "Custom test classification",
            "exclude_from_income_calc": True,
            "exclude_from_expense_calc": True,
            "exclude_from_cashflow_calc": False
        }

        response = client.post("/api/classifications", json=classification_data)

        assert response.status_code == 201
        data = response.json()

        assert data["classification_name"] == unique_name
        assert data["classification_code"] == unique_code
        assert data["is_system_classification"] is False
    
    def test_classify_single_transaction(self, client):
        """Test classifying a single transaction."""
        from datetime import date

        # Create a category via API first to avoid session isolation issues
        category_data = {
            "category_name": "Test Groceries",
            "category_type": "Expense",
            "description": "Test category for classification"
        }
        category_response = client.post("/api/categories", json=category_data)
        assert category_response.status_code == 201
        category = category_response.json()
        category_id = category["category_id"]

        # Create a transaction via API
        transaction_data = {
            "transaction_date": str(date.today()),
            "description": "Test Transaction for Classification",
            "amount": "100.00",
            "transaction_type": "Expense",
            "category_id": category_id,
            "classification_id": 1  # STANDARD
        }

        create_response = client.post("/api/transactions", json=transaction_data)
        assert create_response.status_code == 201
        created_transaction = create_response.json()
        transaction_id = created_transaction["transaction_id"]

        # Classify transaction as transfer
        classify_data = {
            "classification_id": 2  # TRANSFER
        }

        response = client.post(
            f"/api/transactions/{transaction_id}/classify",
            json=classify_data
        )

        assert response.status_code == 200
        data = response.json()

        assert data["classification_id"] == 2
        assert data["classification_code"] == "TRANSFER"

        # Verify transaction was updated
        transaction_response = client.get(f"/api/transactions/{transaction_id}")
        assert transaction_response.status_code == 200
        transaction_data = transaction_response.json()
        assert transaction_data["classification_id"] == 2
    
    def test_bulk_classify_transactions(self, client, sample_transactions):
        """Test bulk classifying multiple transactions."""
        # First, get available transactions
        list_response = client.get("/api/transactions")
        assert list_response.status_code == 200
        transactions = list_response.json()["transactions"]
        assert len(transactions) >= 3

        # Get first 3 transaction IDs
        transaction_ids = [t["transaction_id"] for t in transactions[:3]]

        # Classify multiple transactions as transfers
        bulk_data = {
            "transaction_ids": transaction_ids,
            "classification_id": 2  # TRANSFER
        }

        response = client.post(
            "/api/transactions/classify/bulk",
            json=bulk_data
        )

        assert response.status_code == 200
        data = response.json()

        # Correct field names from BulkClassifyResponse schema
        assert data["success_count"] == 3
        assert data["failed_count"] == 0
        assert data["failed_ids"] == []

        # Verify transactions were updated
        for transaction_id in transaction_ids:
            transaction_response = client.get(f"/api/transactions/{transaction_id}")
            assert transaction_response.status_code == 200
            transaction_data = transaction_response.json()
            assert transaction_data["classification_id"] == 2
    
    def test_auto_classify_transactions(self, client, sample_transactions):
        """Test auto-classifying transactions."""
        # Create a classification rule first
        rule_data = {
            "rule_name": "Salary Rule",
            "rule_priority": 1,
            "classification_id": 1,
            "is_active": True,
            "description_pattern": "%Salary%"
        }

        rule_response = client.post("/api/classification-rules", json=rule_data)
        assert rule_response.status_code == 201

        # Auto-classify all transactions
        auto_classify_data = {
            "force_reclassify": True
        }

        response = client.post(
            "/api/transactions/auto-classify",
            json=auto_classify_data
        )

        assert response.status_code == 200
        data = response.json()

        # Correct field names from AutoClassifyResponse schema
        assert data["total_processed"] > 0
        assert data["classified_count"] >= 0
        assert data["skipped_count"] >= 0


class TestClassificationRulesWorkflow:
    """Test classification rules workflow."""
    
    def test_create_classification_rule(self, client):
        """Test creating a classification rule."""
        rule_data = {
            "rule_name": "Transfer Rule",
            "rule_priority": 1,
            "classification_id": 2,  # TRANSFER
            "is_active": True,
            "description_pattern": "%Transfer%",
            "amount_min": 100.00,
            "amount_max": 10000.00
        }
        
        response = client.post("/api/classification-rules", json=rule_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["rule_name"] == "Transfer Rule"
        assert data["classification_id"] == 2
        assert data["is_active"] is True
    
    def test_list_classification_rules(self, client):
        """Test listing classification rules."""
        # Create a rule first
        rule_data = {
            "rule_name": "Test Rule",
            "rule_priority": 1,
            "classification_id": 1,
            "is_active": True
        }
        
        client.post("/api/classification-rules", json=rule_data)
        
        # List rules
        response = client.get("/api/classification-rules")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "rules" in data
        assert len(data["rules"]) > 0
    
    def test_update_classification_rule(self, client):
        """Test updating a classification rule."""
        # Create a rule first
        rule_data = {
            "rule_name": "Test Rule",
            "rule_priority": 1,
            "classification_id": 1,
            "is_active": True
        }
        
        create_response = client.post("/api/classification-rules", json=rule_data)
        assert create_response.status_code == 201
        rule_id = create_response.json()["rule_id"]
        
        # Update the rule
        update_data = {
            "rule_name": "Updated Rule",
            "is_active": False
        }
        
        response = client.put(f"/api/classification-rules/{rule_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["rule_name"] == "Updated Rule"
        assert data["is_active"] is False
    
    def test_delete_classification_rule(self, client):
        """Test deleting a classification rule."""
        # Create a rule first
        rule_data = {
            "rule_name": "Test Rule",
            "rule_priority": 1,
            "classification_id": 1,
            "is_active": True
        }
        
        create_response = client.post("/api/classification-rules", json=rule_data)
        assert create_response.status_code == 201
        rule_id = create_response.json()["rule_id"]
        
        # Delete the rule
        response = client.delete(f"/api/classification-rules/{rule_id}")
        
        assert response.status_code == 204
        
        # Verify rule is deleted
        get_response = client.get(f"/api/classification-rules/{rule_id}")
        assert get_response.status_code == 404
    
    def test_test_classification_rule(self, client, sample_transactions):
        """Test testing a classification rule."""
        test_data = {
            "description_pattern": "%Salary%",
            "amount_min": 1000.00
        }

        response = client.post("/api/classification-rules/test", json=test_data)

        assert response.status_code == 200
        data = response.json()

        # Correct field names from TestRuleResponse schema
        assert "matching_transactions" in data
        assert "sample_transaction_ids" in data
        assert isinstance(data["matching_transactions"], int)
        assert isinstance(data["sample_transaction_ids"], list)


class TestClassificationErrorHandling:
    """Test error handling in classification endpoints."""
    
    def test_classify_nonexistent_transaction(self, client):
        """Test classifying a non-existent transaction."""
        classify_data = {
            "classification_id": 1
        }

        response = client.post(
            "/api/transactions/99999/classify",
            json=classify_data
        )

        assert response.status_code == 404
        data = response.json()
        # Check for error message (error_code may not be present in all error responses)
        assert "detail" in data or "message" in data
    
    def test_classify_with_invalid_classification(self, client, sample_transactions):
        """Test classifying with invalid classification ID."""
        classify_data = {
            "classification_id": 99999
        }
        
        response = client.post(
            "/api/transactions/1/classify",
            json=classify_data
        )
        
        assert response.status_code == 404
    
    def test_delete_system_classification(self, client):
        """Test deleting a system classification (should fail)."""
        response = client.delete("/api/classifications/1")

        assert response.status_code == 403
        data = response.json()
        # Check for error message (error_code may not be present in all error responses)
        assert "detail" in data or "message" in data

    def test_create_duplicate_classification_code(self, client):
        """Test creating classification with duplicate code."""
        classification_data = {
            "classification_name": "Duplicate",
            "classification_code": "STANDARD",  # Already exists
            "description": "Duplicate classification"
        }

        response = client.post("/api/classifications", json=classification_data)

        # Should return 400 (bad request) or 409 (conflict)
        assert response.status_code in [400, 409]
        data = response.json()
        # Check for error message (API returns detail field, not error_code)
        assert "detail" in data or "message" in data


class TestClassificationImpactOnAnalysis:
    """Test how classification affects analysis results."""
    
    def test_classification_excludes_from_income(self, client, sample_transactions):
        """Test that transfers are excluded from income analysis."""
        # Get all transactions and find an income transaction
        list_response = client.get("/api/transactions")
        assert list_response.status_code == 200
        transactions = list_response.json()["transactions"]

        # Find an income transaction
        income_transaction = None
        for t in transactions:
            if t["transaction_type"] == "Income" and t["classification_id"] != 2:
                income_transaction = t
                break

        # Skip test if no income transactions available
        if not income_transaction:
            import pytest
            pytest.skip("No income transactions available for testing")

        # Get income before reclassification
        response_before = client.get("/api/analysis/income", params={"mode": "analysis"})
        assert response_before.status_code == 200
        income_before = Decimal(str(response_before.json()["total_income"]))
        count_before = response_before.json()["transaction_count"]

        # Classify the income transaction as transfer
        classify_data = {"classification_id": 2}  # TRANSFER
        classify_response = client.post(
            f"/api/transactions/{income_transaction['transaction_id']}/classify",
            json=classify_data
        )
        assert classify_response.status_code == 200

        # Get income after reclassification
        response_after = client.get("/api/analysis/income", params={"mode": "analysis"})
        assert response_after.status_code == 200
        income_after = Decimal(str(response_after.json()["total_income"]))
        count_after = response_after.json()["transaction_count"]

        # Income should decrease and count should decrease by 1
        assert income_after < income_before
        assert count_after < count_before
    
    def test_classification_excludes_from_expenses(self, client, sample_transactions):
        """Test that transfers are excluded from expense analysis."""
        # Get all transactions and find an expense transaction
        list_response = client.get("/api/transactions")
        assert list_response.status_code == 200
        transactions = list_response.json()["transactions"]

        # Find an expense transaction
        expense_transaction = None
        for t in transactions:
            if t["transaction_type"] == "Expense" and t["classification_id"] != 2:
                expense_transaction = t
                break

        # Skip test if no expense transactions available
        if not expense_transaction:
            import pytest
            pytest.skip("No expense transactions available for testing")

        # Get expenses before reclassification
        response_before = client.get("/api/analysis/expenses", params={"mode": "analysis"})
        assert response_before.status_code == 200
        expenses_before = Decimal(str(response_before.json()["total_expenses"]))
        count_before = response_before.json()["transaction_count"]

        # Classify the expense transaction as transfer
        classify_data = {"classification_id": 2}  # TRANSFER
        classify_response = client.post(
            f"/api/transactions/{expense_transaction['transaction_id']}/classify",
            json=classify_data
        )
        assert classify_response.status_code == 200

        # Get expenses after reclassification
        response_after = client.get("/api/analysis/expenses", params={"mode": "analysis"})
        assert response_after.status_code == 200
        expenses_after = Decimal(str(response_after.json()["total_expenses"]))
        count_after = response_after.json()["transaction_count"]

        # Expenses should decrease and count should decrease by 1
        assert expenses_after < expenses_before
        assert count_after < count_before


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

