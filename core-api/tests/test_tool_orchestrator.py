"""
Tests for AI Assistant ToolOrchestrator.

Verifies date range calculations, tool routing, query tool execution,
action proposals, and navigation link creation.
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from financial_analysis.database.base import Base
from financial_analysis.database.models import (
    Transaction, Category, Account,
)
from financial_analysis.database.assistant_models import AssistantActionLog
from financial_analysis.services.assistant.tool_orchestrator import (
    ToolOrchestrator, _convert_decimals,
)


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Create categories
    groceries = Category(category_name="Groceries", category_type="Expense")
    salary = Category(category_name="Salary", category_type="Income")
    rent = Category(category_name="Rent", category_type="Expense")
    uncategorized = Category(category_name="Uncategorized", category_type="Expense")

    session.add_all([groceries, salary, rent, uncategorized])
    session.commit()

    yield session
    session.close()


@pytest.fixture
def orchestrator(db_session):
    """Create a ToolOrchestrator with test DB."""
    return ToolOrchestrator(db_session)


@pytest.fixture
def sample_transactions(db_session):
    """Seed sample transactions for testing."""
    groceries = db_session.query(Category).filter_by(category_name="Groceries").first()
    salary = db_session.query(Category).filter_by(category_name="Salary").first()
    rent = db_session.query(Category).filter_by(category_name="Rent").first()
    uncategorized = db_session.query(Category).filter_by(category_name="Uncategorized").first()

    today = date.today()
    transactions = [
        Transaction(
            transaction_date=today - timedelta(days=5),
            amount=Decimal("50.00"),
            transaction_type="Expense",
            category_id=groceries.category_id,
            source="Whole Foods",
            description="Weekly groceries",
        ),
        Transaction(
            transaction_date=today - timedelta(days=10),
            amount=Decimal("75.50"),
            transaction_type="Expense",
            category_id=groceries.category_id,
            source="Trader Joes",
            description="Groceries run",
        ),
        Transaction(
            transaction_date=today - timedelta(days=3),
            amount=Decimal("5000.00"),
            transaction_type="Income",
            category_id=salary.category_id,
            source="Acme Corp",
            description="Monthly salary",
        ),
        Transaction(
            transaction_date=today - timedelta(days=1),
            amount=Decimal("1500.00"),
            transaction_type="Expense",
            category_id=rent.category_id,
            source="Landlord",
            description="Monthly rent",
        ),
        Transaction(
            transaction_date=today - timedelta(days=2),
            amount=Decimal("22.00"),
            transaction_type="Expense",
            category_id=uncategorized.category_id,
            source="Amazon",
            description="Misc purchase",
        ),
    ]
    db_session.add_all(transactions)
    db_session.commit()
    return transactions


class TestConvertDecimals:
    """Tests for Decimal to float conversion utility."""

    def test_decimal(self):
        assert _convert_decimals(Decimal("10.50")) == 10.50

    def test_dict(self):
        result = _convert_decimals({"a": Decimal("1.5"), "b": "text"})
        assert result == {"a": 1.5, "b": "text"}

    def test_list(self):
        result = _convert_decimals([Decimal("1.0"), Decimal("2.0")])
        assert result == [1.0, 2.0]

    def test_nested(self):
        result = _convert_decimals({"items": [{"val": Decimal("3.14")}]})
        assert result == {"items": [{"val": 3.14}]}

    def test_passthrough(self):
        assert _convert_decimals("hello") == "hello"
        assert _convert_decimals(42) == 42
        assert _convert_decimals(None) is None


class TestGetDateRange:
    """Tests for period-to-date-range conversion."""

    def test_this_month(self, orchestrator):
        start, end = orchestrator._get_date_range("this_month")
        today = date.today()
        assert start == today.replace(day=1)
        assert end == today

    def test_last_month(self, orchestrator):
        start, end = orchestrator._get_date_range("last_month")
        today = date.today()
        first_of_month = today.replace(day=1)
        assert end == first_of_month - timedelta(days=1)
        assert start.day == 1
        assert start.month == end.month

    def test_this_year(self, orchestrator):
        start, end = orchestrator._get_date_range("this_year")
        today = date.today()
        assert start == date(today.year, 1, 1)
        assert end == today

    def test_last_year(self, orchestrator):
        start, end = orchestrator._get_date_range("last_year")
        today = date.today()
        assert start == date(today.year - 1, 1, 1)
        assert end == date(today.year - 1, 12, 31)

    def test_custom_range(self, orchestrator):
        start, end = orchestrator._get_date_range(
            "custom", "2026-01-01", "2026-03-31"
        )
        assert start == date(2026, 1, 1)
        assert end == date(2026, 3, 31)

    def test_default_is_this_month(self, orchestrator):
        start, end = orchestrator._get_date_range(None)
        today = date.today()
        assert start == today.replace(day=1)
        assert end == today

    def test_this_quarter(self, orchestrator):
        start, end = orchestrator._get_date_range("this_quarter")
        today = date.today()
        quarter = (today.month - 1) // 3
        expected_start_month = quarter * 3 + 1
        assert start == date(today.year, expected_start_month, 1)
        assert end == today


class TestExecuteTool:
    """Tests for tool routing."""

    @pytest.mark.asyncio
    async def test_unknown_tool(self, orchestrator):
        result = await orchestrator.execute_tool("nonexistent_tool", {})
        assert "error" in result
        assert "Unknown tool" in result["error"]

    @pytest.mark.asyncio
    async def test_routes_to_handler(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("create_navigation_link", {
            "page": "dashboard"
        })
        assert result["type"] == "navigation"


class TestSearchTransactions:
    """Tests for transaction search tool."""

    @pytest.mark.asyncio
    async def test_search_by_merchant(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("search_transactions", {
            "merchant": "Whole Foods"
        })
        assert result["count"] == 1
        assert result["transactions"][0]["source"] == "Whole Foods"

    @pytest.mark.asyncio
    async def test_search_by_category(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("search_transactions", {
            "category": "Groceries"
        })
        assert result["count"] == 2

    @pytest.mark.asyncio
    async def test_search_by_description(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("search_transactions", {
            "description": "rent"
        })
        assert result["count"] == 1

    @pytest.mark.asyncio
    async def test_search_by_amount_range(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("search_transactions", {
            "amount_min": 100,
            "amount_max": 2000,
        })
        assert result["count"] == 1
        assert result["transactions"][0]["source"] == "Landlord"

    @pytest.mark.asyncio
    async def test_search_uncategorized(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("search_transactions", {
            "is_uncategorized": True
        })
        assert result["count"] == 1
        assert result["transactions"][0]["source"] == "Amazon"

    @pytest.mark.asyncio
    async def test_search_with_limit(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("search_transactions", {
            "limit": 2
        })
        assert result["count"] == 2
        assert result["limit"] == 2

    @pytest.mark.asyncio
    async def test_search_by_date_range(self, orchestrator, sample_transactions):
        today = date.today()
        result = await orchestrator.execute_tool("search_transactions", {
            "date_from": (today - timedelta(days=4)).isoformat(),
            "date_to": today.isoformat(),
        })
        # Should include transactions from last 4 days
        assert result["count"] >= 1


class TestNavigationLink:
    """Tests for navigation link creation tool."""

    @pytest.mark.asyncio
    async def test_basic_link(self, orchestrator):
        result = await orchestrator.execute_tool("create_navigation_link", {
            "page": "transactions"
        })
        assert result["type"] == "navigation"
        assert result["url"] == "/transactions"
        assert result["page"] == "transactions"

    @pytest.mark.asyncio
    async def test_link_with_filters(self, orchestrator):
        result = await orchestrator.execute_tool("create_navigation_link", {
            "page": "transactions",
            "filters": {"category": "Groceries", "date_from": "2026-01-01"},
        })
        assert "category=Groceries" in result["url"]
        assert "date_from=2026-01-01" in result["url"]

    @pytest.mark.asyncio
    async def test_link_with_label(self, orchestrator):
        result = await orchestrator.execute_tool("create_navigation_link", {
            "page": "analysis",
            "label": "View spending analysis",
        })
        assert result["label"] == "View spending analysis"

    @pytest.mark.asyncio
    async def test_default_label(self, orchestrator):
        result = await orchestrator.execute_tool("create_navigation_link", {
            "page": "dashboard"
        })
        assert result["label"] == "View dashboard"


class TestProposeCategorization:
    """Tests for categorization proposal tool."""

    @pytest.mark.asyncio
    async def test_propose_by_ids(self, orchestrator, sample_transactions):
        tx_ids = [sample_transactions[0].transaction_id]
        result = await orchestrator.execute_tool("propose_categorization", {
            "transaction_ids": tx_ids,
            "category_name": "Rent",
        })
        assert result["type"] == "action_proposal"
        assert result["requires_confirmation"] is True
        assert result["preview"]["transaction_count"] == 1

    @pytest.mark.asyncio
    async def test_propose_by_merchant_pattern(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("propose_categorization", {
            "merchant_pattern": "Foods",
            "category_name": "Groceries",
        })
        assert result["type"] == "action_proposal"
        assert result["preview"]["transaction_count"] == 1

    @pytest.mark.asyncio
    async def test_propose_unknown_category(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("propose_categorization", {
            "transaction_ids": [1],
            "category_name": "NonExistent",
        })
        assert "error" in result

    @pytest.mark.asyncio
    async def test_propose_no_matching_transactions(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("propose_categorization", {
            "merchant_pattern": "ZZZZZ_NO_MATCH",
            "category_name": "Groceries",
        })
        assert "error" in result

    @pytest.mark.asyncio
    async def test_propose_missing_ids_and_pattern(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("propose_categorization", {
            "category_name": "Groceries",
        })
        assert "error" in result


class TestProposeCategoryRule:
    """Tests for category rule proposal tool."""

    @pytest.mark.asyncio
    async def test_propose_contains_rule(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("propose_category_rule", {
            "pattern": "Whole",
            "pattern_type": "contains",
            "category_name": "Groceries",
        })
        assert result["type"] == "action_proposal"
        assert result["requires_confirmation"] is True
        assert result["preview"]["matching_transactions"] >= 1

    @pytest.mark.asyncio
    async def test_propose_exact_rule(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("propose_category_rule", {
            "pattern": "Whole Foods",
            "pattern_type": "exact",
            "category_name": "Groceries",
        })
        assert result["type"] == "action_proposal"
        assert result["preview"]["matching_transactions"] == 1

    @pytest.mark.asyncio
    async def test_propose_rule_unknown_category(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("propose_category_rule", {
            "pattern": "test",
            "pattern_type": "contains",
            "category_name": "NonExistent",
        })
        assert "error" in result

    @pytest.mark.asyncio
    async def test_propose_rule_with_name(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("propose_category_rule", {
            "pattern": "Trader",
            "pattern_type": "starts_with",
            "category_name": "Groceries",
            "rule_name": "Trader Joe's Rule",
        })
        assert result["preview"]["rule_name"] == "Trader Joe's Rule"
