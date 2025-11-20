# OpenAPI Specification Generation

The Spearmint Core API uses an automated process to generate its OpenAPI (Swagger) specification. This specification is the "source of truth" for generating our SDKs (Python and TypeScript).

## How it works

The OpenAPI spec is generated directly from the FastAPI application instance. Since FastAPI automatically builds the schema based on Pydantic models and route definitions, we simply need to extract this schema to a JSON file.

### The Generation Script

We use a dedicated script: `core-api/scripts/generate_openapi.py`.

**Usage:**
```bash
cd core-api
python scripts/generate_openapi.py [output_path]
```

**Default Output:** `../sdk/openapi.json`

**Key Features:**
*   **Stdout Suppression:** The script actively suppresses `logging` and `stdout` during the import of the FastAPI app. This prevents startup logs (e.g., "Uvicorn running...") from corrupting the JSON output.
*   **Standalone:** It does not require the server to be running on a port. It imports the app object in memory.

## CI/CD Integration

The specification is generated automatically in GitHub Actions workflow `.github/workflows/sdk-generation.yml`.

1.  **Trigger:** Pushes to `core-api/**`.
2.  **Action:**
    *   Installs dependencies.
    *   Runs `scripts/generate_openapi.py`.
    *   Saves the result to `sdk/openapi.json`.
    *   Feeds this JSON into the **LibLab CLI** to generate client libraries.

## Manual Verification

To verify the spec locally without running the full build:

```bash
cd core-api
python scripts/generate_openapi.py my_spec.json
cat my_spec.json
```
