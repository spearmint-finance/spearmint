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
start_api.bat
# OR manually:
venv\Scripts\activate
python run_api.py

# Run backend tests
venv\Scripts\activate
pytest tests/ -v
pytest tests/ --cov=src

# Initialize database
python -m src.financial_analysis.database.init_db

# Verify setup
python verify_setup.py
```

### Frontend

```bash
# Start frontend dev server (runs on http://localhost:5173)
cd frontend
start_frontend.bat
# OR: npm run dev

# Build for production
npm run build

# Run linting
npm run lint

# Run E2E tests
npm run test:e2e
npm run test:e2e:ui        # Interactive UI mode
npm run test:e2e:headed    # Run with visible browser
npm run test:e2e:debug     # Debug mode
```

### Full Stack Development

Run both servers in separate terminals:
- **Terminal 1:** `start_api.bat` (backend on :8000)
- **Terminal 2:** `cd frontend && start_frontend.bat` (frontend on :5173)

## Architecture Overview

### Backend Structure

```
src/financial_analysis/
├── api/
│   ├── main.py              # FastAPI app with CORS, error handlers, middleware
│   ├── routes/              # API route handlers (8 router modules)
│   │   ├── transactions.py
│   │   ├── analysis.py
│   │   ├── classifications.py
│   │   ├── projections.py
│   │   ├── reports.py
│   │   └── ...
│   └── schemas/             # Pydantic validation models
├── database/
│   ├── models.py            # SQLAlchemy ORM models
│   ├── views.py             # Database views for complex queries
│   └── init_db.py           # Database initialization
├── services/                # Business logic layer
│   ├── import_service.py    # Excel import & validation
│   ├── classification_service.py  # Auto-classification engine
│   ├── analysis_service.py  # Income/expense/cash flow analysis
│   ├── projection_service.py # Statistical forecasting
│   └── transaction_service.py
└── utils/                   # Utility functions
```

### Frontend Structure

```
frontend/src/
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

## Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Detailed architecture overview
- [API.md](docs/API.md) - Complete API documentation
- [CLASSIFICATION_API.md](docs/CLASSIFICATION_API.md) - Classification system guide
- [README.md](README.md) - Project overview & quick start
- API Docs: http://localhost:8000/api/docs (Swagger UI)
- API Docs: http://localhost:8000/api/redoc (ReDoc)
