# Product Requirements Document: MCP Server for AI Agent Integration

**Product:** Spearmint Personal Finance Engine
**Feature:** Model Context Protocol (MCP) Server
**Owner:** Product Team
**Status:** Ready for Implementation
**Last Updated:** 2026-02-02

---

## Executive Summary

Spearmint currently provides a REST API and web interface for financial data management. However, the rise of AI agents (Claude, ChatGPT, Copilot) creates an opportunity to let users interact with their financial data through natural language. An MCP (Model Context Protocol) server would enable users to ask questions like "What's my spending trend for groceries this year?" or "How much did I spend on dining out last month?" directly through their AI assistant.

This PRD defines the architecture, security model, and deployment strategy for a Spearmint MCP Server that can be auto-generated from our existing OpenAPI specification.

**Expected Impact:**
- Enable conversational finance management for users already using AI assistants
- Reduce friction for common queries (no need to navigate UI for quick answers)
- Position Spearmint as AI-native personal finance tooling
- Maintain security while exposing data to AI agents

---

## Problem Statement

### The User Problem

Users who have adopted AI assistants (Claude Desktop, ChatGPT, GitHub Copilot) want to query their personal finance data without switching contexts:

- **Quick lookups:** "How much did I spend on subscriptions last month?"
- **Trend analysis:** "Show me my grocery spending trend over the last 6 months"
- **Financial health:** "What's my current runway if I lost my job today?"
- **Transaction search:** "Find all transactions from Home Depot"
- **Planning:** "What would happen if my rent increased by $200/month?"

Currently, users must leave their AI assistant, open the Spearmint web app, navigate to the right page, and find the information themselves. This context-switching breaks the conversational flow and reduces the value of having a comprehensive financial data store.

### The Technical Problem

1. **No MCP server exists** - We have a REST API but no MCP-compatible interface
2. **Security is complex** - Financial data requires strong authentication; MCP connections must be user-isolated
3. **Token limits matter** - AI models have context limits; we must return concise, relevant data
4. **Maintenance burden** - Manual MCP server updates when API changes would create drift
5. **Installation friction** - Users need a simple way to connect their AI assistant to their Spearmint instance

### Evidence

**Market Trends:**
- Anthropic launched MCP in November 2024; adoption growing rapidly
- OpenAI plugins/GPTs enable similar AI-to-data patterns
- "AI-native" is becoming a product differentiator

**User Signals:**
- GitHub issues requesting Claude/ChatGPT integration
- Users manually copying data from Spearmint into AI chats
- Power users asking about API access for automation

---

## Goals & Success Metrics

### Goals

1. **Enable AI-powered queries:** Users can ask their AI assistant questions about their finances
2. **Maintain security:** Financial data is only accessible to authenticated users
3. **Minimize maintenance:** Auto-generate MCP server from OpenAPI spec in CI/CD pipeline
4. **Optimize for AI:** Return data formatted for minimal token usage and maximum AI comprehension

### Success Metrics

| Metric | Target | Timeframe |
|--------|--------|-----------|
| % of active users connecting MCP server | 20% | 3 months post-launch |
| Avg. MCP queries per user per week | 10 | 3 months post-launch |
| Token efficiency (avg tokens per response) | <2000 | Launch |
| Security incidents | 0 | Ongoing |
| Spec-to-MCP generation success rate | 99% | Ongoing |

---

## What is MCP?

**Model Context Protocol (MCP)** is an open standard (developed by Anthropic) that allows AI applications to connect to external data sources and tools. It defines:

- **Tools:** Functions the AI can call (e.g., `get_spending_summary`, `search_transactions`)
- **Resources:** Data the AI can read (e.g., list of accounts, categories)
- **Prompts:** Pre-defined prompt templates for common use cases

MCP servers communicate with AI clients via JSON-RPC over HTTP/SSE (Server-Sent Events) or stdio. We will use **HTTP/SSE transport** for maximum platform compatibility.

**Why MCP over direct API integration?**
- Standardized interface understood by Claude, ChatGPT, Gemini, and other AI systems
- Built-in schema description for AI to understand available operations
- Native support in Claude Desktop, Claude Code, ChatGPT, and Gemini CLI

**Why HTTP/SSE transport?**
- **Universal compatibility:** Works with all major AI platforms
- **ChatGPT requirement:** ChatGPT only supports remote HTTP/SSE servers (no local stdio)
- **Simpler architecture:** Single transport to maintain
- **Bundled deployment:** Runs as part of the Spearmint container

---

## User Stories

### Primary User Stories

**As a user, I want to:**

1. **Query spending by category** so I can understand where my money goes
   - *Example:* "What did I spend on groceries last month?"
   - *MCP Tool:* `get_expense_breakdown(category, start_date, end_date)`

2. **Search for specific transactions** so I can find records quickly
   - *Example:* "Find all Amazon transactions over $100"
   - *MCP Tool:* `search_transactions(query, min_amount, max_amount)`

3. **Get financial summaries** so I can understand my overall health
   - *Example:* "What's my net cash flow this month?"
   - *MCP Tool:* `get_financial_summary(period)`

4. **Check account balances** so I can know where I stand
   - *Example:* "What's my checking account balance?"
   - *MCP Tool:* `get_account_balance(account_name)`

5. **Run scenario projections** so I can plan for the future
   - *Example:* "What if I lost my job in 3 months?"
   - *MCP Tool:* `run_scenario_preview(adjustments)`

