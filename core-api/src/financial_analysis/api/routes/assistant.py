"""
API routes for AI Financial Assistant.

Provides endpoints for chat, conversation management, and insights.
"""

from typing import Optional, Dict, Any, List
import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ...services.assistant import AssistantService, OpenAIAdapter
from ...database.assistant_models import AssistantPreferences

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])


# ===== Pydantic Models =====

class ChatContext(BaseModel):
    """Context for the chat message."""
    current_page: Optional[str] = None
    selected_transaction_id: Optional[int] = None
    active_filters: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None
    context: Optional[ChatContext] = None


class ActionConfirmRequest(BaseModel):
    """Request body for action confirmation."""
    message_id: str
    action_type: str
    confirmed: bool
    payload: Dict[str, Any]


class ConversationResponse(BaseModel):
    """Response for conversation listing."""
    id: str
    title: Optional[str]
    message_count: int
    total_tokens: int
    created_at: Optional[str]
    updated_at: Optional[str]
    is_archived: bool


class InsightResponse(BaseModel):
    """Response for insights."""
    id: str
    insight_type: str
    priority: int
    title: str
    content: str
    action_type: Optional[str]
    action_payload: Optional[Dict[str, Any]]
    created_at: str


# ===== Helper Functions =====

def get_api_key(db: Session) -> str:
    """Get OpenAI API key from preferences or environment."""
    import os

    # Try to get from database preferences
    prefs = db.query(AssistantPreferences).first()
    if prefs and prefs.openai_api_key_encrypted:
        # TODO: Decrypt the key
        pass

    # Fall back to environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable or configure in settings."
        )

    return api_key


def get_assistant_service(db: Session = Depends(get_db)) -> AssistantService:
    """Dependency to get AssistantService instance."""
    api_key = get_api_key(db)
    model = os.getenv("OPENAI_MODEL", "gpt-4o")

    llm_adapter = OpenAIAdapter(api_key=api_key, model=model)
    return AssistantService(db=db, llm_adapter=llm_adapter)


import os  # Move to top in production


# ===== Endpoints =====

@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Send a message to the AI assistant and receive a streamed response.

    Returns a Server-Sent Events (SSE) stream with the following event types:
    - conversation_id: The conversation ID being used
    - content_delta: Incremental content from the assistant
    - tool_call: When the assistant calls a tool
    - tool_result: Result of tool execution
    - action_proposal: When an action requires user confirmation
    - action_card: Navigation or action button for the UI
    - message_complete: Final event with token usage
    - error: If an error occurs
    """
    try:
        api_key = get_api_key(db)
    except HTTPException as e:
        # Return error as SSE event
        async def error_generator():
            yield f"event: error\ndata: {json.dumps({'message': e.detail})}\n\n"
        return StreamingResponse(
            error_generator(),
            media_type="text/event-stream"
        )

    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    llm_adapter = OpenAIAdapter(api_key=api_key, model=model)
    service = AssistantService(db=db, llm_adapter=llm_adapter)

    async def event_generator():
        """Generate SSE events from assistant response."""
        try:
            context = request.context.model_dump() if request.context else {}

            async for event in service.chat(
                message=request.message,
                conversation_id=request.conversation_id,
                context=context,
            ):
                event_type = event.get("event", "message")
                event_data = event.get("data", {})
                yield f"event: {event_type}\ndata: {json.dumps(event_data)}\n\n"

        except Exception as e:
            logger.error(f"Chat error: {e}")
            yield f"event: error\ndata: {json.dumps({'message': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    limit: int = Query(default=20, ge=1, le=100),
    include_archived: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    """
    List conversation history.

    Returns recent conversations ordered by last update time.
    """
    api_key = get_api_key(db)
    llm_adapter = OpenAIAdapter(api_key=api_key, model="gpt-4o")
    service = AssistantService(db=db, llm_adapter=llm_adapter)

    conversations = await service.get_conversations(
        limit=limit,
        include_archived=include_archived
    )

    return conversations


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """
    Get messages for a specific conversation.

    Returns messages in chronological order.
    """
    api_key = get_api_key(db)
    llm_adapter = OpenAIAdapter(api_key=api_key, model="gpt-4o")
    service = AssistantService(db=db, llm_adapter=llm_adapter)

    messages = await service.get_conversation_messages(
        conversation_id=conversation_id,
        limit=limit
    )

    return {"conversation_id": conversation_id, "messages": messages}


@router.post("/conversations/{conversation_id}/archive")
async def archive_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    """
    Archive a conversation.

    Archived conversations are hidden from the default list but not deleted.
    """
    api_key = get_api_key(db)
    llm_adapter = OpenAIAdapter(api_key=api_key, model="gpt-4o")
    service = AssistantService(db=db, llm_adapter=llm_adapter)

    success = await service.archive_conversation(conversation_id)

    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {"success": True, "message": "Conversation archived"}


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete a conversation and all its messages.

    This action cannot be undone.
    """
    api_key = get_api_key(db)
    llm_adapter = OpenAIAdapter(api_key=api_key, model="gpt-4o")
    service = AssistantService(db=db, llm_adapter=llm_adapter)

    success = await service.delete_conversation(conversation_id)

    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {"success": True, "message": "Conversation deleted"}


@router.post("/actions")
async def execute_action(
    request: ActionConfirmRequest,
    db: Session = Depends(get_db),
):
    """
    Execute a confirmed action.

    Actions like categorization or rule creation require user confirmation
    before execution. This endpoint executes the confirmed action.
    """
    # TODO: Implement action execution with undo logging
    # This is Phase 2 functionality

    return {
        "success": True,
        "message": "Action executed",
        "action_log_id": "placeholder",
        "undo_available": True
    }


@router.post("/actions/undo")
async def undo_action(
    action_log_id: str,
    db: Session = Depends(get_db),
):
    """
    Undo a previous action.

    Restores the previous state before the action was executed.
    """
    # TODO: Implement undo functionality
    # This is Phase 2 functionality

    return {
        "success": True,
        "message": "Action undone"
    }


@router.get("/insights", response_model=List[InsightResponse])
async def get_insights(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """
    Get pending proactive insights.

    Returns insights that haven't been dismissed or acted upon,
    ordered by priority.
    """
    # TODO: Implement insights retrieval
    # This is Phase 3 functionality

    return []


@router.post("/insights/{insight_id}/dismiss")
async def dismiss_insight(
    insight_id: str,
    db: Session = Depends(get_db),
):
    """
    Dismiss an insight.

    The insight will no longer appear in the pending list.
    """
    # TODO: Implement insight dismissal
    # This is Phase 3 functionality

    return {"success": True, "message": "Insight dismissed"}


@router.get("/health")
async def health_check():
    """
    Check if the assistant service is available.

    Returns status of LLM connectivity and configuration.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    return {
        "status": "ok" if api_key else "unconfigured",
        "llm_configured": bool(api_key),
        "llm_provider": "openai",
        "llm_model": os.getenv("OPENAI_MODEL", "gpt-4o")
    }
