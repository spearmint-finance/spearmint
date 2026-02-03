# Product Requirements Document: AI Financial Assistant

**Product:** Spearmint Personal Finance Engine
**Feature:** AI Financial Assistant ("Minty")
**Owner:** Product Team
**Status:** Draft
**Last Updated:** 2026-02-03

---

## Executive Summary

Users love Spearmint's depth but often feel overwhelmed navigating its many features. They want to ask natural-language questions about their finances ("How much did I spend on dining out last quarter?") and have routine maintenance tasks handled automatically ("Categorize all my Amazon transactions as Shopping").

This PRD defines the **AI Financial Assistant**—an embedded chatbot that serves as a conversational interface to Spearmint's analytical power. It enables users to query their financial data using plain English, receive actionable insights, and delegate routine bookkeeping tasks to an intelligent agent.

**Expected Impact:**
- Reduce time-to-insight from 3+ minutes (manual navigation) to <30 seconds (ask a question)
- Increase user engagement by 50% through conversational interactions
- Reduce uncategorized transactions by 80% via AI-assisted classification
- Enable non-technical household members to access financial insights

---

## Problem Statement

### The User Problem

Spearmint provides powerful financial analysis, but users face friction accessing insights:

1. **Complex Navigation:** Users must know which page to visit and which filters to apply to answer questions like "What's my biggest expense category this year?"

2. **Data Entry Burden:** Manually categorizing transactions, creating classification rules, and setting up accounts requires significant effort and domain knowledge.

3. **Interpretation Gap:** Charts and numbers require financial literacy to interpret. Users want plain-English explanations: "You're spending 23% more on groceries this month compared to your 6-month average."

4. **Routine Maintenance:** Tasks like reviewing uncategorized transactions, detecting duplicate imports, and reconciling account balances are tedious but critical.

5. **Household Accessibility:** Only the "power user" who set up Spearmint can effectively use it. Partners and family members struggle with the interface.

### Evidence

**User Interview Insights (N=20):**
- 18/20 users said they wish they could "just ask" for information
- 16/20 users spend 10+ minutes/week on manual categorization
- 14/20 users said their partner/spouse never uses Spearmint because it's "too complicated"
- 12/20 users reported giving up on finding specific information due to navigation complexity

**Support Ticket Analysis (Last 90 Days):**
- 89 tickets asking "How do I find X?" (navigation confusion)
- 56 tickets asking "What does this chart mean?" (interpretation)
- 34 tickets asking "Can you automate categorization?" (routine tasks)

**Competitive Analysis:**
- Copilot for Microsoft 365, Notion AI, and Coda AI have proven conversational interfaces drive engagement
- Fintech competitors (Monarch, Copilot Money) are adding AI assistants
- Opportunity to differentiate with deep integration and task execution (not just Q&A)

---

## Goals & Success Metrics

### Goals

1. **Democratize financial insights:** Any household member can get answers in <30 seconds
2. **Reduce manual data entry:** AI handles 80%+ of categorization decisions
3. **Increase feature discovery:** Users discover and use more Spearmint features through natural conversation
4. **Build trust through transparency:** Every AI action is explainable and reversible

### Success Metrics

| Metric | Target | Timeframe |
|--------|--------|-----------|
| % of active users who interact with AI Assistant weekly | 60% | 3 months post-launch |
| Avg. queries per user per week | 8 | 3 months post-launch |
| % of uncategorized transactions (reduction) | 80% reduction | 2 months post-launch |
| User satisfaction (feature rating) | 4.6/5 | 1 month post-launch |
| Time-to-answer for common questions | <30 seconds | Launch |

---

## User Stories

### Primary User Stories (MVP)

**As a user, I want to:**

1. **Ask natural-language questions about my finances** so I can get answers without navigating multiple pages
   - *Example:* "How much did I spend on restaurants last month?"
   - *Example:* "What's my average monthly income this year?"
   - *Example:* "Show me my biggest expense categories"
   - *Acceptance:* User receives accurate, formatted answer within 5 seconds

2. **Get proactive insights and alerts** so I'm aware of important changes in my finances
   - *Example:* "Your grocery spending is 34% higher this month than your 6-month average"
   - *Example:* "You have 47 uncategorized transactions from the last import"
   - *Acceptance:* Assistant surfaces relevant insights without being asked

3. **Ask for explanations of my data** so I can understand what charts and numbers mean
   - *Example:* "Why did my net worth drop this month?"
   - *Example:* "Explain my cash flow trend"
   - *Acceptance:* User receives plain-English explanation with specific transaction references

4. **Delegate categorization tasks** so I don't have to manually classify every transaction
   - *Example:* "Categorize all Starbucks transactions as Dining Out"
   - *Example:* "Review my uncategorized transactions and suggest categories"
   - *Acceptance:* Assistant proposes categories with confidence scores; user can approve/reject

5. **Create rules through conversation** so I can automate future categorization without learning the rule system
   - *Example:* "Always categorize Amazon as Shopping"
   - *Example:* "Transactions from 'ACME Corp' should be marked as my salary"
   - *Acceptance:* Assistant creates the appropriate classification/category rule

6. **Navigate to relevant pages** so I can deep-dive after getting an overview
   - *Example:* "Show me my dining expenses" → navigates to Expenses page with Dining filter
   - *Example:* "Open my Chase account" → navigates to Accounts page with Chase selected
   - *Acceptance:* Assistant provides link/button that navigates to the correct filtered view

### Secondary User Stories (Post-MVP)

**As a user, I want to:**

7. **Ask "what-if" questions conversationally** so I can explore scenarios without learning the Scenario Builder
   - *Example:* "What happens to my runway if I lose my job?"
   - *Acceptance:* Assistant invokes Scenario feature and presents results conversationally

8. **Get recommendations** so I can improve my financial health
   - *Example:* "How can I reduce my expenses?"
   - *Example:* "Am I on track for my savings goal?"
   - *Acceptance:* Assistant provides actionable, personalized recommendations

9. **Bulk-edit transactions through conversation** so I can fix data quality issues quickly
   - *Example:* "Merge all 'WAL-MART' and 'WALMART' transactions"
   - *Acceptance:* Assistant identifies duplicates and offers to merge

10. **Share insights with my partner** so we can discuss finances together
    - *Example:* "Send my partner a summary of this month's spending"
    - *Future iteration:* Not in MVP

---

## User Interface

### UI Placement Options

**Option A: Floating Action Button (FAB) — Recommended**

- Persistent chat bubble in bottom-right corner of all pages
- Click to expand chat panel (slide-in from right, 400px width)
- Does not obscure main content; can be minimized
- Familiar pattern (Intercom, Drift, Zendesk)

**Option B: Sidebar Tab**

- New tab in the left sidebar: "Assistant" with chat icon
- Full-page chat experience when selected
- Integrates with existing navigation pattern
- Less discoverable; requires explicit navigation

**Option C: Command Palette**

- Keyboard shortcut (Cmd+K / Ctrl+K) opens modal
- Quick text input with AI responses
- Power-user oriented; less accessible for casual users
- Good complement to FAB, not replacement

**Recommendation:** Implement Option A (FAB) for primary access, with Option C (Command Palette) as a power-user shortcut.

### Chat Panel Components

```
┌─────────────────────────────────────┐
│  🌿 Minty                      [−] [×] │  ← Header with minimize/close
├─────────────────────────────────────┤
│                                     │
│  [Welcome message or context]       │  ← Initial greeting or insight
│                                     │
│  ┌─────────────────────────────┐   │
│  │ User: How much did I spend  │   │  ← User message bubble
│  │ on dining this month?       │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 🌿 You spent $847.23 on     │   │  ← AI response bubble
│  │ Dining Out this month.      │   │
│  │                             │   │
│  │ That's 12% higher than      │   │
│  │ your 3-month average.       │   │
│  │                             │   │
│  │ [View Transactions →]       │   │  ← Action button
│  └─────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │ Ask Minty anything...       │   │  ← Input field
│  └─────────────────────────────┘ [↑] │  ← Send button
│                                     │
│  [Suggested: "Show uncategorized"]  │  ← Quick action chips
│  [Suggested: "Monthly summary"]     │
└─────────────────────────────────────┘
```

### Interaction Patterns

1. **Query → Response:** User asks, AI answers with data and optional actions
2. **Action Proposal:** AI proposes changes (e.g., categorization), user confirms/rejects
3. **Multi-turn Conversation:** Follow-up questions maintain context
4. **Navigation Assist:** AI provides deep-links to relevant pages with pre-applied filters
5. **Bulk Operations:** AI shows preview of affected items before executing

---

## Functional Requirements

