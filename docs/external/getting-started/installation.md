# Installation

Spearmint runs as a self-hosted application on your own hardware. This guide covers the quickest way to get started.

## Prerequisites

- **Docker** and **Docker Compose** installed on your system
- A modern web browser
- Your bank export files (CSV or Excel format)

## Quick Start (Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/spearmint-finance/spearmint.git
cd spearmint
```

### 2. Start the Application

```bash
docker-compose up -d
```

This starts:
- **Backend API** on `http://localhost:8000`
- **Frontend Web App** on `http://localhost:5173`
- **SQLite Database** (stored in a Docker volume)

### 3. Access Spearmint

Open your browser and navigate to:

```
http://localhost:5173
```

You'll see an empty dashboard ready for your first import.

---

## Alternative: Development Setup

If you want to run Spearmint without Docker (for development or customization):

### One-Command Setup

```bash
# Windows (PowerShell)
.\scripts\setup-local-dev.ps1

# Linux/macOS
./scripts/setup-local-dev.sh
```

This automated script:
- Creates a Python virtual environment
- Installs all backend dependencies
- Initializes the database
- Installs frontend dependencies
- Generates and links the SDK

### Start the Servers

After setup, start the development servers:

```bash
# Terminal 1 - Backend API
.\scripts\start_api.ps1      # Windows
./scripts/start_api.sh       # Linux/macOS
# API runs on http://localhost:8000

# Terminal 2 - Frontend
cd web-app
npm run dev
# Frontend runs on http://localhost:5173
```

---

## Verifying Your Installation

### Check the API

Visit the API documentation:

```
http://localhost:8000/api/docs
```

You should see the Swagger UI with all available endpoints.

### Check the Frontend

Visit the web application:

```
http://localhost:5173
```

You should see the Spearmint dashboard.

---

## What's Next?

Your Spearmint instance is ready! Next steps:

1. **[Import your first bank file](first-import.md)** — Get your transaction data into Spearmint
2. **[Understand accounts](../concepts/accounts.md)** — Set up your financial accounts
3. **[Learn about classifications](../concepts/classifications.md)** — See how Spearmint calculates accurately

---

## Troubleshooting

### Port Already in Use

If port 8000 or 5173 is already in use, you can modify the ports in:
- `docker-compose.yml` for Docker setup
- `.env` files for development setup

### Database Reset

To start fresh with an empty database:

```bash
# Docker
docker-compose down -v
docker-compose up -d

# Development
rm core-api/financial_analysis.db
python -m src.financial_analysis.database.init_db
```

### Need Help?

- Check the [FAQ](../reference/faq.md)
- Open an issue on [GitHub](https://github.com/spearmint-finance/spearmint/issues)

