# Repository Structure and Folder Usage

Authoritative guide for where things live and why. Use this to place new code, docs, tests, and scripts.

---

## Top-Level Folders

- `api-gateway`: Nginx API gateway
  - Config: `nginx.conf`, templating, TLS, headers, caching
  - Run/deploy: Dockerfile, compose/k8s manifests, CI/CD references
  - Docs/tests: Load testing, gateway-specific readmes, troubleshooting

- `cli`: Command-line interface
  - Code: CLI source, packaging
  - Docs: usage, commands reference, examples
  - Tests: unit/integration for CLI behaviors

- `core-api`: Backend API (FastAPI)
  - Code: app, routers, models, services, tasks
  - API validation: spectral, schema checks, openapi generation
  - Deploy: Dockerfile, k8s manifests, environment configs
  - Tests: unit/integration, fixtures, test data
  - Docs: internal architecture, endpoint docs

- `database`: Data layer
  - Schema: `schema/`, migrations, DDL
  - Seeds/data: `seeds/`, `data/`
  - Validation: data checks, linters for SQL
  - Deploy: k8s or infra manifests for DB
  - Docs: schema conventions, migration process

- `dev-tools`: Developer utilities
  - Scripts/tools for local build/run/debug (cross-cutting)
  - SDK generation helpers, restart scripts, local env helpers
  - Docs for developer workflows

- `docs`: Product documentation
  - `external/`: user-facing, publishable
  - `internal/`: team-only (development, docker, sdk, process)
  - Keep root `docs/` as the entry point with indexes

- `logs`: Centralized logs
  - Organize by component (e.g., `core-api/`, `web-app/`)
  - Add `.gitignore` to avoid committing log files

- `product`: Product management
  - Specs, roadmaps, gap analysis, requirements

- `scripts`: Cross-repo orchestration (optional)
  - Use for overarching scripts that touch multiple parts
  - Prefer placing service-specific scripts in their respective folders
  - Many developer-local scripts belong in `dev-tools`

- `sdk`: SDK generation and outputs
  - OpenAPI spec, generator configs
  - Generated outputs (TypeScript/Python)
  - Publishing workflows to npm and usage docs

- `web-app`: Frontend app (Vite/React)
  - Code, tests, validation, deployment manifests
  - Docs for setup, development, and testing

---

## Conventions

- Docs placement:
  - Internal developer docs → `docs/internal/<area>/...`
  - External/publishable docs → `docs/external/...`
- Scripts placement:
  - Service-specific → in that service folder
  - Cross-cutting developer helpers → `dev-tools`
  - Cross-repo orchestration/ops → `scripts`
- Tests co-located per project (`tests/` inside each service)
- Use lowercase, hyphenated filenames for docs (e.g., `hot-reload.md`)

---

## Notes

- This document reflects the current desired conventions; propose updates via PR if needs evolve.