6. **Connect easily** so I can start using AI queries quickly
   - *Acceptance:* User can connect in under 5 minutes with clear instructions

### Secondary User Stories

**As a user, I want to:**

7. **Get spending alerts** when AI detects anomalies in my data
   - *Future iteration*

8. **Create transactions via voice** through the AI assistant
   - *Future iteration - requires write access*

9. **Generate financial reports** in natural language
   - *Future iteration*

---

## Architecture

### Decision: SDK-Based MCP Server

The MCP server will be a **TypeScript application that uses the Spearmint SDK** to interact with the REST API. This mirrors the architecture of the CLI and ensures consistent behavior across all clients.

**Key Architectural Principles:**

1. **SDK as the integration layer** - MCP server calls SDK, not REST API directly
2. **Consistent with CLI** - Same pattern used by the command-line interface
3. **Language-portable** - If backend changes language, SDK regenerates, MCP keeps working
4. **Bundled deployment** - Runs alongside the API in the same container

### Platform Compatibility

| Platform | Transport | Connection Method |
|----------|-----------|-------------------|
| **Claude Desktop** | HTTP/SSE | Direct URL or via tunnel |
| **Claude Code** | HTTP/SSE | Direct URL or via tunnel |
| **ChatGPT** | HTTP/SSE | Requires public URL (ngrok/Cloudflare Tunnel) |
| **Gemini CLI** | HTTP/SSE | Direct URL or via tunnel |

> **Note:** ChatGPT cannot connect to localhost. Users wanting ChatGPT integration must expose their Spearmint instance via a tunnel service (ngrok, Cloudflare Tunnel) or run it on a publicly accessible server.

### Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  CLI            │     │  MCP Server     │     │  Web App        │
│  (TypeScript)   │     │  (TypeScript)   │     │  (React)        │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                        ┌────────▼────────┐
                        │  TypeScript SDK │
                        │  @spearmint/sdk │
                        │  (auto-generated│
                        │   from OpenAPI) │
                        └────────┬────────┘
                                 │ HTTP
                        ┌────────▼────────┐
                        │  REST API       │
                        │  (Python/       │
                        │   FastAPI)      │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │  Database       │
                        │  (SQLite)       │
                        └─────────────────┘
```

### Container Architecture

The MCP server runs as a separate Node.js process within the Spearmint container:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Spearmint Container                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────┐   ┌─────────────────────────────────┐ │
│  │  FastAPI (Python)           │   │  MCP Server (Node.js)           │ │
│  │  Port 8000                  │   │  Port 3001                      │ │
│  │                             │   │                                 │ │
│  │  /api/transactions          │   │  /mcp/sse                       │ │
│  │  /api/reports               │◄──│  /mcp/messages                  │ │
│  │  /api/accounts              │   │                                 │ │
│  │  /api/analysis              │   │  Uses @spearmint/sdk            │ │
│  │  ...                        │   │  to call REST API               │ │
│  └─────────────────────────────┘   └─────────────────────────────────┘ │
│                                                                         │
│  Process Manager (pm2 or supervisord) manages both processes            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                    │                              │
                    │ Port 8000 (API)              │ Port 3001 (MCP)
                    ▼                              ▼
            ┌───────────────┐              ┌───────────────┐
            │ Web App       │              │ AI Clients    │
            │ Direct API    │              │ Claude/GPT/   │
            │ calls         │              │ Gemini        │
            └───────────────┘              └───────────────┘
```

### Why SDK-Based Architecture?

| Benefit | Description |
|---------|-------------|
| **Consistency** | CLI, MCP, and web app all use the same SDK interface |
| **Decoupling** | MCP server doesn't know FastAPI internals |
| **Portability** | Backend can change languages; regenerate SDK, MCP keeps working |
| **Type Safety** | TypeScript SDK provides full type checking for MCP tools |
| **Auth Handling** | SDK handles authentication, retries, error formatting |
| **Testability** | Can mock SDK for MCP server unit tests |

### Auto-Generation Pipeline

The pipeline generates both the SDK and MCP server code:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CI/CD Pipeline                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────┐                                                          │
│  │ OpenAPI   │                                                          │
│  │ Spec      │                                                          │
│  └─────┬─────┘                                                          │
│        │                                                                │
│        ├──────────────────────┐                                         │
│        │                      │                                         │
│        ▼                      ▼                                         │
│  ┌───────────┐          ┌───────────┐                                   │
│  │ LibLab    │          │ MCP       │                                   │
│  │ SDK Gen   │          │ Generator │                                   │
│  └─────┬─────┘          └─────┬─────┘                                   │
│        │                      │                                         │
│        ▼                      ▼                                         │
│  ┌───────────┐          ┌───────────┐          ┌───────────┐           │
│  │ TypeScript│          │ MCP Tool  │─────────►│ AI        │           │
│  │ SDK       │          │ Defs      │          │ Optimizer │           │
│  └─────┬─────┘          └───────────┘          │ (Claude)  │           │
│        │                      │                └─────┬─────┘           │
│        │                      │                      │                  │
│        │                      ▼                      ▼                  │
│        │               ┌─────────────────────────────────┐              │
│        └──────────────►│  MCP Server (TypeScript)        │              │
│                        │  - Uses SDK for API calls       │              │
│                        │  - AI-optimized tool descriptions│              │
│                        └─────────────────────────────────┘              │
│                                       │                                 │
│                              ┌────────▼────────┐                        │
│                              │ Build Docker    │                        │
│                              │ Image           │                        │
│                              └─────────────────┘                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Generation Steps:**

