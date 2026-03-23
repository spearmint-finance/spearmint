# Contributing to Spearmint

Thank you for your interest in contributing to Spearmint! This guide will help you get set up and start contributing.

## Quick Start

### Docker (Recommended)

```bash
git clone https://github.com/spearmint-finance/spearmint.git
cd spearmint
cp .env.example .env
docker-compose up -d
```

Services will be available at:
- **Frontend:** http://localhost:7173
- **API Gateway:** http://localhost:7080
- **API Docs (Swagger):** http://localhost:7080/docs

### Local Development

```bash
# Backend
cd core-api
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run_api.py  # http://localhost:8000

# Frontend (separate terminal)
cd web-app
npm install
npm run dev  # http://localhost:5173
```

See `docs/LOCAL_DEVELOPMENT_QUICKSTART.md` for detailed setup instructions.

## Project Structure

```
spearmint/
├── core-api/          # FastAPI backend (Python 3.10+, SQLAlchemy 2.0)
├── web-app/           # React frontend (TypeScript, Material-UI, Vite)
├── api-gateway/       # API gateway
├── marketing-site/    # Next.js marketing site
├── mcp-server/        # MCP server (TypeScript)
├── docs/              # Architecture & API documentation
├── product/           # PRDs and roadmap
├── scripts/           # Development scripts
└── docker-compose.yml
```

## Development Workflow

1. **Fork** the repository and create a feature branch from `main`
2. **Make changes** — keep PRs focused on a single concern
3. **Test locally** — run `npm run test:e2e` in `web-app/` for E2E tests
4. **Lint** — run `npm run lint` in the relevant package
5. **Open a PR** against `main` with a clear description of what changed and why

### Useful Commands

| Directory | Command | Description |
|-----------|---------|-------------|
| `web-app/` | `npm run dev` | Start frontend dev server |
| `web-app/` | `npm run build` | Production build |
| `web-app/` | `npm run lint` | ESLint check |
| `web-app/` | `npm run test:e2e` | Run Playwright E2E tests |
| `web-app/` | `npm run test:e2e:headed` | Run tests with browser visible |
| `core-api/` | `python run_api.py` | Start backend server |
| Root | `npm run validate:all` | Validate OpenAPI spec |

## What to Work On

Check the [GitHub Issues](https://github.com/spearmint-finance/spearmint/issues) for open tasks. Issues labeled `product-directive` have defined acceptance criteria and are ready for implementation. Issues labeled `good first issue` are suitable for newcomers.

See `product/PRIORITIZED-ROADMAP.md` for the current priority order.

## Conventions

- **Backend:** Python with type hints, FastAPI route handlers, SQLAlchemy 2.0 models
- **Frontend:** TypeScript strict mode, functional React components, Material-UI v5
- **Commits:** Use [conventional commits](https://www.conventionalcommits.org/) — `feat(scope):`, `fix(scope):`, `docs(scope):`, etc.
- **PRs:** One concern per PR. Include a description of what changed and why.

## Architecture Notes

- **Database:** SQLite for development, PostgreSQL for production
- **API:** RESTful, documented via OpenAPI/Swagger (auto-generated from FastAPI)
- **Frontend state:** React Query for server state, local state for UI
- **Testing:** Playwright for E2E tests (frontend), Vitest for unit tests (MCP server)

## Getting Help

- Open a [GitHub Issue](https://github.com/spearmint-finance/spearmint/issues) for bugs or feature requests
- Check `docs/` for architecture documentation
- Review `product/feature-planning/` for PRDs on planned features

## License

Spearmint is MIT licensed. By contributing, you agree that your contributions will be licensed under the same license.
