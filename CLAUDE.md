# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A full-stack financial analysis application that imports Excel transaction data, automatically classifies transactions, and provides income/expense analysis, cash flow tracking, and financial projections.

**Key Concept:** The application has a **dual-view system**:
- **Analysis View** - Excludes transfers/internal transactions for accurate financial calculations
- **Complete View** - Shows all transactions for reconciliation and auditing

## Workflow Status

✅ **Pre-commit hooks** - Integrated
✅ **API validation** - Full pipeline (Structural + Spectral + Postman Governance)
✅ **CI/CD pipeline** - Automated deployment and versioning
✅ **Postman integration** - SDK generation, collection creation, spec publishing with retry logic

## Tech Stack

**Backend:**
- FastAPI (Python 3.10+) with SQLAlchemy 2.0+ ORM
- SQLite database (development)
- Pandas/NumPy for data processing
- Statistical libraries: scipy, statsmodels, scikit-learn

**Frontend:**
- React 18+ with TypeScript 5+
- Material-UI (MUI) v5 components
- TanStack Query (React Query) for server state
- Recharts for visualizations
- React Router v6 for navigation

## Development Commands

### Backend

```bash
# Start backend API server (runs on http://localhost:8000)
cd core-api
source venv/bin/activate                # Linux/Mac
# OR: .\venv\Scripts\Activate.ps1       # Windows PowerShell
python -m uvicorn src.financial_analysis.api.main:app --reload --port 8000

# Run backend tests
cd core-api
source venv/bin/activate
pytest tests/ -v
pytest tests/ --cov=src

# Initialize database
cd core-api
source venv/bin/activate
python -m src.financial_analysis.database.init_db
```

### Frontend

```bash
# Start frontend dev server (runs on http://localhost:5173)
cd web-app
npm run dev

# Build for production
cd web-app
npm run build

# Run linting
cd web-app
npm run lint

# Run E2E tests
cd web-app
npm run test:e2e
npm run test:e2e:ui        # Interactive UI mode
npm run test:e2e:headed    # Run with visible browser
npm run test:e2e:debug     # Debug mode
```

### Full Stack Development

Run both servers in separate terminals:
- **Terminal 1:** `cd core-api && source venv/bin/activate && python -m uvicorn src.financial_analysis.api.main:app --reload --port 8000`
- **Terminal 2:** `cd web-app && npm run dev`

## Architecture Overview

### Backend Structure

```
core-api/
├── src/financial_analysis/
│   ├── api/
│   │   ├── main.py              # FastAPI app with CORS, error handlers, middleware
│   │   ├── routes/              # API route handlers (8 router modules)
│   │   │   ├── transactions.py
│   │   │   ├── analysis.py
│   │   │   ├── classifications.py
│   │   │   ├── projections.py
│   │   │   ├── reports.py
│   │   │   └── ...
│   │   └── schemas/             # Pydantic validation models
│   ├── database/
│   │   ├── models.py            # SQLAlchemy ORM models
│   │   ├── views.py             # Database views for complex queries
│   │   └── init_db.py           # Database initialization
│   ├── services/                # Business logic layer
│   │   ├── import_service.py    # Excel import & validation
│   │   ├── classification_service.py  # Auto-classification engine
│   │   ├── analysis_service.py  # Income/expense/cash flow analysis
│   │   ├── projection_service.py # Statistical forecasting
│   │   └── transaction_service.py
│   └── utils/                   # Utility functions
└── venv/                        # Python virtual environment
```

### Frontend Structure

```
web-app/src/
├── components/
│   ├── common/              # Layout, Header, Sidebar
│   ├── Dashboard/
│   ├── Transactions/
│   ├── Analysis/            # Income/Expense deep-dive pages
│   ├── Classifications/     # Classification management UI
│   ├── Projections/
│   ├── Import/
│   └── Settings/
├── api/                     # Axios API client & endpoints
├── hooks/                   # Custom React hooks (useClassifications, etc.)
├── types/                   # TypeScript type definitions
└── theme.ts                 # Material-UI theme config
```

## Core Database Models

**Transaction** - Core financial transaction record
- Fields: transaction_date, amount, transaction_type (Income/Expense), category_id, classification_id
- Relationships: belongs to Category, TransactionClassification
- Indexes on: date, type, category_id, classification_id

