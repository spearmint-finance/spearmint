# Docker Compose Hot Reload Setup

This document explains how hot reload works in the Docker Compose development environment.

---

## 🔥 **Hot Reload Status**

| Service | Hot Reload | Rebuild Needed? | How It Works |
|---------|-----------|-----------------|--------------|
| **Core API** | ✅ Yes | ❌ No | Volume mount + `--reload` flag |
| **Frontend** | ✅ Yes | ❌ No | Volume mount + Vite dev server |
| **Gateway** | ❌ No | ✅ Yes | Nginx config changes require restart |
| **Database** | N/A | N/A | Data persisted in volume |

---

## 🚀 **Quick Start**

```bash
# First time setup
docker compose build

# Start all services with hot reload
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

---

## 📝 **Making Code Changes**

### **Backend Changes (Python/FastAPI)**

1. **Edit files** in `core-api/src/`
2. **Save the file**
3. **Watch the logs** - API auto-reloads:

  ```bash
  docker compose logs -f core-api
  ```
1. **No rebuild needed!** ✅

**Example:**

```bash
# Edit a file
code core-api/src/financial_analysis/api/routes/persons.py

# Save it - watch the logs
docker compose logs -f core-api
# You'll see: "Reloading..."
```

---

### **Frontend Changes (React/TypeScript)**

1. **Edit files** in `web-app/src/`
2. **Save the file**
3. **Browser auto-refreshes** via Vite HMR
4. **No rebuild needed!** ✅

**Example:**

```bash
# Edit a component
code web-app/src/components/Dashboard/Dashboard.tsx

# Save it - browser updates automatically
# Open: http://localhost:8080
```

---

### **Gateway Changes (nginx.conf)**

1. **Edit** `api-gateway/nginx.conf`
2. **Restart the gateway:**

  ```bash
  docker compose restart gateway
  ```
1. **No full rebuild needed** - just restart

---

### **Dependency Changes**

If you add/remove dependencies, you need to rebuild:

**Backend (Python):**

```bash
# After editing core-api/requirements.txt
docker compose build core-api
docker compose up -d core-api
```

**Frontend (npm):**

```bash
# After editing web-app/package.json
docker compose build web-app
docker compose up -d web-app
```

---

## 🔧 **How It Works**

### **Core API Hot Reload**

**docker-compose.yml:**

```yaml
core-api:
  volumes:
    - ./core-api/src:/app/src  # Mount source code
  command: uvicorn ... --reload  # Enable auto-reload
```

- Source code is **volume mounted**
- Uvicorn watches for file changes
- Automatically reloads on save

---

### **Frontend Hot Reload**

**docker-compose.yml:**

```yaml
web-app:
  build:
    dockerfile: web-app/Dockerfile.dev  # Dev Dockerfile
  volumes:
    - ./web-app/src:/app/src           # Mount source
    - /app/node_modules                # Preserve node_modules
  ports:
    - "5173:5173"                      # Vite dev server
```

**Dockerfile.dev:**

```dockerfile
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

- Runs **Vite dev server** (not production build)
- Source code is **volume mounted**
- Vite HMR via WebSocket
- Gateway proxies WebSocket connections

---

## 🌐 **Access URLs**

| Service | URL | Description |
|---------|-----|-------------|
| **Gateway** | <http://localhost:8080> | Main entry point |
| **API Docs** | <http://localhost:8080/api/docs> | Swagger UI |
| **Frontend** | <http://localhost:8080> | React app (via gateway) |
| **Core API** | <http://localhost:8000> | Direct API access |
| **Frontend Dev** | <http://localhost:5173> | Direct Vite server |

**Recommended:** Use <http://localhost:8080> (through gateway) to match production.

---

## 🐛 **Troubleshooting**

### **Changes Not Reflecting**

1. **Check logs:**

  ```bash
  docker compose logs -f core-api
  docker compose logs -f web-app
  ```

1. **Verify volume mounts:**

  ```bash
  docker compose exec core-api ls -la /app/src
  docker compose exec web-app ls -la /app/src
  ```

1. **Hard refresh browser:** Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

### **Port Already in Use**

```bash
# Stop all containers
docker compose down

# Check what's using the port
netstat -ano | findstr :8080
netstat -ano | findstr :5173

# Kill the process or change ports in docker-compose.yml
```

### **WebSocket Connection Failed**

If Vite HMR isn't working:

1. Check gateway logs: `docker compose logs -f gateway`
2. Verify nginx WebSocket config in `api-gateway/nginx.conf`
3. Restart gateway: `docker compose restart gateway`

---

## 📊 **Performance Tips**

1. **Use WSL2** (Windows) - Much faster file watching
2. **Exclude node_modules** - Already done via volume config
3. **Use .dockerignore** - Prevents copying unnecessary files
4. **Limit log output** - Use `docker compose logs -f --tail=100`

---

## 🎯 **Development Workflow**

```bash
# Morning: Start everything
docker compose up -d

# During development: Just code!
# - Edit backend files → Auto-reload
# - Edit frontend files → Browser updates
# - No manual restarts needed

# Evening: Stop everything
docker compose down

# Weekly: Rebuild to get latest dependencies
docker compose build
docker compose up -d
```

---

## ✅ **Summary**

**You can now develop with Docker Compose and get instant feedback!**

- ✅ **Backend changes** → Auto-reload in ~1 second
- ✅ **Frontend changes** → Browser updates instantly
- ✅ **No rebuilds** needed for code changes
- ✅ **Full production-like environment** with hot reload
