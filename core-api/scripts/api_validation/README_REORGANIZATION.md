# API Validation Reorganization Summary

## Overview

All API validation tools have been consolidated into `core-api/scripts/api_validation/` for better organization and clarity.

## What Changed

### Files Moved

| Old Location | New Location | Purpose |
|--------------|--------------|---------|
| `dev-tools/validate_spec.py` | `core-api/scripts/api_validation/postman_validation.py` | Postman governance validation |
| `dev-tools/run_precommit_tests.py` | `core-api/scripts/api_validation/run_all_validations.py` | Validation test orchestrator |
| `dev-tools/commit-testing-log/` | `core-api/scripts/api_validation/logs/` | Validation test logs |

### Files Updated

| File | Changes |
|------|---------|
| `.pre-commit-config.yaml` | Updated paths to new script locations |
| `.github/workflows/deploy-and-version.yml` | Updated Postman validation path |
| `core-api/.env.example` | Added Postman API credentials section |

### New Structure

```
core-api/
├── scripts/
│   └── api_validation/
│       ├── api_validation.py              # Structural + Spectral validation
│       ├── postman_validation.py          # Postman governance validation (MOVED)
│       ├── run_all_validations.py         # Test orchestrator (MOVED)
│       ├── .spectral-google.yaml          # Spectral ruleset
│       ├── logs/                          # Validation logs (NEW)
│       │   ├── latest_report.json
│       │   ├── latest_report.md
│       │   └── test_report_*.json
│       └── README.md                      # Validation documentation
├── .env.example                           # Includes validation credentials
└── .env                                   # Your local credentials (gitignored)
```

## Why This Organization?

### Before (Confusing)
- ❌ Validation split between `core-api/scripts/` and `dev-tools/`
- ❌ Unclear where `.env` belongs
- ❌ Hard to find all validation-related files

### After (Clear)
- ✅ All validation in one place: `core-api/scripts/api_validation/`
- ✅ Clear ownership: `.env` is for core-api validation
- ✅ Logical grouping: Everything about validating the API spec is together

## How to Use

### Run All Validations

```bash
# From repository root
python core-api/scripts/api_validation/run_all_validations.py

# Verbose mode
python core-api/scripts/api_validation/run_all_validations.py --verbose
```

### Run Individual Validations

```bash
# Structural + Spectral validation
python core-api/scripts/api_validation/api_validation.py --file sdk/openapi.json

# Postman governance validation
python core-api/scripts/api_validation/postman_validation.py --spec-file sdk/openapi.json
```

### Configure Environment Variables

1. Copy the template:
   ```bash
   cp core-api/.env.example core-api/.env
   ```

2. Edit `core-api/.env` and add your credentials:
   ```bash
   POSTMAN_API_KEY=your-api-key-here
   POSTMAN_WORKSPACE_ID=your-workspace-id-here
   ```

3. Load environment variables:
   
   **Windows (PowerShell):**
   ```powershell
   Get-Content core-api/.env | ForEach-Object {
       if ($_ -match '^([^=]+)=(.*)$') {
           [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
       }
   }
   ```
   
   **Linux/macOS (Bash):**
   ```bash
   export $(cat core-api/.env | xargs)
   ```

## Pre-Commit Hooks

Pre-commit hooks automatically run validation before commits. They now use the new paths:

```bash
# Install pre-commit (one-time)
pip install pre-commit
pre-commit install

# Hooks will run automatically on commit
git commit -m "Your message"

# Or run manually
pre-commit run --all-files
```

## CI/CD Integration

The GitHub Actions workflow has been updated to use the new paths:

```yaml
# .github/workflows/deploy-and-version.yml
- name: Validate spec against Postman governance & security rules
  run: |
    python core-api/scripts/api_validation/postman_validation.py \
      --spec-file sdk/openapi.json \
      --workspace-id "${{ secrets.POSTMAN_WORKSPACE_ID }}" \
      --fail-severity ERROR
```

## Migration Guide

If you have local scripts or documentation referencing the old paths:

### Update Script Paths

| Old Path | New Path |
|----------|----------|
| `python dev-tools/validate_spec.py` | `python core-api/scripts/api_validation/postman_validation.py` |
| `python dev-tools/run_precommit_tests.py` | `python core-api/scripts/api_validation/run_all_validations.py` |
| `dev-tools/commit-testing-log/` | `core-api/scripts/api_validation/logs/` |

### Update Environment Variables

Move your `.env` file from repository root to `core-api/.env`:

```bash
# If you have .env at root
mv .env core-api/.env
```

## Documentation

- **Main README:** `core-api/scripts/api_validation/README.md`
- **Pre-commit Setup:** `dev-tools/docs/PRE_COMMIT_HOOK_SETUP.md` (needs update)
- **Validation Guide:** `dev-tools/docs/PRE_COMMIT_VALIDATION.md` (needs update)
- **Implementation Plan:** `dev-tools/docs/VALIDATION_SETUP_IMPLEMENTATION_PLAN.md` (needs update)

## Next Steps

1. ✅ Files moved and paths updated
2. ✅ CI/CD workflow updated
3. ✅ Pre-commit config updated
4. ✅ Validation tested and working
5. ⏳ Update documentation files (in progress)
6. ⏳ Commit and push changes

## Questions?

See the main validation documentation at `core-api/scripts/api_validation/README.md`

