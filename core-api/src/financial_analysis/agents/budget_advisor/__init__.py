"""Budget Advisor A2A agent — registers on import."""

from .agent import BudgetAdvisorAgent
from ..registry import AgentRegistry

_agent = BudgetAdvisorAgent()
AgentRegistry.register(_agent)
