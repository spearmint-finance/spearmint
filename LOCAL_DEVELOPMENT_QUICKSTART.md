# Local Development Quick Start

How to start everything locally for development.

---

## 🚀 **Quick Start (3 Steps)**

### **1. Generate and Link Local SDK (One-Time Setup)**

```powershell
# Generate SDK
.\sdk\scripts\generate-sdk.ps1

# Link it to web-app
cd sdk\output\typescript
npm link

cd ..\..\..\web-app
npm link @spearmint-finance/sdk
cd ..
```

---

### **2. Start Backend API**

**Terminal 1:**
```powershell
.\start_api.ps1
```

**What it does:**
- ✅ Activates virtual environment (if needed)
- ✅ Sets PYTHONPATH
- ✅ Starts FastAPI with uvicorn
- ✅ Enables auto-reload on code changes

**Access:**
- API Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/api/health

---

### **3. Start Frontend**

**Terminal 2:**
```powershell
cd web-app
.\start_frontend.bat
```

**What it does:**
- ✅ Starts Vite dev server
- ✅ Enables hot module replacement (HMR)
- ✅ Uses local SDK via npm link

**Access:**
- Frontend: http://localhost:5173

---

## 🔄 **Development Workflow**

### **Making API Changes:**

```powershell
# 1. Edit API code
code core-api\src\financial_analysis\api\routes\persons.py

# 2. Backend auto-reloads (already running in Terminal 1)
# Check Terminal 1 - you'll see "Reloading..."

# 3. Regenerate SDK
.\sdk\scripts\generate-sdk.ps1

# 4. Frontend automatically picks up changes!
# Check Terminal 2 - Vite will hot reload
```

---

### **Making Frontend Changes:**

```powershell
# 1. Edit frontend code
code web-app\src\components\Dashboard\Dashboard.tsx

# 2. Save file
# Vite automatically hot reloads in browser!
```

---

## 🐳 **Alternative: Docker Compose**

If you prefer to run everything in Docker:

```powershell
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

**Access:**
- Frontend: http://localhost:8080 (through gateway)
- API Docs: http://localhost:8080/api/docs

**Note:** Docker Compose uses published SDK by default. To use local SDK, see `LOCAL_SDK_DEVELOPMENT.md`.

---

## 📊 **What's Running?**

### **Local Development (Recommended):**

| Service | Port | URL | Auto-Reload |
|---------|------|-----|-------------|
| **Backend API** | 8000 | http://localhost:8000/api/docs | ✅ Yes |
| **Frontend** | 5173 | http://localhost:5173 | ✅ Yes (HMR) |
| **Local SDK** | - | npm link | ✅ Yes |

### **Docker Compose:**

| Service | Port | URL | Auto-Reload |
|---------|------|-----|-------------|
| **API Gateway** | 8080 | http://localhost:8080 | ❌ No |
| **Backend API** | 8000 | http://localhost:8000/api/docs | ✅ Yes |
| **Frontend** | 5173 | http://localhost:5173 | ✅ Yes (HMR) |
| **PostgreSQL** | 5432 | - | - |

---

## 🔍 **Verify Everything is Working**

### **Check Backend:**

```powershell
# Health check
curl http://localhost:8000/api/health

# Or open in browser
start http://localhost:8000/api/docs
```

### **Check Frontend:**

```powershell
# Open in browser
start http://localhost:5173
```

### **Check SDK Link:**

```powershell
cd web-app
npm ls @spearmint-finance/sdk
```

**Expected output:**
```
@spearmint-finance/sdk@0.1.0 -> ./../sdk/output/typescript
```

---

## 🛑 **Stopping Everything**

### **Local Development:**

- Press `Ctrl+C` in each terminal (Terminal 1 and Terminal 2)

### **Docker Compose:**

```powershell
docker compose down
```

---

## 🔧 **Troubleshooting**

### **"Virtual environment not found"**

```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1

# Install dependencies
cd core-api
pip install -r requirements.txt
```

### **"uvicorn: command not found"**

```powershell
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install uvicorn
pip install uvicorn
```

### **"Port 8000 already in use"**

```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace <PID> with actual PID)
taskkill /PID <PID> /F
```

### **"Port 5173 already in use"**

Vite will automatically try the next available port (5174, 5175, etc.)

### **"SDK changes not reflecting"**

```powershell
# Regenerate SDK
.\sdk\scripts\generate-sdk.ps1

# Restart frontend
# Press Ctrl+C in Terminal 2, then:
cd web-app
.\start_frontend.bat
```

### **"Module not found" errors in backend**

```powershell
# Make sure you're in the right directory
cd core-api

# Install dependencies
pip install -r requirements.txt

# Try running directly with uvicorn
uvicorn src.financial_analysis.api.main:app --reload
```

---

## 📚 **Related Documentation**

- **SDK Development:** `LOCAL_SDK_DEVELOPMENT.md`
- **SDK Generation:** `sdk/scripts/README.md`
- **Docker Hot Reload:** `DOCKER_HOT_RELOAD.md`
- **Full Stack Guide:** `docs/FULLSTACK_QUICKSTART.md`

---

## ✅ **Summary**

**For daily development:**

```powershell
# Terminal 1 - Backend
.\start_api.ps1

# Terminal 2 - Frontend
cd web-app
.\start_frontend.bat

# Make changes, save, and see them instantly!
```

**After API changes:**

```powershell
# Regenerate SDK
.\sdk\scripts\generate-sdk.ps1

# Changes automatically available in frontend!
```

**This gives you:**
- ✅ Instant feedback on all changes
- ✅ Hot reload for frontend and backend
- ✅ Local SDK for testing API changes
- ✅ No Docker overhead
- ✅ Fast iteration cycle

---

## 🎯 **Next Steps**

1. ✅ Start backend: `.\start_api.ps1`
2. ✅ Start frontend: `cd web-app && .\start_frontend.bat`
3. ✅ Open browser: http://localhost:5173
4. ✅ Make changes and see them instantly!
5. ✅ Check API docs: http://localhost:8000/api/docs

