# Quick Start Guide - Financial Analysis API

This guide will help you verify and test the Phase 2 analysis features in under 5 minutes.

---

## ⚡ Super Quick Start (30 seconds)

### Step 1: Verify Setup

```bash
# Make sure you're in the project directory
cd d:\CodingProjects\financial-analysis

# Activate virtual environment
venv\Scripts\activate

# Run verification script
python verify_setup.py
```

**Expected:** All checks should pass ✅

---

### Step 2: Start the API Server

**Option A - Windows Batch File (Easiest):**
```bash
scripts\start_api.bat
```

**Option B - Python Script:**
```bash
# Make sure virtual environment is activated!
venv\Scripts\activate

# Start server
python run_api.py
```

**Expected Output:**
```
================================================================================
  Financial Analysis API Server
================================================================================
  Environment: development
  Debug Mode: True
  Host: 0.0.0.0
  Port: 8000

🌐 API will be available at:
   - http://localhost:8000/api/docs (Swagger UI)
   - http://127.0.0.1:8000/api/docs (Swagger UI)

📝 Press CTRL+C to stop the server
================================================================================

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**Important:** 
- The server binds to `0.0.0.0:8000` (all interfaces)
- Access it via `http://localhost:8000` or `http://127.0.0.1:8000`
- Keep this terminal window open!

---

### Step 3: Test the API

**Option A - Open Browser (Interactive):**

Open your browser and go to:
```
http://localhost:8000/api/docs
```

This opens the **Swagger UI** where you can click and test endpoints!

**Option B - Run Test Script:**

Open a **NEW terminal** (keep the server running):
```bash
cd d:\CodingProjects\financial-analysis
venv\Scripts\activate
python test_analysis_api.py
```

Type `y` when asked to create sample data.

---

## 🎯 What You Can Test

### Available Endpoints

All endpoints are under `/api/analysis/`:

1. **GET /api/analysis/income** - Total income analysis
2. **GET /api/analysis/income/trends** - Income trends over time
3. **GET /api/analysis/expenses** - Total expense analysis
4. **GET /api/analysis/expenses/trends** - Expense trends over time
5. **GET /api/analysis/cashflow** - Net cash flow (income - expenses)
6. **GET /api/analysis/cashflow/trends** - Cash flow trends
7. **GET /api/analysis/health** - Financial health indicators

### Quick Tests in Swagger UI

1. **Test Income Analysis:**
   - Find `GET /api/analysis/income`
   - Click "Try it out"
   - Click "Execute"
   - See total income and breakdown by category

2. **Test Expense Analysis:**
   - Find `GET /api/analysis/expenses`
   - Click "Try it out"
   - Set `top_n` to 5
   - Click "Execute"
   - See top 5 spending categories

3. **Test Cash Flow:**
   - Find `GET /api/analysis/cashflow`
   - Click "Try it out"
   - Click "Execute"
   - See net cash flow (income - expenses)

4. **Test Financial Health:**
   - Find `GET /api/analysis/health`
   - Click "Try it out"
   - Click "Execute"
   - See income-to-expense ratio, savings rate

5. **Test Trends:**
   - Find `GET /api/analysis/income/trends`
   - Click "Try it out"
   - Set `period` to "monthly"
   - Click "Execute"
   - See income by month

---

## 🔧 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'fastapi'"

**Cause:** Virtual environment not activated or dependencies not installed

**Solution:**
```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python verify_setup.py
```

---

### Problem: Server shuts down immediately

**Cause:** Not running in virtual environment

**Solution:**
```bash
# Use the batch file (it activates venv automatically)
scripts\start_api.bat

# OR activate venv manually first
venv\Scripts\activate
python run_api.py
```

---

### Problem: "Cannot connect to API"

**Cause:** Server not running

**Solution:**
1. Check if server is running in another terminal
2. Look for "Application startup complete" message
3. Try accessing http://localhost:8000/api/health

---

### Problem: "No data" or empty results

**Cause:** No transactions in database

**Solution:**
```bash
# Option 1: Create sample data via test script
python test_analysis_api.py
# Type 'y' when asked

# Option 2: Import your Excel file
# Use Swagger UI: POST /api/import/file-path
# Or use the import endpoint with your file path
```

---

### Problem: Database errors

**Cause:** Database not initialized

**Solution:**
```bash
# Initialize/reset database
python src/financial_analysis/database/init_db.py --reset
```

---

## 📊 Sample API Calls

### Using curl (Command Line)

```bash
# Get income analysis
curl http://localhost:8000/api/analysis/income

# Get expenses with top 5 categories
curl "http://localhost:8000/api/analysis/expenses?top_n=5"

# Get cash flow
curl http://localhost:8000/api/analysis/cashflow

# Get financial health
curl http://localhost:8000/api/analysis/health

# Get monthly income trends
curl "http://localhost:8000/api/analysis/income/trends?period=monthly"

# Get income for specific date range
curl "http://localhost:8000/api/analysis/income?start_date=2025-01-01&end_date=2025-01-31"
```

### Using PowerShell

```powershell
# Get income analysis
Invoke-RestMethod -Uri "http://localhost:8000/api/analysis/income" | ConvertTo-Json

# Get expenses
Invoke-RestMethod -Uri "http://localhost:8000/api/analysis/expenses" | ConvertTo-Json

# Get cash flow
Invoke-RestMethod -Uri "http://localhost:8000/api/analysis/cashflow" | ConvertTo-Json
```

---

## ✅ Verification Checklist

- [ ] Virtual environment activated
- [ ] All dependencies installed (`verify_setup.py` passes)
- [ ] Database initialized
- [ ] API server starts without errors
- [ ] Can access http://localhost:8000/api/docs
- [ ] Health check works: http://localhost:8000/api/health
- [ ] Sample data created (via test script)
- [ ] Income analysis returns data
- [ ] Expense analysis returns data
- [ ] Cash flow analysis returns data
- [ ] Financial health indicators calculate
- [ ] Trends return time-series data

---

## 📚 Next Steps

Once everything is working:

1. **Import Your Data:**
   - Use `POST /api/import/file-path` in Swagger UI
   - Point to your `data/transactions.xlsx` file

2. **Explore Analysis:**
   - Try different date ranges
   - Compare different time periods
   - Analyze spending patterns

3. **Continue Development:**
   - Next: Relationship detection (Task 2)
   - Then: Projections and forecasting (Task 3)
   - Finally: Reports and exports (Task 4)

---

## 🆘 Still Having Issues?

1. **Run the verification script:**
   ```bash
   python verify_setup.py
   ```

2. **Check the detailed guide:**
   - See `docs/VERIFICATION_PHASE2.md` for comprehensive troubleshooting

3. **Check logs:**
   - Look in `logs/` directory for error messages
   - Server output shows detailed error information

4. **Test imports:**
   ```bash
   python -c "from src.financial_analysis.api.main import app; print('Success!')"
   ```

---

**Happy Testing! 🎉**

