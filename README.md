# Spearmint Financial Analysis

[![npm version](https://img.shields.io/npm/v/@spearmint-finance/sdk)](https://www.npmjs.com/package/@spearmint-finance/sdk)

A comprehensive financial analysis application designed to provide deep insights into personal or business financial health through intelligent transaction classification, trend analysis, and predictive forecasting.

> **Note:** This project includes automated pre-commit testing to ensure code quality and API specification validation.

## Overview

This tool imports transaction data from Excel files, stores it in a relational database, and provides powerful analysis capabilities including:

- **Smart Transaction Classification** - Automatically identifies and classifies transactions to prevent double-counting
- **Income & Expense Analysis** - Detailed breakdowns with category-level insights
- **Cash Flow Tracking** - Accurate net cash flow calculations with transfer exclusions
- **Financial Projections** - Statistical forecasting with confidence intervals
- **Trend Analysis** - Identify spending patterns and income stability
- **Reconciliation Tools** - Validate data accuracy with dual-view modes

## Key Features

### Transaction Classification System
- Prevents double-counting of credit card payments, transfers, and internal transactions
- Automatic pattern-based classification with configurable rules
- Transaction relationship linking (e.g., credit card payment ↔ receipt)
- Dual view modes: Analysis View (accurate calculations) and Complete View (audit trail)

### Analysis Capabilities
- Income analysis by source/category with trend tracking
- Expense categorization with pattern detection
- Time period flexibility (daily, weekly, monthly, quarterly, yearly)
- Custom date range selection and period comparisons

### Financial Projections
- Multiple statistical methods (Linear Regression, Moving Average, ARIMA, etc.)
- Short, medium, and long-term forecasting
- Confidence intervals and scenario analysis
- Classification-aware data preparation for accurate projections

## Project Structure

```
financial-analysis/
├── .product/
│   └── analyzer.prd                    # Product Requirements Document
├── backend/
│   ├── src/financial_analysis/         # Python backend application
│   │   ├── api/                        # FastAPI routes and schemas
│   │   ├── database/                   # SQLAlchemy models and migrations
│   │   ├── services/                   # Business logic services
│   │   └── utils/                      # Utility functions
│   ├── tests/                          # Backend tests
│   ├── requirements.txt                # Python dependencies
│   └── run_api.py                      # API server entry point
├── frontend/
│   ├── src/                            # React application source
│   │   ├── components/                 # React components
│   │   ├── api/                        # API client configuration
│   │   ├── types/                      # TypeScript type definitions
│   │   └── theme.ts                    # Material-UI theme
│   ├── package.json                    # Node dependencies
│   └── vite.config.ts                  # Vite configuration
├── data/
│   └── transactions.xlsx               # Sample transaction data
├── docs/                               # Documentation
│   ├── ARCHITECTURE.md                 # System architecture
│   ├── PHASE4_FRONTEND_FOUNDATION.md   # Frontend progress
│   └── API.md                          # API documentation
├── FULLSTACK_QUICKSTART.md             # Quick start guide
└── README.md
```

## Documentation

See [Product Requirements Document](.product/analyzer.prd) for comprehensive specifications including:
- Database schema design
- Feature specifications
- Technical architecture
- Implementation roadmap
- Success criteria

## Technology Stack

### Backend
- **Framework:** FastAPI (Python 3.10+)
- **Database:** SQLite (development) → PostgreSQL (production)
- **ORM:** SQLAlchemy 2.0+
- **Data Processing:** Pandas, NumPy, SciPy
- **Statistical Analysis:** statsmodels, scikit-learn
- **Excel Parsing:** openpyxl
- **Validation:** Pydantic 2.0+

### Frontend
- **Framework:** React 18.3+ with TypeScript 5+
- **Build Tool:** Vite 5.4+
- **UI Library:** Material-UI (MUI) v5
- **Routing:** React Router v6
- **State Management:** TanStack Query (React Query)
- **HTTP Client:** Axios
- **Charts:** Recharts
- **Forms:** React Hook Form
- **Styling:** Emotion (CSS-in-JS)

## Getting Started

### ⚡ Quick Setup (Recommended)

**One-command setup for local development:**

```bash
# Windows (PowerShell)
.\scripts\setup-local-dev.ps1

# Linux/macOS
./scripts/setup-local-dev.sh
```

This automated script sets up:
- ✅ Python virtual environment and backend dependencies
- ✅ Database initialization
- ✅ Frontend dependencies
- ✅ SDK generation and linking for hot reload
- ✅ Environment configuration

**After setup, start development servers:**

```bash
# Terminal 1 - Backend
.\scripts\start_api.ps1
# Backend runs on http://localhost:8000

# Terminal 2 - Frontend
cd web-app
.\start_frontend.bat
# Frontend runs on http://localhost:5173
```

**See Also:**
- Complete Guide: [dev-tools/docs/LOCAL_DEVELOPMENT_GUIDE.md](dev-tools/docs/LOCAL_DEVELOPMENT_GUIDE.md)
- Quick Start: [LOCAL_DEVELOPMENT_QUICKSTART.md](docs/LOCAL_DEVELOPMENT_QUICKSTART.md)
- SDK Development: [LOCAL_SDK_DEVELOPMENT.md](docs/LOCAL_SDK_DEVELOPMENT.md)

---

### 📋 Manual Setup (Alternative)

If you prefer manual setup, see [FULLSTACK_QUICKSTART.md](FULLSTACK_QUICKSTART.md) for detailed instructions.

**Backend:**
```bash
python -m venv .venv
.venv\Scripts\activate
cd core-api
pip install -r requirements.txt
python -m src.financial_analysis.database.init_db
```

**Frontend:**
```bash
cd web-app
npm install
npm run build
```

## Development Status

### ✅ Phase 1: Backend Foundation (Complete)
- Database schema with SQLAlchemy models
- FastAPI application with 15+ REST endpoints
- Excel import service with validation
- Automatic classification engine
- Comprehensive API documentation (Swagger/ReDoc)

### ✅ Phase 2: Analysis Engine (Complete)
- Income/expense analysis service
- Trend analysis (daily, weekly, monthly, quarterly, yearly)
- Cash flow calculations with classification awareness
- Financial health indicators
- Analysis API endpoints

### 🚧 Phase 3: API Enhancements (85% Complete)
- Relationship detection and linking
- Projection service with statistical forecasting
- Report generation service
- Classification management API
- Advanced filtering and search

### 🚧 Phase 4: Frontend Foundation (54% Complete - In Progress)
- ✅ React + Vite + TypeScript setup
- ✅ Material-UI theme and styling
- ✅ React Router navigation
- ✅ React Query API integration
- ✅ Application layout (header, sidebar)
- ✅ Loading states and error handling
- 🚧 Dashboard with overview cards
- 🚧 Transaction list with filtering
- 🚧 Transaction detail/edit forms
- 🚧 Charts with Recharts
- 🚧 Responsive design optimization

### 📋 Phase 5: Frontend Features (Upcoming)
- Import interface with drag-and-drop
- Analysis & reports components
- Classification management UI
- Projections visualization
- Settings & configuration

### 📋 Phase 6: Integration & Polish (Upcoming)
- End-to-end integration testing
- Performance optimization
- User experience refinement
- Documentation completion

## API Documentation

The backend provides comprehensive API documentation:

- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc
- **OpenAPI JSON:** http://localhost:8000/api/openapi.json

### Key Endpoints

- `/api/transactions` - Transaction CRUD operations
- `/api/analysis/summary` - Financial analysis summary
- `/api/analysis/trends` - Trend data by period
- `/api/categories` - Category management
- `/api/import/excel` - Excel file import
- `/api/classifications` - Classification rules
- `/api/projections/forecast` - Financial forecasting
- `/api/reports/cash-flow` - Cash flow reports

## Testing

### Backend Tests
```bash
venv\Scripts\activate
pytest tests/ -v
pytest tests/ --cov=src
```

### Frontend Tests
```bash
cd frontend
npm run lint
npm run build  # Verify TypeScript compilation
```

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Phase 4 Progress](docs/PHASE4_FRONTEND_FOUNDATION.md)
- [Full Stack Quick Start](FULLSTACK_QUICKSTART.md)
- [Product Requirements](. product/analyzer.prd)

## Contributing

This is a private project. For development:

1. Create a feature branch
2. Make changes with proper testing
3. Update documentation
4. Submit pull request for review

## License

Private project - All rights reserved

## Author

Harry Mower