**TransactionClassification** - Transaction classification types (13 system classifications)
- Fields: classification_name, classification_code, exclude_from_income_calc, exclude_from_expense_calc, exclude_from_cashflow_calc
- Examples: "Regular Transaction", "Internal Transfer", "Credit Card Payment", "Refund/Return"

**Category** - Hierarchical transaction categories
- Fields: category_name, category_type (Income/Expense/Both), parent_category_id
- Self-referential relationship for hierarchy

**ClassificationRule** - Pattern-based auto-classification rules
- Fields: rule_name, classification_id, pattern_type, pattern_value, priority
- Used to automatically classify transactions on import

## Key Services

### ImportService (`import_service.py`)
- Parses Excel files with openpyxl
- Validates transaction data with Pydantic
- Automatically applies classification rules
- Deduplicates transactions
- Returns import summary with statistics

### ClassificationService (`classification_service.py`)
- Applies pattern-based classification rules
- Detects transaction relationships (transfers, CC payments)
- Links related transactions
- Manages classification rules CRUD

### AnalysisService (`analysis_service.py`)
- **CRITICAL:** All analysis methods filter `is_transfer=False` by default to prevent double-counting
- Methods: `get_income_analysis()`, `get_expense_analysis()`, `get_income_trends()`, `get_expense_trends()`
- Supports view mode toggle (analysis vs complete)
- Groups by category, calculates totals, averages, counts
- Time period aggregation (daily, weekly, monthly, quarterly, yearly)

### ProjectionService (`projection_service.py`)
- Statistical forecasting with multiple methods (Linear Regression, Moving Average, ARIMA)
- Short/medium/long-term projections with confidence intervals
- Classification-aware data preparation

## Important Implementation Details

### Transfer Filtering
**CRITICAL:** When working with income/expense analysis, transfers MUST be excluded to prevent double-counting. The `AnalysisService` methods have `is_transfer=False` filters:

```python
# In analysis_service.py
def get_income_analysis(self, ...):
    query = query.filter(Transaction.is_transfer == False)  # CRITICAL
```

### Classification System
The system has 13 standard classification types that control which transactions are included in financial calculations:

1. **Regular Transaction** - Normal income/expenses (included in all calculations)
2. **Internal Transfer** - Between own accounts (excluded from all calculations)
3. **Refund/Return** - Money back (excluded from expense calc)
4. **Credit Card Reward** - Cashback/points (may exclude from income)
5. **Work Reimbursement** - Employer reimbursements
6. **Insurance Reimbursement** - Insurance claims
7. **Investment Distribution** - Dividends/capital gains
8. **Reimbursable Expense** - Work expenses pending reimbursement
9. **Credit Card Payment** - Paying CC bill (excluded from calculations)
10. **Credit Card Receipt** - CC receiving payment (excluded from calculations)
11. **Loan Disbursement** - Receiving loan
12. **Loan Payment - Principal** - Repaying loan principal
13. **Loan Payment - Interest** - Interest expense

### API Endpoints Organization
All API endpoints use `/api` prefix:
- `/api/transactions` - Transaction CRUD
- `/api/analysis/summary` - Financial summary
- `/api/analysis/income`, `/api/analysis/expenses` - Detailed analysis
- `/api/analysis/trends/{period}` - Time-series trends
- `/api/classifications` - Classification types CRUD
- `/api/classifications/rules` - Classification rules CRUD
- `/api/classifications/apply-rules` - Manual rule application
- `/api/projections/forecast` - Generate forecasts
- `/api/reports/cash-flow` - Cash flow reports
- `/api/import/excel` - Excel file import

### Frontend Routing
- `/dashboard` - Overview with KPIs
- `/transactions` - Transaction list with filtering
- `/analysis` - Main analysis page
- `/analysis/income` - Income deep-dive with trends & categories
- `/analysis/expenses` - Expense deep-dive with trends & categories
- `/classifications` - Classification management (types & rules)
- `/projections` - Financial projections
- `/import` - Excel import interface
- `/settings` - Category management & settings

## Testing Notes

### Backend Tests
- Tests in `tests/` directory
- Use pytest fixtures for database setup/teardown
- Test files mirror source structure
- Run with `pytest tests/ -v`

### Frontend E2E Tests (Playwright)
- Test files: `test-*.spec.ts` in root
- Use `@playwright/test` framework
- Tests verify expense analysis, classification rules, capital expenses
- Run with `npm run test:e2e` from frontend directory