1. **Generate OpenAPI spec** → From FastAPI app (existing)
2. **Generate TypeScript SDK** → LibLab builds `@spearmint/sdk` (existing)
3. **Generate MCP tool definitions** → Map SDK methods to MCP tools
4. **AI optimization pass** → Use Claude API to optimize tool descriptions
5. **Generate MCP server code** → TypeScript server using FastMCP + SDK
6. **Validation** → Test MCP server against live API
7. **Build** → Include MCP server in Docker image

---

## MCP Tool Design

### Core Tools (MVP)

| Tool Name | Description | Parameters | Returns |
|-----------|-------------|------------|---------|
| `get_financial_summary` | Get income/expense summary for a period | `start_date`, `end_date` | Total income, expenses, net, top categories |
| `get_expense_breakdown` | Break down expenses by category | `start_date`, `end_date`, `category?` | Category totals, percentages |
| `get_income_breakdown` | Break down income by source | `start_date`, `end_date`, `category?` | Source totals, percentages |
| `search_transactions` | Search transactions by various criteria | `query?`, `category?`, `min_amount?`, `max_amount?`, `start_date?`, `end_date?`, `limit?` | Transaction list (capped) |
| `get_account_balances` | Get current balances for all accounts | None | Account name, type, balance pairs |
| `get_cashflow_trend` | Get cash flow trend over time | `period` (monthly/weekly), `months` | Date/cashflow pairs |
| `get_spending_trend` | Get spending trend for a category | `category`, `period`, `months` | Date/amount pairs |
| `run_scenario_preview` | Preview a what-if scenario | `adjustments[]` | Baseline vs scenario comparison |

### MCP Resources (MVP)

| Resource URI | Description |
|--------------|-------------|
| `spearmint://accounts` | List of all financial accounts |
| `spearmint://categories` | List of all transaction categories |
| `spearmint://classifications` | List of classification types |
| `spearmint://recent-transactions` | Last 50 transactions (summary view) |

### MCP Prompts (MVP)

| Prompt Name | Description | Arguments |
|-------------|-------------|-----------|
| `monthly-summary` | Generate a monthly financial summary | `month`, `year` |
| `budget-check` | Check spending against typical patterns | `category` |
| `runway-analysis` | Analyze financial runway | `assumed_income_change?` |

---

## Security & Authentication

### Authentication Model

**Approach: API Key via HTTP Header**

Since the MCP server is exposed as HTTP endpoints, authentication uses standard HTTP headers:

```
┌─────────────────┐                    ┌─────────────────────────────────┐
│  AI Client      │     HTTP/SSE       │  Spearmint Container            │
│  (Claude,       │◄──────────────────►│                                 │
│   ChatGPT,      │  Authorization:    │  ┌─────────────────────────┐   │
│   Gemini)       │  Bearer <api-key>  │  │  MCP Endpoints          │   │
└─────────────────┘                    │  │  /mcp/sse               │   │
                                       │  │  /mcp/messages          │   │
                                       │  └────────────┬────────────┘   │
                                       │               │                 │
                                       │  ┌────────────▼────────────┐   │
                                       │  │  API Key Validation     │   │
                                       │  │  + Rate Limiting        │   │
                                       │  └─────────────────────────┘   │
                                       └─────────────────────────────────┘
```

### Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| **User Isolation** | Each MCP connection uses user-specific API key |
| **No Cross-User Access** | API key scoped to single user's data |
| **Secure Storage** | API keys stored hashed in database |
| **Key Rotation** | Users can regenerate keys from Settings |
| **Audit Logging** | Log all MCP queries with timestamps |
| **Read-Only Default** | MVP tools are read-only (no writes via MCP) |
| **Rate Limiting** | Limit requests per minute per API key |

### API Key Management

**New Backend Endpoints:**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/auth/api-keys` | Generate new API key |
| `GET` | `/api/auth/api-keys` | List user's API keys (masked) |
| `DELETE` | `/api/auth/api-keys/{id}` | Revoke an API key |

**API Key Format:**
```
smint_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Token Optimization Strategies

AI models have context limits. Financial data can be verbose. We need strategies to minimize token usage while preserving information.

### Strategy 1: Summarization Transforms

**Instead of returning:**
```json
{
  "transactions": [
    {"id": 1, "date": "2026-01-15", "description": "AMAZON.COM PURCHASE", "amount": -45.99, "category": "Shopping", ...20 more fields...},
    // ... 100 more transactions
  ]
}
```

**Return:**
```json
{
  "summary": "Found 100 transactions totaling $3,450.22",
  "top_by_amount": [
    {"date": "2026-01-15", "desc": "Amazon", "amount": -45.99, "cat": "Shopping"},
    {"date": "2026-01-10", "desc": "Rent", "amount": -1800.00, "cat": "Housing"}
  ],
  "breakdown": {"Shopping": 12, "Housing": 1, "Food": 45, "Other": 42}
}
```

### Strategy 2: Smart Field Selection

Only return fields relevant to the query:
- Balance queries → account, balance, as_of_date
- Trend queries → date, value pairs only
- Search queries → date, description, amount, category only

