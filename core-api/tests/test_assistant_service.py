"""
Tests for AI Assistant AssistantService.

Verifies the agentic chat loop, event streaming, tool call handling,
conversation management, and error handling with mocked LLM adapter.
"""

import pytest
from datetime import datetime, timezone
from typing import AsyncGenerator, Dict, Any, List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from financial_analysis.database.base import Base
from financial_analysis.database.models import Category, Transaction
from financial_analysis.database.assistant_models import (
    AssistantConversation,
    AssistantMessage,
)
from financial_analysis.services.assistant.assistant_service import AssistantService
from financial_analysis.services.assistant.llm_adapter import (
    LLMAdapter, StreamEvent, ToolCall, LLMResponse,
)


# ===== Mock LLM Adapter =====

class MockLLMAdapter(LLMAdapter):
    """Mock LLM adapter that returns predefined responses."""

    def __init__(self, responses: Optional[List[List[StreamEvent]]] = None):
        """
        Args:
            responses: List of response sequences. Each call to chat_completion
                      pops the first sequence. If exhausted, returns a simple content response.
        """
        self.responses = list(responses) if responses else []
        self.call_count = 0
        self.call_args: List[Dict] = []

    async def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = True,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[StreamEvent, None]:
        self.call_args.append({
            "messages": messages,
            "tools": tools,
            "stream": stream,
        })
        self.call_count += 1

        if self.responses:
            events = self.responses.pop(0)
        else:
            events = [
                StreamEvent(type="content", data="Default response"),
                StreamEvent(type="usage", data={"total_tokens": 10}),
                StreamEvent(type="done", data={"model": "mock-model"}),
            ]

        for event in events:
            yield event

    async def chat_completion_sync(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        return LLMResponse(
            content="Sync response",
            tool_calls=[],
            tokens_used=5,
            model="mock-model",
        )


# ===== Fixtures =====

@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Create categories needed by tool orchestrator
    groceries = Category(category_name="Groceries", category_type="Expense")
    salary = Category(category_name="Salary", category_type="Income")
    session.add_all([groceries, salary])
    session.commit()

    yield session
    session.close()


def make_service(db_session, responses=None) -> tuple:
    """Create an AssistantService with a mock LLM adapter."""
    mock_llm = MockLLMAdapter(responses)
    service = AssistantService(db=db_session, llm_adapter=mock_llm)
    return service, mock_llm


async def collect_events(gen) -> List[Dict[str, Any]]:
    """Collect all events from an async generator."""
    events = []
    async for event in gen:
        events.append(event)
    return events


# ===== Tests =====

class TestChatBasicFlow:
    """Tests for basic chat message flow."""

    @pytest.mark.asyncio
    async def test_emits_conversation_id(self, db_session):
        service, _ = make_service(db_session)
        events = await collect_events(service.chat("Hello"))

        conv_event = next(e for e in events if e["event"] == "conversation_id")
        assert conv_event["data"]["id"] is not None

    @pytest.mark.asyncio
    async def test_emits_content_delta(self, db_session):
        service, _ = make_service(db_session, [
            [
                StreamEvent(type="content", data="Hello "),
                StreamEvent(type="content", data="there!"),
                StreamEvent(type="usage", data={"total_tokens": 15}),
                StreamEvent(type="done", data={"model": "mock-model"}),
            ]
        ])
        events = await collect_events(service.chat("Hi"))

        deltas = [e for e in events if e["event"] == "content_delta"]
        assert len(deltas) == 2
        assert deltas[0]["data"]["delta"] == "Hello "
        assert deltas[1]["data"]["delta"] == "there!"

    @pytest.mark.asyncio
    async def test_emits_message_complete(self, db_session):
        service, _ = make_service(db_session, [
            [
                StreamEvent(type="content", data="Reply"),
                StreamEvent(type="usage", data={"total_tokens": 20}),
                StreamEvent(type="done", data={"model": "gpt-4o"}),
            ]
        ])
        events = await collect_events(service.chat("Question"))

        complete = next(e for e in events if e["event"] == "message_complete")
        assert complete["data"]["tokens_used"] == 20
        assert complete["data"]["model"] == "gpt-4o"
        # message_id should be an actual message ID, not conversation ID
        assert complete["data"]["message_id"] is not None

    @pytest.mark.asyncio
    async def test_saves_user_message(self, db_session):
        service, _ = make_service(db_session)
        events = await collect_events(service.chat("Test message"))

        conv_id = next(e for e in events if e["event"] == "conversation_id")["data"]["id"]
        msgs = db_session.query(AssistantMessage).filter_by(
            conversation_id=conv_id, role="user"
        ).all()
        assert len(msgs) == 1
        assert msgs[0].content == "Test message"

    @pytest.mark.asyncio
    async def test_saves_assistant_message(self, db_session):
        service, _ = make_service(db_session, [
            [
                StreamEvent(type="content", data="My reply"),
                StreamEvent(type="usage", data={"total_tokens": 10}),
                StreamEvent(type="done", data={"model": "mock"}),
            ]
        ])
        events = await collect_events(service.chat("Hello"))

        conv_id = next(e for e in events if e["event"] == "conversation_id")["data"]["id"]
        msgs = db_session.query(AssistantMessage).filter_by(
            conversation_id=conv_id, role="assistant"
        ).all()
        assert len(msgs) == 1
        assert msgs[0].content == "My reply"


class TestChatWithExistingConversation:
    """Tests for continuing an existing conversation."""

    @pytest.mark.asyncio
    async def test_reuses_conversation_id(self, db_session):
        service, _ = make_service(db_session)

        # First message
        events1 = await collect_events(service.chat("First"))
        conv_id = next(e for e in events1 if e["event"] == "conversation_id")["data"]["id"]

        # Second message in same conversation
        events2 = await collect_events(service.chat("Second", conversation_id=conv_id))
        conv_id2 = next(e for e in events2 if e["event"] == "conversation_id")["data"]["id"]

        assert conv_id == conv_id2

    @pytest.mark.asyncio
    async def test_includes_history_in_llm_call(self, db_session):
        service, mock_llm = make_service(db_session)

        events1 = await collect_events(service.chat("First"))
        conv_id = next(e for e in events1 if e["event"] == "conversation_id")["data"]["id"]

        await collect_events(service.chat("Second", conversation_id=conv_id))

        # Second LLM call should include history
        second_call = mock_llm.call_args[1]
        messages = second_call["messages"]
        # System + history (user "First" + assistant reply) + new user "Second"
        assert len(messages) >= 4


class TestChatWithToolCalls:
    """Tests for tool call handling in chat loop."""

    @pytest.mark.asyncio
    async def test_tool_call_events(self, db_session):
        tool_call = ToolCall(id="call_1", name="create_navigation_link", arguments={"page": "dashboard"})
        service, _ = make_service(db_session, [
            # First LLM call returns tool call
            [
                StreamEvent(type="tool_call", data=tool_call),
                StreamEvent(type="usage", data={"total_tokens": 10}),
                StreamEvent(type="done", data={"model": "mock"}),
            ],
            # Second LLM call (after tool execution) returns content
            [
                StreamEvent(type="content", data="Here's your dashboard link."),
                StreamEvent(type="usage", data={"total_tokens": 15}),
                StreamEvent(type="done", data={"model": "mock"}),
            ],
        ])

        events = await collect_events(service.chat("Show me the dashboard"))

        # Should have tool_call and tool_result events
        tc_events = [e for e in events if e["event"] == "tool_call"]
        assert len(tc_events) == 1
        assert tc_events[0]["data"]["name"] == "create_navigation_link"

        tr_events = [e for e in events if e["event"] == "tool_result"]
        assert len(tr_events) == 1

    @pytest.mark.asyncio
    async def test_tool_call_triggers_followup_llm(self, db_session):
        tool_call = ToolCall(id="call_1", name="create_navigation_link", arguments={"page": "transactions"})
        service, mock_llm = make_service(db_session, [
            [
                StreamEvent(type="tool_call", data=tool_call),
                StreamEvent(type="usage", data={"total_tokens": 10}),
                StreamEvent(type="done", data={"model": "mock"}),
            ],
            [
                StreamEvent(type="content", data="Done."),
                StreamEvent(type="usage", data={"total_tokens": 5}),
                StreamEvent(type="done", data={"model": "mock"}),
            ],
        ])

        await collect_events(service.chat("Go to transactions"))

        # LLM should have been called twice
        assert mock_llm.call_count == 2

    @pytest.mark.asyncio
    async def test_tool_result_saved_to_db(self, db_session):
        tool_call = ToolCall(id="call_1", name="create_navigation_link", arguments={"page": "dashboard"})
        service, _ = make_service(db_session, [
            [
                StreamEvent(type="tool_call", data=tool_call),
                StreamEvent(type="usage", data={"total_tokens": 10}),
                StreamEvent(type="done", data={"model": "mock"}),
            ],
            [
                StreamEvent(type="content", data="Here you go."),
                StreamEvent(type="usage", data={"total_tokens": 5}),
                StreamEvent(type="done", data={"model": "mock"}),
            ],
        ])

        events = await collect_events(service.chat("Dashboard"))
        conv_id = next(e for e in events if e["event"] == "conversation_id")["data"]["id"]

        tool_msgs = db_session.query(AssistantMessage).filter_by(
            conversation_id=conv_id, role="tool"
        ).all()
        assert len(tool_msgs) == 1
        assert tool_msgs[0].tool_call_id == "call_1"

    @pytest.mark.asyncio
    async def test_navigation_emits_action_card(self, db_session):
        tool_call = ToolCall(id="call_1", name="create_navigation_link", arguments={"page": "analysis"})
        service, _ = make_service(db_session, [
            [
                StreamEvent(type="tool_call", data=tool_call),
                StreamEvent(type="usage", data={"total_tokens": 10}),
                StreamEvent(type="done", data={"model": "mock"}),
            ],
            [
                StreamEvent(type="content", data="Here's the link."),
                StreamEvent(type="usage", data={"total_tokens": 5}),
                StreamEvent(type="done", data={"model": "mock"}),
            ],
        ])

        events = await collect_events(service.chat("Go to analysis"))

        action_cards = [e for e in events if e["event"] == "action_card"]
        assert len(action_cards) == 1
        assert action_cards[0]["data"]["type"] == "navigation"


class TestChatErrorHandling:
    """Tests for error handling in chat flow."""

    @pytest.mark.asyncio
    async def test_llm_error_event(self, db_session):
        service, _ = make_service(db_session, [
            [StreamEvent(type="error", data="API rate limit exceeded")],
        ])

        events = await collect_events(service.chat("Hello"))
        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert "rate limit" in error_events[0]["data"]["message"]

    @pytest.mark.asyncio
    async def test_llm_exception_caught(self, db_session):
        """Test that exceptions from LLM are caught and emitted as error events."""

        class FailingLLM(LLMAdapter):
            async def chat_completion(self, **kwargs):
                raise ConnectionError("Connection refused")
                yield  # make it a generator

            async def chat_completion_sync(self, **kwargs):
                raise ConnectionError("Connection refused")

        service = AssistantService(db=db_session, llm_adapter=FailingLLM())
        events = await collect_events(service.chat("Hello"))

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) == 1
        assert "Connection refused" in error_events[0]["data"]["message"]

    @pytest.mark.asyncio
    async def test_error_stops_streaming(self, db_session):
        """After an error event, no more events should follow except conversation_id."""
        service, _ = make_service(db_session, [
            [StreamEvent(type="error", data="Something broke")],
        ])

        events = await collect_events(service.chat("Hello"))
        # Should have: conversation_id, error — no message_complete
        event_types = [e["event"] for e in events]
        assert "message_complete" not in event_types


