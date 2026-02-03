"""
AI Assistant service for natural language financial queries.

This module provides:
- LLM adapters for OpenAI (primary) and future providers
- Conversation management with history persistence
- Tool orchestration for executing financial queries
- Response streaming via SSE
"""

from .llm_adapter import LLMAdapter, OpenAIAdapter
from .conversation_manager import ConversationManager
from .tool_orchestrator import ToolOrchestrator
from .assistant_service import AssistantService

__all__ = [
    'LLMAdapter',
    'OpenAIAdapter',
    'ConversationManager',
    'ToolOrchestrator',
    'AssistantService',
]
