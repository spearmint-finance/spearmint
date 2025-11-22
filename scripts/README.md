# Spearmint Scripts

Utility scripts for managing the Spearmint application.

---

## 🐳 Docker Compose Scripts

### `restart-docker.ps1` / `restart-docker.sh` / `restart-docker.bat`

Update and restart the local Docker Compose cluster.

**Quick Start:**

```bash
# Windows (PowerShell)
.\scripts\restart-docker.ps1

# Windows (Command Prompt)
.\scripts\restart-docker.bat

# Linux/macOS
./scripts/restart-docker.sh
```

**Options:**

| Option | Description |
|--------|-------------|
| `-Build` / `--build` | Force rebuild of all Docker images |
| `-Clean` / `--clean` | Remove volumes and perform clean start (⚠️ deletes data) |
| `-Logs` / `--logs` | Show logs after starting services |
| `-Help` / `--help` | Show help message |

**Examples:**

```bash
# Quick restart (pull latest images and restart)
.\scripts\restart-docker.ps1

# Rebuild all images and restart
.\scripts\restart-docker.ps1 -Build

# Clean restart (deletes all data!)
.\scripts\restart-docker.ps1 -Clean

# Rebuild and show logs
.\scripts\restart-docker.ps1 -Build -Logs
```

**What it does:**

1. ✅ Stops all running containers
2. ✅ Optionally removes volumes (if `-Clean` flag used)
3. ✅ Pulls latest images OR rebuilds images (if `-Build` flag used)
4. ✅ Starts all services in detached mode
5. ✅ Shows service status
6. ✅ Displays access URLs
7. ✅ Optionally shows logs (if `-Logs` flag used)

**Services Started:**

| Service | Description | URL |
|---------|-------------|-----|
| `gateway` | API Gateway (nginx) | http://localhost:8080 |
| `core-api` | Backend API (FastAPI) | http://localhost:8000 |
| `web-app` | Frontend (React) | http://localhost:80 |
| `db` | PostgreSQL Database | localhost:5432 |

---

## 📦 Version Management

### `bump_version.py`

Bump the application version across all components.

**Usage:**

```bash
python scripts/bump_version.py <major|minor|patch>
```

**Examples:**

```bash
# Bump patch version (0.0.13 -> 0.0.14)
python scripts/bump_version.py patch

# Bump minor version (0.0.13 -> 0.1.0)
python scripts/bump_version.py minor

# Bump major version (0.0.13 -> 1.0.0)
python scripts/bump_version.py major
```

**What it updates:**

- `version.json` - Central version file
- `core-api/src/financial_analysis/api/main.py` - API version
- `web-app/package.json` - Frontend version
- `cli/pyproject.toml` - CLI version

---

## 🔧 Manual Docker Commands

If you prefer manual control:

### Start Services

```bash
# Start all services
docker compose up -d

# Start specific service
docker compose up -d gateway

# Start with logs
docker compose up
```

### Stop Services

```bash
# Stop all services
docker compose down

# Stop and remove volumes (⚠️ deletes data)
docker compose down -v
```

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f core-api

# Last 100 lines
docker compose logs --tail=100 -f
```

### Rebuild Images

```bash
# Rebuild all images
docker compose build

# Rebuild without cache
docker compose build --no-cache

# Rebuild specific service
docker compose build core-api
```

### Restart Services

```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart core-api
```

### Check Status

```bash
# Show running services
docker compose ps

# Show resource usage
docker compose stats
```

---

## 🚀 Quick Reference

**Most Common Commands:**

```bash
# Quick restart everything
.\scripts\restart-docker.ps1

# Rebuild after code changes
.\scripts\restart-docker.ps1 -Build

# View logs
docker compose logs -f

# Stop everything
docker compose down
```

---

## 📚 Related Documentation

- [Docker Compose File](../docker-compose.yml) - Service definitions
- [Full Stack Quick Start](../docs/FULLSTACK_QUICKSTART.md) - Development setup
- [Architecture](../docs/ARCHITECTURE.md) - System architecture

---

## ⚠️ Important Notes

### Data Persistence

- **SQLite data** is stored in `./database/data/` (mounted volume)
- **PostgreSQL data** is stored in Docker volume `postgres_data`
- Using `-Clean` flag **DELETES ALL DATA** - use with caution!

### Hot Reload

- **Backend (core-api):** Code changes auto-reload (volume mounted)
- **Frontend (web-app):** Requires rebuild to see changes (production build in container)
- For frontend development, use `npm run dev` locally instead of Docker

### Port Conflicts

If ports are already in use:

```bash
# Check what's using port 8080
netstat -ano | findstr :8080

# Kill process (Windows)
taskkill /PID <pid> /F

# Or change ports in docker-compose.yml
```

---

## 🐛 Troubleshooting

**Problem:** "Docker Compose not found"
```bash
# Install Docker Desktop
# https://www.docker.com/products/docker-desktop
```

**Problem:** Services won't start
```bash
# Check logs
docker compose logs

# Check if ports are in use
netstat -ano | findstr :8080
netstat -ano | findstr :8000
```

**Problem:** Database connection errors
```bash
# Restart database service
docker compose restart db

# Or clean restart (⚠️ deletes data)
.\scripts\restart-docker.ps1 -Clean
```

---

**Need help?** Check the [documentation](../docs/) or open an issue.