## Common Development Workflows

### Adding a New API Endpoint
1. Create Pydantic schema in `api/schemas/`
2. Add service method in appropriate `services/*.py`
3. Create route handler in `api/routes/`
4. Register router in `api/main.py` (if new router)
5. Test via Swagger UI at http://localhost:8000/api/docs

### Adding a New Frontend Page
1. Create component in `components/[Section]/`
2. Define TypeScript types in `types/`
3. Create API client functions in `api/`
4. Add route in `App.tsx`
5. Add navigation link in `components/common/Sidebar.tsx`
6. Use React Query hooks for data fetching

### Working with Classifications
- System classifications (is_system_classification=true) CANNOT be deleted
- Custom classifications can be created/edited/deleted
- Classification rules use pattern matching (contains, starts_with, ends_with, exact, regex)
- Rules have priority (higher = applied first)
- Apply rules manually via `/api/classifications/apply-rules` or automatically on import

## Worktree Management

This project supports parallel AI agent development using Git worktrees. The CLI is built with TypeScript/Node.js.

### Setup (one-time)

```bash
# Build and link the CLI
cd worktree-cli && npm install && npm run build && npm link
cd ..

# Or use directly without installing globally
node ./worktree-cli/dist/index.js --help
```

### Creating a Worktree for Yourself

If you need to work in isolation (e.g., for a long-running task or to avoid conflicts with another agent):

```bash
# Auto-generate everything (name, branch, ports)
worktree create

# Output shows name (e.g., wt-a3f2) and ports

# Or specify a branch
worktree create -b feature/my-feature
```

Then work in the new directory (shown in output, e.g., `.worktrees/wt-a3f2`)

Your worktree will have:
- Auto-assigned backend port (e.g., 8001)
- Auto-assigned frontend port (e.g., 5174)
- Isolated database: `financial_analysis_<name>.db`

### Starting Services in a Worktree

```bash
# Backend (from worktree directory)
cd .worktrees/wt-a3f2
source core-api/venv/bin/activate  # or .\core-api\venv\Scripts\Activate.ps1 on Windows
cd core-api && python -m uvicorn src.financial_analysis.api.main:app --reload --port $API_PORT

# Frontend (separate terminal)
cd .worktrees/wt-a3f2/web-app
npm run dev
```

### Checking Existing Worktrees

```bash
worktree list --detailed
```

### Cleanup After Work

```bash
# Remove worktree and delete the branch
worktree remove -n wt-a3f2 --delete-branch

# Or cleanup ALL worktrees at once
worktree cleanup
```

## Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Detailed architecture overview
- [API.md](docs/API.md) - Complete API documentation
- [CLASSIFICATION_API.md](docs/CLASSIFICATION_API.md) - Classification system guide
- [README.md](README.md) - Project overview & quick start
- [worktree-cli/README.md](worktree-cli/README.md) - Worktree CLI documentation
- API Docs: http://localhost:8000/api/docs (Swagger UI)
- API Docs: http://localhost:8000/api/redoc (ReDoc)

# mx-cli Memory Management Rules

## When to Save Memories

Save a memory after:
- **Completing significant implementation milestones** - Major features, bug fixes, architectural changes
- **Making important technical decisions** - Why a specific approach was chosen, trade-offs considered
- **Resolving complex bugs or issues** - Root cause, solution, and lessons learned
- **Discovering important patterns or gotchas** - Reusable patterns, common pitfalls, best practices
- **Context switching between tasks** - Current progress, next steps, any blockers
- **Fixing validation errors** - OpenAPI validation fixes, schema corrections, compliance issues

## What to Include in Memories

Include these details when creating memories:
- **Implementation details** - What was done and how
- **Technical decisions** - Why this approach was chosen
- **Code patterns** - Reusable patterns discovered
- **Integration points** - How components interact
- **Testing strategies** - What tests were written and why
- **Deployment details** - How to deploy or configure
- **References** - GitHub issue numbers, commit hashes, PR links
- **Gotchas** - Common mistakes or edge cases to avoid
- **Next steps** - What should be done next

## How to Save Memories

Use the mx-cli memory command in non-interactive mode:

```bash
mx memories create \
  --conversation-id "NEW" \
  --content "Detailed memory content here. Include issue numbers (#X), commit hashes, and specific details." \
  --topics "topic1,topic2,topic3"
```

