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
    Transaction, Category, CategoryRule, Account, AccountBalance, Entity,
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


@pytest.fixture
def sample_accounts(db_session):
    """Seed sample accounts with balance snapshots for testing."""
    today = date.today()

    checking = Account(
        account_name="Chase Checking",
        account_type="checking",
        institution_name="Chase",
        is_active=True,
    )
    savings = Account(
        account_name="Ally Savings",
        account_type="savings",
        institution_name="Ally",
        is_active=True,
    )
    inactive = Account(
        account_name="Old Account",
        account_type="checking",
        institution_name="OldBank",
        is_active=False,
    )
    db_session.add_all([checking, savings, inactive])
    db_session.commit()

    # Add balance snapshots
    db_session.add_all([
        AccountBalance(
            account_id=checking.account_id,
            balance_date=today - timedelta(days=30),
            total_balance=Decimal("1000.00"),
            balance_type="statement",
        ),
        AccountBalance(
            account_id=checking.account_id,
            balance_date=today,
            total_balance=Decimal("2500.50"),
            balance_type="statement",
        ),
        AccountBalance(
            account_id=savings.account_id,
            balance_date=today,
            total_balance=Decimal("10000.00"),
            balance_type="statement",
        ),
    ])
    db_session.commit()

    return {"checking": checking, "savings": savings, "inactive": inactive}


class TestGetAccountBalance:
    """Tests for account balance tool (uses AccountBalance snapshots)."""

    @pytest.mark.asyncio
    async def test_get_all_accounts(self, orchestrator, sample_accounts):
        result = await orchestrator.execute_tool("get_account_balance", {
            "include_all": True,
        })
        assert "accounts" in result
        assert len(result["accounts"]) == 2  # Only active accounts
        assert result["total_balance"] == pytest.approx(12500.50)

    @pytest.mark.asyncio
    async def test_get_specific_account(self, orchestrator, sample_accounts):
        result = await orchestrator.execute_tool("get_account_balance", {
            "account_name": "Chase Checking",
        })
        assert result["name"] == "Chase Checking"
        assert result["balance"] == pytest.approx(2500.50)  # Most recent snapshot
        assert result["type"] == "checking"

    @pytest.mark.asyncio
    async def test_get_account_case_insensitive(self, orchestrator, sample_accounts):
        result = await orchestrator.execute_tool("get_account_balance", {
            "account_name": "chase checking",
        })
        assert result["name"] == "Chase Checking"

    @pytest.mark.asyncio
    async def test_get_unknown_account(self, orchestrator, sample_accounts):
        result = await orchestrator.execute_tool("get_account_balance", {
            "account_name": "NonExistent",
        })
        assert "error" in result

    @pytest.mark.asyncio
    async def test_default_returns_all(self, orchestrator, sample_accounts):
        result = await orchestrator.execute_tool("get_account_balance", {})
        assert "accounts" in result
        assert len(result["accounts"]) == 2

    @pytest.mark.asyncio
    async def test_excludes_inactive_accounts(self, orchestrator, sample_accounts):
        result = await orchestrator.execute_tool("get_account_balance", {
            "include_all": True,
        })
        account_names = [a["name"] for a in result["accounts"]]
        assert "Old Account" not in account_names

    @pytest.mark.asyncio
    async def test_account_without_balance_returns_zero(self, db_session, orchestrator):
        no_balance_account = Account(
            account_name="Empty Account",
            account_type="checking",
            institution_name="TestBank",
            is_active=True,
        )
        db_session.add(no_balance_account)
        db_session.commit()

        result = await orchestrator.execute_tool("get_account_balance", {
            "account_name": "Empty Account",
        })
        assert result["balance"] == 0.0