class TestConversationManagement:
    """Tests for conversation CRUD through the service."""

    @pytest.mark.asyncio
    async def test_get_conversations(self, db_session):
        service, _ = make_service(db_session)

        # Create conversations by chatting
        await collect_events(service.chat("First conversation"))
        await collect_events(service.chat("Second conversation"))

        convs = await service.get_conversations()
        assert len(convs) == 2

    @pytest.mark.asyncio
    async def test_get_conversation_messages(self, db_session):
        service, _ = make_service(db_session)

        events = await collect_events(service.chat("Hello"))
        conv_id = next(e for e in events if e["event"] == "conversation_id")["data"]["id"]

        messages = await service.get_conversation_messages(conv_id)
        # Should have user message + assistant message
        assert len(messages) >= 2

    @pytest.mark.asyncio
    async def test_archive_conversation(self, db_session):
        service, _ = make_service(db_session)

        events = await collect_events(service.chat("Hello"))
        conv_id = next(e for e in events if e["event"] == "conversation_id")["data"]["id"]

        result = await service.archive_conversation(conv_id)
        assert result is True

        # Should not appear in default listing
        convs = await service.get_conversations()
        assert all(c["id"] != conv_id for c in convs)

    @pytest.mark.asyncio
    async def test_delete_conversation(self, db_session):
        service, _ = make_service(db_session)

        events = await collect_events(service.chat("Hello"))
        conv_id = next(e for e in events if e["event"] == "conversation_id")["data"]["id"]

        result = await service.delete_conversation(conv_id)
        assert result is True

        convs = await service.get_conversations()
        assert len(convs) == 0