**Important:**
- Always use `--conversation-id "NEW"` to create a new conversation for the memory
- Always use `--content` flag (non-interactive mode) for CI/CD and scripting compatibility
- Use `--topics` (not `--tags`) for categorization

## When to Search Memories

Search for memories before:
- **Starting new work** - Check if similar work has been done
- **Solving similar problems** - Find patterns and solutions from past work
- **Working with unfamiliar code** - Understand prior decisions and patterns
- **Making architectural changes** - Understand existing design decisions

```bash
mx memories search --query "relevant keywords or issue number"
```

## Topic Conventions

Use consistent topics for better searchability:

**Component Topics:** `mx-cli`, `mx-core-api`, `mx-api-gateway`, `mx-mcp-server`

**Type Topics:** `implementation`, `decision`, `pattern`, `gotcha`, `integration`, `testing`, `deployment`

**Feature Topics:** `openapi-validation`, `openapi-compliance`, `schema-validation`, `neo4j`, `version-management`, `ci-cd`, `memory-management`

**Status Topics:** `completed`, `in-progress`, `blocked`, `needs-review`

Example: `--topics "mx-cli,implementation,version-management,completed"`

## Integration with Workflow

Make memory operations part of your standard task completion:

1. **Before starting work** - Search memories for related context
2. **During implementation** - Note important decisions and patterns
3. **After completing work** - Save memory with details and references
4. **When switching tasks** - Save progress before switching
5. **When resuming work** - Search for saved progress and context

## Retrieve Full Memory Details

After finding a memory with search, get full details:

```bash
mx memories get <memory-id>
```

## Best Practices

- **Search first** - Check for existing memories before asking for context
- **Use consistent topics** - Enables better searchability across memories
- **Include references** - Link to GitHub issues, commits, and PRs for traceability
- **Keep focused** - One memory per significant milestone or decision
- **Write for others** - Assume future readers are unfamiliar with the work
- **Update when needed** - If implementation details change, create a new memory
- **Non-interactive mode** - Always use `--conversation-id "NEW"` and `--content` flags for automation compatibility

## Example Memory Creation

```bash
mx memories create \
  --conversation-id "NEW" \
  --content "Issue #13: Fixed nested memory object access in mx-cli search command.
API returns {data: [{memory: {...}, score: 0.66}]} but CLI was accessing properties directly.
Solution: Extract nested memory object first (const m = result.memory).
Added 5 comprehensive test cases. All 188 tests pass.
Commits: e04151c, 50434a1, 9380b26.
Pattern: Always check API response structure before accessing nested properties." \
  --topics "mx-cli,search,nested-objects,testing,completed"
```

## Example Memory Search

```bash
# Search by issue number
mx memories search --query "issue #13"

# Search by component
mx memories search --query "Neo4j adapter"

# Search by feature
mx memories search --query "OpenAPI validation"
```

---

## OpenAPI Validation Expectations

When working on mx-core-api, all code changes must pass **full OpenAPI 3.0 compliance validation**:

### Validation Requirements

1. **Pre-commit validation** - Automatically runs full OpenAPI spec validation (`.spectral-full.yml`)
2. **Local validation** - Run `npm run validate:openapi:local` before committing
3. **CI/CD validation** - Full validation runs in GitHub Actions pipeline

### Common Validation Tasks to Save as Memories

- **Schema fixes** - Document how you fixed invalid schema structures (e.g., `z.record()` → `z.object().passthrough()`)
- **$ref siblings** - Document how you resolved `$ref` sibling property violations
- **Unused components** - Document decisions to remove or use previously unused schemas
- **Route documentation** - Document patterns for adding `@openapi` JSDoc annotations

### Validation Commands

```bash
# Full OpenAPI compliance (default)
npm run validate:openapi:local

# All validations
npm run validate:all

# REST design only (legacy)
npx spectral lint openapi-spec.json --ruleset .spectral-api-rules.yml
```

### Resources

- Migration Guide: `mx-core-api/docs/OPENAPI_VALIDATION_MIGRATION.md`
- Validation Guide: `mx-core-api/docs/OPENAPI_VALIDATION.md`
- AI Instructions: `mx-core-api/.ai/api-instructions.md`

---

**Use this prompt in Claude Code settings or as a system message to enable systematic memory management during task execution.**

