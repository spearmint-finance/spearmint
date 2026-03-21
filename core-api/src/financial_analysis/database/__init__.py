"""Database module for financial analysis tool."""

# Import all models to register them with Base
from .models import (
    Transaction,
    Category,
    Account,
)
from .assistant_models import (
    AssistantConversation,
    AssistantMessage,
    AssistantActionLog,
    AssistantPreferences,
    AssistantInsight,
)