### Strategy 3: Pagination with Context

```json
{
  "results": [...10 items...],
  "total_count": 150,
  "showing": "1-10",
  "next_page_hint": "Ask for more with 'show me more transactions' or 'get transactions page 2'"
}
```

### Strategy 4: Pre-computed Insights

For common queries, return pre-computed insights:
```json
{
  "monthly_summary": {
    "total_income": 5000,
    "total_expenses": 3500,
    "net_cashflow": 1500,
    "vs_last_month": "+5%",
    "insight": "Spending on dining out increased 23% this month"
  }
}
```

### Token Budget Guidelines

| Tool | Max Response Tokens | Strategy |
|------|---------------------|----------|
| `get_financial_summary` | 500 | Pre-computed summary |
| `search_transactions` | 1500 | Top 10 + pagination hint |
| `get_expense_breakdown` | 800 | Category totals only |
| `get_cashflow_trend` | 600 | Data points + trend description |
| `run_scenario_preview` | 1000 | Key deltas + recommendation |

---

## Installation & Distribution

### Bundled in Spearmint Container

The MCP server is **built into the Spearmint container** as a separate Node.js process. No separate installation required.

When users deploy Spearmint via Docker, the MCP endpoints are automatically available:
- `http://localhost:3001/sse` - SSE endpoint for MCP connections
- `http://localhost:3001/messages` - JSON-RPC message endpoint

**Port Configuration:**
| Service | Internal Port | Purpose |
|---------|---------------|---------|
| REST API | 8000 | Web app, SDK, direct API calls |
| MCP Server | 3001 | AI client connections |

Users can map these ports as needed in their `docker-compose.yml`:
```yaml
services:
  spearmint:
    image: spearmint/spearmint:latest
    ports:
      - "8000:8000"  # REST API
      - "3001:3001"  # MCP Server
```

### User Setup Flow

#### Step 1: Generate API Key

1. Open Spearmint web app
2. Navigate to **Settings → API Keys**
3. Click **"Generate New Key"**
4. Copy the key (shown once): `smint_live_abc123...`

#### Step 2: Configure AI Client

**Claude Desktop / Claude Code:**
```json
{
  "mcpServers": {
    "spearmint": {
      "url": "http://localhost:3001/sse",
      "headers": {
        "Authorization": "Bearer smint_live_abc123..."
      }
    }
  }
}
```

**Gemini CLI** (`~/.gemini/settings.json`):
```json
{
  "mcpServers": {
    "spearmint": {
      "httpUrl": "http://localhost:3001",
      "headers": {
        "Authorization": "Bearer smint_live_abc123..."
      }
    }
  }
}
```

**ChatGPT** (requires public URL):
1. Expose MCP server via tunnel: `ngrok http 3001`
2. In ChatGPT: Settings → Connectors → Add MCP
3. Enter URL: `https://abc123.ngrok.io/sse`
4. Add header: `Authorization: Bearer smint_live_abc123...`

#### Step 3: Test Connection

Ask your AI assistant: *"What's my account balance?"*

### One-Click Setup (Settings Page)

The Spearmint Settings page will provide:
- **Copy Config** button with pre-filled JSON for each platform
- **QR Code** for mobile setup (future)
- **Connection test** button to verify MCP is working

---

## Auto-Generation Pipeline

### Pipeline Integration

The MCP server generation integrates into the existing CI/CD pipeline, running after SDK generation:

```yaml
# Addition to .github/workflows/deploy-and-version.yml

# After build-sdk job completes...

generate-mcp-server:
  needs: build-sdk
  runs-on: ubuntu-latest
  steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Download SDK artifact
      uses: actions/download-artifact@v4
      with:
        name: typescript-sdk
        path: sdk/output/typescript/

    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'

    - name: Generate MCP tool definitions from SDK
      run: |
        node scripts/generate_mcp_tools.js \
          --sdk sdk/output/typescript/ \
          --output mcp-server/src/tools.json

    - name: AI optimization pass
      env:
        ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      run: |
        node scripts/optimize_mcp_tools.js \
          --input mcp-server/src/tools.json \
          --output mcp-server/src/tools.json

    - name: Build MCP server
      working-directory: mcp-server
      run: |
        npm ci
        npm run build

    - name: Test MCP server
      working-directory: mcp-server
      run: npm test

    - name: Upload MCP server artifact
      uses: actions/upload-artifact@v4
      with:
        name: mcp-server
        path: mcp-server/dist/
```

### MCP Server Implementation

The MCP server is a TypeScript application using FastMCP and the Spearmint SDK:

**Project Structure:**
```
mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts          # Entry point, starts HTTP server
│   ├── server.ts         # FastMCP server configuration
│   ├── tools/
│   │   ├── index.ts      # Tool registry
│   │   ├── financial.ts  # Financial summary tools
│   │   ├── transactions.ts # Transaction search tools
│   │   └── accounts.ts   # Account balance tools
│   ├── utils/
│   │   └── tokenOptimizer.ts  # Response optimization
│   └── tools.json        # AI-optimized tool definitions (generated)
└── tests/
    └── tools.test.ts
```

