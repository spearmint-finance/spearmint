"""
Tests for AI Assistant ConversationManager.

Verifies conversation CRUD, message persistence, context building,
and system prompt generation.
"""

import pytest
from datetime import date, datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from financial_analysis.database.base import Base
from financial_analysis.database.assistant_models import (
    AssistantConversation,
    AssistantMessage,
)
from financial_analysis.services.assistant.conversation_manager import (
    ConversationManager,
)


@pytest.fixture
def db_session():
    """Create a test database session with assistant tables."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def manager(db_session):
    """Create a ConversationManager with test DB."""
    return ConversationManager(db_session)


class TestGetOrCreateConversation:
    """Tests for conversation creation and retrieval."""

    def test_create_new_conversation(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        assert conv.id is not None
        assert len(conv.id) == 36  # UUID format
        assert conv.message_count == 0
        assert conv.is_archived is False

    def test_retrieve_existing_conversation(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        retrieved = manager.get_or_create_conversation(conv.id)
        assert retrieved.id == conv.id

    def test_nonexistent_id_creates_new(self, manager, db_session):
        conv = manager.get_or_create_conversation("nonexistent-id")
        assert conv.id != "nonexistent-id"

    def test_multiple_conversations(self, manager, db_session):
        conv1 = manager.get_or_create_conversation()
        conv2 = manager.get_or_create_conversation()
        assert conv1.id != conv2.id


class TestAddMessage:
    """Tests for message persistence."""

    def test_add_user_message(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        msg = manager.add_message(
            conversation_id=conv.id,
            role="user",
            content="Hello",
        )
        assert msg.id is not None
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.conversation_id == conv.id

    def test_message_count_increments(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        manager.add_message(conv.id, "user", "First")
        manager.add_message(conv.id, "assistant", "Reply")

        db_session.refresh(conv)
        assert conv.message_count == 2

    def test_token_tracking(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        manager.add_message(conv.id, "assistant", "Reply", tokens_used=100)
        manager.add_message(conv.id, "assistant", "More", tokens_used=50)

        db_session.refresh(conv)
        assert conv.total_tokens == 150

    def test_title_from_first_user_message(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        manager.add_message(conv.id, "user", "How much did I spend on groceries?")

        db_session.refresh(conv)
        assert conv.title == "How much did I spend on groceries?"

    def test_title_truncated_for_long_messages(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        long_msg = "x" * 150
        manager.add_message(conv.id, "user", long_msg)

        db_session.refresh(conv)
        assert len(conv.title) == 103  # 100 chars + "..."
        assert conv.title.endswith("...")

    def test_title_not_overwritten_by_second_message(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        manager.add_message(conv.id, "user", "First question")
        manager.add_message(conv.id, "user", "Second question")

        db_session.refresh(conv)
        assert conv.title == "First question"

    def test_add_message_with_tool_calls(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        tool_calls = [
            {"id": "call_1", "name": "get_spending_summary", "arguments": {"period": "this_month"}}
        ]
        msg = manager.add_message(
            conv.id, "assistant", "",
            tool_calls=tool_calls,
        )
        assert msg.tool_calls == tool_calls

    def test_add_tool_response(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        msg = manager.add_message(
            conv.id, "tool", '{"total": 500}',
            tool_call_id="call_1",
        )
        assert msg.tool_call_id == "call_1"
        assert msg.role == "tool"


class TestGetRecentMessages:
    """Tests for message retrieval and formatting."""

    def test_empty_conversation(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        messages = manager.get_recent_messages(conv.id)
        assert messages == []

    def test_chronological_order(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        manager.add_message(conv.id, "user", "First")
        manager.add_message(conv.id, "assistant", "Second")
        manager.add_message(conv.id, "user", "Third")

        messages = manager.get_recent_messages(conv.id)
        assert len(messages) == 3
        assert messages[0]["content"] == "First"
        assert messages[1]["content"] == "Second"
        assert messages[2]["content"] == "Third"

    def test_respects_limit(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        for i in range(10):
            manager.add_message(conv.id, "user", f"Message {i}")

        messages = manager.get_recent_messages(conv.id, limit=3)
        assert len(messages) == 3

    def test_tool_calls_formatted_for_openai(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        manager.add_message(
            conv.id, "assistant", "",
            tool_calls=[{"id": "call_1", "name": "get_cash_flow", "arguments": {"period": "this_month"}}],
        )

        messages = manager.get_recent_messages(conv.id)
        assert len(messages) == 1
        msg = messages[0]
        assert "tool_calls" in msg
        assert msg["tool_calls"][0]["type"] == "function"
        assert msg["tool_calls"][0]["function"]["name"] == "get_cash_flow"

    def test_tool_response_includes_call_id(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        manager.add_message(conv.id, "tool", '{"data": 1}', tool_call_id="call_1")

        messages = manager.get_recent_messages(conv.id)
        assert messages[0]["tool_call_id"] == "call_1"


class TestBuildMessages:
    """Tests for complete message list construction."""

    def test_includes_system_prompt(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        messages = manager.build_messages(conv.id, "Hello")

        assert messages[0]["role"] == "system"
        assert "Minty" in messages[0]["content"]

    def test_includes_new_message(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        messages = manager.build_messages(conv.id, "What's my balance?")

        assert messages[-1]["role"] == "user"
        assert messages[-1]["content"] == "What's my balance?"

    def test_includes_history(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        manager.add_message(conv.id, "user", "Old question")
        manager.add_message(conv.id, "assistant", "Old answer")

        messages = manager.build_messages(conv.id, "New question")
        # system + 2 history + new message
        assert len(messages) == 4

    def test_context_in_system_prompt(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        context = {
            "current_page": "transactions",
            "active_filters": {"category": "Groceries"},
        }
        messages = manager.build_messages(conv.id, "Hello", context=context)

        system_content = messages[0]["content"]
        assert "transactions" in system_content
        assert "Groceries" in system_content


class TestSystemPrompt:
    """Tests for system prompt generation."""

    def test_includes_date(self, manager):
        prompt = manager._build_system_prompt({})
        assert date.today().isoformat() in prompt["content"]

    def test_includes_context_page(self, manager):
        prompt = manager._build_system_prompt({"current_page": "analysis"})
        assert "analysis" in prompt["content"]

    def test_includes_selected_transaction(self, manager):
        prompt = manager._build_system_prompt({"selected_transaction_id": 42})
        assert "42" in prompt["content"]

    def test_includes_active_filters(self, manager):
        prompt = manager._build_system_prompt({
            "active_filters": {
                "date_from": "2026-01-01",
                "category": "Rent",
            }
        })
        content = prompt["content"]
        assert "2026-01-01" in content
        assert "Rent" in content


class TestListConversations:
    """Tests for conversation listing."""

    def test_empty_list(self, manager, db_session):
        convs = manager.list_conversations()
        assert convs == []

    def test_returns_conversations(self, manager, db_session):
        manager.get_or_create_conversation()
        manager.get_or_create_conversation()

        convs = manager.list_conversations()
        assert len(convs) == 2

    def test_excludes_archived_by_default(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        manager.archive_conversation(conv.id)

        convs = manager.list_conversations()
        assert len(convs) == 0

    def test_includes_archived_when_requested(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        manager.archive_conversation(conv.id)

        convs = manager.list_conversations(include_archived=True)
        assert len(convs) == 1

    def test_respects_limit(self, manager, db_session):
        for _ in range(5):
            manager.get_or_create_conversation()

        convs = manager.list_conversations(limit=3)
        assert len(convs) == 3


class TestArchiveConversation:
    """Tests for conversation archival."""

    def test_archive_existing(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        result = manager.archive_conversation(conv.id)
        assert result is True

        db_session.refresh(conv)
        assert conv.is_archived is True

    def test_archive_nonexistent(self, manager, db_session):
        result = manager.archive_conversation("nonexistent")
        assert result is False


class TestDeleteConversation:
    """Tests for conversation deletion."""

    def test_delete_existing(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        conv_id = conv.id
        result = manager.delete_conversation(conv_id)
        assert result is True

        found = db_session.query(AssistantConversation).filter_by(id=conv_id).first()
        assert found is None

    def test_delete_nonexistent(self, manager, db_session):
        result = manager.delete_conversation("nonexistent")
        assert result is False

    def test_cascade_deletes_messages(self, manager, db_session):
        conv = manager.get_or_create_conversation()
        manager.add_message(conv.id, "user", "Hello")
        manager.add_message(conv.id, "assistant", "Hi")

        conv_id = conv.id
        manager.delete_conversation(conv_id)

        msgs = db_session.query(AssistantMessage).filter_by(conversation_id=conv_id).all()
        assert len(msgs) == 0


class TestCleanupOldConversations:
    """Tests for conversation cleanup."""

    def test_no_cleanup_under_limit(self, manager, db_session):
        for _ in range(3):
            manager.get_or_create_conversation()

        deleted = manager.cleanup_old_conversations(keep_count=5)
        assert deleted == 0

    def test_cleanup_over_limit(self, manager, db_session):
        for _ in range(5):
            manager.get_or_create_conversation()

        deleted = manager.cleanup_old_conversations(keep_count=2)
        assert deleted == 3

        remaining = db_session.query(AssistantConversation).count()
        assert remaining == 2
