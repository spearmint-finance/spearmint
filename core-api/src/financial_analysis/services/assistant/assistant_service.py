"""
Main Assistant Service for AI Financial Assistant.

Orchestrates the conversation flow between user, LLM, and tools.
"""

from typing import Dict, Any, Optional, List, AsyncGenerator
import json
import logging

from sqlalchemy.orm import Session

from .llm_adapter import LLMAdapter, OpenAIAdapter, StreamEvent, ToolCall
from .conversation_manager import ConversationManager
from .tool_orchestrator import ToolOrchestrator
from .tools import ASSISTANT_TOOLS, READ_ONLY_TOOLS

logger = logging.getLogger(__name__)


class AssistantService:
    """
    Main service for AI Financial Assistant.

    Coordinates:
    - Conversation history management
    - LLM API calls with streaming
    - Tool execution and response formatting
    """

    def __init__(
        self,
        db: Session,
        llm_adapter: LLMAdapter,
    ):
        """
        Initialize assistant service.

        Args:
            db: SQLAlchemy database session
            llm_adapter: LLM adapter instance (OpenAI, etc.)
        """
        self.db = db
        self.llm = llm_adapter
        self.conversation_manager = ConversationManager(db)
        self.tool_orchestrator = ToolOrchestrator(db)

    async def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Process a chat message and stream the response.

        Args:
            message: User's message
            conversation_id: Optional existing conversation ID
            context: Optional context (current page, filters, etc.)

        Yields:
            SSE event dicts for streaming to frontend
        """
        context = context or {}

        # Get or create conversation
        conversation = self.conversation_manager.get_or_create_conversation(
            conversation_id
        )

        # Emit conversation ID
        yield {
            "event": "conversation_id",
            "data": {"id": conversation.id}
        }

        # Save user message
        self.conversation_manager.add_message(
            conversation_id=conversation.id,
            role="user",
            content=message,
        )

        # Build messages for LLM
        messages = self.conversation_manager.build_messages(
            conversation_id=conversation.id,
            new_message=message,
            context=context,
        )

        # Call LLM with streaming
        full_content = ""
        tool_calls: List[ToolCall] = []
        tokens_used = 0
        model = ""

        try:
            async for event in self.llm.chat_completion(
                messages=messages,
                tools=ASSISTANT_TOOLS,
                stream=True,
            ):
                if event.type == "content":
                    full_content += event.data
                    yield {
                        "event": "content_delta",
                        "data": {"delta": event.data}
                    }

                elif event.type == "tool_call":
                    tool_calls.append(event.data)

                elif event.type == "usage":
                    tokens_used = event.data.get("total_tokens", 0)

                elif event.type == "done":
                    model = event.data.get("model", "")

                elif event.type == "error":
                    yield {
                        "event": "error",
                        "data": {"message": event.data}
                    }
                    return

        except Exception as e:
            logger.error(f"LLM error: {e}")
            yield {
                "event": "error",
                "data": {"message": f"AI service error: {str(e)}"}
            }
            return

        # Execute tool calls if any
        if tool_calls:
            # Save assistant message with tool_calls first (before tool execution)
            self.conversation_manager.add_message(
                conversation_id=conversation.id,
                role="assistant",
                content="",  # Content is empty when making tool calls
                tool_calls=[
                    {"id": tc.id, "name": tc.name, "arguments": tc.arguments}
                    for tc in tool_calls
                ],
                tokens_used=0,
                model=model,
            )

            tool_results = []
            for tc in tool_calls:
                yield {
                    "event": "tool_call",
                    "data": {
                        "id": tc.id,
                        "name": tc.name,
                        "arguments": tc.arguments
                    }
                }

                # Execute tool
                result = await self.tool_orchestrator.execute_tool(
                    tc.name,
                    tc.arguments
                )
                tool_results.append((tc, result))

                yield {
                    "event": "tool_result",
                    "data": {
                        "tool": tc.name,
                        "result": result
                    }
                }

                # If tool requires confirmation, emit action card
                if result.get("requires_confirmation"):
                    yield {
                        "event": "action_proposal",
                        "data": result
                    }

                # If tool provides navigation, emit action card
                if result.get("type") == "navigation":
                    yield {
                        "event": "action_card",
                        "data": {
                            "type": "navigation",
                            "url": result["url"],
                            "label": result["label"]
                        }
                    }

                # Add tool result to messages for follow-up LLM call
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments)
                        }
                    }]
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result)
                })

                # Save tool response message to database
                self.conversation_manager.add_message(
                    conversation_id=conversation.id,
                    role="tool",
                    content=json.dumps(result),
                    tool_call_id=tc.id,
                )

            # Get final response from LLM after tool execution
            async for event in self.llm.chat_completion(
                messages=messages,
                tools=ASSISTANT_TOOLS,
                stream=True,
            ):
                if event.type == "content":
                    full_content += event.data
                    yield {
                        "event": "content_delta",
                        "data": {"delta": event.data}
                    }

                elif event.type == "usage":
                    tokens_used += event.data.get("total_tokens", 0)

                elif event.type == "done":
                    model = event.data.get("model", "")

        # Save final assistant message (response after tool execution or direct response)
        final_message = None
        if full_content or not tool_calls:
            final_message = self.conversation_manager.add_message(
                conversation_id=conversation.id,
                role="assistant",
                content=full_content,
                tool_calls=None,
                tokens_used=tokens_used,
                model=model,
            )

        # Emit completion
        yield {
            "event": "message_complete",
            "data": {
                "tokens_used": tokens_used,
                "model": model,
                "message_id": final_message.id if final_message else conversation.id,
            }
        }

    async def get_conversations(
        self,
        limit: int = 20,
        include_archived: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get list of conversations.

        Args:
            limit: Maximum number of conversations
            include_archived: Include archived conversations

        Returns:
            List of conversation dicts
        """
        conversations = self.conversation_manager.list_conversations(
            limit=limit,
            include_archived=include_archived
        )

        return [
            {
                "id": c.id,
                "title": c.title,
                "message_count": c.message_count,
                "total_tokens": c.total_tokens,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "updated_at": c.updated_at.isoformat() if c.updated_at else None,
                "is_archived": c.is_archived,
            }
            for c in conversations
        ]

    async def get_conversation_messages(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get messages for a conversation.

        Args:
            conversation_id: Conversation ID
            limit: Maximum number of messages

        Returns:
            List of message dicts
        """
        messages = self.conversation_manager.get_recent_messages(
            conversation_id=conversation_id,
            limit=limit
        )
        return messages

    async def archive_conversation(self, conversation_id: str) -> bool:
        """Archive a conversation."""
        return self.conversation_manager.archive_conversation(conversation_id)

    async def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation."""
        return self.conversation_manager.delete_conversation(conversation_id)


def create_assistant_service(
    db: Session,
    api_key: str,
    model: str = "gpt-4o",
) -> AssistantService:
    """
    Factory function to create an AssistantService with OpenAI adapter.

    Args:
        db: SQLAlchemy database session
        api_key: OpenAI API key
        model: Model to use (default: gpt-4o)

    Returns:
        Configured AssistantService
    """
    llm_adapter = OpenAIAdapter(api_key=api_key, model=model)
    return AssistantService(db=db, llm_adapter=llm_adapter)