**Example Tool Implementation:**
```typescript
// mcp-server/src/tools/financial.ts

import { FastMCP } from 'fastmcp';
import { SpearmintClient } from '@spearmint/sdk';
import { optimizeForTokens } from '../utils/tokenOptimizer';
import toolDefinitions from '../tools.json';

export function registerFinancialTools(mcp: FastMCP, client: SpearmintClient) {

  // Tool: get_financial_summary
  mcp.tool(
    'get_financial_summary',
    toolDefinitions.get_financial_summary,  // AI-optimized description
    async ({ start_date, end_date }) => {
      const summary = await client.reports.getSummary({
        startDate: start_date,
        endDate: end_date,
      });

      // Optimize response for token efficiency
      return optimizeForTokens({
        total_income: summary.totalIncome,
        total_expenses: summary.totalExpenses,
        net_cashflow: summary.netCashflow,
        top_expense_categories: summary.topCategories.slice(0, 5),
        insight: generateInsight(summary),
      });
    }
  );

  // Tool: get_expense_breakdown
  mcp.tool(
    'get_expense_breakdown',
    toolDefinitions.get_expense_breakdown,
    async ({ start_date, end_date, category }) => {
      const breakdown = await client.reports.getExpenseBreakdown({
        startDate: start_date,
        endDate: end_date,
        category,
      });

      return optimizeForTokens(breakdown);
    }
  );
}
```

**Server Entry Point:**
```typescript
// mcp-server/src/index.ts

import { FastMCP } from 'fastmcp';
import { SpearmintClient } from '@spearmint/sdk';
import { registerFinancialTools } from './tools/financial';
import { registerTransactionTools } from './tools/transactions';
import { registerAccountTools } from './tools/accounts';

const API_URL = process.env.SPEARMINT_URL || 'http://localhost:8000';

async function main() {
  const mcp = new FastMCP('spearmint');

  // Create SDK client (API key passed per-request via MCP auth)
  const createClient = (apiKey: string) => new SpearmintClient({
    baseUrl: API_URL,
    apiKey,
  });

  // Register tools with auth middleware
  mcp.use(async (req, next) => {
    const apiKey = req.headers.authorization?.replace('Bearer ', '');
    if (!apiKey) throw new Error('API key required');

    req.client = createClient(apiKey);
    return next();
  });

  registerFinancialTools(mcp);
  registerTransactionTools(mcp);
  registerAccountTools(mcp);

  // Start HTTP/SSE server
  await mcp.serve({
    transport: 'http',
    port: parseInt(process.env.MCP_PORT || '3001'),
  });

  console.log('MCP server running on port 3001');
}

main().catch(console.error);
```

### AI Optimization Script

Uses Claude to improve tool descriptions for better AI comprehension:

```typescript
// scripts/optimize_mcp_tools.js

import Anthropic from '@anthropic-ai/sdk';
import fs from 'fs';

const client = new Anthropic();

async function optimizeToolDescription(tool) {
  const response = await client.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1000,
    messages: [{
      role: 'user',
      content: `
        Rewrite this MCP tool description to be optimal for an AI assistant.

        Current tool:
        ${JSON.stringify(tool, null, 2)}

        Requirements:
        1. Description should explain WHEN to use this tool (not just what it does)
        2. Parameter descriptions should include examples
        3. Add a "usage_hint" field with a sample user query
        4. Keep total description under 200 tokens

        Return the improved tool definition as JSON only.
      `
    }]
  });

  return JSON.parse(response.content[0].text);
}

async function main() {
  const inputFile = process.argv[2];
  const outputFile = process.argv[3];

  const tools = JSON.parse(fs.readFileSync(inputFile, 'utf-8'));

  const optimized = await Promise.all(
    Object.entries(tools).map(async ([name, tool]) => {
      const improved = await optimizeToolDescription({ name, ...tool });
      return [name, improved];
    })
  );

  fs.writeFileSync(outputFile, JSON.stringify(Object.fromEntries(optimized), null, 2));
  console.log(`Optimized ${optimized.length} tool descriptions`);
}

main();
```

### Generator: SDK → MCP Tools

Generates MCP tool definitions by analyzing the SDK's TypeScript types:

```typescript
// scripts/generate_mcp_tools.js

import ts from 'typescript';
import fs from 'fs';
import path from 'path';

/**
 * Analyzes the SDK source to extract method signatures
 * and generate corresponding MCP tool definitions.
 */
function generateToolsFromSDK(sdkPath: string): Record<string, ToolDefinition> {
  const tools = {};

  // Parse SDK client classes
  const clientFile = path.join(sdkPath, 'src/client.ts');
  const sourceFile = ts.createSourceFile(
    clientFile,
    fs.readFileSync(clientFile, 'utf-8'),
    ts.ScriptTarget.Latest
  );

  // Extract methods and their parameter types
  // Map to MCP tool definitions
  // ... (implementation details)

  return tools;
}

// Example output:
// {
//   "get_financial_summary": {
//     "description": "Get financial summary for a date range",
//     "inputSchema": {
//       "type": "object",
//       "properties": {
//         "start_date": { "type": "string" },
//         "end_date": { "type": "string" }
//       },
//       "required": ["start_date", "end_date"]
//     }
//   }
// }
```

### Docker Integration

The Dockerfile builds both the API and MCP server:

