"""
Tool definitions for AI Assistant.

Defines the tools (functions) that the LLM can call to interact with
Spearmint's financial data and services.
"""

from typing import List, Dict, Any

# OpenAI function calling tool definitions
ASSISTANT_TOOLS: List[Dict[str, Any]] = [
    # ===== QUERY TOOLS (Read-only) =====
    {
        "type": "function",
        "function": {
            "name": "get_spending_summary",
            "description": "Get total spending amount, optionally filtered by category and time period. Use this when the user asks about spending, expenses, or how much they spent on something.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category name to filter by (e.g., 'Groceries', 'Dining Out', 'Utilities')"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["this_month", "last_month", "this_quarter", "last_quarter", "this_year", "last_year", "custom"],
                        "description": "Time period for the summary. Use 'custom' with date_from/date_to for specific ranges."
                    },
                    "date_from": {
                        "type": "string",
                        "format": "date",
                        "description": "Start date (YYYY-MM-DD) for custom period"
                    },
                    "date_to": {
                        "type": "string",
                        "format": "date",
                        "description": "End date (YYYY-MM-DD) for custom period"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_income_summary",
            "description": "Get total income amount, optionally filtered by category and time period. Use this when the user asks about income, earnings, or money received.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Income category to filter by (e.g., 'Salary', 'Freelance', 'Investments')"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["this_month", "last_month", "this_quarter", "last_quarter", "this_year", "last_year", "custom"],
                        "description": "Time period for the summary"
                    },
                    "date_from": {
                        "type": "string",
                        "format": "date",
                        "description": "Start date (YYYY-MM-DD) for custom period"
                    },
                    "date_to": {
                        "type": "string",
                        "format": "date",
                        "description": "End date (YYYY-MM-DD) for custom period"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_categories",
            "description": "Get the top spending or income categories ranked by total amount. Use this when the user asks about their biggest expenses or income sources.",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["expense", "income"],
                        "description": "Whether to get expense or income categories"
                    },
                    "limit": {
                        "type": "integer",
                        "default": 5,
                        "description": "Number of categories to return (1-10)"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["this_month", "last_month", "this_quarter", "this_year"],
                        "description": "Time period for the analysis"
                    }
                },
                "required": ["type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_transactions",
            "description": "Search for transactions by merchant name, description, amount, or date range. Use this when the user wants to find specific transactions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "merchant": {
                        "type": "string",
                        "description": "Merchant or payee name to search for (partial match)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Transaction description text to search for"
                    },
                    "category": {
                        "type": "string",
                        "description": "Category name to filter by"
                    },
                    "amount_min": {
                        "type": "number",
                        "description": "Minimum transaction amount"
                    },
                    "amount_max": {
                        "type": "number",
                        "description": "Maximum transaction amount"
                    },
                    "date_from": {
                        "type": "string",
                        "format": "date",
                        "description": "Start date (YYYY-MM-DD)"
                    },
                    "date_to": {
                        "type": "string",
                        "format": "date",
                        "description": "End date (YYYY-MM-DD)"
                    },
                    "is_uncategorized": {
                        "type": "boolean",
                        "description": "Only return transactions without a category"
                    },
                    "limit": {
                        "type": "integer",
                        "default": 20,
                        "description": "Maximum number of transactions to return (1-50)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_account_balance",
            "description": "Get the current balance of a specific account or all accounts. Use this when the user asks about account balances or how much money they have.",
            "parameters": {
                "type": "object",
                "properties": {
                    "account_name": {
                        "type": "string",
                        "description": "Name of the account (e.g., 'Chase Checking', 'Savings')"
                    },
                    "include_all": {
                        "type": "boolean",
                        "default": False,
                        "description": "Return all account balances"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_cash_flow",
            "description": "Get net cash flow (income minus expenses) for a period. Use this when the user asks about cash flow, savings, or whether they're making or losing money.",
            "parameters": {
                "type": "object",
                "properties": {
                    "period": {
                        "type": "string",
                        "enum": ["this_month", "last_month", "this_quarter", "this_year"],
                        "description": "Time period for cash flow analysis"
                    },
                    "include_breakdown": {
                        "type": "boolean",
                        "default": True,
                        "description": "Include income/expense breakdown in response"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_periods",
            "description": "Compare spending, income, or cash flow between two time periods. Use this when the user asks to compare periods or asks about trends.",
            "parameters": {
                "type": "object",
                "properties": {
                    "metric": {
                        "type": "string",
                        "enum": ["spending", "income", "net_cash_flow"],
                        "description": "Which metric to compare"
                    },
                    "category": {
                        "type": "string",
                        "description": "Optional category to filter by"
                    },
                    "period_1": {
                        "type": "string",
                        "enum": ["this_month", "last_month", "this_quarter", "last_quarter"],
                        "description": "First period to compare"
                    },
                    "period_2": {
                        "type": "string",
                        "enum": ["this_month", "last_month", "this_quarter", "last_quarter"],
                        "description": "Second period to compare"
                    }
                },
                "required": ["metric", "period_1", "period_2"]
            }
        }
    },

    # ===== ACTION TOOLS (Require Confirmation - Phase 2) =====
    {
        "type": "function",
        "function": {
            "name": "propose_categorization",
            "description": "Propose categorizing one or more transactions. Returns a preview that the user must confirm before changes are made.",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of transaction IDs to categorize"
                    },
                    "merchant_pattern": {
                        "type": "string",
                        "description": "Match transactions by merchant name pattern instead of IDs"
                    },
                    "category_name": {
                        "type": "string",
                        "description": "Target category name to assign"
                    }
                },
                "required": ["category_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "propose_category_rule",
            "description": "Propose creating a rule to automatically categorize future transactions matching a pattern.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Text pattern to match in transaction descriptions"
                    },
                    "pattern_type": {
                        "type": "string",
                        "enum": ["contains", "starts_with", "ends_with", "exact", "regex"],
                        "description": "How to match the pattern"
                    },
                    "category_name": {
                        "type": "string",
                        "description": "Category to assign when pattern matches"
                    },
                    "rule_name": {
                        "type": "string",
                        "description": "Human-readable name for the rule"
                    }
                },
                "required": ["pattern", "pattern_type", "category_name"]
            }
        }
    },

    # ===== NAVIGATION TOOLS =====
    {
        "type": "function",
        "function": {
            "name": "create_navigation_link",
            "description": "Create a link to navigate the user to a specific page with optional filters applied. Use this to help users drill down into data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "page": {
                        "type": "string",
                        "enum": [
                            "dashboard",
                            "transactions",
                            "analysis",
                            "analysis/income",
                            "analysis/expenses",
                            "accounts",
                            "projections",
                            "scenarios",
                            "classifications",
                            "settings"
                        ],
                        "description": "Target page to navigate to"
                    },
                    "filters": {
                        "type": "object",
                        "description": "Query parameters to apply",
                        "properties": {
                            "category": {"type": "string"},
                            "account": {"type": "string"},
                            "date_from": {"type": "string"},
                            "date_to": {"type": "string"},
                            "transaction_id": {"type": "integer"}
                        }
                    },
                    "label": {
                        "type": "string",
                        "description": "Button label to display to the user"
                    }
                },
                "required": ["page"]
            }
        }
    }
]


# Tool names that require user confirmation before execution
CONFIRMATION_REQUIRED_TOOLS = {
    "propose_categorization",
    "propose_category_rule",
    "propose_mark_as_transfer",
}

# Tool names that are read-only (safe to execute without confirmation)
READ_ONLY_TOOLS = {
    "get_spending_summary",
    "get_income_summary",
    "get_top_categories",
    "search_transactions",
    "get_account_balance",
    "get_cash_flow",
    "compare_periods",
    "create_navigation_link",
}
