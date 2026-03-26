"""
Integration tests for the is_cleared transaction filter.

Covers: filtering cleared-only, uncleared-only, and no filter (all).
"""

import pytest
from datetime import date


def make_transaction(client, category_id: int) -> dict:
    resp = client.post("/api/transactions", json={
        "transaction_date": str(date.today()),
        "amount": "100.00",
        "transaction_type": "Expense",
        "category_id": category_id,
    })
    assert resp.status_code == 201, resp.text
    return resp.json()


class TestClearedFilter:
    def test_filter_cleared_returns_only_cleared(self, client, sample_categories):
        """is_cleared=true returns only cleared transactions."""
        cat_id = sample_categories[1].category_id
        tx1 = make_transaction(client, cat_id)
        tx2 = make_transaction(client, cat_id)

        # Clear tx1 only
        client.post("/api/accounts/transactions/clear", json={
            "transaction_ids": [tx1["transaction_id"]],
        })

        resp = client.get("/api/transactions?is_cleared=true")
        assert resp.status_code == 200
        ids = [t["transaction_id"] for t in resp.json()["transactions"]]
        assert tx1["transaction_id"] in ids
        assert tx2["transaction_id"] not in ids

    def test_filter_uncleared_returns_only_uncleared(self, client, sample_categories):
        """is_cleared=false returns only uncleared transactions."""
        cat_id = sample_categories[1].category_id
        tx1 = make_transaction(client, cat_id)
        tx2 = make_transaction(client, cat_id)

        # Clear tx1 only
        client.post("/api/accounts/transactions/clear", json={
            "transaction_ids": [tx1["transaction_id"]],
        })

        resp = client.get("/api/transactions?is_cleared=false")
        assert resp.status_code == 200
        ids = [t["transaction_id"] for t in resp.json()["transactions"]]
        assert tx2["transaction_id"] in ids
        assert tx1["transaction_id"] not in ids

    def test_no_cleared_filter_returns_all(self, client, sample_categories):
        """Omitting is_cleared returns both cleared and uncleared."""
        cat_id = sample_categories[1].category_id
        tx1 = make_transaction(client, cat_id)
        tx2 = make_transaction(client, cat_id)

        client.post("/api/accounts/transactions/clear", json={
            "transaction_ids": [tx1["transaction_id"]],
        })

        resp = client.get("/api/transactions")
        assert resp.status_code == 200
        ids = [t["transaction_id"] for t in resp.json()["transactions"]]
        assert tx1["transaction_id"] in ids
        assert tx2["transaction_id"] in ids