```dockerfile
# Dockerfile

# Stage 1: Build MCP server
FROM node:20-alpine AS mcp-builder
WORKDIR /mcp
COPY mcp-server/package*.json ./
RUN npm ci
COPY mcp-server/ ./
RUN npm run build

# Stage 2: Build Python API
FROM python:3.11-slim AS api-builder
WORKDIR /app
COPY core-api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY core-api/ ./

# Stage 3: Final image
FROM python:3.11-slim
WORKDIR /app

# Install Node.js runtime for MCP server
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Copy Python API
COPY --from=api-builder /app /app
COPY --from=api-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy MCP server
COPY --from=mcp-builder /mcp/dist /app/mcp-server
COPY --from=mcp-builder /mcp/node_modules /app/mcp-server/node_modules

# Install process manager
RUN npm install -g pm2

# Copy startup script
COPY scripts/start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000 3001

CMD ["/app/start.sh"]
```

**Startup Script:**
```bash
#!/bin/bash
# scripts/start.sh

# Start MCP server in background
pm2 start /app/mcp-server/index.js --name mcp-server

# Start FastAPI (foreground)
uvicorn src.financial_analysis.api.main:app --host 0.0.0.0 --port 8000
```

---

## Open Questions

### Q1: Should we support write operations?

**Options:**
- **Read-only (MVP):** Safer, simpler, covers 90% of use cases
- **Write with confirmation:** Allow creates/updates but require confirmation
- **Full read/write:** Maximum capability, higher risk

**Recommendation:** Start read-only, add writes in v2 with explicit user confirmation flow.

---

### Q2: How do we handle multi-user Spearmint instances?

**Context:** Spearmint supports multiple users sharing a ledger (family finances).

**Options:**
- **One API key per user:** Each user generates their own key
- **Shared API key with user header:** Single key, pass user context
- **User switcher in MCP:** Let AI switch between user contexts

**Recommendation:** One API key per user for MVP. Clear isolation, simple mental model.

---

### Q3: How do we handle Spearmint instances behind VPN/Tailscale?

**Context:** Many users run Spearmint on home servers accessible via Tailscale.

**Options:**
- **Direct connection:** User configures Tailscale URL in MCP config
- **Tunnel service:** Provide a secure tunnel (like ngrok) for users
- **Cloud relay:** Spearmint provides optional cloud relay (privacy tradeoff)

**Recommendation:** Document Tailscale setup; user configures their Tailscale domain in the AI client. No cloud relay in MVP (preserves self-hosted ethos).

---

### ~~Q4: Which MCP transport to support?~~ (RESOLVED)

**Decision:** HTTP/SSE only.

**Rationale:**
- Universal compatibility (Claude, ChatGPT, Gemini all support HTTP)
- ChatGPT does not support stdio (remote-only)
- Simpler architecture with single transport
- Bundled deployment in container

---

### Q4: How do we handle API spec changes that break MCP clients?

**Context:** If we change an API endpoint, existing MCP server versions may break.

**Options:**
- **Semver for MCP package:** Breaking changes = major version bump
- **API versioning:** `/api/v1/` vs `/api/v2/`
- **Graceful degradation:** MCP server handles missing endpoints gracefully

**Recommendation:** Semver for MCP package + graceful degradation (return helpful error if endpoint missing).

---

### ~~Q6: Should we build a custom MCP generator or use/contribute to existing tools?~~ (RESOLVED)

**Decision:** Custom generator that reads SDK types and generates MCP tool definitions.

**Rationale:**
- FastMCP (TypeScript) for MCP protocol handling
- Custom script to map SDK methods → MCP tools
- AI optimization pass for descriptions
- Maintains SDK as source of truth

---

## Technical Constraints

1. **TypeScript implementation:** MCP server written in TypeScript using FastMCP library
2. **SDK-based:** MCP server uses `@spearmint/sdk` for all API interactions
3. **HTTP/SSE transport:** FastMCP handles Server-Sent Events
4. **Bundled in container:** MCP server runs as separate Node.js process in same container
5. **Process manager:** Use pm2 or supervisord to manage both Python API and Node.js MCP processes
6. **Offline capable:** MCP server works without internet (connects to local API)
7. **Port allocation:** API on port 8000, MCP on port 3001 (internal to container)

---

## Out of Scope (Future Iterations)

- Write operations (create/update transactions)
- Multi-turn conversations with memory
- Proactive notifications/alerts
- Voice integration (beyond what AI client provides)
- Custom prompt library management
- MCP marketplace listing
- Enterprise SSO integration

---

## Implementation Phases

### Phase 1: Foundation (MVP)

**Deliverables:**
- [ ] API key generation endpoint in FastAPI backend
- [ ] API key management UI in Settings page
- [ ] MCP server project scaffolding (`mcp-server/`)
- [ ] 5 core MCP tools using SDK (hand-written)
- [ ] Docker integration (multi-process container)
- [ ] Documentation for Claude Desktop, Gemini CLI, and ChatGPT setup

**Tools in scope:**
- `get_financial_summary` → `client.reports.getSummary()`
- `get_expense_breakdown` → `client.reports.getExpenseBreakdown()`
- `search_transactions` → `client.transactions.search()`
- `get_account_balances` → `client.accounts.list()` + balances
- `get_cashflow_trend` → `client.reports.getCashflow()`

### Phase 2: Auto-Generation Pipeline

**Deliverables:**
- [ ] SDK → MCP tool generator script (`generate_mcp_tools.js`)
- [ ] AI optimization script (`optimize_mcp_tools.js`)
- [ ] CI/CD integration (generate after SDK build)
- [ ] Automated MCP server tests
- [ ] Integration with existing `deploy-and-version.yml` workflow

