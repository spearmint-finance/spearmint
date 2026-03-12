"""Base class for A2A agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session


class A2AAgent(ABC):
    """Base class for all A2A-compliant agents.

    Subclasses must implement get_agent_card() and invoke().
    """

    @abstractmethod
    def get_agent_card(self) -> Dict[str, Any]:
        """Return the agent card for A2A discovery."""
        ...

    @abstractmethod
    async def invoke(
        self,
        skill: str,
        params: Dict[str, Any],
        negotiation: Optional[Dict[str, Any]],
        db: Session,
    ) -> Dict[str, Any]:
        """Invoke a skill on this agent.

        Returns an A2A response envelope:
            {"status": "completed"|"needs_input"|"error", "result": {...}, ...}
        """
        ...

    @property
    def name(self) -> str:
        """Agent name derived from the agent card."""
        return self.get_agent_card()["name"]
