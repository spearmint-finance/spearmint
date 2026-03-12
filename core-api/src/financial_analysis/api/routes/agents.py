"""A2A agent endpoints — discovery and invocation."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ...agents.registry import AgentRegistry
from ...agents.budget_advisor.schemas import A2ARequest

# Trigger agent registration on import
import src.financial_analysis.agents.budget_advisor  # noqa: F401

router = APIRouter()


@router.get("/agents")
def list_agents():
    """List all registered A2A agents (discovery endpoint)."""
    return AgentRegistry.list_all()


@router.get("/agents/{agent_name}")
def get_agent_card(agent_name: str):
    """Get a specific agent's card."""
    agent = AgentRegistry.get(agent_name)
    if not agent:
        raise HTTPException(404, detail=f"Agent '{agent_name}' not found")
    return agent.get_agent_card()


@router.post("/{agent_name}")
async def invoke_agent(
    agent_name: str,
    request: A2ARequest,
    db: Session = Depends(get_db),
):
    """Invoke an A2A agent skill."""
    agent = AgentRegistry.get(agent_name)
    if not agent:
        raise HTTPException(404, detail=f"Agent '{agent_name}' not found")

    negotiation = request.negotiation.model_dump() if request.negotiation else None
    result = await agent.invoke(request.skill, request.params, negotiation, db)
    return result
