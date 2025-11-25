# Pre-Commit Hook Setup

## Overview

The pre-commit hook now **mimics the CI/CD workflow** exactly, running the same validation scripts that run in GitHub Actions.

## What It Does

### Test 1: OpenAPI Spec Validation (Full Pipeline)

**Script:** `core-api/scripts/api_validation/api_validation.py --file sdk/openapi.json`

**What it validates:**
1. ✅ **Structural Validation** - OpenAPI 3.0 schema compliance
2. ✅ **Bundling External Refs** - Resolves $ref references
3. ✅ **Spectral Linting** - 100+ Google API Design rules (if Spectral CLI installed)
4. ✅ **Post-Bundle Validation** - Validates bundled spec

**Requirements:**
- Python 3.11+
- `openapi-spec-validator` package (installed via `pip install -r core-api/requirements.txt`)
- `@stoplight/spectral-cli` package (installed via `npm install` from repository root)

**Note:** If Spectral CLI is not installed, the script will skip Spectral linting with a warning and continue with other validation steps.

### Test 2: OpenAPI Spec Validation (Postman Governance)

**Script:** `dev-tools/validate_spec.py --spec-file sdk/openapi.json --workspace-id $POSTMAN_WORKSPACE_ID`

**What it validates:**
- ✅ Postman governance rules
- ✅ Security rules
- ✅ API design standards

**Requirements:**
- Postman CLI installed
- `POSTMAN_WORKSPACE_ID` environment variable set
- `POSTMAN_API_KEY` environment variable set (for authentication)

**Note:** If `POSTMAN_WORKSPACE_ID` is not set, this test is **skipped** (not failed).

## Setup Instructions

### 1. Install Spectral CLI (for 100+ Google API Design rules)

```bash
# From repository root
npm install
```

This installs `@stoplight/spectral-cli` from `package.json`.

**Verify:**
```bash
npx @stoplight/spectral-cli --version
```

### 2. Install Postman CLI (for governance rules)

**Windows:**
```powershell
# Download and install from:
# https://www.postman.com/downloads/postman-cli/

# Verify installation
postman --version
```

**Linux/macOS:**
```bash
curl -o- "https://dl-cli.pstmn.io/install/linux64.sh" | sh
export PATH="$HOME/.postman/bin:$PATH"

# Verify installation
postman --version
```

### 3. Configure Postman Environment Variables

Create a `.env` file in the repository root:

```bash
POSTMAN_API_KEY=your-api-key-here
POSTMAN_WORKSPACE_ID=your-workspace-id-here
```

**Get your credentials:**
- **API Key:** https://go.postman.co/settings/me/api-keys
- **Workspace ID:** From your Postman workspace URL

**Load environment variables:**

**Windows (PowerShell):**
```powershell
# Load .env file
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
    }
}

# Verify
echo $env:POSTMAN_WORKSPACE_ID
```

**Linux/macOS (Bash):**
```bash
# Load .env file
export $(cat .env | xargs)

# Verify
echo $POSTMAN_WORKSPACE_ID
```

## Running Pre-Commit Tests

### Compact Mode (Default)
```bash
python dev-tools/run_precommit_tests.py
```

**Output:**
```
Running pre-commit tests...
[OK] OpenAPI Spec Validation (Full Pipeline)
[SKIPPED] Postman validation - POSTMAN_WORKSPACE_ID not set

1/1 tests passed
[PASSED] All tests passed
```

### Verbose Mode (Detailed Output)
```bash
python dev-tools/run_precommit_tests.py --verbose
```

**Output:**
```
================================================================================
PRE-COMMIT TEST SUITE
================================================================================
Timestamp: 2025-11-24T23:45:00
Log directory: dev-tools/commit-testing-log
================================================================================

================================================================================
Running: OpenAPI Spec Validation (Full Pipeline)
================================================================================
Starting OpenAPI Validation Pipeline
================================================================================

--- Structural Validation (before) ---
✅ Structural validation passed.

--- Bundling External Refs ---
✅ Bundling completed.

--- Spectral Linting ---
Linting with Spectral: D:\CodingProjects\spearmint\sdk\openapi.json
Using ruleset: D:\CodingProjects\spearmint\core-api\scripts\api_validation\.spectral-google.yaml
✅ Spectral linting passed.

--- Structural Validation (after) ---
✅ Structural validation passed.

================================================================================
Validation Summary
================================================================================
✅ PASS: Structural Validation (before)
✅ PASS: Bundling External Refs
✅ PASS: Spectral Linting
✅ PASS: Structural Validation (after)
================================================================================
✅ All validation steps passed!
================================================================================

[OK] OpenAPI Spec Validation (Full Pipeline)

[SKIPPED] Postman validation - POSTMAN_WORKSPACE_ID not set
To enable: Set POSTMAN_WORKSPACE_ID environment variable

================================================================================
TEST SUMMARY
================================================================================
Total Tests:  2
Passed:       1
Failed:       0
Skipped:      1
================================================================================

[PASSED] All tests passed!
```

## What Happens If Spectral CLI Is Not Installed?

The validation script will output:
```
--- Spectral Linting ---
⚠️ Spectral CLI not found. Linting skipped.
Install with: npm install -g @stoplight/spectral-cli
```

The test will **continue** and **pass** (non-fatal), but you won't get the 100+ Google API Design rule checks.

## What Happens If Postman Is Not Configured?

The Postman validation test will be **skipped** (not failed):
```
[SKIPPED] Postman validation - POSTMAN_WORKSPACE_ID not set
```

## Troubleshooting

### Spectral CLI not found
```bash
# Install from repository root
npm install

# Verify
npx @stoplight/spectral-cli --version
```

### Postman CLI not found
```bash
# Windows: Download from https://www.postman.com/downloads/postman-cli/
# Linux/macOS:
curl -o- "https://dl-cli.pstmn.io/install/linux64.sh" | sh
export PATH="$HOME/.postman/bin:$PATH"
```

### POSTMAN_WORKSPACE_ID not set
```bash
# Create .env file with your credentials
# Then load it (see "Configure Postman Environment Variables" above)
```

### Tests failing
```bash
# Run with verbose output to see details
python dev-tools/run_precommit_tests.py --verbose

# Check test logs
cat dev-tools/commit-testing-log/latest_report.md
```

