# Spearmint — Personal CFO for Your Household

[![npm version](https://img.shields.io/npm/v/@spearmint-finance/sdk)](https://www.npmjs.com/package/@spearmint-finance/sdk)

**Business-class finance for the household.** Spearmint is a free, self-hosted financial engine that treats your household like a business — separating operating costs from capital investments, tracking multiple entities, and providing professional-grade reporting. No subscriptions, no cloud dependency, your data stays on your hardware.

> *"Most apps tell you what you spent. Spearmint tells you what you're building."*

## Key Features

### CapEx/OpEx Separation
A $15,000 kitchen remodel isn't the same as a grocery bill. Toggle "Capital Expenditure" on a transaction and it moves from Operating Expenses to Asset Investment. Your monthly burn rate drops from $18,000 to $3,000 — your actual living expenses.

### Multi-Entity Accounting
Manage personal, business, and rental property finances in one place. Each entity gets its own P&L, cash flow, and net worth — with a consolidated view across all entities.

### Professional Reporting
- **Balance Report** — Assets vs. liabilities over time
- **Income & Expense Detail** — Category-level breakdown
- **Cash Flow** — Waterfall analysis with transfer exclusions
- **CapEx Report** — Capital investment tracking
- **Receivables** — Outstanding reimbursements owed to you
- **Reconciliation** — Statement vs. calculated balance verification
- **Summary** — Key financial indicators at a glance

### Transaction Splits
Split a single transaction across multiple categories, entities, and people. "Split Evenly" distributes amounts automatically. Each split row can be assigned to a different entity — track shared household expenses at the per-person level.

### Category Management
Full category CRUD with hierarchy support, entity-scoped categories, search, type/entity filters, and inline editing. Categories automatically scope to the active entity — your "Business Travel" category stays out of your personal budget.

### Smart Automation
- **Transaction Rules** — Pattern matching on description, source, amount, payment method. Auto-assign categories and entities.
- **Classification Rules** — Auto-exclude transfers, reimbursements, and internal transactions
- **Transaction Relationships** — Detect transfer pairs, credit card payments, reimbursements, dividend reinvestments

### AI Financial Assistant
Built-in chat assistant with action execution — ask questions about your finances, get insights, and let the AI help categorize and classify transactions.

### Data Pipeline
1. **Import** — CSV upload with saved import profiles (system remembers your bank's format)
2. **Clean** — Automatic deduplication
3. **Classify** — Rules engine assigns categories and classifications
4. **Verify** — Review uncategorized items
5. **Report** — Data flows into dashboards, analysis, and forecasts

## Getting Started

### Prerequisites

- **Docker** (recommended): Docker Engine 20+ and Docker Compose v2+
- **Local dev**: Python 3.10+, Node.js 18+, npm 9+

### Option 1: Docker Compose (Recommended)

```bash
git clone https://github.com/spearmint-finance/spearmint.git
cd spearmint
cp .env.example .env        # optional — customize ports
docker-compose up -d
```

This starts the full stack:

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:7173 | Main application UI |
| API Gateway | http://localhost:7080 | Entry point for all API calls |
| API Docs (Swagger) | http://localhost:7080/api/docs | Interactive API documentation |
| MCP Server | http://localhost:7001 | AI assistant integration |

Data is persisted in a Docker volume (`database/data/`). To start fresh, run `docker-compose down -v`.

#### Customizing Ports

Edit `.env` to change default ports (useful if you have other services running):

```bash
GATEWAY_PORT=8080
WEB_PORT=5173
MCP_PORT=3001
DB_PORT=5432
```

#### AI Assistant (Optional)

To enable the AI financial assistant, add your API key to `.env`:

```bash
OPENAI_KEY=sk-...        # OpenAI
# or
ANTHROPIC_KEY=sk-ant-... # Anthropic
```

The assistant works without these keys — it just won't be able to generate responses.

### Option 2: Local Development

```bash
git clone https://github.com/spearmint-finance/spearmint.git
cd spearmint

# One-command setup (installs Python + Node dependencies)
./scripts/setup-local-dev.sh    # Linux/macOS
.\scripts\setup-local-dev.ps1  # Windows
```

Then start both servers:

```bash
# Terminal 1 — Backend
cd core-api
python run_api.py              # http://localhost:8000

# Terminal 2 — Frontend
cd web-app
npm run dev                    # http://localhost:5173
```

The backend creates a SQLite database automatically on first run — no migration step needed.

#### Verify It's Working

1. Open http://localhost:5173 (local) or http://localhost:7173 (Docker)
2. You should see an empty dashboard
3. Navigate to **Accounts** → **Add Account** to create your first account
4. Go to **Transactions** → **Import** to upload a bank CSV

See [docs/LOCAL_DEVELOPMENT_QUICKSTART.md](docs/LOCAL_DEVELOPMENT_QUICKSTART.md) for detailed setup and troubleshooting.

## Project Structure

```
spearmint/
├── core-api/           # FastAPI backend (Python)
├── web-app/            # React frontend (TypeScript)
├── sdk/                # Generated TypeScript SDK
├── api-gateway/        # API gateway
├── marketing-site/     # Next.js marketing site
├── docker-compose.yml  # One-command deployment
└── docs/               # Architecture & API docs
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy 2.0, Python 3.10+ |
| Frontend | React 18, TypeScript 5, Material-UI v5, Vite |
| Charts | Recharts |
| State | TanStack Query |
| Database | SQLite (dev) / PostgreSQL (prod) |
| AI | LLM-powered assistant with A2A agent protocol |

## API Documentation

- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

## Current Status

Spearmint is in active development. Core financial tracking, analysis, and reporting are production-ready. See the [roadmap](product/PRIORITIZED-ROADMAP.md) for what's next.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions and guidelines.

## Disclaimer

Spearmint is a tracking and reporting tool — **not a financial advisor**. It may contain bugs that affect calculations. Do not rely solely on this software for financial decisions. Always verify against your bank statements and consult a qualified professional for financial, tax, or legal advice. See [DISCLAIMER.md](DISCLAIMER.md) for full details.

## License

PolyForm Noncommercial — free for personal use, contributions welcome, no commercial use. See [LICENSE](LICENSE).

## Author

Harry Mower