### Phase 3: Optimization & Expansion

**Deliverables:**
- [ ] Token optimization utilities (`tokenOptimizer.ts`)
- [ ] Additional tools (scenarios, trends, projections)
- [ ] MCP resources (`spearmint://accounts`, etc.)
- [ ] MCP prompts (pre-built templates)
- [ ] Response caching for common queries

### Phase 4: Polish & Documentation

**Deliverables:**
- [ ] Comprehensive user documentation (setup guides per platform)
- [ ] Video setup guide
- [ ] Settings page "Copy Config" buttons for each AI platform
- [ ] Connection test button in Settings
- [ ] Usage analytics (opt-in)
- [ ] Error handling and graceful degradation

---

## Success Criteria Checklist

Before marking this feature "complete," we must validate:

**Core Functionality:**
- [ ] MCP HTTP/SSE endpoints respond at `/mcp/sse` and `/mcp/messages`
- [ ] User can generate API key in Spearmint Settings
- [ ] API key authentication works for MCP endpoints
- [ ] All 5 MVP tools return accurate data

**Platform Compatibility:**
- [ ] Claude Desktop connects and queries successfully
- [ ] Gemini CLI connects and queries successfully
- [ ] ChatGPT connects via ngrok tunnel and queries successfully

**User Experience:**
- [ ] User can connect Claude Desktop to Spearmint in <5 minutes
- [ ] User can ask "What did I spend on groceries last month?" and get accurate answer
- [ ] User can search transactions via natural language
- [ ] Settings page has "Copy Config" buttons for each platform

**Technical Quality:**
- [ ] MCP endpoints auto-generate when API spec changes
- [ ] Average response uses <2000 tokens
- [ ] No security incidents from MCP access
- [ ] Documentation covers Claude, Gemini, and ChatGPT setup
- [ ] MCP endpoints work with Tailscale/VPN setups

---

## Appendix A: MCP Protocol Reference

**Official Documentation:** https://modelcontextprotocol.io/

**Key Concepts:**
- **Server:** Provides tools, resources, and prompts to AI clients
- **Client:** AI application (Claude Desktop, etc.) that connects to servers
- **Transport:** Communication layer (stdio, HTTP+SSE)
- **Tool:** A function the AI can call with parameters
- **Resource:** Data the AI can read (like a file or database query)
- **Prompt:** A pre-defined template for common interactions

---

## Appendix B: Platform Configuration Examples

### Claude Desktop / Claude Code

**Configuration file locations:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "spearmint": {
      "url": "http://localhost:3001/sse",
      "headers": {
        "Authorization": "Bearer smint_live_abc123..."
      }
    }
  }
}
```

### Gemini CLI

**Configuration file:** `~/.gemini/settings.json`

```json
{
  "mcpServers": {
    "spearmint": {
      "httpUrl": "http://localhost:3001",
      "headers": {
        "Authorization": "Bearer smint_live_abc123..."
      }
    }
  }
}
```

### ChatGPT (Developer Mode)

ChatGPT requires a publicly accessible URL. Use a tunnel service:

```bash
# Option 1: ngrok (tunnel the MCP port)
ngrok http 3001
# Creates URL like: https://abc123.ngrok.io

# Option 2: Cloudflare Tunnel
cloudflared tunnel --url http://localhost:3001
# Creates URL like: https://xyz789.trycloudflare.com
```

Then in ChatGPT:
1. Settings → Connectors → Advanced → Developer Mode
2. Add new MCP connector:
   - URL: `https://abc123.ngrok.io/sse`
   - Header: `Authorization: Bearer smint_live_abc123...`

### With Tailscale (Remote Access)

If running Spearmint on a home server with Tailscale:

```json
{
  "mcpServers": {
    "spearmint": {
      "url": "http://my-server.tail1234.ts.net:3001/sse",
      "headers": {
        "Authorization": "Bearer smint_live_abc123..."
      }
    }
  }
}
```

---

## Appendix C: Competitive Landscape

| Product | MCP Support | Notes |
|---------|-------------|-------|
| Mint (defunct) | None | No longer operational |
| YNAB | None | No AI integration |
| Copilot (finance) | None | No API access |
| Monarch Money | None | No self-hosted option |
| Actual Budget | None | Self-hosted, no MCP |
| **Spearmint** | **Planned** | **First self-hosted PFM with MCP** |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-02-02 | Product Team | Initial draft for collaborative review |
| 0.2 | 2026-02-02 | Product Team | Decision: HTTP/SSE only (no stdio), bundled in container |
| 0.3 | 2026-02-02 | Product Team | Decision: SDK-based architecture (TypeScript MCP server using SDK) |
| 0.4 | 2026-02-02 | Product Team | Finalized: MVP tools, token optimization (best effort), AI auto-optimization, pm2 |

---

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Transport** | HTTP/SSE only | Universal platform support (ChatGPT requires remote HTTP) |
| **Deployment** | Bundled in container | Simpler for users, no separate install |
| **Implementation** | TypeScript + SDK | Consistent with CLI architecture; decoupled from backend |
| **API Integration** | Via SDK, not direct | SDK handles auth, types, retries; portable if backend language changes |
| **MCP Library** | FastMCP (TypeScript) | MIT licensed, well-maintained, HTTP transport support |
| **Token Optimization** | Best effort | Implement summarization/field selection as time allows |
| **MVP Tools** | 5 tools approved | get_financial_summary, get_expense_breakdown, search_transactions, get_account_balances, get_cashflow_trend |
| **AI Optimization** | Auto in CI/CD | Claude optimizes tool descriptions automatically during build |
| **Process Manager** | pm2 | Node.js native, simpler than supervisord, good logging |

