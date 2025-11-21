# Pre-Commit API Validation Setup

This document explains how the pre-commit validation system works and how to set it up on your local machine.

## What Is Pre-Commit Validation?

Pre-commit validation automatically checks your OpenAPI specification for errors **before you commit code**. This catches API problems early and prevents invalid specs from being pushed to the repository.

When you modify the FastAPI application code, the validation system:
1. Generates the OpenAPI specification from your changes
2. Validates the spec is structurally correct (OpenAPI 3.x compliance)
3. Bundles any external `$ref` files
4. Lints the spec against Google API Design rules
5. Re-validates to ensure everything is still valid

If any validation step fails, your commit is blocked and you see the errors.

## Setup (One-Time)

### 1. Install Pre-Commit Framework

```bash
pip install pre-commit
```

### 2. Install Git Hooks

Run this from the repository root:

```bash
pre-commit install
```

This installs a Git hook that runs validation automatically before each commit.

### 3. Verify Installation

```bash
pre-commit run --all-files
```

This runs the validation against all API files to make sure everything is working.

## How It Works

### Automatic (On Every Commit)

Once installed, validation runs **automatically** when you commit changes to API code:

```bash
git commit -m "Update API endpoints"
# ✅ Pre-commit validation runs automatically
# If valid → commit succeeds
# If invalid → commit blocked, see errors below
```

### Manual (Without Committing)

To validate without committing:

```bash
# From repo root
python core-api/scripts/api_validation/api_validation.py --generate
```

## What Gets Validated

### 1. Structural Compliance (openapi-spec-validator)
- OpenAPI 3.x schema rules
- Required fields present
- Valid data types
- Proper nesting and references

### 2. External Reference Resolution (swagger-cli)
- `$ref` files are bundled and resolvable
- Prevents broken links in generated SDKs

### 3. API Design Consistency (Spectral)
- Paths are kebab-case: `/user-accounts`, not `/userAccounts`
- Schemas are PascalCase: `UserAccount`, not `user_account`
- Properties are camelCase: `userId`, not `user_id`
- All operations have `operationId` and `summary`
- Required metadata present

### 4. Validation Sandwich
- The spec is validated before AND after linting
- Ensures linting doesn't corrupt the spec

## When Validation Runs

Validation is **triggered only** when you modify files in:
```
core-api/src/financial_analysis/api/**/*.py
```

This means:
- ✅ Changes to API code → validation runs
- ❌ Changes to tests → validation doesn't run
- ❌ Changes to unrelated code → validation doesn't run

## If Validation Fails

You'll see output like:

```
OpenAPI Validation.................................................Failed
- hook id: openapi-validation
- exit code: 1

❌ Validation Error: Schema 'UserAccount' must be PascalCase
```

**To fix:**
1. Read the error message carefully
2. Update your API code or OpenAPI spec accordingly
3. Retry: `git commit -m "Update API endpoints"`

## If You Need to Skip Validation

Use `--no-verify` to bypass pre-commit checks (use sparingly):

```bash
git commit --no-verify -m "Emergency fix"
```

## Troubleshooting

### "pre-commit not found" on commit

Reinstall the hooks:
```bash
pre-commit install --install-hooks
```

### "Spectral CLI not found" (warning)

This is non-fatal. Spectral linting is optional:
```bash
# Optional: install Spectral globally for full linting
npm install -g @stoplight/spectral-cli
```

Without it, structural validation still runs (most important part).

### Validation is slow

First run may be slow as npm tools download. Subsequent runs are faster. If consistently slow:
```bash
# Run manually to see where time is spent
python core-api/scripts/api_validation/api_validation.py --generate --verbose
```

### I modified code but validation didn't run

Check that your changes are in `core-api/src/financial_analysis/api/`:
```bash
# This will trigger validation
core-api/src/financial_analysis/api/main.py

# This won't
core-api/tests/test_api.py
```

## For Team Leads

### Ensure all developers set up pre-commit:

Add this to your onboarding checklist:
```bash
cd spearmint
pip install pre-commit
pre-commit install
```

### Monitor validation failures in CI/CD:

Pre-commit is local only. For server validation, see `.github/workflows/` (future CI setup).

### Customize rules:

Edit the Spectral ruleset to enforce team standards:
```
core-api/scripts/api_validation/.spectral-google.yaml
```

Changes take effect immediately on next commit.

## Files Involved

| File | Purpose |
|------|---------|
| `.pre-commit-config.yaml` | Defines when/what validation runs |
| `core-api/scripts/api_validation/api_validation.py` | Main validation script |
| `core-api/scripts/api_validation/.spectral-google.yaml` | Google API Design ruleset |
| `core-api/scripts/generate_openapi.py` | Generates spec from FastAPI app |
| `core-api/scripts/api_validation/README.md` | Technical reference |

## Key Takeaways

✅ **Pre-commit validation catches API problems before push**
✅ **Setup is one-time: `pip install pre-commit` + `pre-commit install`**
✅ **Runs automatically on API code commits**
✅ **Can run manually without committing**
✅ **Can skip with `--no-verify` if needed (rare)**

## Questions?

Refer to:
- `core-api/scripts/api_validation/README.md` — Technical details
- `.pre-commit-config.yaml` — Hook configuration
- `sdk/docs/internal/openapi-generation.md` — How the spec is generated
