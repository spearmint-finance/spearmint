"""
Database models for AI Assistant feature.

Stores conversation history, messages, action audit logs,
user preferences, and proactive insights.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean,
    ForeignKey, Index, JSON
)
from sqlalchemy.orm import relationship
from .base import Base


def utc_now():
    """Get current UTC time (timezone-aware)."""
    return datetime.now(timezone.utc)


class AssistantConversation(Base):
    """
    Conversation sessions for the AI assistant.

    Groups related messages into logical conversations.
    """
    __tablename__ = "assistant_conversations"

    id = Column(String(36), primary_key=True)  # UUID
    title = Column(String(255))  # Auto-generated from first message
    message_count = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)  # For usage tracking
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    # Relationships
    messages = relationship(
        "AssistantMessage",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="AssistantMessage.created_at"
    )

    __table_args__ = (
        Index('idx_conversations_updated', 'updated_at'),
        Index('idx_conversations_archived', 'is_archived'),
    )

    def __repr__(self):
        return f"<AssistantConversation(id={self.id}, title='{self.title}')>"


class AssistantMessage(Base):
    """
    Individual messages within conversations.

    Stores user messages, assistant responses, and tool calls/results.
    """
    __tablename__ = "assistant_messages"

    id = Column(String(36), primary_key=True)  # UUID
    conversation_id = Column(
        String(36),
        ForeignKey('assistant_conversations.id', ondelete='CASCADE'),
        nullable=False
    )
    role = Column(String(20), nullable=False)  # 'user', 'assistant', 'system', 'tool'
    content = Column(Text, nullable=False)  # Message text or tool result JSON
    tool_calls = Column(JSON)  # JSON array of tool calls (if assistant)
    tool_call_id = Column(String(50))  # Tool call ID (if tool response)
    tokens_used = Column(Integer)  # Token count for this message
    model = Column(String(50))  # Model used (e.g., 'gpt-4o')

    # For action messages
    action_type = Column(String(50))  # 'categorize', 'create_rule', etc.
    action_status = Column(String(20))  # 'proposed', 'confirmed', 'executed', 'undone'
    action_payload = Column(JSON)  # Action details

    created_at = Column(DateTime, default=utc_now, nullable=False)

    # Relationships
    conversation = relationship("AssistantConversation", back_populates="messages")
    action_logs = relationship(
        "AssistantActionLog",
        back_populates="message",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_messages_conversation', 'conversation_id'),
        Index('idx_messages_created', 'created_at'),
        Index('idx_messages_role', 'role'),
    )

    def __repr__(self):
        return f"<AssistantMessage(id={self.id}, role='{self.role}')>"


class AssistantActionLog(Base):
    """
    Audit log for AI-initiated actions.

    Enables undo capability by storing previous state before changes.
    """
    __tablename__ = "assistant_action_log"

    id = Column(String(36), primary_key=True)  # UUID
    message_id = Column(
        String(36),
        ForeignKey('assistant_messages.id', ondelete='SET NULL'),
        nullable=True
    )
    action_type = Column(String(50), nullable=False)  # 'categorize_transaction', 'create_rule', etc.
    entity_type = Column(String(50), nullable=False)  # 'transaction', 'category_rule', etc.
    entity_id = Column(String(50), nullable=False)  # ID of affected entity
    previous_state = Column(JSON)  # JSON snapshot before change
    new_state = Column(JSON)  # JSON snapshot after change
    executed_at = Column(DateTime, default=utc_now, nullable=False)
    undone_at = Column(DateTime)  # NULL if not undone

    # Relationships
    message = relationship("AssistantMessage", back_populates="action_logs")

    __table_args__ = (
        Index('idx_action_log_entity', 'entity_type', 'entity_id'),
        Index('idx_action_log_message', 'message_id'),
        Index('idx_action_log_executed', 'executed_at'),
    )

    def __repr__(self):
        return f"<AssistantActionLog(id={self.id}, action='{self.action_type}')>"


class AssistantPreferences(Base):
    """
    User preferences for AI Assistant.

    Stores LLM configuration, API keys, and insight preferences.
    """
    __tablename__ = "assistant_preferences"

    id = Column(String(36), primary_key=True)  # Single row or user_id for multi-user
    llm_provider = Column(String(20), default='openai')
    llm_model = Column(String(50), default='gpt-4o')
    openai_api_key_encrypted = Column(Text)  # Encrypted API key
    insights_enabled = Column(Boolean, default=True)
    anomaly_threshold = Column(String(10), default='0.25')  # 25% deviation triggers insight
    max_history_messages = Column(Integer, default=50)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    def __repr__(self):
        return f"<AssistantPreferences(id={self.id}, provider='{self.llm_provider}')>"


class AssistantInsight(Base):
    """
    Proactive insights queue.

    Stores insights generated by the system for user review.
    """
    __tablename__ = "assistant_insights"

    id = Column(String(36), primary_key=True)  # UUID
    insight_type = Column(String(30), nullable=False)  # 'anomaly', 'uncategorized', 'duplicate', etc.
    priority = Column(Integer, default=0)  # Higher = more important
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)  # Markdown content
    action_type = Column(String(50))  # Suggested action type
    action_payload = Column(JSON)  # JSON for suggested action
    created_at = Column(DateTime, default=utc_now, nullable=False)
    dismissed_at = Column(DateTime)
    acted_on_at = Column(DateTime)

    __table_args__ = (
        Index('idx_insights_pending', 'dismissed_at', 'acted_on_at', 'priority'),
        Index('idx_insights_type', 'insight_type'),
        Index('idx_insights_created', 'created_at'),
    )

    def __repr__(self):
        return f"<AssistantInsight(id={self.id}, type='{self.insight_type}')>"