class TestMessageIdFix:
    """Tests verifying the message_id fix (was returning conversation.id, now returns message.id)."""

    @pytest.mark.asyncio
    async def test_message_id_is_not_conversation_id(self, db_session):
        service, _ = make_service(db_session, [
            [
                StreamEvent(type="content", data="Reply"),
                StreamEvent(type="usage", data={"total_tokens": 10}),
                StreamEvent(type="done", data={"model": "mock"}),
            ]
        ])

        events = await collect_events(service.chat("Hello"))
        conv_id = next(e for e in events if e["event"] == "conversation_id")["data"]["id"]
        msg_id = next(e for e in events if e["event"] == "message_complete")["data"]["message_id"]

        # message_id should be the actual message UUID, not the conversation UUID
        # They should be different since they're separate entities
        assert msg_id != conv_id

    @pytest.mark.asyncio
    async def test_message_id_exists_in_db(self, db_session):
        service, _ = make_service(db_session, [
            [
                StreamEvent(type="content", data="Reply"),
                StreamEvent(type="usage", data={"total_tokens": 10}),
                StreamEvent(type="done", data={"model": "mock"}),
            ]
        ])

        events = await collect_events(service.chat("Hello"))
        msg_id = next(e for e in events if e["event"] == "message_complete")["data"]["message_id"]

        msg = db_session.query(AssistantMessage).filter_by(id=msg_id).first()
        assert msg is not None
        assert msg.role == "assistant"
