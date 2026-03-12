"""In-memory registry for A2A agent discovery."""

from typing import Any, Dict, List, Optional

from .base import A2AAgent


class AgentRegistry:
    """Singleton registry of A2A agents."""

    _agents: Dict[str, A2AAgent] = {}

    @classmethod
    def register(cls, agent: A2AAgent) -> None:
        cls._agents[agent.name] = agent

    @classmethod
    def get(cls, name: str) -> Optional[A2AAgent]:
        return cls._agents.get(name)

    @classmethod
    def list_all(cls) -> List[Dict[str, Any]]:
        return [a.get_agent_card() for a in cls._agents.values()]