class TestSpendingSummary:
    """Tests for spending summary tool with category filtering."""

    @pytest.mark.asyncio
    async def test_total_spending_no_filter(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("get_spending_summary", {
            "period": "this_month",
        })
        assert "total" in result
        assert result["category"] is None
        assert "breakdown" in result

    @pytest.mark.asyncio
    async def test_spending_filtered_by_category(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("get_spending_summary", {
            "category": "Groceries",
            "period": "this_month",
        })
        assert result["category"] == "Groceries"
        # Should only return Groceries total, not all expenses
        assert result["total"] == pytest.approx(125.50)
        assert result["count"] == 2
        # No breakdown when filtered
        assert "breakdown" not in result

    @pytest.mark.asyncio
    async def test_spending_unknown_category(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("get_spending_summary", {
            "category": "NonExistent",
        })
        assert "error" in result

    @pytest.mark.asyncio
    async def test_spending_category_case_insensitive(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("get_spending_summary", {
            "category": "groceries",
            "period": "this_month",
        })
        assert result["category"] == "Groceries"
        assert result["total"] == pytest.approx(125.50)


class TestIncomeSummary:
    """Tests for income summary tool with category filtering."""

    @pytest.mark.asyncio
    async def test_total_income_no_filter(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("get_income_summary", {
            "period": "this_month",
        })
        assert "total" in result
        assert result["category"] is None
        assert "breakdown" in result

    @pytest.mark.asyncio
    async def test_income_filtered_by_category(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("get_income_summary", {
            "category": "Salary",
            "period": "this_month",
        })
        assert result["category"] == "Salary"
        assert result["total"] == pytest.approx(5000.00)
        assert result["count"] == 1
        assert "breakdown" not in result


class TestConfirmCategorize:
    """Tests for categorization action execution."""

    @pytest.mark.asyncio
    async def test_confirm_categorize_updates_transactions(self, orchestrator, db_session, sample_transactions):
        """Confirming a categorization should update transaction categories."""
        tx = sample_transactions[4]  # Amazon - currently Uncategorized
        rent = db_session.query(Category).filter_by(category_name="Rent").first()

        result = await orchestrator.confirm_action(
            action_type="categorize",
            payload={
                "transaction_ids": [tx.transaction_id],
                "category_id": rent.category_id,
                "category_name": "Rent",
            },
            message_id="msg-123",
        )

        assert result["success"] is True
        assert result["updated_count"] == 1
        assert result["category"] == "Rent"
        assert result["undo_available"] is True
        assert len(result["action_log_ids"]) == 1

        # Verify the transaction was actually updated
        db_session.refresh(tx)
        assert tx.category_id == rent.category_id

    @pytest.mark.asyncio
    async def test_confirm_categorize_multiple(self, orchestrator, db_session, sample_transactions):
        """Should update multiple transactions at once."""
        tx_ids = [sample_transactions[0].transaction_id, sample_transactions[1].transaction_id]
        rent = db_session.query(Category).filter_by(category_name="Rent").first()

        result = await orchestrator.confirm_action(
            action_type="categorize",
            payload={
                "transaction_ids": tx_ids,
                "category_id": rent.category_id,
                "category_name": "Rent",
            },
        )

        assert result["success"] is True
        assert result["updated_count"] == 2

    @pytest.mark.asyncio
    async def test_confirm_categorize_creates_action_log(self, orchestrator, db_session, sample_transactions):
        """Should create an undo log entry for each transaction."""
        tx = sample_transactions[0]
        original_category_id = tx.category_id
        rent = db_session.query(Category).filter_by(category_name="Rent").first()

        result = await orchestrator.confirm_action(
            action_type="categorize",
            payload={
                "transaction_ids": [tx.transaction_id],
                "category_id": rent.category_id,
                "category_name": "Rent",
            },
            message_id="msg-456",
        )

        log = db_session.query(AssistantActionLog).filter_by(id=result["action_log_ids"][0]).first()
        assert log is not None
        assert log.action_type == "categorize_transaction"
        assert log.entity_type == "transaction"
        assert log.entity_id == str(tx.transaction_id)
        assert log.previous_state["category_id"] == original_category_id
        assert log.new_state["category_id"] == rent.category_id
        assert log.message_id == "msg-456"
        assert log.undone_at is None

    @pytest.mark.asyncio
    async def test_confirm_categorize_missing_payload(self, orchestrator):
        """Should error when payload is incomplete."""
        result = await orchestrator.confirm_action(
            action_type="categorize",
            payload={"transaction_ids": []},
        )
        assert "error" in result

    @pytest.mark.asyncio
    async def test_confirm_categorize_nonexistent_category(self, orchestrator, sample_transactions):
        """Should error when category no longer exists."""
        result = await orchestrator.confirm_action(
            action_type="categorize",
            payload={
                "transaction_ids": [sample_transactions[0].transaction_id],
                "category_id": 99999,
                "category_name": "Gone",
            },
        )
        assert "error" in result

    @pytest.mark.asyncio
    async def test_confirm_unknown_action_type(self, orchestrator):
        """Should error for unknown action types."""
        result = await orchestrator.confirm_action(
            action_type="unknown_action",
            payload={},
        )
        assert "error" in result


class TestConfirmCreateRule:
    """Tests for category rule creation action execution."""

    @pytest.mark.asyncio
    async def test_confirm_create_rule(self, orchestrator, db_session, sample_transactions):
        """Confirming a rule creation should create the rule."""
        groceries = db_session.query(Category).filter_by(category_name="Groceries").first()

        result = await orchestrator.confirm_action(
            action_type="create_rule",
            payload={
                "pattern": "Whole Foods",
                "pattern_type": "contains",
                "category_id": groceries.category_id,
                "category_name": "Groceries",
                "rule_name": "Whole Foods Rule",
            },
            message_id="msg-789",
        )

        assert result["success"] is True
        assert result["action"] == "create_rule"
        assert result["rule_name"] == "Whole Foods Rule"
        assert result["undo_available"] is True

        # Verify rule was actually created in DB
        rule = db_session.query(CategoryRule).filter_by(rule_id=result["rule_id"]).first()
        assert rule is not None
        assert rule.source_pattern == "%Whole Foods%"
        assert rule.category_id == groceries.category_id

    @pytest.mark.asyncio
    async def test_confirm_create_rule_exact_pattern(self, orchestrator, db_session, sample_transactions):
        """Exact pattern type should not add wildcards."""
        groceries = db_session.query(Category).filter_by(category_name="Groceries").first()

        result = await orchestrator.confirm_action(
            action_type="create_rule",
            payload={
                "pattern": "Whole Foods",
                "pattern_type": "exact",
                "category_id": groceries.category_id,
                "category_name": "Groceries",
            },
        )

        rule = db_session.query(CategoryRule).filter_by(rule_id=result["rule_id"]).first()
        assert rule.source_pattern == "Whole Foods"

    @pytest.mark.asyncio
    async def test_confirm_create_rule_starts_with(self, orchestrator, db_session, sample_transactions):
        """starts_with pattern type should add trailing wildcard."""
        groceries = db_session.query(Category).filter_by(category_name="Groceries").first()

        result = await orchestrator.confirm_action(
            action_type="create_rule",
            payload={
                "pattern": "Trader",
                "pattern_type": "starts_with",
                "category_id": groceries.category_id,
                "category_name": "Groceries",
            },
        )

        rule = db_session.query(CategoryRule).filter_by(rule_id=result["rule_id"]).first()
        assert rule.source_pattern == "Trader%"

    @pytest.mark.asyncio
    async def test_confirm_create_rule_creates_action_log(self, orchestrator, db_session, sample_transactions):
        """Should create an undo log entry."""
        groceries = db_session.query(Category).filter_by(category_name="Groceries").first()

        result = await orchestrator.confirm_action(
            action_type="create_rule",
            payload={
                "pattern": "Test",
                "pattern_type": "contains",
                "category_id": groceries.category_id,
                "category_name": "Groceries",
                "rule_name": "Test Rule",
            },
            message_id="msg-rule",
        )

        log = db_session.query(AssistantActionLog).filter_by(id=result["action_log_id"]).first()
        assert log is not None
        assert log.action_type == "create_category_rule"
        assert log.entity_type == "category_rule"
        assert log.previous_state is None
        assert log.new_state["rule_name"] == "Test Rule"

    @pytest.mark.asyncio
    async def test_confirm_create_rule_nonexistent_category(self, orchestrator):
        """Should error when category no longer exists."""
        result = await orchestrator.confirm_action(
            action_type="create_rule",
            payload={
                "pattern": "test",
                "pattern_type": "contains",
                "category_id": 99999,
            },
        )
        assert "error" in result

    @pytest.mark.asyncio
    async def test_confirm_create_rule_missing_pattern(self, orchestrator):
        """Should error when pattern is missing."""
        result = await orchestrator.confirm_action(
            action_type="create_rule",
            payload={"category_id": 1},
        )
        assert "error" in result


class TestUndoAction:
    """Tests for action undo functionality."""

    @pytest.mark.asyncio
    async def test_undo_categorize(self, orchestrator, db_session, sample_transactions):
        """Undoing a categorization should restore the previous category."""
        tx = sample_transactions[4]  # Amazon - Uncategorized
        original_category_id = tx.category_id
        rent = db_session.query(Category).filter_by(category_name="Rent").first()

        # First, execute the action
        confirm_result = await orchestrator.confirm_action(
            action_type="categorize",
            payload={
                "transaction_ids": [tx.transaction_id],
                "category_id": rent.category_id,
                "category_name": "Rent",
            },
        )
        assert confirm_result["success"] is True
        db_session.refresh(tx)
        assert tx.category_id == rent.category_id

        # Now undo it
        undo_result = await orchestrator.undo_action(confirm_result["action_log_ids"][0])
        assert undo_result["success"] is True
        assert undo_result["action"] == "undo_categorize"

        # Verify the transaction was restored
        db_session.refresh(tx)
        assert tx.category_id == original_category_id

    @pytest.mark.asyncio
    async def test_undo_create_rule(self, orchestrator, db_session, sample_transactions):
        """Undoing a rule creation should delete the rule."""
        groceries = db_session.query(Category).filter_by(category_name="Groceries").first()

        # First, create a rule
        confirm_result = await orchestrator.confirm_action(
            action_type="create_rule",
            payload={
                "pattern": "UndoTest",
                "pattern_type": "contains",
                "category_id": groceries.category_id,
                "category_name": "Groceries",
                "rule_name": "Undo Test Rule",
            },
        )
        assert confirm_result["success"] is True
        rule_id = confirm_result["rule_id"]

        # Verify rule exists
        assert db_session.query(CategoryRule).filter_by(rule_id=rule_id).first() is not None

        # Undo it
        undo_result = await orchestrator.undo_action(confirm_result["action_log_id"])
        assert undo_result["success"] is True
        assert undo_result["action"] == "undo_create_rule"

        # Verify rule was deleted
        assert db_session.query(CategoryRule).filter_by(rule_id=rule_id).first() is None

    @pytest.mark.asyncio
    async def test_undo_nonexistent_log(self, orchestrator):
        """Should error when action log doesn't exist."""
        result = await orchestrator.undo_action("nonexistent-id")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_undo_already_undone(self, orchestrator, db_session, sample_transactions):
        """Should error when action has already been undone."""
        tx = sample_transactions[4]
        rent = db_session.query(Category).filter_by(category_name="Rent").first()

        confirm_result = await orchestrator.confirm_action(
            action_type="categorize",
            payload={
                "transaction_ids": [tx.transaction_id],
                "category_id": rent.category_id,
                "category_name": "Rent",
            },
        )

        # Undo once
        await orchestrator.undo_action(confirm_result["action_log_ids"][0])

        # Try to undo again
        result = await orchestrator.undo_action(confirm_result["action_log_ids"][0])
        assert "error" in result
        assert "already been undone" in result["error"]


@pytest.fixture
def sample_entity(db_session):
    """Seed a sample entity for testing."""
    entity = Entity(
        entity_name="Personal",
        entity_type="personal",
        is_default=True,
    )
    db_session.add(entity)
    db_session.commit()
    return entity


class TestProposeEntityAssignment:
    """Tests for entity assignment proposal tool."""

    @pytest.mark.asyncio
    async def test_propose_by_ids(self, orchestrator, sample_transactions, sample_entity):
        tx_ids = [sample_transactions[0].transaction_id]
        result = await orchestrator.execute_tool("propose_entity_assignment", {
            "transaction_ids": tx_ids,
            "entity_name": "Personal",
        })
        assert result["type"] == "action_proposal"
        assert result["action"] == "assign_entity"
        assert result["requires_confirmation"] is True
        assert result["preview"]["transaction_count"] == 1
        assert result["preview"]["entity"] == "Personal"

    @pytest.mark.asyncio
    async def test_propose_by_merchant_pattern(self, orchestrator, sample_transactions, sample_entity):
        result = await orchestrator.execute_tool("propose_entity_assignment", {
            "merchant_pattern": "Foods",
            "entity_name": "Personal",
        })
        assert result["type"] == "action_proposal"
        assert result["preview"]["transaction_count"] == 1

    @pytest.mark.asyncio
    async def test_propose_unknown_entity(self, orchestrator, sample_transactions):
        result = await orchestrator.execute_tool("propose_entity_assignment", {
            "transaction_ids": [1],
            "entity_name": "NonExistent",
        })
        assert "error" in result

    @pytest.mark.asyncio
    async def test_propose_no_matching_transactions(self, orchestrator, sample_transactions, sample_entity):
        result = await orchestrator.execute_tool("propose_entity_assignment", {
            "merchant_pattern": "ZZZZZ_NO_MATCH",
            "entity_name": "Personal",
        })
        assert "error" in result

    @pytest.mark.asyncio
    async def test_propose_missing_ids_and_pattern(self, orchestrator, sample_entity):
        result = await orchestrator.execute_tool("propose_entity_assignment", {
            "entity_name": "Personal",
        })
        assert "error" in result


class TestConfirmEntityAssignment:
    """Tests for entity assignment action execution."""

    @pytest.mark.asyncio
    async def test_confirm_assigns_entity(self, orchestrator, db_session, sample_transactions, sample_entity):
        tx = sample_transactions[0]
        assert tx.entity_id is None

        result = await orchestrator.confirm_action(
            action_type="assign_entity",
            payload={
                "transaction_ids": [tx.transaction_id],
                "entity_id": sample_entity.entity_id,
                "entity_name": "Personal",
            },
            message_id="msg-entity",
        )

        assert result["success"] is True
        assert result["updated_count"] == 1
        assert result["entity"] == "Personal"
        assert result["undo_available"] is True

        db_session.refresh(tx)
        assert tx.entity_id == sample_entity.entity_id

    @pytest.mark.asyncio
    async def test_confirm_multiple(self, orchestrator, db_session, sample_transactions, sample_entity):
        tx_ids = [sample_transactions[0].transaction_id, sample_transactions[1].transaction_id]

        result = await orchestrator.confirm_action(
            action_type="assign_entity",
            payload={
                "transaction_ids": tx_ids,
                "entity_id": sample_entity.entity_id,
                "entity_name": "Personal",
            },
        )

        assert result["success"] is True
        assert result["updated_count"] == 2

    @pytest.mark.asyncio
    async def test_confirm_creates_action_log(self, orchestrator, db_session, sample_transactions, sample_entity):
        tx = sample_transactions[0]

        result = await orchestrator.confirm_action(
            action_type="assign_entity",
            payload={
                "transaction_ids": [tx.transaction_id],
                "entity_id": sample_entity.entity_id,
                "entity_name": "Personal",
            },
            message_id="msg-ent-log",
        )

        log = db_session.query(AssistantActionLog).filter_by(id=result["action_log_ids"][0]).first()
        assert log is not None
        assert log.action_type == "assign_entity"
        assert log.previous_state["entity_id"] is None
        assert log.new_state["entity_id"] == sample_entity.entity_id

    @pytest.mark.asyncio
    async def test_confirm_nonexistent_entity(self, orchestrator, sample_transactions):
        result = await orchestrator.confirm_action(
            action_type="assign_entity",
            payload={
                "transaction_ids": [sample_transactions[0].transaction_id],
                "entity_id": 99999,
                "entity_name": "Gone",
            },
        )
        assert "error" in result

    @pytest.mark.asyncio
    async def test_confirm_missing_payload(self, orchestrator):
        result = await orchestrator.confirm_action(
            action_type="assign_entity",
            payload={"transaction_ids": []},
        )
        assert "error" in result


class TestUndoEntityAssignment:
    """Tests for entity assignment undo."""

    @pytest.mark.asyncio
    async def test_undo_restores_previous_entity(self, orchestrator, db_session, sample_transactions, sample_entity):
        tx = sample_transactions[0]
        assert tx.entity_id is None

        confirm_result = await orchestrator.confirm_action(
            action_type="assign_entity",
            payload={
                "transaction_ids": [tx.transaction_id],
                "entity_id": sample_entity.entity_id,
                "entity_name": "Personal",
            },
        )
        db_session.refresh(tx)
        assert tx.entity_id == sample_entity.entity_id

        undo_result = await orchestrator.undo_action(confirm_result["action_log_ids"][0])
        assert undo_result["success"] is True
        assert undo_result["action"] == "undo_entity_assignment"

        db_session.refresh(tx)
        assert tx.entity_id is None
