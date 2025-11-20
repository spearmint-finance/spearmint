# Full Stack Quick Start Guide

This guide will help you run both the backend API and frontend application together.

---

## Prerequisites

- **Python 3.10+** with virtual environment
- **Node.js 18+** and npm
- **Windows** (batch files provided for Windows)

---

## Quick Start (2 Terminals)

### Terminal 1: Start Backend API

```bash
# Navigate to project root
cd d:\CodingProjects\financial-analysis

# Activate virtual environment
venv\Scripts\activate

# Start API server (Option A - Batch file)
start_api.bat

# OR Option B - Python script
python run_api.py
```

**Backend will be available at:**
- API: http://localhost:8000/api
- Swagger Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

---

### Terminal 2: Start Frontend Application

```bash
# Navigate to frontend directory
cd d:\CodingProjects\financial-analysis\frontend

# Start development server (Option A - Batch file)
start_frontend.bat

# OR Option B - npm command
npm run dev
```

**Frontend will be available at:**
- Application: http://localhost:5173
- API requests automatically proxied to backend

---

## First Time Setup

### Backend Setup (One-time)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m src.financial_analysis.database.init_db

# Verify setup
python verify_setup.py
```

### Frontend Setup (One-time)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Verify build works
npm run build
```

---

## Development Workflow

### 1. Start Both Servers

Open two terminal windows and run:
- **Terminal 1:** Backend API (`start_api.bat`)
- **Terminal 2:** Frontend dev server (`cd frontend && start_frontend.bat`)

### 2. Access the Application

- Open browser to http://localhost:5173
- The frontend will automatically proxy API requests to the backend
- Changes to frontend code will hot-reload automatically
- Changes to backend code will auto-reload if `DEBUG=True`

### 3. Import Sample Data (Optional)

Use the API docs at http://localhost:8000/api/docs to:
1. Navigate to `/api/import/excel` endpoint
2. Upload `data/transactions.xlsx`
3. Refresh the frontend to see imported data

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (localhost:5173)                  │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │         React Frontend (Vite Dev Server)           │     │
│  │  - Material-UI Components                          │     │
│  │  - React Router                                    │     │
│  │  - React Query                                     │     │
│  └────────────────────────────────────────────────────┘     │
│                          │                                    │
│                          │ HTTP Requests (/api/*)            │
│                          ▼                                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │              Vite Proxy                            │     │
│  │  Forwards /api/* → http://localhost:8000/api       │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ Proxied Requests
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (localhost:8000)                │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │         FastAPI Application                        │     │
│  │  - REST API Endpoints                              │     │
│  │  - Pydantic Validation                             │     │
│  │  - CORS Middleware                                 │     │
│  └────────────────────────────────────────────────────┘     │
│                          │                                    │
│                          ▼                                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │         Business Logic Services                    │     │
│  │  - TransactionService                              │     │
│  │  - AnalysisService                                 │     │
│  │  - ClassificationService                           │     │
│  └────────────────────────────────────────────────────┘     │
│                          │                                    │
│                          ▼                                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │         SQLite Database                            │     │
│  │  - Transactions                                    │     │
│  │  - Categories                                      │     │
│  │  - Classifications                                 │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Available API Endpoints

### Transactions
- `GET /api/transactions` - List transactions
- `POST /api/transactions` - Create transaction
- `GET /api/transactions/{id}` - Get transaction
- `PUT /api/transactions/{id}` - Update transaction
- `DELETE /api/transactions/{id}` - Delete transaction

### Analysis
- `GET /api/analysis/summary` - Get analysis summary
- `GET /api/analysis/trends` - Get trend data
- `GET /api/analysis/income` - Income analysis
- `GET /api/analysis/expenses` - Expense analysis

### Categories
- `GET /api/categories` - List categories
- `POST /api/categories` - Create category
- `GET /api/categories/{id}` - Get category
- `PUT /api/categories/{id}` - Update category

### Import
- `POST /api/import/excel` - Import Excel file
- `GET /api/import/history` - Import history

### Classifications
- `GET /api/classifications` - List classifications
- `POST /api/classifications/rules` - Create rule
- `POST /api/classifications/apply` - Apply rules

### Projections
- `POST /api/projections/forecast` - Generate forecast
- `GET /api/projections/{id}` - Get projection

### Reports
- `GET /api/reports/cash-flow` - Cash flow report
- `GET /api/reports/category-breakdown` - Category breakdown

---

## Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError`
```bash
# Solution: Activate virtual environment
venv\Scripts\activate
```

**Problem:** Database not found
```bash
# Solution: Initialize database
python -m src.financial_analysis.database.init_db
```

**Problem:** Port 8000 already in use
```bash
# Solution: Change port in .env or kill process
# Find process: netstat -ano | findstr :8000
# Kill process: taskkill /PID <pid> /F
```

### Frontend Issues

**Problem:** `npm: command not found`
```bash
# Solution: Install Node.js from https://nodejs.org/
```

**Problem:** Dependencies not installed
```bash
# Solution: Install dependencies
cd frontend
npm install
```

**Problem:** Port 5173 already in use
```bash
# Solution: Vite will automatically try next available port
# Or kill the process using port 5173
```

**Problem:** API requests failing (CORS errors)
```bash
# Solution: Ensure backend is running and CORS is configured
# Check backend config.py CORS_ORIGINS includes http://localhost:5173
```

---

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=sqlite:///financial_analysis.db
APP_ENV=development
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173
LOG_LEVEL=INFO
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
```

---

## Development Tips

1. **Hot Reload:** Both frontend and backend support hot reload in development mode
2. **API Documentation:** Use Swagger UI at http://localhost:8000/api/docs for testing
3. **React DevTools:** Install React DevTools browser extension for debugging
4. **Network Tab:** Use browser DevTools Network tab to inspect API calls
5. **Console Logs:** Check browser console for frontend errors, terminal for backend errors

---

## Next Steps

1. Import sample data using the API
2. Explore the Dashboard at http://localhost:5173/dashboard
3. View transactions at http://localhost:5173/transactions
4. Check API documentation at http://localhost:8000/api/docs
5. Start building additional features!

---

## Production Deployment (Future)

### Frontend
- Build: `npm run build` (creates `dist/` folder)
- Deploy to: Vercel, Netlify, AWS S3, or any static hosting

### Backend
- Deploy to: AWS, GCP, Azure, or Heroku
- Use PostgreSQL instead of SQLite
- Set `DEBUG=False` and configure proper CORS origins

---

## Support

For issues or questions:
1. Check the documentation in `docs/` directory
2. Review API documentation at http://localhost:8000/api/docs
3. Check GitHub issues at https://github.com/harrymower/financial-analysis/issues

