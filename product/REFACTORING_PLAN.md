# Spearmint Refactoring Plan

## 1. Executive Summary
This document outlines the plan to refactor the `financial-analysis` project into **Spearmint**, a modular **Monorepo** architecture hosted under the **`spearmint-finance`** GitHub organization.

We will achieve **strict logical and deployment isolation** (Microservices style) while maintaining the developer velocity and atomic commits of a single repository.

## 2. Target Architecture (Monorepo)

All components reside in a single repository. Each component is a self-contained "Package" with its own Dockerfile, tests, and configuration.

```text
spearmint/ (Root of Git Repo)
├── api-gateway/          # Service: Gateway
├── core-api/             # Service: API
├── web-app/              # Service: Frontend
├── cli/                  # Tool: Admin CLI
├── sdk/                  # Libraries: Python/TS Clients
├── database/             # Infra: DB Schema & Seeds
└── infra/                # Infra: Shared K8s & Dev Tools
```

## 3. Standard Component Structure
To maintain the "MemNexus-like" rigor, every service component (`core-api`, `web-app`, `api-gateway`) will follow this strict internal layout:

```text
[component-name]/
├── src/                  # Source code
├── tests/                # Unit & Integration tests
├── k8s/                  # Helm charts / K8s manifests for THIS service
├── docs/                 # Component documentation
├── scripts/              # Build/Run scripts
├── Dockerfile            # Deployment definition
└── README.md             # Entry point
```

## 4. Component Breakdown

### 4.1. Core API (`core-api`)
*   **Role:** The Logic Hub. Standalone Service.
*   **Stack:** Python (FastAPI), SQLAlchemy, Pandas.
*   **Constraint:** The only service that connects to the Database.

### 4.2. Web App (`web-app`)
*   **Role:** The User Interface.
*   **Stack:** React, Vite, TypeScript.
*   **Constraint:** Talks only to API Gateway.

### 4.3. CLI (`cli`)
*   **Role:** Admin Tool.
*   **Stack:** Python (Typer).
*   **Constraint:** Talks only to Core API (via SDK).

### 4.4. Database (`database`)
*   **Role:** Data Persistence.
*   **Content:**
    *   `schema/` (Alembic Migrations)
    *   `seeds/` (Initial Data)
    *   `k8s/` (Postgres Deployment)

### 4.5. API Gateway (`api-gateway`)
*   **Role:** Entry Point.
*   **Stack:** Nginx.
*   **Content:** Nginx Config, Dockerfile.

## 5. Implementation Plan (Phase 1)

1.  **Create Root:** `spearmint/`
2.  **Scaffold Components:** Create `core-api`, `web-app`, `cli`, `sdk`, `database`, `api-gateway`.
3.  **Scaffold Internals:** Create `src`, `k8s`, `tests`, `docs` in each.
4.  **Migrate Files:**
    *   `src/financial_analysis` $\rightarrow$ `core-api/src/spearmint`
    *   `frontend/` $\rightarrow$ `web-app/`
    *   `financial_data.db` $\rightarrow$ `database/data/`
    *   Root scripts $\rightarrow$ `core-api/legacy_scripts/`
5.  **Dockerize:** Create Dockerfiles.

### Phase 2: API Expansion
1.  **Audit:** Review `legacy_scripts/` for business logic.
2.  **Refactor:** Move logic from scripts into `core-api` endpoints.

### Phase 3: SDK Generation (LibLab)
1.  **Tooling:** Configure **LibLab** (https://liblab.com).
2.  **Config:** `sdk/liblab.config.json` created targeting `python` and `typescript`.
3.  **Generate:** Run LibLab CLI against `http://localhost:8080/openapi.json`.

### Phase 4: Client Migration
1.  **CLI:** Implement `cli` commands using the generated Python SDK.
2.  **Web App:** Connect `web-app` using the generated TypeScript SDK.

## 6. Immediate Action Items
1.  Execute the directory creation and file movement.
