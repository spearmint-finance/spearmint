# OpenAPI Validation

This directory contains tools for validating OpenAPI specifications.

## Quick Start

### Setup Pre-Commit Hook

Pre-commit hooks automatically validate the OpenAPI spec before each commit:

```bash
# 1. Install pre-commit (one-time)
pip install pre-commit

# 2. Install the git hook (one-time, run from repo root)
pre-commit install

# 3. Commit as normal - validation runs automatically
git commit -m "Update API"
```

### Manual Validation

Validate without committing:

```bash
# Generate and validate the spec
python core-api/scripts/api_validation/api_validation.py --generate

# Validate an existing spec file
python core-api/scripts/api_validation/api_validation.py --file sdk/openapi.json

# Fetch spec from a running server and validate
python core-api/scripts/api_validation/api_validation.py --fetch http://localhost:8000/api/openapi.json
```

## What Gets Validated

### 1. **Structural Validation** (openapi-spec-validator)
   - OpenAPI 3.x schema compliance
   - Required fields present
   - Valid data types
   - Proper structure

### 2. **Bundling** (swagger-cli)
   - External `$ref` files are resolved and bundled
   - Prevents broken references in generated SDKs

### 3. **Style/Design Linting** (Spectral)
   - Google API Design rules (`core-api/scripts/api_validation/.spectral-google.yaml`)
   - Enforces consistency across endpoints
   - Examples:
     - Paths must be kebab-case: `/user-accounts` not `/userAccounts`
     - Schemas must be PascalCase: `UserAccount` not `user_account`
     - Properties must be camelCase: `userId` not `user_id`
     - All operations need `operationId`
     - All operations need `summary`

### 4. **Re-Validation After Changes**
   - Ensures bundling/linting doesn't corrupt the spec
   - Validation-sandwich pattern prevents silent failures

## Setup Details

### `.pre-commit-config.yaml`

Located at the repo root, this file configures:
- **Trigger**: When API code changes (files in `core-api/src/financial_analysis/api/`)
- **Action**: Automatically runs `api_validation.py --generate`
- **Failure**: Blocks commit if validation fails
- **Stage**: Runs before commit (can be overridden with `git commit --no-verify`)

### `api_validation.py`

Main validation script with features:
- Cross-platform (Windows, macOS, Linux)
- Multiple input modes: fetch from URL, generate locally, or validate existing file
- Orchestrates all validation steps
- Structured logging with progress indicators
- Continues on non-fatal warnings (e.g., Spectral CLI not installed)
- Exit code 0 = success, 1 = failure (respects Unix conventions)

### `.spectral-google.yaml`

Spectral ruleset enforcing Google API Design patterns:

| Rule | Severity | Description |
|------|----------|-------------|
| `paths-kebab-case` | error | Paths like `/user-accounts`, `/pet-stores` |
| `operation-operationId-unique` | error | All operations must have unique `operationId` |
| `operation-summary` | error | All operations must have `summary` |
| `schema-names-pascal-case` | error | Schemas like `UserAccount`, `PetStore` |
| `schema-properties-camelCase` | warn | Properties like `userId`, `petName` |
| `parameter-names-camelCase` | warn | Parameters like `userId`, `petName` |
| `request-body-content-type` | error | POST/PUT/PATCH must specify `Content-Type` |
| `response-content-type` | warn | Responses should specify `Content-Type` |
| `info-version` | error | API must have version (e.g., `1.0.0`) |
| `info-contact` | warn | API should have contact information |
| `security-defined` | warn | Recommend defining `securitySchemes` |
| `operation-responses` | error | All operations must define responses |

## Dependencies

Pre-commit hooks require these Python packages (should be in `core-api/requirements.txt`):

- `requests` — fetching specs from remote URLs
- `openapi-spec-validator` — structural validation
- `pre-commit` — hooks infrastructure

Optional npm tools (installed globally or via npx):

- `@apidevtools/swagger-cli` — bundling external refs
- `@stoplight/spectral-cli` — linting with Spectral rules

## Troubleshooting

### Hook not running?

```bash
# Reinstall the hook
pre-commit install --install-hooks

# Run manually to test
pre-commit run --all-files
```

### "Spectral CLI not found"

This is non-fatal. The hook continues with a warning:

```bash
# Optional: install Spectral globally
npm install -g @stoplight/spectral-cli

# Or use npx (slower, runs from npm each time)
npx @stoplight/spectral-cli lint sdk/openapi.json --ruleset core-api/scripts/api_validation/.spectral-google.yaml
```

### Bypass validation for emergency commits

```bash
# Skip all pre-commit hooks
git commit --no-verify -m "Emergency fix"

# Or skip just the OpenAPI hook (not straightforward; use --no-verify)
```

### Want to run validation manually before committing?

```bash
# From repo root
python core-api/scripts/api_validation/api_validation.py --generate --verbose
```

## Next Steps

### CI/CD Integration

Add GitHub Actions workflow (`.github/workflows/openapi-validate.yml`) to:
- Fetch spec from running API on each PR
- Fail the build if validation fails
- Report linting issues as PR comments

### Custom Rules

To modify Spectral rules:

1. Edit `core-api/scripts/api_validation/.spectral-google.yaml`
2. Update rule severity or disable rules as needed
3. Rules take effect immediately on next commit

### Diff Risk Analysis

Monitor dangerous changes (schema renames, path deletions) that might break SDKs. Future enhancement: Python script to detect and flag these.

## References

- [OpenAPI Spec Validator](https://github.com/schemathesis/openapi-spec-validator)
- [Spectral Rules](https://docs.stoplight.io/docs/spectral/674b27b261c3c-rules)
- [Pre-commit Framework](https://pre-commit.com/)
- [Swagger CLI](https://github.com/APIDevTools/swagger-cli)