### FR-1: Natural Language Query Engine

The Assistant must understand and respond to:

| Query Type | Examples | Data Source |
|------------|----------|-------------|
| **Spending queries** | "How much did I spend on X?" | Transactions API |
| **Income queries** | "What was my income last quarter?" | Analysis API |
| **Category queries** | "What are my top 5 expense categories?" | Analysis API |
| **Account queries** | "What's my Chase balance?" | Accounts API |
| **Trend queries** | "How has my spending changed?" | Trends API |
| **Comparison queries** | "Am I spending more this month?" | Analysis API |
| **Search queries** | "Find transactions from Costco" | Transactions API |

**Response Requirements:**
- Responses must be accurate (matches manual query results)
- Responses must include source attribution ("Based on 47 transactions...")
- Responses must offer relevant follow-up actions
- Response time: <5 seconds for 95th percentile

### FR-2: Task Execution Engine

The Assistant can perform the following actions (with user confirmation):

| Task Type | User Intent | Action |
|-----------|-------------|--------|
| **Categorize transaction** | "Categorize this as Groceries" | PATCH /api/transactions/{id} |
| **Bulk categorize** | "Categorize all Starbucks as Dining" | Batch PATCH with confirmation |
| **Create category rule** | "Always categorize X as Y" | POST /api/category-rules |
| **Create classification rule** | "Mark all transfers to Savings as Internal" | POST /api/classification-rules |
| **Mark as transfer** | "This is a transfer, not income" | PATCH transaction classification |
| **Navigate** | "Show me expense analysis" | Client-side navigation |

**Execution Requirements:**
- All destructive/modifying actions require explicit user confirmation
- Bulk operations show preview with count before execution
- All actions are logged and reversible
- Users can undo last AI action

### FR-3: Proactive Insights

The Assistant surfaces insights without being asked:

| Trigger | Insight |
|---------|---------|
| **Post-import** | "I found 23 new transactions. 18 were auto-categorized. 5 need your review." |
| **Anomaly detection** | "Your utility bill was $89 higher than usual this month." |
| **Uncategorized backlog** | "You have 34 uncategorized transactions. Want me to suggest categories?" |
| **Duplicate detection** | "I found 3 potential duplicate transactions from your last import." |
| **Goal tracking** | "You're 80% toward your monthly savings goal." |

**Insight Requirements:**
- Insights appear as chat messages when user opens Assistant
- Users can dismiss or act on insights
- Insights are prioritized by importance/recency
- Users can configure which insights they want to see

### FR-4: Context Awareness

The Assistant understands the user's current context:

| Context | Behavior |
|---------|----------|
| **Current page** | "Show more details" → understands what "this" refers to |
| **Selected transaction** | "Categorize this as..." → applies to selected item |
| **Active filters** | "How much total?" → respects current date/category filters |
| **Conversation history** | "What about last month?" → understands comparison context |

**Context Requirements:**
- Maintain conversation context for at least 10 turns
- Clear context with explicit "new conversation" or session timeout (30 min)
- Page context resets when user navigates

### FR-5: Transparency & Trust

Every AI response must be trustworthy and explainable:

| Requirement | Implementation |
|-------------|----------------|
| **Source citation** | "Based on 47 transactions from Jan 1-31" |
| **Confidence indication** | "I'm 85% confident this is a dining expense" |
| **Reasoning explanation** | "I categorized this as Dining because the merchant 'CHIPOTLE' matches your dining pattern" |
| **Undo capability** | "Undo" button on all AI actions |
| **Audit trail** | All AI actions logged with timestamp |

---

## Non-Functional Requirements

### NFR-1: Performance

- Query response time: <5 seconds (p95)
- Streaming responses for longer answers (first token <1 second)
- Chat panel load time: <500ms
- No impact on main app performance when minimized

### NFR-2: Privacy & Security

- All AI processing uses user's data only (no cross-user training)
- Conversation history stored locally or in user's database (not external)
- LLM prompts never include raw sensitive data (account numbers, SSNs)
- Option for fully local LLM (Ollama) for privacy-conscious users
- No telemetry of conversation content to external services

### NFR-3: Reliability

- Graceful degradation if AI service unavailable
- Clear error messages when queries can't be answered
- Fallback to rule-based responses for common queries
- Rate limiting to prevent abuse (100 queries/hour)

### NFR-4: Accessibility

- Chat panel is keyboard-navigable
- Screen reader compatible (ARIA labels, live regions)
- Responses are text-based (not image-only)
- Supports high-contrast mode
- Respects reduced motion preferences

### NFR-5: Mobile Responsiveness

- Chat panel works on mobile (full-screen modal on small screens)
- Touch-friendly input and buttons
- Voice input option (future)

---

## Technical Design

### Technology Decisions

#### LLM Provider: OpenAI (Primary)

**Decision:** Use OpenAI GPT-4o as the primary LLM provider.

**Rationale:**
- **Function Calling Maturity:** OpenAI's function calling is the most mature and reliable for agentic workflows
- **Streaming Support:** Excellent SSE streaming for real-time responses
- **Cost-Performance Balance:** GPT-4o offers strong reasoning at reasonable cost ($2.50/1M input, $10/1M output)
- **Ecosystem:** Extensive tooling, documentation, and community support
- **Structured Outputs:** Native JSON mode reduces parsing errors

**Model Selection:**
| Use Case | Model | Rationale |
|----------|-------|-----------|
| Primary queries | `gpt-4o` | Best balance of quality and speed |
| Simple lookups | `gpt-4o-mini` | Cost-effective for straightforward queries |
| Fallback | `gpt-3.5-turbo` | Budget fallback if user hits rate limits |

**Future Flexibility:** The adapter pattern allows adding Claude, Ollama, or other providers later without architecture changes.

#### Agent Framework: None (Direct OpenAI SDK)

**Decision:** Use OpenAI Python SDK directly with custom tool orchestration—no agent framework.

**Rationale:**
- **Simplicity:** LangChain/LlamaIndex add complexity without proportional benefit for our use case
- **Control:** Direct SDK gives full control over prompts, tool execution, and error handling
- **Debugging:** Easier to debug without framework abstraction layers
- **Performance:** Lower latency without framework overhead
- **Maintenance:** Fewer dependencies to update; OpenAI SDK is stable

**What We Build Instead:**
- Thin `LLMAdapter` abstraction for provider switching
- `ToolRegistry` for registering and executing tools
- `ConversationManager` for context and history
- `ResponseStreamer` for SSE streaming to frontend

**When to Reconsider:**
- If we need complex multi-agent workflows (Phase 4+)
- If we add RAG over documentation (would benefit from LlamaIndex)
- If we need agent memory beyond conversation history

---

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              Frontend (React)                            │
│  ┌──────────────┐   ┌──────────────┐   ┌─────────────────────────────┐ │
│  │ ChatPanel    │   │ useAssistant │   │ EventSource (SSE)           │ │
│  │ Component    │──▶│ Hook         │──▶│ Stream Handler              │ │
│  │              │   │              │   │                             │ │
│  │ - Messages   │   │ - send()     │   │ - onMessage()               │ │
│  │ - Input      │   │ - history    │   │ - onToolCall()              │ │
│  │ - Actions    │   │ - context    │   │ - onComplete()              │ │
│  └──────────────┘   └──────────────┘   └──────────────┬──────────────┘ │
└────────────────────────────────────────────────────────│────────────────┘
                                                         │ SSE
