# Docker Compose Restart Scripts - Summary

## ✅ **New Scripts Created!**

I've created scripts to easily update and restart your local Docker Compose cluster.

---

## 📁 **Files Created**

1. **`scripts/restart-docker.ps1`** - PowerShell script (Windows)
2. **`scripts/restart-docker.sh`** - Bash script (Linux/macOS)
3. **`scripts/restart-docker.bat`** - Batch wrapper (Windows CMD)
4. **`scripts/README.md`** - Complete documentation

---

## 🚀 **Quick Start**

### **Windows (PowerShell) - RECOMMENDED**

```powershell
# Quick restart
.\scripts\restart-docker.ps1

# Rebuild images and restart
.\scripts\restart-docker.ps1 -Build

# Clean restart (⚠️ deletes all data)
.\scripts\restart-docker.ps1 -Clean

# Rebuild and show logs
.\scripts\restart-docker.ps1 -Build -Logs
```

### **Windows (Command Prompt)**

```cmd
# Quick restart
.\scripts\restart-docker.bat

# With options (forwards to PowerShell)
.\scripts\restart-docker.bat -Build -Logs
```

### **Linux/macOS**

```bash
# Quick restart
./scripts/restart-docker.sh

# Rebuild images and restart
./scripts/restart-docker.sh --build

# Clean restart (⚠️ deletes all data)
./scripts/restart-docker.sh --clean

# Rebuild and show logs
./scripts/restart-docker.sh --build --logs
```

---

## 🎯 **What The Script Does**

### **Step-by-Step Process:**

1. ✅ **Checks Docker Compose** - Verifies Docker is installed
2. ✅ **Stops containers** - Gracefully stops all running services
3. ✅ **Cleans volumes** (optional) - Removes data if `-Clean` flag used
4. ✅ **Pulls/Builds images** - Updates or rebuilds Docker images
5. ✅ **Starts services** - Launches all services in detached mode
6. ✅ **Shows status** - Displays running containers
7. ✅ **Displays URLs** - Shows access URLs for all services
8. ✅ **Shows logs** (optional) - Tails logs if `-Logs` flag used

---

## 🐳 **Services Managed**

| Service | Description | URL |
|---------|-------------|-----|
| **gateway** | API Gateway (nginx) | <http://localhost:8080> |
| **core-api** | Backend API (FastAPI) | <http://localhost:8000> |
| **web-app** | Frontend (React) | <http://localhost:80> |
| **db** | PostgreSQL Database | localhost:5432 |

---

## ⚙️ **Options**

| Option | PowerShell | Bash | Description |
|--------|-----------|------|-------------|
| **Build** | `-Build` | `--build` | Force rebuild of all Docker images |
| **Clean** | `-Clean` | `--clean` | Remove volumes (⚠️ **deletes all data**) |
| **Logs** | `-Logs` | `--logs` | Show logs after starting |
| **Help** | `-Help` | `--help` | Show help message |

---

## 📊 **Common Use Cases**

### **1. Quick Restart After Code Changes**

```powershell
# If you changed backend code and want to rebuild
.\scripts\restart-docker.ps1 -Build
```

**What happens:**

- Stops containers
- Rebuilds Docker images with your latest code
- Starts services
- Shows status

---

### **2. Fresh Start (Clean Database)**

```powershell
# Start from scratch with empty database
.\scripts\restart-docker.ps1 -Clean
```

**What happens:**

- Stops containers
- **Deletes all database data** (asks for confirmation)
- Pulls latest images
- Starts services with fresh database

⚠️ **WARNING:** This deletes all your data!

---

### **3. Update and Restart**

```powershell
# Pull latest images and restart
.\scripts\restart-docker.ps1
```

**What happens:**

- Stops containers
- Pulls latest images from registry
- Starts services
- Shows status

---

### **4. Debug with Logs**

```powershell
# Rebuild and watch logs
.\scripts\restart-docker.ps1 -Build -Logs
```

**What happens:**

- Stops containers
- Rebuilds images
- Starts services
- **Tails logs** (press Ctrl+C to exit)

---

## 🎨 **Features**

### **Colored Output**

- ✅ **Green** - Success messages
- ⚠️ **Yellow** - Warnings and info
- ❌ **Red** - Errors
- 🔵 **Cyan** - Headers and sections

### **Progress Indicators**

```text
Step 1: Stopping running containers...
✓ Containers stopped

Step 2: Building Docker images...
✓ Images built

Step 3: Starting services...
✓ Services started
```

### **Service Status**

```text
NAME                  IMAGE                  STATUS
gateway               spearmint-gateway      Up 2 seconds
core-api              spearmint-core-api     Up 3 seconds
web-app               spearmint-web-app      Up 2 seconds
db                    postgres:15-alpine     Up 3 seconds
```

### **Access URLs**

```text
Access your services at:
  - API Gateway:     http://localhost:8080
  - API Docs:        http://localhost:8080/api/docs
  - Frontend:        http://localhost:80
  - Core API:        http://localhost:8000
  - PostgreSQL:      localhost:5432
```

---

## 📚 **Documentation**

Full documentation available in:

- **`scripts/README.md`** - Complete script documentation
- **`docker-compose.yml`** - Service definitions
- **`docs/FULLSTACK_QUICKSTART.md`** - Development setup guide

---

## 🔧 **Manual Commands (If Needed)**

If you prefer manual control:

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Rebuild
docker compose build --no-cache

# Restart specific service
docker compose restart core-api
```

---

## ⚠️ **Important Notes**

### **Data Persistence**

- **SQLite data:** Stored in `./database/data/` (mounted volume)
- **PostgreSQL data:** Stored in Docker volume `postgres_data`
- **Using `-Clean` deletes ALL data** - use with caution!

### **Hot Reload**

- **Backend (core-api):** ✅ Code changes auto-reload (volume mounted)
- **Frontend (web-app):** ❌ Requires rebuild (production build in container)
  - For frontend dev, use `npm run dev` locally instead

---

## ✅ **Next Steps**

1. **Try it out:**

   ```powershell
   .\scripts\restart-docker.ps1
   ```

2. **Access your services:**
   - API Gateway: <http://localhost:8080>
   - API Docs: <http://localhost:8080/api/docs>
   - Frontend: <http://localhost:80>

3. **Make changes and rebuild:**

   ```powershell
   .\scripts\restart-docker.ps1 -Build
   ```

---

**The scripts are now committed and pushed to the repository!** 🚀
