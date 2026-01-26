# Local Development Guide

**Complete guide to local development with SDK hot reload for the Spearmint Financial Analysis application.**

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Environment Configuration](#environment-configuration)
3. [Development Approaches](#development-approaches)
4. [One-Time Setup](#one-time-setup)
5. [Daily Development Workflow](#daily-development-workflow)
6. [Troubleshooting](#troubleshooting)
7. [Decision Matrix](#decision-matrix)

---

## 🏗️ Architecture Overview

### Production Architecture

```
Browser (example.com)
    ↓
API Gateway (nginx:8080)
    ↓
    ├─→ /api/* → Core API (FastAPI:8000)
    └─→ /* → Frontend (Static Files)
```

**Key Points:**
- SDK calls: `https://example.com/api/transactions`
- Gateway routes `/api/*` to Core API
- Frontend served as static files

### Local Development Architectures

#### Approach 1: Vite Proxy (Recommended for SDK Development)

```
Browser (localhost:5173)
    ↓
Vite Dev Server (:5173)
    ↓
    ├─→ Frontend (React HMR)
    └─→ /api/* → Vite Proxy → Core API (:8000)
```

**Key Points:**
- SDK calls: `http://localhost:5173/api/transactions`
- Vite proxy forwards to Core API
- **Most similar to production** (has proxy layer)
- ✅ **Recommended for SDK development**

#### Approach 2: Direct API Access

```
Browser (localhost:5173)
    ↓
    ├─→ Vite Dev Server (:5173) → Frontend (React HMR)
    └─→ SDK → Core API (:8000) [Direct]
```

**Key Points:**
- SDK calls: `http://localhost:8000/api/transactions`
- **Bypasses Vite proxy entirely**
- Faster but less production-like
- Vite proxy configured but unused

#### Approach 3: Docker with Gateway

```
Browser (localhost:8080)
    ↓
API Gateway (nginx:8080)
    ↓
    ├─→ /api/* → Core API (:8000)
    └─→ /* → Frontend (Vite Dev:5173)
```

**Key Points:**
- SDK calls: `http://localhost:8080/api/transactions`
- **Exact production architecture**
- ❌ No local SDK support (uses published npm package)
- Slower iteration (Docker overhead)

---

## ⚙️ Environment Configuration

### SDK Base URL Priority System

The SDK determines its base URL using a **3-tier priority system**:

```typescript
// web-app/src/api/sdk.ts
const baseUrl =
  import.meta.env.VITE_API_URL ||           // Priority 1: Environment variable
  (typeof window !== "undefined"
    ? window.location.origin                 // Priority 2: Browser origin
    : "http://localhost:8080");              // Priority 3: Fallback
```

### Environment Variable Configurations

#### Configuration 1: Vite Proxy (Recommended)

**File: `web-app/.env`**
```env
# Leave VITE_API_URL unset (or comment it out)
# VITE_API_URL=
```

**Result:**
- SDK uses: `window.location.origin` = `http://localhost:5173`
- SDK calls: `http://localhost:5173/api/transactions`
- Vite proxy intercepts and forwards to Core API
- ✅ **Uses proxy layer** (production-like)

#### Configuration 2: Direct API Access

**File: `web-app/.env`**
```env
VITE_API_URL=http://localhost:8000/api
```

**Result:**
- SDK uses: `http://localhost:8000/api`
- SDK calls: `http://localhost:8000/api/transactions`
- **Bypasses Vite proxy** (direct to Core API)
- ⚠️ Faster but less production-like

#### Configuration 3: Docker Gateway

**File: `docker-compose.yml`**
```yaml
environment:
  - VITE_API_URL=http://localhost:8080
```

**Result:**
- SDK uses: `http://localhost:8080`
- SDK calls: `http://localhost:8080/api/transactions`
- Routes through nginx gateway
- ✅ Exact production architecture

### Vite Proxy Configuration

**File: `web-app/vite.config.ts`**
```typescript
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

**What it does:**
- Intercepts requests to `http://localhost:5173/api/*`
- Forwards to `http://localhost:8000/api/*`
- Handles CORS automatically (same origin)
- Similar to nginx gateway in production

---

## 🚀 Development Approaches

### Approach 1: Local with Vite Proxy ⭐ RECOMMENDED

**Best for:** SDK development, daily development, fast iteration

**Pros:**
- ✅ Full SDK hot reload (via npm link)
- ✅ Proxy layer (similar to production)
- ✅ Fast iteration (~1-2 seconds)
- ✅ No Docker overhead
- ✅ Tests proxy configuration

**Cons:**
- ⚠️ Uses Vite proxy (not nginx gateway)
- ⚠️ Different proxy implementation than production

**When to use:**
- Developing SDK changes
- Daily frontend/backend development
- Testing API changes quickly

---

### Approach 2: Local with Direct API Access

**Best for:** Quick testing, debugging API directly

**Pros:**
- ✅ Fastest (no proxy overhead)
- ✅ Simple setup
- ✅ Direct API access for debugging

**Cons:**
- ❌ No proxy layer (different from production)
- ❌ Vite proxy configured but unused
- ❌ Less production-like

**When to use:**
- Quick API testing
- Debugging Core API directly
- When proxy layer is not needed

---

### Approach 3: Docker with Gateway

**Best for:** Full stack testing, production-like environment

**Pros:**
- ✅ Exact production architecture
- ✅ Tests nginx gateway
- ✅ Tests routing rules
- ✅ Full service orchestration

**Cons:**
- ❌ No local SDK support (uses published npm package)
- ❌ Slower iteration (Docker overhead)
- ❌ Can't use npm link easily
- ❌ Need to rebuild for SDK changes

**When to use:**
- Testing gateway routing
- Testing with PostgreSQL
- Verifying production-like behavior
- Testing multi-service interactions

---

## 🛠️ One-Time Setup

### ⚡ Quick Setup (Recommended)

**Prerequisites:**
- LibLab token configured in `sdk/.env` (required for SDK generation)
  ```bash
  # Create sdk/.env from example
  Copy-Item sdk\.env.example sdk\.env

  # Edit sdk/.env and add your token
  # LIBLAB_TOKEN=your-token-here

  # Get token from: https://developers.liblab.com/
  ```

**Use the automated setup script to configure everything in one command:**

```powershell
# Windows (PowerShell)
.\scripts\setup-local-dev.ps1

# Linux/macOS
./scripts/setup-local-dev.sh

# With automatic server startup (recommended for first-time setup)
.\scripts\setup-local-dev.ps1 -StartServers          # Windows
./scripts/setup-local-dev.sh --start-servers         # Linux/macOS
```

**What it does:**
- ✅ Creates Python virtual environment
- ✅ Installs backend dependencies
- ✅ Initializes database
- ✅ Installs frontend dependencies
- ✅ Generates SDK from OpenAPI spec (using LibLab token)
- ✅ Links SDK to web-app with npm link
- ✅ Configures environment for Vite Proxy
- ✅ Optionally starts both servers in separate terminals (`-StartServers` flag)

**After setup completes, skip to [Daily Development Workflow](#daily-development-workflow).**

---

### 📋 Manual Setup (Alternative)

If you prefer to set up manually or need to troubleshoot, follow these steps:

#### Prerequisites

- **Python 3.10+** with pip
- **Node.js 18+** with npm
- **Git**
- **LibLab CLI** (for SDK generation): `npm install -g liblab`

#### Step 1: Clone Repository

```powershell
git clone https://github.com/spearmint-finance/spearmint.git
cd spearmint
```

### Step 2: Backend Setup

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
cd core-api
pip install -r requirements.txt

# Initialize database
python -m src.financial_analysis.database.init_db

# Return to root
cd ..
```

### Step 3: Frontend Setup

```powershell
# Install dependencies
cd web-app
npm install

# Return to root
cd ..
```

### Step 4: SDK Setup (For Local Development)

```powershell
# Generate SDK from current API
.\sdk\scripts\generate-sdk.ps1

# Install SDK dependencies
cd sdk\output\typescript
npm install

# Create global npm link
npm link

# Link SDK to web-app
cd ..\..\..\web-app
npm link @spearmint-finance/sdk

# Return to root
cd ..
```

### Step 5: Version Management

**IMPORTANT: Single Source of Truth for SDK Versioning**

The project uses `version.json` at the repository root as the **authoritative source** for SDK version numbers.

**Version Synchronization Rules:**

1. **`version.json`** - The single source of truth
   - Location: `D:\CodingProjects\spearmint\version.json`
   - Contains: `{ "version": "0.0.15" }`

2. **`sdk/output/typescript/package.json`** - Must match `version.json`
   - SDK package version must always match the version in `version.json`

3. **`web-app/package.json`** - Must match `version.json`
   - Dependency `@spearmint-finance/sdk` must match the version in `version.json`

**Before making any version-related changes:**

```powershell
# 1. Check the authoritative version
cat version.json
# Output: { "version": "0.0.15" }

# 2. Verify SDK package.json matches
cat sdk\output\typescript\package.json | Select-String "version"
# Should show: "version": "0.0.15"

# 3. Verify web-app package.json matches
cat web-app\package.json | Select-String "@spearmint-finance/sdk"
# Should show: "@spearmint-finance/sdk": "^0.0.15"
```

**When updating versions:**

1. Update `version.json` first
2. Update `sdk/output/typescript/package.json` to match
3. Update `web-app/package.json` dependency to match
4. Regenerate SDK: `.\sdk\scripts\generate-sdk.ps1`
5. Re-link SDK if needed

**Common Version Mismatch Issues:**

```powershell
# Problem: npm link fails with ELSPROBLEMS error
# Cause: Version mismatch between version.json and package.json files

# Solution:
# 1. Check version.json
cat version.json

# 2. Update SDK package.json to match
# Edit sdk/output/typescript/package.json
# Set "version": "0.0.15" (or whatever version.json says)

# 3. Update web-app package.json to match
# Edit web-app/package.json
# Set "@spearmint-finance/sdk": "^0.0.15"

# 4. Re-link SDK
cd sdk\output\typescript
npm link
cd ..\..\web-app
npm link @spearmint-finance/sdk
```

---

### Step 6: Environment Configuration

**For Vite Proxy (Recommended):**

```powershell
cd web-app

# Create .env from example
Copy-Item .env.example .env

# Edit .env to leave VITE_API_URL unset
code .env
```

**Your `.env` should look like:**
```env
# API Configuration
# For local development with Vite proxy (recommended):
# Leave VITE_API_URL unset to use window.location.origin (http://localhost:5173)
# VITE_API_URL=
```

**For Direct API Access:**

```env
VITE_API_URL=http://localhost:8000/api
```

### Step 7: Verify Setup

```powershell
# Check SDK link
cd web-app
npm ls @spearmint-finance/sdk
# Expected: @spearmint-finance/sdk@0.0.15 -> ./../sdk/output/typescript

# Check Python environment
cd ..\core-api
python -c "import fastapi; print('FastAPI installed')"

# Return to root
cd ..
```

---

## 💻 Daily Development Workflow

### Starting Development Servers

Open **2 terminals** and run:

**Terminal 1 - Backend API:**
```powershell
# From project root
.\scripts\start_api.ps1
```

**What happens:**
- ✅ Activates Python virtual environment
- ✅ Sets PYTHONPATH
- ✅ Starts FastAPI on http://localhost:8000
- ✅ Enables auto-reload with `--reload` flag

**Access:**
- API Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/api/health

---

**Terminal 2 - Frontend:**
```powershell
# From project root
cd web-app
.\start_frontend.bat
```

**What happens:**
- ✅ Starts Vite dev server on http://localhost:5173
- ✅ Enables Hot Module Replacement (HMR)
- ✅ Uses local SDK via npm link
- ✅ Proxies `/api` requests (if using Vite proxy)

**Access:**
- Frontend: http://localhost:5173

---

### Development Scenarios

#### Scenario A: Frontend-Only Changes

```powershell
# 1. Edit frontend code
code web-app\src\components\Dashboard\Dashboard.tsx

# 2. Save file
# ✅ Vite automatically hot reloads in browser!
# ✅ No manual steps needed
```

**Expected behavior:**
- Browser updates instantly (< 1 second)
- No page refresh needed (HMR preserves state)

---

#### Scenario B: Backend API Changes

```powershell
# 1. Edit API code
code core-api\src\financial_analysis\api\routes\transactions.py

# 2. Save file
# ✅ Backend auto-reloads (check Terminal 1 - "Reloading...")

# 3. Regenerate SDK (REQUIRED)
.\sdk\scripts\generate-sdk.ps1

# 4. Frontend automatically picks up SDK changes!
# ✅ Check Terminal 2 - Vite will hot reload
# ✅ Browser updates automatically
```

**Expected behavior:**
1. **Terminal 1**: Shows "Reloading..." (~1-2 seconds)
2. **SDK Generation**: Takes ~10-30 seconds
3. **Terminal 2**: Shows HMR update message
4. **Browser**: Updates automatically

**Why this works:**
- `npm link` creates symlink: `web-app/node_modules/@spearmint-finance/sdk` → `sdk/output/typescript/`
- SDK regeneration updates files in `sdk/output/typescript/`
- Vite watches symlinked directory
- Vite detects changes and triggers HMR

---

#### Scenario C: Adding New API Endpoint (Full Cycle)

```powershell
# 1. Create new API endpoint
code core-api\src\financial_analysis\api\routes\persons.py
# Add: @router.get("/persons/{id}")

# 2. Save file - backend auto-reloads

# 3. Regenerate SDK
.\sdk\scripts\generate-sdk.ps1
# ✅ Creates new TypeScript methods in SDK

# 4. Use new SDK method in frontend
code web-app\src\components\Persons\PersonDetail.tsx
# Add: const person = await personsApi.getPersonById(id);

# 5. Save file
# ✅ Terminal 2 shows HMR update
# ✅ Browser updates automatically

# 6. Test in browser
# Open http://localhost:5173
# ✅ See changes immediately!
```

---

### Verifying Your Setup

#### Verify Backend Hot Reload

```powershell
# 1. Edit any Python file in core-api/src/
# 2. Watch Terminal 1 for "Reloading..." message
# 3. Check http://localhost:8000/api/docs to see changes
```

#### Verify Frontend Hot Reload

```powershell
# 1. Edit any React component in web-app/src/
# 2. Watch Terminal 2 for HMR update message
# 3. Browser should update automatically (no refresh)
```

#### Verify SDK Hot Reload

```powershell
# 1. Make API change
# 2. Run: .\sdk\scripts\generate-sdk.ps1
# 3. Watch Terminal 2 for HMR update
# 4. Browser should update automatically
```

#### Verify SDK Link

```powershell
cd web-app
npm ls @spearmint-finance/sdk
# Should show: @spearmint-finance/sdk@0.0.15 -> ./../sdk/output/typescript
# Version number should match version.json
```

#### Verify Vite Proxy is Being Used

Open browser DevTools (F12) → Network tab:
- ✅ **Using Vite Proxy**: Requests to `http://localhost:5173/api/transactions`
- ❌ **Direct API**: Requests to `http://localhost:8000/api/transactions`

---

### Stopping Development

```powershell
# Press Ctrl+C in both terminals
# Terminal 1: Stops backend
# Terminal 2: Stops frontend
```

---

## 🔧 Troubleshooting

### SDK Version Mismatch (ELSPROBLEMS Error)

**Problem:** `npm link` or `npm ls` fails with `ELSPROBLEMS` error showing version mismatch

**Example Error:**
```
npm error code ELSPROBLEMS
npm error invalid: @spearmint-finance/sdk@1.0.0 D:\CodingProjects\spearmint\web-app\node_modules\@spearmint-finance\sdk
```

**Root Cause:** Version mismatch between `version.json`, SDK `package.json`, and web-app `package.json`

**Solution:**

```powershell
# 1. Check the authoritative version
cat version.json
# Output: { "version": "0.0.15" }

# 2. Update SDK package.json to match
code sdk\output\typescript\package.json
# Change "version": "1.0.0" to "version": "0.0.15"

# 3. Update web-app package.json to match
code web-app\package.json
# Change "@spearmint-finance/sdk": "^0.1.0" to "@spearmint-finance/sdk": "^0.0.15"

# 4. Re-link the SDK
cd sdk\output\typescript
npm link

cd ..\..\web-app
npm link @spearmint-finance/sdk

# 5. Verify the link
npm ls @spearmint-finance/sdk
# Should show: @spearmint-finance/sdk@0.0.15 -> .\..\sdk\output\typescript
```

**Prevention:**
- Always check `version.json` before making version changes
- Keep all three files synchronized
- Use the automated setup script which handles version synchronization

---

### SDK Changes Not Reflecting

**Problem:** SDK regenerated but frontend not updating

**Solution:**
```powershell
# 1. Verify npm link is active
cd web-app
npm ls @spearmint-finance/sdk
# Should show: -> ./../sdk/output/typescript

# 2. Regenerate SDK
cd ..
.\sdk\scripts\generate-sdk.ps1

# 3. Restart frontend (if needed)
# Press Ctrl+C in Terminal 2, then:
cd web-app
.\start_frontend.bat
```

---

### "Module not found: @spearmint-finance/sdk"

**Problem:** SDK not found in web-app

**Solution:**
```powershell
# Re-link the SDK
cd sdk\output\typescript
npm link

cd ..\..\web-app
npm link @spearmint-finance/sdk
```

---

### "Cannot find module 'typescript'"

**Problem:** SDK dependencies not installed

**Solution:**
```powershell
# Install SDK dependencies
cd sdk\output\typescript
npm install
npm link
```

---

### Backend Not Auto-Reloading

**Problem:** Python changes not triggering reload

**Solution:**
```powershell
# Check if uvicorn is running with --reload flag
# Look for this in Terminal 1 output:
# "uvicorn ... --reload"

# If not, restart:
# Press Ctrl+C, then:
.\scripts\start_api.ps1
```

---

### Frontend Not Hot Reloading

**Problem:** React changes not updating browser

**Solution:**
```powershell
# 1. Check Vite dev server is running
# Look for "VITE vX.X.X ready" in Terminal 2

# 2. Hard refresh browser
# Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

# 3. Restart frontend
# Press Ctrl+C in Terminal 2, then:
cd web-app
.\start_frontend.bat
```

---

### Vite Proxy Not Working

**Problem:** API requests going directly to Core API instead of through proxy

**Solution:**
```powershell
# 1. Check .env file
cd web-app
code .env
# Make sure VITE_API_URL is unset or commented out

# 2. Restart frontend
# Press Ctrl+C in Terminal 2, then:
.\start_frontend.bat

# 3. Verify in browser DevTools
# Network tab should show requests to localhost:5173/api/*
```

---

### "Virtual environment not found"

**Problem:** Python virtual environment not activated

**Solution:**
```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1

# Install dependencies
cd core-api
pip install -r requirements.txt
```

---

### "Port 8000 already in use"

**Problem:** Another process using port 8000

**Solution:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace <PID> with actual PID)
taskkill /PID <PID> /F
```

---

### "Port 5173 already in use"

**Problem:** Another process using port 5173

**Solution:**
Vite will automatically try the next available port (5174, 5175, etc.)

---

### SDK Generation Fails

**Problem:** `.\sdk\scripts\generate-sdk.ps1` fails

**Solution:**
```powershell
# 1. Check LibLab is installed
liblab --version

# 2. If not installed:
npm install -g liblab

# 3. Check backend is running
# SDK generation needs OpenAPI spec from running API

# 4. Try generating spec only first
cd core-api
python scripts/generate_openapi.py ../sdk/openapi.json
```

---

## 📊 Decision Matrix

### When to Use Each Approach

| Scenario | Recommended Approach | Why |
|----------|---------------------|-----|
| **Daily SDK Development** | Local with Vite Proxy | Fast iteration, SDK hot reload, proxy layer |
| **Quick API Testing** | Local with Direct API | Fastest, simple debugging |
| **Frontend Development** | Local with Vite Proxy | HMR, production-like |
| **Backend Development** | Local with Vite Proxy | Auto-reload, fast iteration |
| **Testing Gateway Routing** | Docker with Gateway | Exact production architecture |
| **Testing with PostgreSQL** | Docker with Gateway | Full database setup |
| **Production-like Testing** | Docker with Gateway | All services orchestrated |
| **CI/CD Pipeline Testing** | Docker with Gateway | Matches deployment environment |

---

### Comparison Table

| Feature | Local + Vite Proxy | Local + Direct API | Docker + Gateway |
|---------|-------------------|-------------------|------------------|
| **SDK Hot Reload** | ✅ Yes | ✅ Yes | ❌ No |
| **Backend Hot Reload** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Frontend Hot Reload** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Proxy Layer** | ✅ Vite Proxy | ❌ None | ✅ Nginx Gateway |
| **Production-Like** | ⚠️ Similar | ❌ No | ✅ Exact |
| **Iteration Speed** | ⚡ Fast (~1-2s) | ⚡ Fastest (<1s) | 🐢 Slow (~5-10s) |
| **Setup Complexity** | ⚠️ Medium | ✅ Simple | ❌ Complex |
| **npm link Support** | ✅ Yes | ✅ Yes | ❌ Difficult |
| **Gateway Testing** | ❌ No | ❌ No | ✅ Yes |
| **PostgreSQL** | ❌ No (SQLite) | ❌ No (SQLite) | ✅ Yes |

---

## 📚 Related Documentation

- **SDK Generation:** `sdk/scripts/README.md`
- **Docker Hot Reload:** `docs/DOCKER_HOT_RELOAD.md`
- **Local SDK Development:** `docs/LOCAL_SDK_DEVELOPMENT.md`
- **Local Development Quickstart:** `docs/LOCAL_DEVELOPMENT_QUICKSTART.md`
- **Full Stack Guide:** `docs/FULLSTACK_QUICKSTART.md`

---

## ✅ Quick Reference

### One-Time Setup

```powershell
# Generate and link SDK
.\sdk\scripts\generate-sdk.ps1
cd sdk\output\typescript && npm install && npm link
cd ..\..\web-app && npm link @spearmint-finance/sdk
cd ..

# Configure environment (Vite Proxy)
cd web-app
Copy-Item .env.example .env
# Leave VITE_API_URL unset in .env
```

### Daily Development

```powershell
# Terminal 1 - Backend
.\scripts\start_api.ps1

# Terminal 2 - Frontend
cd web-app
.\start_frontend.bat

# After API changes
.\sdk\scripts\generate-sdk.ps1
# ✅ Changes automatically available in frontend!
```

### Switching SDK Versions

```powershell
# Use local SDK
cd sdk\output\typescript && npm link
cd ..\..\web-app && npm link @spearmint-finance/sdk

# Use published SDK
cd web-app
npm unlink @spearmint-finance/sdk
npm install @spearmint-finance/sdk
```

---

## 🎯 Summary

**For daily SDK development, use Local with Vite Proxy:**

✅ **Benefits:**
- Fast iteration cycle (~1-2 seconds)
- Full SDK hot reload via npm link
- Proxy layer (similar to production)
- No Docker overhead
- Easy debugging

**This gives you:**
- ✅ Instant feedback on all changes
- ✅ Hot reload for frontend, backend, and SDK
- ✅ Production-like architecture (with proxy)
- ✅ Fast development workflow
- ✅ Easy troubleshooting

**Access:**
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/api/health

---

**Last Updated:** 2025-11-24
**Version:** 1.0.0