┌────────────────────────────────────────────────────────▼────────────────┐
│                           Core API (FastAPI)                             │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                    /api/assistant/                                  │ │
│  │  POST /chat          - Send message, receive streamed response     │ │
│  │  POST /actions       - Execute confirmed action                    │ │
│  │  GET  /conversations - List conversation history                   │ │
│  │  GET  /insights      - Get proactive insights                      │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│  ┌─────────────────────────────────▼──────────────────────────────────┐ │
│  │                     AssistantService                                │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────────┐  │ │
│  │  │ Conversation    │  │ Tool            │  │ Response           │  │ │
│  │  │ Manager         │  │ Orchestrator    │  │ Streamer           │  │ │
│  │  │                 │  │                 │  │                    │  │ │
│  │  │ - History       │  │ - Tool Registry │  │ - SSE Generator    │  │ │
│  │  │ - Context       │  │ - Execution     │  │ - Token Streaming  │  │ │
│  │  │ - Persistence   │  │ - Validation    │  │ - Action Cards     │  │ │
│  │  └─────────────────┘  └─────────────────┘  └────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│  ┌─────────────────────────────────▼──────────────────────────────────┐ │
│  │                      LLM Adapter Layer                              │ │
│  │  ┌─────────────────────────────────────────────────────────────┐   │ │
│  │  │                    OpenAIAdapter (Primary)                   │   │ │
│  │  │  - chat_completion_with_tools()                              │   │ │
│  │  │  - stream_response()                                         │   │ │
│  │  │  - parse_tool_calls()                                        │   │ │
│  │  └─────────────────────────────────────────────────────────────┘   │ │
│  │  ┌─────────────────┐  ┌─────────────────┐                          │ │
│  │  │ OllamaAdapter   │  │ AnthropicAdapter│  (Future)                │ │
│  │  │ (Local/Privacy) │  │ (Alternative)   │                          │ │
│  │  └─────────────────┘  └─────────────────┘                          │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│  ┌─────────────────────────────────▼──────────────────────────────────┐ │
│  │                       Tool Registry                                 │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │ │
│  │  │ Query Tools  │ │ Action Tools │ │ Navigation   │ │ Insight    │ │ │
│  │  │              │ │              │ │ Tools        │ │ Tools      │ │ │
│  │  │ -get_spending│ │ -categorize  │ │ -navigate_to │ │ -get_      │ │ │
│  │  │ -get_income  │ │ -create_rule │ │ -deep_link   │ │  anomalies │ │ │
│  │  │ -search_txns │ │ -bulk_update │ │              │ │ -summarize │ │ │
│  │  │ -get_balance │ │ -mark_transfer│ │             │ │            │ │ │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                    │                                     │
│  ┌─────────────────────────────────▼──────────────────────────────────┐ │
│  │                    Existing Spearmint Services                      │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────────┐ │ │
│  │  │ Transaction │ │ Analysis    │ │ Account     │ │ Category      │ │ │
│  │  │ Service     │ │ Service     │ │ Service     │ │ Service       │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └───────────────┘ │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                   │ │
│  │  │ Classification│ │ Projection │ │ Scenario   │                   │ │
│  │  │ Service     │ │ Service     │ │ Service     │                   │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘                   │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
```

---

### Database Schema

New tables for AI Assistant functionality:

```sql
-- Conversation sessions
CREATE TABLE assistant_conversations (
    id              TEXT PRIMARY KEY,           -- UUID
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title           TEXT,                       -- Auto-generated from first message
    message_count   INTEGER DEFAULT 0,
    total_tokens    INTEGER DEFAULT 0,          -- For usage tracking
    is_archived     BOOLEAN DEFAULT FALSE
);

-- Individual messages within conversations
CREATE TABLE assistant_messages (
    id              TEXT PRIMARY KEY,           -- UUID
    conversation_id TEXT NOT NULL REFERENCES assistant_conversations(id) ON DELETE CASCADE,
    role            TEXT NOT NULL,              -- 'user' | 'assistant' | 'system' | 'tool'
    content         TEXT NOT NULL,              -- Message text or tool result JSON
    tool_calls      TEXT,                       -- JSON array of tool calls (if assistant)
    tool_call_id    TEXT,                       -- Tool call ID (if tool response)
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tokens_used     INTEGER,                    -- Token count for this message
    model           TEXT,                       -- Model used (e.g., 'gpt-4o')

    -- For action messages
    action_type     TEXT,                       -- 'categorize' | 'create_rule' | etc.
    action_status   TEXT,                       -- 'proposed' | 'confirmed' | 'executed' | 'undone'
    action_payload  TEXT,                       -- JSON with action details

    INDEX idx_messages_conversation (conversation_id),
    INDEX idx_messages_created (created_at)
);

-- Audit log for AI-initiated actions (for undo capability)
CREATE TABLE assistant_action_log (
    id              TEXT PRIMARY KEY,           -- UUID
    message_id      TEXT REFERENCES assistant_messages(id),
    action_type     TEXT NOT NULL,              -- 'categorize_transaction' | 'create_rule' | etc.
    entity_type     TEXT NOT NULL,              -- 'transaction' | 'category_rule' | etc.
    entity_id       TEXT NOT NULL,              -- ID of affected entity
    previous_state  TEXT,                       -- JSON snapshot before change
    new_state       TEXT,                       -- JSON snapshot after change
    executed_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    undone_at       TIMESTAMP,                  -- NULL if not undone

    INDEX idx_action_log_entity (entity_type, entity_id),
    INDEX idx_action_log_message (message_id)
);

