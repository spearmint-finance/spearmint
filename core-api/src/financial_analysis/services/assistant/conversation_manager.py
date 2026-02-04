"""
Conversation Manager for AI Assistant.

Handles conversation history, context building, and system prompt generation.
"""

from datetime import date, datetime, timezone
from typing import List, Dict, Any, Optional
from uuid import uuid4
import json
import logging

from sqlalchemy.orm import Session
from sqlalchemy import desc

from ...database.assistant_models import (
    AssistantConversation,
    AssistantMessage,
)

logger = logging.getLogger(__name__)


class ConversationManager:
    """
    Manages conversation history and context for the AI assistant.

    Responsibilities:
    - Create and retrieve conversations
    - Persist messages to database
    - Build message context for LLM calls
    - Generate system prompts with dynamic context
    """

    MAX_CONTEXT_MESSAGES = 20  # Max messages to include in LLM context
    MAX_CONVERSATIONS = 50  # Max conversations to keep per user

    def __init__(self, db: Session):
        """
        Initialize conversation manager.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def get_or_create_conversation(
        self,
        conversation_id: Optional[str] = None
    ) -> AssistantConversation:
        """
        Get existing conversation or create a new one.

        Args:
            conversation_id: Optional ID of existing conversation

        Returns:
            AssistantConversation instance
        """
        if conversation_id:
            conv = self.db.query(AssistantConversation).filter(
                AssistantConversation.id == conversation_id
            ).first()
            if conv:
                return conv

        # Create new conversation
        conv = AssistantConversation(
            id=str(uuid4()),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        self.db.add(conv)
        self.db.commit()
        self.db.refresh(conv)

        logger.info(f"Created new conversation: {conv.id}")
        return conv

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        tool_calls: Optional[List[Dict]] = None,
        tool_call_id: Optional[str] = None,
        tokens_used: Optional[int] = None,
        model: Optional[str] = None,
        action_type: Optional[str] = None,
        action_status: Optional[str] = None,
        action_payload: Optional[Dict] = None,
    ) -> AssistantMessage:
        """
        Add a message to a conversation.

        Args:
            conversation_id: ID of the conversation
            role: Message role ('user', 'assistant', 'system', 'tool')
            content: Message content
            tool_calls: Optional tool calls made by assistant
            tool_call_id: Optional tool call ID (for tool responses)
            tokens_used: Optional token count
            model: Optional model name
            action_type: Optional action type for action messages
            action_status: Optional action status
            action_payload: Optional action payload

        Returns:
            Created AssistantMessage
        """
        message = AssistantMessage(
            id=str(uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_call_id=tool_call_id,
            tokens_used=tokens_used,
            model=model,
            action_type=action_type,
            action_status=action_status,
            action_payload=action_payload,
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(message)

        # Update conversation
        conv = self.db.query(AssistantConversation).filter(
            AssistantConversation.id == conversation_id
        ).first()
        if conv:
            conv.message_count = (conv.message_count or 0) + 1
            if tokens_used:
                conv.total_tokens = (conv.total_tokens or 0) + tokens_used
            conv.updated_at = datetime.now(timezone.utc)

            # Set title from first user message
            if not conv.title and role == 'user':
                conv.title = content[:100] + ('...' if len(content) > 100 else '')

        self.db.commit()
        self.db.refresh(message)

        return message

    def get_recent_messages(
        self,
        conversation_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get recent messages from a conversation formatted for LLM.

        Args:
            conversation_id: ID of the conversation
            limit: Maximum number of messages (defaults to MAX_CONTEXT_MESSAGES)

        Returns:
            List of message dicts with 'role' and 'content'
        """
        limit = limit or self.MAX_CONTEXT_MESSAGES

        messages = self.db.query(AssistantMessage).filter(
            AssistantMessage.conversation_id == conversation_id
        ).order_by(
            desc(AssistantMessage.created_at)
        ).limit(limit).all()

        # Reverse to get chronological order
        messages = list(reversed(messages))

        result = []
        for msg in messages:
            msg_dict = {"role": msg.role, "content": msg.content}

            # Handle tool calls - convert to OpenAI format
            if msg.tool_calls:
                msg_dict["tool_calls"] = [
                    {
                        "id": tc.get("id"),
                        "type": "function",
                        "function": {
                            "name": tc.get("name"),
                            "arguments": json.dumps(tc.get("arguments", {})) if isinstance(tc.get("arguments"), dict) else tc.get("arguments", "{}")
                        }
                    }
                    for tc in msg.tool_calls
                ]

            # Handle tool responses
            if msg.tool_call_id:
                msg_dict["tool_call_id"] = msg.tool_call_id

            result.append(msg_dict)

        return result

    def build_messages(
        self,
        conversation_id: str,
        new_message: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Build complete message list for LLM including history and context.

        Args:
            conversation_id: ID of the conversation
            new_message: New user message to append
            context: Optional context dict (current page, filters, etc.)

        Returns:
            List of messages ready for LLM API call
        """
        context = context or {}

        # Start with system prompt
        messages = [self._build_system_prompt(context)]

        # Add conversation history
        history = self.get_recent_messages(conversation_id)
        messages.extend(history)

        # Add new user message
        messages.append({"role": "user", "content": new_message})

        return messages

    def _build_system_prompt(self, context: Dict[str, Any]) -> Dict[str, str]:
        """
        Build system prompt with dynamic context.

        Args:
            context: Context dict with current page, filters, etc.

        Returns:
            System message dict
        """
        today = date.today().isoformat()

        # Extract context values
        current_page = context.get('current_page', 'unknown')
        selected_transaction_id = context.get('selected_transaction_id')
        active_filters = context.get('active_filters', {})

        # Format active filters
        filters_str = "none"
        if active_filters:
            filter_parts = []
            if active_filters.get('date_from'):
                filter_parts.append(f"from {active_filters['date_from']}")
            if active_filters.get('date_to'):
                filter_parts.append(f"to {active_filters['date_to']}")
            if active_filters.get('category'):
                filter_parts.append(f"category: {active_filters['category']}")
            if active_filters.get('account'):
                filter_parts.append(f"account: {active_filters['account']}")
            if filter_parts:
                filters_str = ", ".join(filter_parts)

        prompt = f"""You are Minty, a helpful and friendly financial assistant for Spearmint, a personal finance application.

Today's date: {today}

Your capabilities:
- Answer questions about spending, income, and account balances
- Search for specific transactions by merchant, amount, or date
- Analyze spending trends and patterns
- Compare spending between time periods
- Help categorize transactions (with user confirmation)
- Create rules for automatic categorization
- Navigate users to relevant pages in the app

Guidelines:
- Always cite your data sources (e.g., "Based on 23 transactions from January 1-31...")
- Use currency formatting with dollar signs and commas ($1,234.56)
- When comparing periods, show both absolute amounts and percentage changes
- For any action that modifies data, clearly explain what will change and ask for confirmation
- Keep responses concise but informative
- Be conversational and helpful, but stay focused on financial topics
- If you're unsure about something, ask clarifying questions

Current context:
- Page: {current_page}
- Selected transaction: {selected_transaction_id or 'none'}
- Active filters: {filters_str}

When the user refers to "this" or "these", consider the current page context and any selected items.
"""
        return {"role": "system", "content": prompt}

    def list_conversations(
        self,
        limit: int = 20,
        include_archived: bool = False
    ) -> List[AssistantConversation]:
        """
        List recent conversations.

        Args:
            limit: Maximum number of conversations to return
            include_archived: Whether to include archived conversations

        Returns:
            List of AssistantConversation objects
        """
        query = self.db.query(AssistantConversation)

        if not include_archived:
            query = query.filter(AssistantConversation.is_archived == False)

        return query.order_by(
            desc(AssistantConversation.updated_at)
        ).limit(limit).all()

    def archive_conversation(self, conversation_id: str) -> bool:
        """
        Archive a conversation.

        Args:
            conversation_id: ID of the conversation to archive

        Returns:
            True if successful, False if not found
        """
        conv = self.db.query(AssistantConversation).filter(
            AssistantConversation.id == conversation_id
        ).first()

        if not conv:
            return False

        conv.is_archived = True
        conv.updated_at = datetime.now(timezone.utc)
        self.db.commit()

        return True

    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation and all its messages.

        Args:
            conversation_id: ID of the conversation to delete

        Returns:
            True if successful, False if not found
        """
        conv = self.db.query(AssistantConversation).filter(
            AssistantConversation.id == conversation_id
        ).first()

        if not conv:
            return False

        self.db.delete(conv)
        self.db.commit()

        logger.info(f"Deleted conversation: {conversation_id}")
        return True

    def cleanup_old_conversations(self, keep_count: int = None) -> int:
        """
        Remove old conversations beyond the keep limit.

        Args:
            keep_count: Number of conversations to keep (defaults to MAX_CONVERSATIONS)

        Returns:
            Number of conversations deleted
        """
        keep_count = keep_count or self.MAX_CONVERSATIONS

        # Get all conversations ordered by update time
        all_convs = self.db.query(AssistantConversation).order_by(
            desc(AssistantConversation.updated_at)
        ).all()

        if len(all_convs) <= keep_count:
            return 0

        # Delete conversations beyond the limit
        to_delete = all_convs[keep_count:]
        count = len(to_delete)

        for conv in to_delete:
            self.db.delete(conv)

        self.db.commit()
        logger.info(f"Cleaned up {count} old conversations")

        return count