---

## Implementation Plan (Phase 1)

This section details the specific implementation approach for the codebase.

### Implementation Order

1. **Backend: Database Model** - Add APIKey model
2. **Backend: Service + Routes** - Auth service and API endpoints
3. **Frontend: API Keys Tab** - Settings UI for key management
4. **MCP Server: Scaffolding** - New TypeScript project
5. **MCP Server: Tools** - 5 core tools using SDK
6. **Docker: Integration** - Add mcp-server service (separate container)
7. **Documentation** - Setup guides

### Backend Changes

#### 1. Database Model (`core-api/src/financial_analysis/database/models.py`)

Add `APIKey` class:

```python
class APIKey(Base):
    """API keys for MCP server authentication."""
    __tablename__ = "api_keys"

    key_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)  # e.g., "Claude Desktop"
    key_prefix = Column(String(12), nullable=False)  # "smint_live_" + first 4 chars
    key_hash = Column(String(128), nullable=False)  # SHA-256 hash
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    expires_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index('idx_api_key_hash', 'key_hash'),
        Index('idx_api_key_active', 'is_active'),
    )
```

#### 2. New Files to Create

| File | Purpose |
|------|---------|
| `api/schemas/auth.py` | Pydantic schemas: APIKeyCreate, APIKeyResponse, APIKeyCreatedResponse |
| `services/auth_service.py` | AuthService class with key generation, validation, revocation |
| `api/routes/auth.py` | Router with POST/GET/DELETE endpoints |

#### 3. API Endpoints

```
POST   /api/auth/api-keys     → Generate new key (returns full key once)
GET    /api/auth/api-keys     → List keys (masked)
DELETE /api/auth/api-keys/{id} → Revoke key
```

#### 4. Register Router (`api/main.py`)

```python
from .routes import auth
app.include_router(auth.router, prefix="/api", tags=["auth"])
```

### Frontend Changes

#### New Files

| File | Purpose |
|------|---------|
| `types/auth.ts` | TypeScript interfaces for API keys |
| `api/auth.ts` | API client functions |
| `hooks/useApiKeys.ts` | React Query hooks for key management |
| `components/Settings/APIKeysManagement.tsx` | UI component for key management |

#### Update Settings Page (`components/Settings/SettingsPage.tsx`)

- Add `VpnKey` icon import
- Add 4th tab "API Keys" at index 3
- Add TabPanel with `<APIKeysManagement />`

#### UI Features

- List existing keys (masked: `smint_live_xxxx...`)
- "Generate New Key" button with name input dialog
- One-time full key display with copy button
- "Copy Config" buttons for Claude/Gemini/ChatGPT
- Revoke button with confirmation

### MCP Server Structure

Create directory `mcp-server/`:

```
mcp-server/
├── package.json
├── tsconfig.json
├── Dockerfile
├── src/
│   ├── index.ts           # Entry point, HTTP server
│   ├── server.ts          # FastMCP configuration
│   ├── middleware/
│   │   └── auth.ts        # API key validation
│   ├── tools/
│   │   ├── index.ts       # Tool registry
│   │   ├── financial.ts   # get_financial_summary
│   │   ├── expenses.ts    # get_expense_breakdown
│   │   ├── transactions.ts # search_transactions
│   │   ├── accounts.ts    # get_account_balances
│   │   └── cashflow.ts    # get_cashflow_trend
│   └── utils/
│       └── tokenOptimizer.ts
└── tests/
```

#### Dependencies

```json
{
  "dependencies": {
    "@spearmint-finance/sdk": "^0.0.15",
    "fastmcp": "^1.0.0"
  }
}
```

### Docker Integration

**Approach:** Separate containers for development. Can consolidate with pm2 later for production.

Add to `docker-compose.yml`:

```yaml
  mcp-server:
    build: ./mcp-server
    ports:
      - "3001:3001"
    environment:
      - SPEARMINT_API_URL=http://core-api:8000
      - MCP_PORT=3001
    depends_on:
      - core-api
```

### Verification Steps

1. **Backend:** `curl -X POST http://localhost:8000/api/auth/api-keys -H "Content-Type: application/json" -d '{"name": "Test"}'`
2. **Frontend:** Navigate to Settings → API Keys, generate and copy config
3. **MCP Server:** `curl http://localhost:3001/sse -H "Authorization: Bearer smint_live_xxx"`
4. **E2E:** Configure Claude Desktop and ask "What's my financial summary?"

---

## Open Feedback Requested

~~1. **Token optimization strategies** - Which approaches to prioritize?~~ → **Best effort; implement as time allows**

~~2. **MVP tool selection** - Are the 5 proposed SDK-mapped tools the right ones?~~ → **Approved**

3. **ChatGPT tunnel documentation** - How detailed should setup instructions be?

~~4. **AI optimization in pipeline** - Should Claude optimize tool descriptions automatically?~~ → **Yes, auto-optimize in CI/CD**

~~5. **Process management** - pm2 vs supervisord for container?~~ → **pm2 (simpler, Node.js native)**
