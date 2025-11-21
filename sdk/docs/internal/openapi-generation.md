# OpenAPI generation and regeneration (internal)

This document captures how the Financial Analysis project's OpenAPI specification is generated, customized, and exported. It is intended for internal developers and CI engineers.

## Overview
- The project uses FastAPI which auto-generates OpenAPI from registered routes and Pydantic models.
- The app overrides `app.openapi` with a custom generator (`custom_openapi`) that post-processes FastAPI's output.
- A script is provided to programmatically export the generated spec to `sdk/openapi.json` for SDK generation and other consumers.

## Key files
- `core-api/src/financial_analysis/api/main.py` — creates the `FastAPI` app, sets `docs_url`, `openapi_url`, and overrides `app.openapi` with `custom_openapi`.
- `core-api/src/financial_analysis/api/openapi_config.py` — provides `get_openapi_config()` (title/version/description/tags/servers) and `customize_openapi_schema(...)` (operationId generation, securitySchemes, common responses, `externalDocs`).
- `core-api/scripts/generate_openapi.py` — imports the `app`, calls `app.openapi()`, and writes the JSON to disk (default: `../sdk/openapi.json`).
- `sdk/openapi.json` — the generated OpenAPI artifact currently present in the repo.

## How the spec is produced (details)
1. At runtime, FastAPI inspects all included routers, endpoint decorators, path params, and Pydantic models to build an OpenAPI dict via `fastapi.openapi.utils.get_openapi(...)`.
2. The project defines `custom_openapi()` in `openapi_config.py` which:
   - Calls `get_openapi(...)` with app metadata (title, version, description, routes, tags, servers).
   - Iterates `paths` and assigns an `operationId` when missing (constructed from HTTP method + cleaned path).
   - Ensures `components.securitySchemes` includes `bearerAuth` and `apiKey` placeholders.
   - Adds common response examples under `components.responses`.
   - Adds `externalDocs` linking to the repo docs.
3. `custom_openapi()` caches the final spec on `app.openapi_schema` and returns it. The running server exposes the spec at `/api/openapi.json` by default.

## How to regenerate the OpenAPI JSON (local)

1) Using the provided script (preferred for reproducible artifact):

```powershell
# from repo root
python .\core-api\scripts\generate_openapi.py
# or specify output path
python .\core-api\scripts\generate_openapi.py .\sdk\openapi.json
```

This imports `src.financial_analysis.api.main:app`, calls `app.openapi()`, and writes the JSON. The default output is `sdk/openapi.json`.

2) Serve the app and fetch the live spec (good for verifying runtime behavior):

```powershell
# start dev server
uvicorn src.financial_analysis.api.main:app --host 0.0.0.0 --port 8000 --reload

# fetch generated spec to a file
Invoke-RestMethod "http://localhost:8000/api/openapi.json" -OutFile .\generated-openapi.json
```

3) From inside a container: the app entrypoint is `src.financial_analysis.api.main:app` in `core-api/Dockerfile`, so the container will expose `/api/openapi.json` on the configured port. Use `docker` or `docker-compose` to fetch the file similarly.

## Where SDKs and tools point
- `sdk/liblab.config.json` and SDK output manifests reference `./openapi.json` in the `sdk` folder. The `generate_openapi.py` script writes to `../sdk/openapi.json` so tooling can consume a stable file.

## Notes & gotchas
- OperationId consistency: `customize_openapi_schema` only creates `operationId` values when missing. If some endpoints already have explicit IDs (e.g., derived from function names), you may end up with mixed naming styles. Consider standardizing operationId values if downstream generators require consistent naming.
- Import-time side effects: `generate_openapi.py` imports the full `app`. Import-time code, middleware, or settings (DB connections, heavy init) will run during spec generation. Ensure environment variables and side effects are safe when running the script in CI.
- External `$ref` resolution: if your schemas reference external files, tools like Spectral may require bundling (`swagger-cli bundle` or similar) before linting or codegen.
- Security definitions vs. enforcement: `securitySchemes` are added as placeholders but endpoints are not yet annotated with `security` requirements — the spec advertises possible schemes but does not enforce them on operations.

## Recommended regeneration workflow (CI-friendly)
1. CI job fetches the running service's `/api/openapi.json` (or runs `python generate_openapi.py` inside the codebase) and writes it to a workspace file.
2. If external refs exist, run a bundling step to produce a single-file spec.
3. Run linters (e.g., `npx @stoplight/spectral-cli lint <spec> --ruleset .spectral-google.yaml`) and fail the job on errors.
4. Use the linted spec to generate SDKs or publish to artifact storage.

## Quick commands (PowerShell) for linting a fetched spec

```powershell
# fetch to file
Invoke-RestMethod "http://localhost:8000/api/openapi.json" -OutFile .\generated-openapi.json

# lint with Spectral (requires @stoplight/spectral-cli installed or use npx)
npx @stoplight/spectral-cli lint .\generated-openapi.json --ruleset .spectral-google.yaml --fail-severity error
```

## Next steps (suggested)
- Add `scripts/fetch-and-lint.ps1` to automate fetch + spectral lint (can be reused in CI).
- Add a GitHub Actions workflow `ci/openapi-lint.yml` that fetches the spec (using a service URL or by running the app), bundles if required, and runs Spectral. Use repository secrets for any credentials.
- Optionally standardize `operationId` generation strategy to force consistent names across endpoints.

## References (source files)
- `core-api/src/financial_analysis/api/main.py`
- `core-api/src/financial_analysis/api/openapi_config.py`
- `core-api/scripts/generate_openapi.py`
- `sdk/openapi.json`

---
Document generated by developer tooling on: 2025-11-21
