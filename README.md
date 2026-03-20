# Spearmint — Personal CFO for Your Household

[![npm version](https://img.shields.io/npm/v/@spearmint-finance/sdk)](https://www.npmjs.com/package/@spearmint-finance/sdk)

**Business-class finance for the household.** Spearmint is a free, self-hosted financial engine that treats your household like a business — separating operating costs from capital investments, tracking multiple entities, and providing professional-grade reporting. No subscriptions, no cloud dependency, your data stays on your hardware.

> *"Most apps tell you what you spent. Spearmint tells you what you're building."*

## Why Spearmint?

| Feature | Spearmint | Monarch ($15/mo) | YNAB ($15/mo) | Firefly III | Actual Budget |
|---------|-----------|-------------------|---------------|-------------|---------------|
| Self-hosted & free | Yes | No | No | Yes | Yes |
| CapEx/OpEx separation | **Yes** | No | No | No | No |
| Multi-entity accounting | **Yes** | No | No | No | No |
| 7 report types | **Yes** | Partial | No | Partial | No |
| AI financial assistant | **Yes** | No | No | No | No |
| Investment tracking | Yes | Yes | No | No | No |
| Transaction rules engine | Yes | Yes | Partial | Yes | No |
| Forecasting & projections | Yes | Partial | No | No | No |

## Key Features

### The "Renovation Moment" — CapEx/OpEx Separation
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

### Smart Automation
- **Categorization Rules** — Pattern matching on description, source, amount, payment method
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

## Quick Start

### Docker (Recommended)

```bash
git clone https://github.com/spearmint-finance/spearmint.git
cd spearmint
docker-compose up -d
```

Open http://localhost:5173 in your browser.

### Local Development

```bash
# One-command setup
./scripts/setup-local-dev.sh    # Linux/macOS
.\scripts\setup-local-dev.ps1  # Windows

# Start servers
# Terminal 1 — Backend (http://localhost:8000)
cd core-api && python run_api.py

# Terminal 2 — Frontend (http://localhost:5173)
cd web-app && npm run dev
```

## Project Structure

```
spearmint/
├── core-api/           # FastAPI backend (Python)
├── web-app/            # React frontend (TypeScript)
├── sdk/                # Generated TypeScript SDK
├── api-gateway/        # API gateway
├── marketing-site/     # Next.js marketing site
├── product/            # PRDs, roadmap, competitive analysis
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

Spearmint is in active development. Core financial tracking, analysis, and reporting are production-ready. See the [product roadmap](product/PRIORITIZED-ROADMAP.md) for what's next.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper testing
4. Submit a pull request

See [LOCAL_DEVELOPMENT_QUICKSTART.md](docs/LOCAL_DEVELOPMENT_QUICKSTART.md) for development setup details.

## License

MIT

## Author

Harry Mower
