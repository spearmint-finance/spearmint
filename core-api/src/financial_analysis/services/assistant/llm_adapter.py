"""
LLM Adapter layer for AI Assistant.

Provides an abstraction over LLM providers to allow switching between
OpenAI, Anthropic, Ollama, etc. without changing application code.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import AsyncGenerator, List, Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class ToolCall:
    """Represents a tool/function call from the LLM."""
    id: str
    name: str
    arguments: Dict[str, Any]


@dataclass
class StreamEvent:
    """Event emitted during streaming response."""
    type: str  # 'content', 'tool_call', 'tool_result', 'error', 'done'
    data: Any


@dataclass
class LLMResponse:
    """Complete response from LLM (non-streaming)."""
    content: str
    tool_calls: List[ToolCall] = field(default_factory=list)
    tokens_used: int = 0
    model: str = ""
    finish_reason: str = ""


class LLMAdapter(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = True,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[StreamEvent, None]:
        """
        Send messages to LLM and get response.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions for function calling
            stream: Whether to stream the response
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response

        Yields:
            StreamEvent objects with response chunks or tool calls
        """
        pass

    @abstractmethod
    async def chat_completion_sync(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """
        Send messages to LLM and get complete response (non-streaming).

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions for function calling
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response

        Returns:
            Complete LLMResponse object
        """
        pass


class OpenAIAdapter(LLMAdapter):
    """OpenAI GPT implementation using the official SDK."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        organization: Optional[str] = None,
    ):
        """
        Initialize OpenAI adapter.

        Args:
            api_key: OpenAI API key
            model: Model to use (gpt-4o, gpt-4o-mini, etc.)
            organization: Optional organization ID
        """
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError(
                "openai package is required. Install with: pip install openai"
            )

        self.client = AsyncOpenAI(
            api_key=api_key,
            organization=organization,
        )
        self.model = model

    async def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = True,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[StreamEvent, None]:
        """Stream chat completion from OpenAI."""

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        if max_tokens:
            kwargs["max_tokens"] = max_tokens

        try:
            if stream:
                async for event in self._stream_response(**kwargs):
                    yield event
            else:
                response = await self.client.chat.completions.create(**kwargs)
                yield self._parse_response(response)

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            yield StreamEvent(type="error", data=str(e))

    async def _stream_response(self, **kwargs) -> AsyncGenerator[StreamEvent, None]:
        """Handle streaming response from OpenAI."""

        response = await self.client.chat.completions.create(**kwargs)

        collected_tool_calls: Dict[int, Dict[str, Any]] = {}
        current_content = ""

        async for chunk in response:
            choice = chunk.choices[0] if chunk.choices else None
            if not choice:
                continue

            delta = choice.delta

            # Handle content streaming
            if delta.content:
                current_content += delta.content
                yield StreamEvent(type="content", data=delta.content)

            # Handle tool calls
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    idx = tc.index
                    if idx not in collected_tool_calls:
                        collected_tool_calls[idx] = {
                            "id": tc.id or "",
                            "name": "",
                            "arguments": "",
                        }

                    if tc.id:
                        collected_tool_calls[idx]["id"] = tc.id
                    if tc.function:
                        if tc.function.name:
                            collected_tool_calls[idx]["name"] = tc.function.name
                        if tc.function.arguments:
                            collected_tool_calls[idx]["arguments"] += tc.function.arguments

            # Check for finish
            if choice.finish_reason:
                # Emit any collected tool calls
                for idx in sorted(collected_tool_calls.keys()):
                    tc_data = collected_tool_calls[idx]
                    try:
                        args = json.loads(tc_data["arguments"]) if tc_data["arguments"] else {}
                    except json.JSONDecodeError:
                        args = {}

                    tool_call = ToolCall(
                        id=tc_data["id"],
                        name=tc_data["name"],
                        arguments=args,
                    )
                    yield StreamEvent(type="tool_call", data=tool_call)

                # Emit usage if available
                if chunk.usage:
                    yield StreamEvent(
                        type="usage",
                        data={
                            "prompt_tokens": chunk.usage.prompt_tokens,
                            "completion_tokens": chunk.usage.completion_tokens,
                            "total_tokens": chunk.usage.total_tokens,
                        }
                    )

                yield StreamEvent(
                    type="done",
                    data={"finish_reason": choice.finish_reason, "model": self.model}
                )

    def _parse_response(self, response) -> StreamEvent:
        """Parse a non-streaming response."""
        choice = response.choices[0]
        message = choice.message

        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                try:
                    args = json.loads(tc.function.arguments) if tc.function.arguments else {}
                except json.JSONDecodeError:
                    args = {}

                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=args,
                ))

        return StreamEvent(
            type="complete",
            data=LLMResponse(
                content=message.content or "",
                tool_calls=tool_calls,
                tokens_used=response.usage.total_tokens if response.usage else 0,
                model=response.model,
                finish_reason=choice.finish_reason,
            )
        )

    async def chat_completion_sync(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """Get complete response from OpenAI (non-streaming)."""

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        if max_tokens:
            kwargs["max_tokens"] = max_tokens

        try:
            response = await self.client.chat.completions.create(**kwargs)
            choice = response.choices[0]
            message = choice.message

            tool_calls = []
            if message.tool_calls:
                for tc in message.tool_calls:
                    try:
                        args = json.loads(tc.function.arguments) if tc.function.arguments else {}
                    except json.JSONDecodeError:
                        args = {}

                    tool_calls.append(ToolCall(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=args,
                    ))

            return LLMResponse(
                content=message.content or "",
                tool_calls=tool_calls,
                tokens_used=response.usage.total_tokens if response.usage else 0,
                model=response.model,
                finish_reason=choice.finish_reason,
            )

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