-- User preferences for AI Assistant
CREATE TABLE assistant_preferences (
    id                      TEXT PRIMARY KEY,   -- Single row, or user_id for multi-user
    llm_provider            TEXT DEFAULT 'openai',
    llm_model               TEXT DEFAULT 'gpt-4o',
    openai_api_key          TEXT,               -- Encrypted
    insights_enabled        BOOLEAN DEFAULT TRUE,
    anomaly_threshold       REAL DEFAULT 0.25,  -- 25% deviation triggers insight
    max_history_messages    INTEGER DEFAULT 50,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Proactive insights queue
CREATE TABLE assistant_insights (
    id              TEXT PRIMARY KEY,           -- UUID
    insight_type    TEXT NOT NULL,              -- 'anomaly' | 'uncategorized' | 'duplicate' | etc.
    priority        INTEGER DEFAULT 0,          -- Higher = more important
    title           TEXT NOT NULL,
    content         TEXT NOT NULL,              -- Markdown content
    action_type     TEXT,                       -- Suggested action type
    action_payload  TEXT,                       -- JSON for suggested action
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dismissed_at    TIMESTAMP,
    acted_on_at     TIMESTAMP,

    INDEX idx_insights_pending (dismissed_at, acted_on_at, priority DESC)
);
```

---

### API Endpoints

#### `POST /api/assistant/chat`

Send a message and receive a streamed response.

**Request:**
```json
{
  "message": "How much did I spend on groceries last month?",
  "conversation_id": "conv_abc123",  // Optional, creates new if omitted
  "context": {
    "current_page": "transactions",
    "selected_transaction_id": "txn_xyz",
    "active_filters": {
      "date_from": "2026-01-01",
      "date_to": "2026-01-31"
    }
  }
}
```

**Response (SSE Stream):**
```
event: message_start
data: {"conversation_id": "conv_abc123", "message_id": "msg_def456"}

event: content_delta
data: {"delta": "You spent "}

event: content_delta
data: {"delta": "$523.47"}

event: content_delta
data: {"delta": " on Groceries last month"}

event: tool_call
data: {"tool": "get_spending_summary", "args": {"category": "Groceries", "period": "last_month"}}

event: tool_result
data: {"tool": "get_spending_summary", "result": {"total": 523.47, "count": 23}}

event: action_card
data: {"type": "navigation", "label": "View Transactions", "url": "/transactions?category=Groceries&date_from=2026-01-01"}

event: message_complete
data: {"tokens_used": 847, "model": "gpt-4o"}
```

#### `POST /api/assistant/actions`

Execute a confirmed action.

**Request:**
```json
{
  "message_id": "msg_def456",
  "action_type": "bulk_categorize",
  "confirmed": true,
  "payload": {
    "transaction_ids": ["txn_1", "txn_2", "txn_3"],
    "category_id": "cat_groceries"
  }
}
```

**Response:**
```json
{
  "success": true,
  "affected_count": 3,
  "action_log_id": "log_ghi789",
  "undo_available": true,
  "message": "Categorized 3 transactions as Groceries"
}
```

#### `POST /api/assistant/actions/undo`

Undo a previous action.

**Request:**
```json
{
  "action_log_id": "log_ghi789"
}
```

#### `GET /api/assistant/conversations`

List conversation history.

**Response:**
```json
{
  "conversations": [
    {
      "id": "conv_abc123",
      "title": "Grocery spending analysis",
      "message_count": 12,
      "created_at": "2026-02-03T10:30:00Z",
      "updated_at": "2026-02-03T10:45:00Z"
    }
  ],
  "total": 24
}
```

#### `GET /api/assistant/insights`

Get pending proactive insights.

**Response:**
```json
{
  "insights": [
    {
      "id": "ins_001",
      "type": "uncategorized",
      "priority": 2,
      "title": "47 uncategorized transactions",
      "content": "You have 47 transactions from your last import that need categories.",
      "suggested_action": {
        "type": "review_uncategorized",
        "label": "Review Now"
      }
    },
    {
      "id": "ins_002",
      "type": "anomaly",
      "priority": 1,
      "title": "Utility bill 34% higher",
      "content": "Your electric bill was $89 higher than your 6-month average.",
      "suggested_action": {
        "type": "view_transaction",
        "transaction_id": "txn_electric_001"
      }
    }
  ]
}
```

---

### Tool Definitions (OpenAI Function Calling)

```python
ASSISTANT_TOOLS = [
    # ===== QUERY TOOLS (Read-only) =====
    {
        "type": "function",
        "function": {
            "name": "get_spending_summary",
            "description": "Get total spending, optionally filtered by category and time period. Use this when the user asks about spending, expenses, or how much they spent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category name to filter by (e.g., 'Groceries', 'Dining Out')"
                    },
                    "period": {
                        "type": "string",
                        "enum": ["this_month", "last_month", "this_quarter", "last_quarter", "this_year", "last_year", "custom"],
                        "description": "Time period for the summary"
                    },
                    "date_from": {
                        "type": "string",
                        "format": "date",
                        "description": "Start date (ISO format) for custom period"
                    },
                    "date_to": {
                        "type": "string",
                        "format": "date",
                        "description": "End date (ISO format) for custom period"
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
            "description": "Get total income, optionally filtered by category and time period.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "period": {"type": "string", "enum": ["this_month", "last_month", "this_quarter", "last_quarter", "this_year", "last_year", "custom"]},
                    "date_from": {"type": "string", "format": "date"},
                    "date_to": {"type": "string", "format": "date"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_categories",
            "description": "Get the top spending or income categories ranked by total amount.",
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
                        "description": "Number of categories to return"
                    },
                    "period": {"type": "string", "enum": ["this_month", "last_month", "this_quarter", "this_year"]}
                },
                "required": ["type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_transactions",
            "description": "Search for transactions by merchant name, description, amount, or date range.",
            "parameters": {
                "type": "object",
                "properties": {
                    "merchant": {"type": "string", "description": "Merchant name to search for (partial match)"},
                    "description": {"type": "string", "description": "Transaction description to search for"},
                    "category": {"type": "string"},
                    "amount_min": {"type": "number"},
                    "amount_max": {"type": "number"},
                    "date_from": {"type": "string", "format": "date"},
                    "date_to": {"type": "string", "format": "date"},
                    "is_uncategorized": {"type": "boolean", "description": "Only return uncategorized transactions"},
                    "limit": {"type": "integer", "default": 20}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_account_balance",
            "description": "Get the current balance of a specific account or all accounts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "account_name": {"type": "string", "description": "Name of the account (e.g., 'Chase Checking')"},
                    "include_all": {"type": "boolean", "description": "Return all account balances"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_cash_flow",
            "description": "Get net cash flow (income minus expenses) for a period.",
            "parameters": {
                "type": "object",
                "properties": {
                    "period": {"type": "string", "enum": ["this_month", "last_month", "this_quarter", "this_year"]},
                    "include_breakdown": {"type": "boolean", "description": "Include income/expense breakdown"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_periods",
            "description": "Compare spending or income between two time periods.",
            "parameters": {
                "type": "object",
                "properties": {
                    "metric": {"type": "string", "enum": ["spending", "income", "net_cash_flow"]},
                    "category": {"type": "string"},
                    "period_1": {"type": "string", "enum": ["this_month", "last_month", "this_quarter", "last_quarter"]},
                    "period_2": {"type": "string", "enum": ["this_month", "last_month", "this_quarter", "last_quarter"]}
                },
                "required": ["metric", "period_1", "period_2"]
            }
        }
    },

    # ===== ACTION TOOLS (Require Confirmation) =====
    {
        "type": "function",
        "function": {
            "name": "propose_categorization",
            "description": "Propose categorizing one or more transactions. Returns a preview that the user must confirm.",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Transaction IDs to categorize"
                    },
                    "merchant_pattern": {
                        "type": "string",
                        "description": "Alternatively, match by merchant name pattern"
                    },
                    "category_name": {
                        "type": "string",
                        "description": "Target category name"
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
            "description": "Propose creating a rule to automatically categorize future transactions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Text pattern to match in transaction description"},
                    "pattern_type": {"type": "string", "enum": ["contains", "starts_with", "ends_with", "exact", "regex"]},
                    "category_name": {"type": "string"},
                    "rule_name": {"type": "string", "description": "Human-readable name for the rule"}
                },
                "required": ["pattern", "pattern_type", "category_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "propose_mark_as_transfer",
            "description": "Propose marking a transaction as an internal transfer (excluded from income/expense calculations).",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_id": {"type": "string"},
                    "related_transaction_id": {"type": "string", "description": "The corresponding transaction in the other account"}
                },
                "required": ["transaction_id"]
            }
        }
    },

    # ===== NAVIGATION TOOLS =====
    {
        "type": "function",
        "function": {
            "name": "create_navigation_link",
            "description": "Create a link to navigate the user to a specific page with optional filters applied.",
            "parameters": {
                "type": "object",
                "properties": {
                    "page": {
                        "type": "string",
                        "enum": ["dashboard", "transactions", "analysis", "analysis/income", "analysis/expenses", "accounts", "projections", "scenarios", "classifications", "settings"],
                        "description": "Target page"
                    },
                    "filters": {
                        "type": "object",
                        "description": "Query parameters to apply",
                        "properties": {
                            "category": {"type": "string"},
                            "account": {"type": "string"},
                            "date_from": {"type": "string"},
                            "date_to": {"type": "string"},
                            "transaction_id": {"type": "string"}
                        }
                    },
                    "label": {"type": "string", "description": "Button label to display"}
                },
                "required": ["page"]
            }
        }
    }
]
```

---

### Implementation: Core Classes

#### LLM Adapter (Provider Abstraction)

```python
# src/financial_analysis/services/assistant/llm_adapter.py

from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict, Any
from dataclasses import dataclass
import openai

@dataclass
class ToolCall:
    id: str
    name: str
    arguments: Dict[str, Any]

@dataclass
class LLMResponse:
    content: str
    tool_calls: List[ToolCall]
    tokens_used: int
    model: str

class LLMAdapter(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict],
        tools: List[Dict],
        stream: bool = True
    ) -> AsyncGenerator[str, None] | LLMResponse:
        pass

class OpenAIAdapter(LLMAdapter):
    """OpenAI GPT implementation."""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model

    async def chat_completion(
        self,
        messages: List[Dict],
        tools: List[Dict],
        stream: bool = True
    ) -> AsyncGenerator[str, None]:

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            stream=stream
        )

        if stream:
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield {"type": "content", "data": chunk.choices[0].delta.content}
                if chunk.choices[0].delta.tool_calls:
                    yield {"type": "tool_call", "data": chunk.choices[0].delta.tool_calls}
        else:
            yield response
```

#### Tool Orchestrator

```python
# src/financial_analysis/services/assistant/tool_orchestrator.py

from typing import Dict, Any, Callable
from .tools import TOOL_IMPLEMENTATIONS

class ToolOrchestrator:
    """Executes tool calls and manages confirmations."""

    def __init__(self, db_session, services: Dict):
        self.db = db_session
        self.services = services
        self.pending_actions: Dict[str, Dict] = {}  # message_id -> action details

    async def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool and return the result."""

        tool_fn = TOOL_IMPLEMENTATIONS.get(tool_name)
        if not tool_fn:
            return {"error": f"Unknown tool: {tool_name}"}

        # Check if tool requires confirmation
        if tool_name.startswith("propose_"):
            return await self._handle_proposal(tool_name, args)

        # Execute read-only tools directly
        return await tool_fn(self.services, args)

    async def _handle_proposal(self, tool_name: str, args: Dict) -> Dict:
        """Handle action proposals that need user confirmation."""

        # Generate preview
        if tool_name == "propose_categorization":
            preview = await self._preview_categorization(args)
            return {
                "type": "action_proposal",
                "action": "categorize",
                "preview": preview,
                "requires_confirmation": True
            }
        # ... other proposals

    async def confirm_action(self, message_id: str, action_payload: Dict) -> Dict:
        """Execute a confirmed action and log it for undo."""

        # Capture previous state
        previous_state = await self._capture_state(action_payload)

        # Execute action
        result = await self._execute_action(action_payload)

        # Log for undo
        await self._log_action(message_id, action_payload, previous_state, result)

        return result

    async def undo_action(self, action_log_id: str) -> Dict:
        """Undo a previously executed action."""

        log_entry = await self._get_action_log(action_log_id)
        if not log_entry or log_entry.undone_at:
            return {"error": "Action cannot be undone"}

        # Restore previous state
        await self._restore_state(log_entry.previous_state)

        # Mark as undone
        log_entry.undone_at = datetime.utcnow()
        await self.db.commit()

        return {"success": True, "message": "Action undone"}
```

#### Conversation Manager

```python
# src/financial_analysis/services/assistant/conversation_manager.py

class ConversationManager:
    """Manages conversation history and context."""

    MAX_CONTEXT_MESSAGES = 20

    def __init__(self, db_session):
        self.db = db_session

    async def get_or_create_conversation(self, conversation_id: str = None) -> str:
        """Get existing conversation or create new one."""
        if conversation_id:
            conv = await self.db.get(AssistantConversation, conversation_id)
            if conv:
                return conv

        # Create new conversation
        conv = AssistantConversation(id=str(uuid4()))
        self.db.add(conv)
        await self.db.commit()
        return conv

    async def build_messages(
        self,
        conversation_id: str,
        new_message: str,
        context: Dict
    ) -> List[Dict]:
        """Build message list for LLM including history and context."""

        messages = [self._build_system_prompt(context)]

        # Add conversation history
        history = await self._get_recent_messages(conversation_id)
        messages.extend(history)

        # Add new user message
        messages.append({"role": "user", "content": new_message})

        return messages

    def _build_system_prompt(self, context: Dict) -> Dict:
        """Build system prompt with current context."""

        today = date.today().isoformat()

        prompt = f"""You are Minty, a helpful financial assistant for Spearmint.

Today's date: {today}

Your capabilities:
- Answer questions about spending, income, and account balances
- Search for specific transactions
- Help categorize transactions (with user confirmation)
- Create rules for automatic categorization
- Navigate to relevant pages in the app

Guidelines:
- Always cite your data sources (e.g., "Based on 23 transactions from January...")
- For any action that modifies data, explain what will change and ask for confirmation
- Keep responses concise but informative
- Use currency formatting ($X,XXX.XX)
- When comparing periods, show absolute and percentage changes

Current context:
- Page: {context.get('current_page', 'unknown')}
- Selected transaction: {context.get('selected_transaction_id', 'none')}
- Active filters: {context.get('active_filters', {})}
"""
        return {"role": "system", "content": prompt}
```

---

### Frontend Integration

#### React Hook

```typescript
// src/hooks/useAssistant.ts

import { useState, useCallback, useRef } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  toolCalls?: ToolCall[];
  actionCard?: ActionCard;
  timestamp: Date;
}

interface UseAssistantOptions {
  onActionProposed?: (action: ActionProposal) => void;
}

export function useAssistant(options: UseAssistantOptions = {}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    // Add user message
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Create assistant message placeholder
    const assistantMessageId = crypto.randomUUID();
    setMessages(prev => [...prev, {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      timestamp: new Date(),
    }]);

    // Build context
    const context = {
      current_page: window.location.pathname,
      // Add selected items, filters, etc.
    };

    // Connect to SSE endpoint
    const response = await fetch('/api/assistant/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: content,
        conversation_id: conversationId,
        context,
      }),
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader!.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6));
          handleSSEEvent(data, assistantMessageId);
        }
      }
    }

    setIsLoading(false);
  }, [conversationId]);

  const handleSSEEvent = (event: any, messageId: string) => {
    switch (event.type) {
      case 'content_delta':
        setMessages(prev => prev.map(m =>
          m.id === messageId
            ? { ...m, content: m.content + event.delta }
            : m
        ));
        break;
      case 'action_card':
        setMessages(prev => prev.map(m =>
          m.id === messageId
            ? { ...m, actionCard: event.card }
            : m
        ));
        break;
      case 'conversation_id':
        setConversationId(event.id);
        break;
    }
  };

  const confirmAction = useCallback(async (messageId: string, payload: any) => {
    const response = await fetch('/api/assistant/actions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message_id: messageId,
        confirmed: true,
        payload,
      }),
    });
    return response.json();
  }, []);

  const undoAction = useCallback(async (actionLogId: string) => {
    const response = await fetch('/api/assistant/actions/undo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action_log_id: actionLogId }),
    });
    return response.json();
  }, []);

  return {
    messages,
    isLoading,
    sendMessage,
    confirmAction,
    undoAction,
    conversationId,
  };
}
```

---

### Cost Analysis

#### OpenAI Pricing (as of 2026)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| gpt-4o | $2.50 | $10.00 |
| gpt-4o-mini | $0.15 | $0.60 |
| gpt-3.5-turbo | $0.50 | $1.50 |

#### Estimated Usage Per User

| Interaction Type | Avg Tokens | Frequency/Month | Cost (gpt-4o) |
|------------------|------------|-----------------|---------------|
| Simple query | 500 in / 200 out | 30 | $0.10 |
| Complex analysis | 1500 in / 500 out | 10 | $0.09 |
| Categorization task | 2000 in / 300 out | 5 | $0.04 |
| **Total per user** | | | **~$0.25/month** |

#### Cost Mitigation Strategies

1. **Model Routing:** Use gpt-4o-mini for simple queries (60% of traffic) → 80% cost reduction for those queries
2. **Caching:** Cache common queries (e.g., "What are my top categories?") with short TTL
3. **Context Pruning:** Summarize long conversation history instead of including all messages
4. **Rate Limiting:** 100 queries/hour per user prevents runaway costs

---

### Security Considerations

#### API Key Management

```python
# API keys stored encrypted in database
# Decrypted only in memory during request

from cryptography.fernet import Fernet

class APIKeyManager:
    def __init__(self, encryption_key: bytes):
        self.cipher = Fernet(encryption_key)

    def encrypt_key(self, api_key: str) -> str:
        return self.cipher.encrypt(api_key.encode()).decode()

    def decrypt_key(self, encrypted_key: str) -> str:
        return self.cipher.decrypt(encrypted_key.encode()).decode()
```

#### Prompt Injection Prevention

```python
def sanitize_user_input(message: str) -> str:
    """Prevent prompt injection attacks."""

    # Remove potential injection patterns
    dangerous_patterns = [
        "ignore previous instructions",
        "disregard above",
        "new instructions:",
        "system:",
    ]

    sanitized = message
    for pattern in dangerous_patterns:
        sanitized = sanitized.replace(pattern.lower(), "[filtered]")

    return sanitized
```

#### Data Minimization

```python
def prepare_transaction_for_llm(transaction: Transaction) -> Dict:
    """Only send necessary fields to LLM—no sensitive data."""

    return {
        "id": transaction.id,
        "date": transaction.date.isoformat(),
        "description": transaction.description,  # Merchant name only
        "amount": float(transaction.amount),
        "category": transaction.category.name if transaction.category else None,
        # Explicitly exclude:
        # - account_number
        # - full_memo (may contain sensitive info)
        # - any PII
    }
```

---

### Data Flow Example

**User Query:** "How much did I spend on groceries last month?"

```
┌──────────────────────────────────────────────────────────────────────────┐
│ 1. User sends message via ChatPanel                                      │
│    POST /api/assistant/chat                                              │
│    {message: "How much did I spend on groceries last month?"}            │
└────────────────────────────────────────────────────────────────────────┬─┘
                                                                         │
┌────────────────────────────────────────────────────────────────────────▼─┐
│ 2. AssistantService builds context                                       │
│    - Load conversation history                                           │
│    - Build system prompt with today's date                               │
│    - Add page context                                                    │
└────────────────────────────────────────────────────────────────────────┬─┘
                                                                         │
┌────────────────────────────────────────────────────────────────────────▼─┐
│ 3. OpenAI API call with tools                                            │
│    model: gpt-4o                                                         │
│    messages: [system, ...history, user]                                  │
│    tools: [get_spending_summary, search_transactions, ...]               │
└────────────────────────────────────────────────────────────────────────┬─┘
                                                                         │
┌────────────────────────────────────────────────────────────────────────▼─┐
│ 4. LLM decides to call tool                                              │
│    tool_call: get_spending_summary                                       │
│    args: {category: "Groceries", period: "last_month"}                   │
└────────────────────────────────────────────────────────────────────────┬─┘
                                                                         │
┌────────────────────────────────────────────────────────────────────────▼─┐
│ 5. ToolOrchestrator executes tool                                        │
│    → AnalysisService.get_expense_analysis(category="Groceries", ...)     │
│    Result: {total: 523.47, count: 23, avg: 22.76, ...}                   │
└────────────────────────────────────────────────────────────────────────┬─┘
                                                                         │
┌────────────────────────────────────────────────────────────────────────▼─┐
│ 6. Tool result sent back to LLM                                          │
│    LLM formats human-readable response                                   │
└────────────────────────────────────────────────────────────────────────┬─┘
                                                                         │
┌────────────────────────────────────────────────────────────────────────▼─┐
│ 7. Response streamed to frontend via SSE                                 │
│    event: content_delta → "You spent $523.47 on Groceries..."            │
│    event: action_card → {type: "navigation", url: "/transactions?..."}   │
│    event: message_complete → {tokens_used: 847}                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Plan

### Overview

The AI Financial Assistant will be implemented across 4 phases, with Phase 1 (MVP) targeted for completion in 6 weeks. Each phase builds on the previous, allowing for user feedback and iteration.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        IMPLEMENTATION TIMELINE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Phase 1: Query Assistant (MVP)                                              │
│  ════════════════════════════════                                            │
│  Weeks 1-6 │████████████████████████████████████████│                        │
│            │ Sprint 1 │ Sprint 2 │ Sprint 3 │                                │
│            │Foundation│ Tools    │ Frontend │                                │
│                                              ▼                               │
│                                         🚀 MVP Launch                        │
│                                                                              │
│  Phase 2: Task Automation                                                    │
│  ════════════════════════════                                                │
│  Weeks 7-10│                    │██████████████████│                         │
│            │                    │Sprint 4│Sprint 5│                          │
│            │                    │Actions │Polish  │                          │
│                                                   ▼                          │
│                                              🚀 Phase 2 Launch               │
│                                                                              │
│  Phase 3: Proactive Intelligence                                             │
│  ═══════════════════════════════                                             │
│  Weeks 11-14                    │                  │████████████████│        │
│                                                    │Sprint 6│Sprint 7│       │
│                                                    │Insights│Alerts  │       │
│                                                                     ▼        │
│                                                                🚀 Phase 3    │
│                                                                              │
│  Phase 4: Advanced Features                                                  │
│  ══════════════════════════                                                  │
│  Weeks 15-20                                       │        │████████████│   │
│                                                             │ Sprints 8-10│  │
│                                                             │ Scenarios,  │  │
│                                                             │ Voice, etc. │  │
│                                                                          ▼   │
│                                                                     🚀 1.0   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Phase 1: Query Assistant (MVP)

**Duration:** 6 weeks (3 sprints)
**Goal:** Users can ask natural language questions and get accurate answers about their financial data.

#### Sprint 1: Foundation (Weeks 1-2)

**Focus:** Core infrastructure, LLM integration, basic API

| Task | Description | Owner | Est. |
|------|-------------|-------|------|
| **Backend Setup** | | | |
| B1.1 | Create `assistant/` module structure under `services/` | Backend | 2h |
| B1.2 | Implement `LLMAdapter` base class and `OpenAIAdapter` | Backend | 4h |
| B1.3 | Add `openai` to requirements.txt, configure API key handling | Backend | 2h |
| B1.4 | Implement `ConversationManager` with basic history | Backend | 4h |
| B1.5 | Create database migration for `assistant_*` tables | Backend | 3h |
| B1.6 | Implement `/api/assistant/chat` endpoint (non-streaming) | Backend | 4h |
| B1.7 | Add SSE streaming support to chat endpoint | Backend | 6h |
| **Security** | | | |
| S1.1 | Implement `APIKeyManager` with Fernet encryption | Backend | 3h |
| S1.2 | Add input sanitization for prompt injection | Backend | 2h |
| S1.3 | Add rate limiting middleware (100 req/hour) | Backend | 2h |
| **Testing** | | | |
| T1.1 | Unit tests for `OpenAIAdapter` (with mocks) | Backend | 4h |
| T1.2 | Unit tests for `ConversationManager` | Backend | 3h |
| T1.3 | Integration test for `/api/assistant/chat` | Backend | 4h |

**Sprint 1 Deliverables:**
- [ ] OpenAI integration working with streaming
- [ ] Conversation history persisted to database
- [ ] API key securely stored and encrypted
- [ ] Basic `/api/assistant/chat` endpoint functional
- [ ] Rate limiting in place

**Definition of Done:**
- Can send a message and receive streamed response
- Conversation persists across page refreshes
- All tests passing (>80% coverage on new code)

---

#### Sprint 2: Query Tools (Weeks 3-4)

**Focus:** Implement read-only tools, connect to existing services

| Task | Description | Owner | Est. |
|------|-------------|-------|------|
| **Tool Implementation** | | | |
| B2.1 | Implement `ToolOrchestrator` base class | Backend | 4h |
| B2.2 | Implement `get_spending_summary` tool | Backend | 4h |
| B2.3 | Implement `get_income_summary` tool | Backend | 3h |
| B2.4 | Implement `search_transactions` tool | Backend | 4h |
| B2.5 | Implement `get_top_categories` tool | Backend | 3h |
| B2.6 | Implement `get_account_balance` tool | Backend | 3h |
| B2.7 | Implement `get_cash_flow` tool | Backend | 3h |
| B2.8 | Implement `compare_periods` tool | Backend | 4h |
| B2.9 | Implement `create_navigation_link` tool | Backend | 2h |
| **System Prompt** | | | |
| B2.10 | Design and iterate on system prompt | Backend | 4h |
| B2.11 | Add dynamic context injection (current date, page) | Backend | 2h |
| **Testing** | | | |
| T2.1 | Unit tests for each tool (8 tools × 2h) | Backend | 16h |
| T2.2 | Integration tests for tool execution flow | Backend | 4h |
| T2.3 | End-to-end test: query → tool → response | Backend | 4h |
| **Quality** | | | |
| Q2.1 | Create eval dataset (50 test queries with expected outputs) | QA | 6h |
| Q2.2 | Run accuracy evaluation, iterate on prompts | Backend | 4h |

**Sprint 2 Deliverables:**
- [ ] All 8 query tools implemented and tested
- [ ] Tool orchestration working with multi-tool calls
- [ ] System prompt tuned for accuracy
- [ ] Eval dataset created with 90%+ accuracy on test queries

**Definition of Done:**
- Can answer: spending queries, income queries, category rankings, account balances
- Responses cite sources (transaction counts, date ranges)
- 90%+ accuracy on eval dataset
- All tests passing

---

#### Sprint 3: Frontend & Polish (Weeks 5-6)

**Focus:** Build chat UI, integrate with backend, polish UX

| Task | Description | Owner | Est. |
|------|-------------|-------|------|
| **Frontend Components** | | | |
| F3.1 | Create `ChatPanel` component (slide-in drawer) | Frontend | 6h |
| F3.2 | Create `ChatMessage` component (user/assistant bubbles) | Frontend | 4h |
| F3.3 | Create `ChatInput` component with send button | Frontend | 3h |
| F3.4 | Create `ActionCard` component for navigation links | Frontend | 3h |
| F3.5 | Create `FloatingActionButton` (FAB) component | Frontend | 2h |
| F3.6 | Implement `useAssistant` hook with SSE streaming | Frontend | 6h |
| F3.7 | Add typing indicator during streaming | Frontend | 2h |
| F3.8 | Implement message history scroll and auto-scroll | Frontend | 2h |
| **Integration** | | | |
| F3.9 | Integrate FAB into `Layout` component | Frontend | 2h |
| F3.10 | Pass page context (current route, filters) to API | Frontend | 3h |
| F3.11 | Handle navigation actions from ActionCards | Frontend | 2h |
| **UX Polish** | | | |
| F3.12 | Add keyboard shortcut (Cmd+K) to open chat | Frontend | 2h |
| F3.13 | Add minimize/close functionality | Frontend | 2h |
| F3.14 | Mobile responsive layout (full-screen on small screens) | Frontend | 4h |
| F3.15 | Add empty state / welcome message | Frontend | 2h |
| F3.16 | Add suggested prompts chips | Frontend | 3h |
| **Accessibility** | | | |
| A3.1 | Add ARIA labels and roles | Frontend | 3h |
| A3.2 | Ensure keyboard navigation works | Frontend | 2h |
| A3.3 | Test with screen reader | Frontend | 2h |
| **Testing** | | | |
| T3.1 | Component tests for ChatPanel, ChatMessage | Frontend | 4h |
| T3.2 | E2E test: open chat, send query, verify response | QA | 4h |
| T3.3 | Mobile testing (iOS Safari, Android Chrome) | QA | 3h |
| **Documentation** | | | |
| D3.1 | User-facing help documentation | Docs | 3h |
| D3.2 | API documentation for `/api/assistant/*` | Backend | 2h |

**Sprint 3 Deliverables:**
- [ ] Fully functional chat UI accessible from FAB
- [ ] Streaming responses with typing indicator
- [ ] Navigation actions working
- [ ] Mobile responsive
- [ ] Keyboard accessible (Cmd+K, tab navigation)
- [ ] E2E tests passing

**Definition of Done:**
- User can open chat from any page
- User can ask questions and see streamed responses
- Navigation links work correctly
- Works on mobile devices
- Accessibility audit passes

---

### Phase 2: Task Automation

**Duration:** 4 weeks (2 sprints)
**Goal:** Users can categorize transactions and create rules through conversation.

#### Sprint 4: Action Tools (Weeks 7-8)

| Task | Description | Owner | Est. |
|------|-------------|-------|------|
| **Action Tools** | | | |
| B4.1 | Implement `propose_categorization` tool | Backend | 6h |
| B4.2 | Implement bulk categorization preview logic | Backend | 4h |
| B4.3 | Implement `propose_category_rule` tool | Backend | 4h |
| B4.4 | Implement `propose_mark_as_transfer` tool | Backend | 3h |
| **Confirmation Flow** | | | |
| B4.5 | Implement action confirmation endpoint | Backend | 4h |
| B4.6 | Implement state capture for undo | Backend | 4h |
| B4.7 | Implement `assistant_action_log` persistence | Backend | 3h |
| B4.8 | Implement undo endpoint and logic | Backend | 4h |
| **Frontend** | | | |
| F4.1 | Create `ActionProposal` component (confirm/cancel) | Frontend | 4h |
| F4.2 | Create `BulkPreview` component (show affected items) | Frontend | 4h |
| F4.3 | Create `UndoToast` notification component | Frontend | 2h |
| F4.4 | Integrate confirmation flow in useAssistant | Frontend | 3h |
| **Testing** | | | |
| T4.1 | Unit tests for action tools | Backend | 6h |
| T4.2 | Integration test for confirm/undo flow | Backend | 4h |
| T4.3 | E2E test: categorize → confirm → undo | QA | 4h |

**Sprint 4 Deliverables:**
- [ ] Categorization via conversation working
- [ ] Confirmation UI with preview
- [ ] Undo capability functional
- [ ] Action audit log persisted

---

#### Sprint 5: Polish & Edge Cases (Weeks 9-10)

| Task | Description | Owner | Est. |
|------|-------------|-------|------|
| **Edge Cases** | | | |
| B5.1 | Handle no matching transactions gracefully | Backend | 2h |
| B5.2 | Handle duplicate rule creation attempts | Backend | 2h |
| B5.3 | Handle partial failures in bulk operations | Backend | 3h |
| B5.4 | Add confirmation threshold (>10 items = extra warning) | Backend | 2h |
| **UX Improvements** | | | |
| F5.1 | Add progress indicator for bulk operations | Frontend | 3h |
| F5.2 | Add success/error animations | Frontend | 2h |
| F5.3 | Improve action card design (icons, colors) | Frontend | 3h |
| **Follow-up Prompts** | | | |
| B5.5 | "Create rule for future?" prompt after categorization | Backend | 3h |
| B5.6 | "Review similar?" prompt after single categorization | Backend | 3h |
| **Testing & QA** | | | |
| T5.1 | Regression testing on Phase 1 features | QA | 4h |
| T5.2 | User acceptance testing (3-5 users) | QA | 8h |
| T5.3 | Performance testing (response times) | Backend | 3h |
| **Documentation** | | | |
| D5.1 | Update user documentation with action features | Docs | 3h |

**Sprint 5 Deliverables:**
- [ ] Edge cases handled gracefully
- [ ] Follow-up prompts working
- [ ] User feedback incorporated
- [ ] Performance within targets (<5s p95)

---

### Phase 3: Proactive Intelligence

**Duration:** 4 weeks (2 sprints)
**Goal:** System proactively surfaces insights and anomalies.

#### Sprint 6: Insight Generation (Weeks 11-12)

| Task | Description | Owner | Est. |
|------|-------------|-------|------|
| **Insight Engine** | | | |
| B6.1 | Create `InsightGenerator` service | Backend | 4h |
| B6.2 | Implement uncategorized transaction detection | Backend | 3h |
| B6.3 | Implement spending anomaly detection (z-score) | Backend | 6h |
| B6.4 | Implement duplicate transaction detection | Backend | 4h |
| B6.5 | Implement post-import insight generation | Backend | 4h |
| B6.6 | Create `/api/assistant/insights` endpoint | Backend | 3h |
| **Scheduling** | | | |
| B6.7 | Add background job for daily insight generation | Backend | 4h |
| B6.8 | Add post-import hook for insight generation | Backend | 3h |
| **Frontend** | | | |
| F6.1 | Create `InsightCard` component | Frontend | 3h |
| F6.2 | Show pending insights when chat opens | Frontend | 3h |
| F6.3 | Add dismiss/act-on functionality | Frontend | 3h |
| **Testing** | | | |
| T6.1 | Unit tests for anomaly detection | Backend | 4h |
| T6.2 | Integration test for insight generation | Backend | 3h |

---

#### Sprint 7: Alerts & Preferences (Weeks 13-14)

| Task | Description | Owner | Est. |
|------|-------------|-------|------|
| **User Preferences** | | | |
| B7.1 | Add insight preferences to `assistant_preferences` | Backend | 2h |
| B7.2 | Implement preference-aware insight filtering | Backend | 3h |
| F7.1 | Create insight preferences UI in Settings | Frontend | 4h |
| **Notification Badge** | | | |
| F7.2 | Add badge to FAB showing insight count | Frontend | 3h |
| F7.3 | Add subtle animation for new insights | Frontend | 2h |
| **Insight Actions** | | | |
| B7.3 | Connect insights to action tools | Backend | 4h |
| B7.4 | "Fix all uncategorized" bulk action | Backend | 4h |
| **Testing & Polish** | | | |
| T7.1 | E2E test for insight → action flow | QA | 4h |
| T7.2 | User acceptance testing | QA | 6h |

---

### Phase 4: Advanced Features

**Duration:** 6 weeks (3 sprints)
**Goal:** Scenario integration, recommendations, voice input.

#### Sprints 8-10 (Weeks 15-20)

| Feature | Tasks | Est. Total |
|---------|-------|------------|
| **Scenario Integration** | | 40h |
| | Add `run_scenario` tool | 8h |
| | Conversational scenario builder | 16h |
| | Present scenario results in chat | 8h |
| | Testing | 8h |
| **Recommendations** | | 30h |
| | Implement recommendation engine | 12h |
| | "How can I save money?" queries | 8h |
| | Goal tracking integration | 6h |
| | Testing | 4h |
| **Voice Input (Optional)** | | 20h |
| | Integrate Web Speech API | 8h |
| | Add microphone button to chat | 4h |
| | Handle voice-to-text errors | 4h |
| | Testing | 4h |
| **Ollama Local LLM** | | 24h |
| | Implement `OllamaAdapter` | 8h |
| | Add model selection UI | 6h |
| | Performance optimization | 6h |
| | Testing | 4h |

---

### Dependencies

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DEPENDENCY GRAPH                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐                                                        │
│  │ B1.1 Module  │                                                        │
│  │ Structure    │                                                        │
│  └──────┬───────┘                                                        │
│         │                                                                │
│         ▼                                                                │
│  ┌──────────────┐     ┌──────────────┐                                  │
│  │ B1.2 LLM     │────▶│ B1.6 Chat    │                                  │
│  │ Adapter      │     │ Endpoint     │                                  │
│  └──────────────┘     └──────┬───────┘                                  │
│                              │                                           │
│  ┌──────────────┐            │      ┌──────────────┐                    │
│  │ B1.5 DB      │────────────┼─────▶│ B1.4 Convo   │                    │
│  │ Migration    │            │      │ Manager      │                    │
│  └──────────────┘            │      └──────────────┘                    │
│                              │                                           │
│                              ▼                                           │
│                       ┌──────────────┐                                  │
│                       │ B1.7 SSE     │                                  │
│                       │ Streaming    │                                  │
│                       └──────┬───────┘                                  │
│                              │                                           │
│         ┌────────────────────┼────────────────────┐                     │
│         │                    │                    │                     │
│         ▼                    ▼                    ▼                     │
│  ┌──────────────┐     ┌──────────────┐    ┌──────────────┐             │
│  │ B2.1 Tool    │     │ B2.2-B2.9    │    │ F3.6 React   │             │
│  │ Orchestrator │────▶│ Query Tools  │    │ Hook         │             │
│  └──────────────┘     └──────────────┘    └──────┬───────┘             │
│                                                   │                     │
│                                                   ▼                     │
│                                           ┌──────────────┐             │
│                                           │ F3.1-F3.5    │             │
│                                           │ UI Components│             │
│                                           └──────────────┘             │
│                                                                          │
│  ═══════════════════════════════════════════════════════════════════    │
│                           PHASE 1 COMPLETE                               │
│  ═══════════════════════════════════════════════════════════════════    │
│                                                                          │
│  ┌──────────────┐     ┌──────────────┐                                  │
│  │ B4.1-B4.4    │────▶│ B4.5-B4.8    │                                  │
│  │ Action Tools │     │ Confirm/Undo │                                  │
│  └──────────────┘     └──────┬───────┘                                  │
│                              │                                           │
│                              ▼                                           │
│                       ┌──────────────┐                                  │
│                       │ F4.1-F4.4    │                                  │
│                       │ Action UI    │                                  │
│                       └──────────────┘                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Testing Strategy

#### Unit Tests
- **Coverage Target:** 80% on all new code
- **Focus:** Tool implementations, LLM adapter, conversation manager
- **Mocking:** OpenAI API calls mocked for deterministic tests

#### Integration Tests
- **Scope:** API endpoints, tool orchestration, database persistence
- **Environment:** Test database with seeded financial data

#### End-to-End Tests
- **Framework:** Playwright (existing setup)
- **Scenarios:**
  - Open chat, send query, verify response appears
  - Ask spending question, verify correct amount
  - Categorize transaction, confirm, verify change
  - Undo categorization, verify restored

#### Accuracy Evaluation
- **Eval Dataset:** 100 queries with expected tool calls and responses
- **Metrics:**
  - Tool selection accuracy (correct tool called)
  - Parameter accuracy (correct args passed)
  - Response accuracy (answer matches expected)
- **Target:** 90%+ accuracy before launch

#### Performance Tests
- **Response Time:** p95 < 5 seconds
- **Streaming:** First token < 1 second
- **Load Test:** 10 concurrent users, no degradation

---

### Milestones & Checkpoints

| Milestone | Date | Success Criteria |
|-----------|------|------------------|
| **M1: Backend Foundation** | Week 2 | LLM integration working, streaming functional |
| **M2: Tools Complete** | Week 4 | All 8 query tools passing tests, 90% eval accuracy |
| **M3: MVP Launch** | Week 6 | Full UI, E2E tests passing, deployed to staging |
| **M4: Actions Launch** | Week 10 | Categorization, rules, undo working in production |
| **M5: Insights Launch** | Week 14 | Proactive insights surfacing, preferences working |
| **M6: v1.0 Release** | Week 20 | All Phase 4 features complete, voice optional |

---

### Risk Mitigation During Implementation

| Risk | Detection | Mitigation |
|------|-----------|------------|
| **OpenAI API instability** | Monitor error rates | Implement retry logic, circuit breaker |
| **Slow response times** | Performance tests in CI | Model routing (use mini for simple queries) |
| **Poor accuracy** | Eval dataset results | Iterate on prompts, add examples |
| **Scope creep** | Sprint planning | Strict MVP scope, defer to Phase 2+ |
| **Security vulnerabilities** | Security review | Pre-launch penetration testing |

---

### Team & Resources

#### Required Skills
- **Backend:** Python, FastAPI, async programming, OpenAI SDK
- **Frontend:** React, TypeScript, SSE handling, accessibility
- **DevOps:** Rate limiting, API key management, monitoring

#### Recommended Team Allocation
| Role | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|---------|---------|---------|---------|
| Backend Engineer | 1.0 FTE | 0.5 FTE | 0.5 FTE | 0.5 FTE |
| Frontend Engineer | 0.5 FTE | 0.5 FTE | 0.3 FTE | 0.3 FTE |
| QA Engineer | 0.25 FTE | 0.25 FTE | 0.25 FTE | 0.25 FTE |

#### External Dependencies
- OpenAI API account with billing
- Staging environment for testing
- User cohort for acceptance testing (5-10 users)

---

## Phased Rollout

### Phase 1: Query Assistant (MVP)
- Natural language queries for spending, income, categories
- Read-only operations
- Basic context awareness (current page)
- FAB interface

### Phase 2: Task Automation
- Transaction categorization
- Rule creation through conversation
- Bulk operations with confirmation
- Undo capability

### Phase 3: Proactive Intelligence
- Anomaly detection and alerts
- Post-import insights
- Uncategorized transaction suggestions
- Goal tracking reminders

### Phase 4: Advanced Features
- Scenario modeling through conversation
- Personalized recommendations
- Voice input
- Multi-user conversations (household)

---

## Out of Scope (Future Iterations)

- Voice input/output
- Integration with external services (banks, brokerages)
- Financial advice or recommendations (fiduciary concerns)
- Multi-user real-time collaboration
- Mobile native app integration
- Training on user data to improve model

---

## Open Questions

- **Q:** Which LLM provider should we use as the default?
  - **Decision:** OpenAI GPT-4o as primary provider
  - **Rationale:** Most mature function calling, excellent streaming, strong cost-performance balance
  - **Future:** Adapter pattern allows adding Claude/Ollama later

- **Q:** Should we use an agent framework (LangChain, LlamaIndex)?
  - **Decision:** No framework—use OpenAI SDK directly with custom orchestration
  - **Rationale:** Simpler debugging, lower latency, fewer dependencies, sufficient for our use case
  - **Reconsider if:** We need multi-agent workflows or RAG over documentation

- **Q:** Should conversation history persist across sessions?
  - **Decision:** Yes, store in user's local SQLite database (last 50 conversations)

- **Q:** How do we handle ambiguous queries?
  - **Decision:** Ask clarifying questions rather than guessing

- **Q:** What's the cost model for LLM usage?
  - **Decision:** User provides their own OpenAI API key (BYOK model)
  - **Estimated cost:** ~$0.25/user/month for typical usage
  - **Future:** Consider hosted option with usage-based pricing for convenience

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **LLM hallucinations** | User sees incorrect data | All responses cite sources; verify against actual API results |
| **Accidental data modification** | User frustration, data loss | Require confirmation for all writes; provide undo |
| **Cost overruns** | Users hit API limits | Rate limiting; usage dashboard; local LLM option |
| **Privacy concerns** | User distrust | Transparent data handling; local LLM option; no external logging |
| **Scope creep** | Delayed launch | Strict MVP definition; phase 1 is read-only only |

---

## Success Criteria Checklist

Before marking Phase 1 "complete," we must validate:

- [ ] User can ask "How much did I spend on X?" and get accurate answer
- [ ] User can ask "What are my top expense categories?" and see ranked list
- [ ] User can ask "Find transactions from Y" and see results
- [ ] Responses include source citations (transaction count, date range)
- [ ] Response time is <5 seconds for 95% of queries
- [ ] Chat panel is accessible via FAB on all pages
- [ ] Chat panel works on mobile devices
- [ ] Chat panel is keyboard navigable
- [ ] Users can close/minimize chat without losing context
- [ ] Error states are handled gracefully
- [ ] LLM adapter supports OpenAI (primary) and Ollama (local fallback)

---

## Appendix: Example Conversations

### Example 1: Spending Query

```
User: How much did I spend on restaurants this month?

Minty: You spent $423.18 on Dining Out this month across 12 transactions.

That's 8% less than last month ($459.32). Your most frequent restaurant
was Chipotle (4 visits, $52.40 total).

[View All Dining Transactions →]
```

### Example 2: Categorization Task

```
User: Categorize all my Amazon transactions as Shopping

Minty: I found 34 Amazon transactions totaling $1,247.89.

I'll categorize all of them as "Shopping". This will update:
• 28 currently uncategorized
• 6 currently marked as "Other"

[Preview Changes] [Apply All] [Cancel]

User: [clicks Apply All]

Minty: Done! I've categorized 34 transactions as Shopping.

Would you like me to create a rule so future Amazon transactions are
automatically categorized as Shopping?

[Yes, Create Rule] [No Thanks]
```

### Example 3: Insight Explanation

```
User: Why did my expenses spike in December?

Minty: Your December expenses were $8,234—47% higher than your
6-month average ($5,602).

The main drivers were:
1. **Gifts** — $1,847 (vs. $89 avg) — Holiday shopping
2. **Travel** — $1,234 (vs. $156 avg) — Flight to Denver
3. **Dining Out** — $623 (vs. $412 avg) — Holiday gatherings

If we exclude the one-time holiday expenses, your "baseline" spending
was actually $4,530—below your average.

[View December Transactions →] [Mark Travel as CapEx?]
```

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-02-03 | Product Team | Initial draft |
| 0.2 | 2026-02-03 | Product Team | Added comprehensive technical design: OpenAI as primary LLM, no agent framework, database schema, API design, tool definitions, cost analysis, security considerations |
| 0.3 | 2026-02-03 | Product Team | Added detailed implementation plan: 6-week MVP timeline, sprint breakdowns, task assignments, dependency graph, testing strategy, milestones |

---

**Next Steps:**
1. Product team review and sign-off on PRD
2. Engineering team review of technical design
3. Create Jira/Linear epics and stories from sprint tasks
4. UX design exploration (Figma mockups for chat panel)
5. Security review scheduling
6. Kick off Sprint 1
