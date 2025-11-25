# API Validation Setup - Comprehensive Implementation Plan

## Executive Summary

This plan addresses the critical finding that Spectral CLI validation (100+ Google API Design rules) has never been running in any environment. The infrastructure exists but the tools were never installed or properly configured.

**Current State:**
- ❌ Spectral CLI: Not installed, 100+ rules never executed
- ⚠️ Postman Validation: Works in CI/CD only, not locally
- ✅ Basic Structural Validation: Working (openapi-spec-validator)

**Target State:**
- ✅ Spectral CLI: Installed as project dependency, running locally and in CI/CD
- ✅ Postman Validation: Working in both CI/CD and local development
- ✅ Pre-commit hooks: Properly validate with clear error messages
- ✅ Setup automation: One-command setup for all validation tools

---

## Prerequisites

**Required Tools:**
- Node.js 18+ (already required for frontend)
- Python 3.11+ (already required for backend)
- Git (already required)
- Postman CLI (will be installed by setup script)

**Required Secrets/Environment Variables:**
- `POSTMAN_API_KEY` (already in GitHub Secrets)
- `POSTMAN_WORKSPACE_ID` (already in GitHub Secrets, needs local setup)

---

## Implementation Plan

### Phase 1: Add Spectral CLI as Project Dependency

**Files to Create:**
1. `package.json` (repository root)

**Files to Modify:**
1. `.gitignore` (add node_modules to root)

**Commands to Run:**
```bash
# From repository root (d:\CodingProjects\spearmint)
npm init -y
npm install --save-dev @stoplight/spectral-cli@6.11.0
```

**Verification:**
```bash
npx @stoplight/spectral-cli --version
# Should output: 6.11.0 (or similar)
```

**Rollback:**
```bash
git checkout package.json package-lock.json
rm -rf node_modules
```

---

### Phase 2: Update CI/CD Workflows

**Files to Modify:**
1. `.github/workflows/deploy-and-version.yml`

**Current State Analysis:**
The CI/CD workflow already calls `python scripts/api_validation/api_validation.py --file ../sdk/openapi.json` which is designed to run the full validation pipeline including:
1. ✅ Structural validation (OpenAPI schema compliance)
2. ✅ Bundling external refs
3. ✅ **Spectral linting** (100+ Google API Design rules) - **Currently being skipped!**
4. ✅ Post-bundle structural validation

**The Problem:**
The `api_validation.py` script uses `npx @stoplight/spectral-cli` to run Spectral linting, but the CI/CD workflow does NOT install Node.js dependencies. Therefore, Spectral linting silently fails with a warning and continues (non-fatal error handling in the script).

**The Solution:**
Add ONE step to install Node.js dependencies BEFORE the existing validation step. This will install `@stoplight/spectral-cli` from `package.json` (created in Phase 1), and the existing `api_validation.py` call will automatically run Spectral linting.

**Changes Required:**

**Location:** After line 66 (after OpenAPI spec generation, BEFORE "Validate OpenAPI Spec Structure")

**Add new step:**
```yaml
      - name: Install Node.js dependencies for validation
        run: |
          npm install
          echo "✓ Node.js dependencies installed (including Spectral CLI)"
```

**That's it!** The existing validation step at line 67-74 will now automatically run Spectral linting because:
- `api_validation.py` already has Spectral linting in its pipeline (line 258: `("Spectral Linting", self.lint_with_spectral)`)
- It will find `@stoplight/spectral-cli` installed via `npm install`
- It will use the ruleset at `core-api/scripts/api_validation/.spectral-google.yaml`
- It will output detailed results to the GitHub Actions log

**Verification:**
```bash
# Push changes to GitHub
git push origin main

# Check GitHub Actions workflow run
# Look for these lines in the "Validate OpenAPI Spec Structure" step output:
#   --- Spectral Linting ---
#   Linting with Spectral: /path/to/spec
#   Using ruleset: /path/to/.spectral-google.yaml
#   ✅ Spectral linting passed.
#   (or rule violations if any exist)
```

**Expected Output in CI/CD Logs:**
```
Starting OpenAPI Validation Pipeline
================================================================================

--- Structural Validation (before) ---
✅ Structural validation passed.

--- Bundling External Refs ---
✅ Bundling completed.

--- Spectral Linting ---
Linting with Spectral: /home/runner/work/spearmint/spearmint/sdk/openapi.json
Using ruleset: /home/runner/work/spearmint/spearmint/core-api/scripts/api_validation/.spectral-google.yaml
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
```

**Rollback:**
```bash
git checkout .github/workflows/deploy-and-version.yml
```

**Note:** We do NOT need to add a separate Spectral linting step because `api_validation.py` already does it. Adding `npm install` is the ONLY change needed to enable the 100+ Spectral rules that are already coded into the validation pipeline.

---

### Phase 3: Configure Local Postman Workspace ID

**Files to Create:**
1. `dev-tools/setup_postman_local.ps1` (PowerShell script)
2. `dev-tools/setup_postman_local.sh` (Bash script)
3. `.env.example` (repository root - template for environment variables)

**Files to Modify:**
1. `dev-tools/validate_spec.py` (improve error messages)
2. `README.md` (add setup instructions)

**Implementation Details:**

**Step 3.1: Create .env.example template**

**File:** `.env.example` (repository root)
```bash
# Postman API Configuration
# Get your API key from: https://go.postman.co/settings/me/api-keys
POSTMAN_API_KEY=your-api-key-here

# Get workspace ID from Postman workspace URL
# Example: https://www.postman.com/workspace/my-workspace-{workspace-id}
POSTMAN_WORKSPACE_ID=your-workspace-id-here
```

**Step 3.2: Create PowerShell setup script**

**File:** `dev-tools/setup_postman_local.ps1`
```powershell
# Postman Local Setup Script for Windows
# Sets up Postman CLI and environment variables for local validation

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Postman Local Validation Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Postman CLI is installed
Write-Host "Checking Postman CLI..." -ForegroundColor Yellow
try {
    $postmanVersion = postman --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Postman CLI found: $postmanVersion" -ForegroundColor Green
    } else {
        throw "Not found"
    }
} catch {
    Write-Host "[ERROR] Postman CLI not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Install Postman CLI:" -ForegroundColor Yellow
    Write-Host "  1. Download from: https://www.postman.com/downloads/postman-cli/" -ForegroundColor Gray
    Write-Host "  2. Or use winget: winget install Postman.PostmanCLI" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

# Check for .env file
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "[WARNING] .env file not found" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Creating .env from template..." -ForegroundColor Gray
    Copy-Item ".env.example" ".env"
    Write-Host "[OK] Created .env file" -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT: Edit .env and add your Postman credentials:" -ForegroundColor Yellow
    Write-Host "  1. Get API key from: https://go.postman.co/settings/me/api-keys" -ForegroundColor Gray
    Write-Host "  2. Get workspace ID from your Postman workspace URL" -ForegroundColor Gray
    Write-Host ""
    exit 0
}

# Load .env file
Write-Host "Loading .env file..." -ForegroundColor Gray
Get-Content ".env" | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.*)$') {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
}

# Verify environment variables
$apiKey = $env:POSTMAN_API_KEY
$workspaceId = $env:POSTMAN_WORKSPACE_ID

if (-not $apiKey -or $apiKey -eq "your-api-key-here") {
    Write-Host "[ERROR] POSTMAN_API_KEY not configured in .env" -ForegroundColor Red
    Write-Host "Get your API key from: https://go.postman.co/settings/me/api-keys" -ForegroundColor Yellow
    exit 1
}

if (-not $workspaceId -or $workspaceId -eq "your-workspace-id-here") {
    Write-Host "[ERROR] POSTMAN_WORKSPACE_ID not configured in .env" -ForegroundColor Red
    Write-Host "Get workspace ID from your Postman workspace URL" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Environment variables configured" -ForegroundColor Green

# Test Postman authentication
Write-Host ""
Write-Host "Testing Postman authentication..." -ForegroundColor Yellow
try {
    postman login --with-api-key $apiKey 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Postman authentication successful" -ForegroundColor Green
    } else {
        throw "Authentication failed"
    }
} catch {
    Write-Host "[ERROR] Postman authentication failed" -ForegroundColor Red
    Write-Host "Check your POSTMAN_API_KEY in .env" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run validation locally:" -ForegroundColor Cyan
Write-Host "  python dev-tools/validate_spec.py --spec-file sdk/openapi.json" -ForegroundColor Gray
Write-Host ""
```

**Step 3.3: Create Bash setup script**

**File:** `dev-tools/setup_postman_local.sh`
```bash
#!/bin/bash
# Postman Local Setup Script for Linux/macOS
# Sets up Postman CLI and environment variables for local validation

set -e

echo ""
echo "========================================"
echo "  Postman Local Validation Setup"
echo "========================================"
echo ""

# Check if Postman CLI is installed
echo "Checking Postman CLI..."
if command -v postman &> /dev/null; then
    echo "[OK] Postman CLI found: $(postman --version)"
else
    echo "[ERROR] Postman CLI not found"
    echo ""
    echo "Install Postman CLI:"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  curl -o- 'https://dl-cli.pstmn.io/install/linux64.sh' | sh"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  curl -o- 'https://dl-cli.pstmn.io/install/osx_64.sh' | sh"
    fi
    echo ""
    exit 1
fi

# Check for .env file
echo ""
echo "Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "[WARNING] .env file not found"
    echo ""
    echo "Creating .env from template..."
    cp .env.example .env
    echo "[OK] Created .env file"
    echo ""
    echo "IMPORTANT: Edit .env and add your Postman credentials:"
    echo "  1. Get API key from: https://go.postman.co/settings/me/api-keys"
    echo "  2. Get workspace ID from your Postman workspace URL"
    echo ""
    exit 0
fi

# Load .env file
echo "Loading .env file..."
export $(grep -v '^#' .env | xargs)

# Verify environment variables
if [ -z "$POSTMAN_API_KEY" ] || [ "$POSTMAN_API_KEY" = "your-api-key-here" ]; then
    echo "[ERROR] POSTMAN_API_KEY not configured in .env"
    echo "Get your API key from: https://go.postman.co/settings/me/api-keys"
    exit 1
fi

if [ -z "$POSTMAN_WORKSPACE_ID" ] || [ "$POSTMAN_WORKSPACE_ID" = "your-workspace-id-here" ]; then
    echo "[ERROR] POSTMAN_WORKSPACE_ID not configured in .env"
    echo "Get workspace ID from your Postman workspace URL"
    exit 1
fi

echo "[OK] Environment variables configured"

# Test Postman authentication
echo ""
echo "Testing Postman authentication..."
if postman login --with-api-key "$POSTMAN_API_KEY" &> /dev/null; then
    echo "[OK] Postman authentication successful"
else
    echo "[ERROR] Postman authentication failed"
    echo "Check your POSTMAN_API_KEY in .env"
    exit 1
fi

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "You can now run validation locally:"
echo "  python dev-tools/validate_spec.py --spec-file sdk/openapi.json"
echo ""
```

**Verification:**
```bash
# Windows
.\dev-tools\setup_postman_local.ps1

# Linux/macOS
chmod +x dev-tools/setup_postman_local.sh
./dev-tools/setup_postman_local.sh
```

**Rollback:**
```bash
git checkout .env.example dev-tools/setup_postman_local.ps1 dev-tools/setup_postman_local.sh
rm .env  # If created
```

---

### Phase 4: Update Pre-commit Test Runner

**Files to Modify:**
1. `dev-tools/run_precommit_tests.py`

**Changes Required:**

**Location:** Line 50-60 (in `__init__` method, update test definitions)

**Change test command to use environment variables:**
```python
# Get workspace ID from environment
workspace_id = os.environ.get('POSTMAN_WORKSPACE_ID', '')
postman_cmd = f'python dev-tools/validate_spec.py --spec-file sdk/openapi.json --fail-severity WARNING --output-file {output_file}'
if workspace_id:
    postman_cmd += f' --workspace-id {workspace_id}'

{
    'name': 'OpenAPI Spec Validation (Postman)',
    'description': 'Validate OpenAPI spec against Postman governance rules',
    'command': postman_cmd,
    'timeout': 30,
    'required_env': ['POSTMAN_WORKSPACE_ID'],  # New field
    'skip_if_missing_env': True  # New field
}
```

**Location:** Line 100-150 (in `run_test` method)

**Add environment variable checking:**
```python
def run_test(self, test: dict) -> dict:
    """Run a single test and return results."""
    # Check for required environment variables
    if test.get('required_env'):
        missing_env = [var for var in test['required_env'] if not os.environ.get(var)]
        if missing_env and test.get('skip_if_missing_env'):
            return {
                'name': test['name'],
                'success': True,
                'skipped': True,
                'skip_reason': f"Missing environment variables: {', '.join(missing_env)}",
                'output': '',
                'error': '',
                'duration': 0
            }

    # ... rest of existing code
```

**Verification:**
```bash
# Without POSTMAN_WORKSPACE_ID
python dev-tools/run_precommit_tests.py --verbose
# Should show: [SKIPPED] OpenAPI Spec Validation (Postman) - Missing environment variables

# With POSTMAN_WORKSPACE_ID
$env:POSTMAN_WORKSPACE_ID = "your-workspace-id"
python dev-tools/run_precommit_tests.py --verbose
# Should run Postman validation
```

**Rollback:**
```bash
git checkout dev-tools/run_precommit_tests.py
```

---

### Phase 5: Create Unified Setup Script

**Files to Create:**
1. `dev-tools/setup_validation_tools.ps1` (PowerShell)
2. `dev-tools/setup_validation_tools.sh` (Bash)

**Files to Modify:**
1. `scripts/setup-local-dev.ps1` (add validation setup step)
2. `scripts/setup-local-dev.sh` (add validation setup step)
3. `README.md` (add validation setup section)

**Implementation Details:**

**Step 5.1: Create unified PowerShell setup script**

**File:** `dev-tools/setup_validation_tools.ps1`
```powershell
# Unified Validation Tools Setup Script for Windows
# Installs and configures all API validation tools

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  API Validation Tools Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install Spectral CLI
Write-Host "[1/3] Installing Spectral CLI..." -ForegroundColor Yellow
Write-Host ""

if (Test-Path "package.json") {
    Write-Host "  Installing from package.json..." -ForegroundColor Gray
    npm install
    Write-Host "  [OK] Spectral CLI installed" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] package.json not found" -ForegroundColor Red
    Write-Host "  Run this from repository root" -ForegroundColor Yellow
    exit 1
}

# Verify Spectral installation
try {
    $spectralVersion = npx @stoplight/spectral-cli --version 2>&1
    Write-Host "  [OK] Spectral CLI version: $spectralVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Spectral CLI installation failed" -ForegroundColor Red
    exit 1
}

# Step 2: Setup Postman CLI
Write-Host ""
Write-Host "[2/3] Setting up Postman CLI..." -ForegroundColor Yellow
Write-Host ""

.\dev-tools\setup_postman_local.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [WARNING] Postman setup incomplete" -ForegroundColor Yellow
    Write-Host "  You can complete it later by running:" -ForegroundColor Gray
    Write-Host "    .\dev-tools\setup_postman_local.ps1" -ForegroundColor Gray
}

# Step 3: Verify all tools
Write-Host ""
Write-Host "[3/3] Verifying validation tools..." -ForegroundColor Yellow
Write-Host ""

$allGood = $true

# Check Spectral
try {
    npx @stoplight/spectral-cli --version | Out-Null
    Write-Host "  [OK] Spectral CLI" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Spectral CLI not working" -ForegroundColor Red
    $allGood = $false
}

# Check Postman
try {
    postman --version | Out-Null
    Write-Host "  [OK] Postman CLI" -ForegroundColor Green
} catch {
    Write-Host "  [WARNING] Postman CLI not installed" -ForegroundColor Yellow
    Write-Host "    Install from: https://www.postman.com/downloads/postman-cli/" -ForegroundColor Gray
}

# Check environment variables
if ($env:POSTMAN_WORKSPACE_ID) {
    Write-Host "  [OK] POSTMAN_WORKSPACE_ID configured" -ForegroundColor Green
} else {
    Write-Host "  [WARNING] POSTMAN_WORKSPACE_ID not configured" -ForegroundColor Yellow
    Write-Host "    Run: .\dev-tools\setup_postman_local.ps1" -ForegroundColor Gray
}

Write-Host ""
if ($allGood) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run validation:" -ForegroundColor Cyan
    Write-Host "  python dev-tools/run_precommit_tests.py --verbose" -ForegroundColor Gray
} else {
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "  Setup Incomplete" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please fix the errors above and try again" -ForegroundColor Yellow
}
Write-Host ""
```

**Step 5.2: Create unified Bash setup script**

**File:** `dev-tools/setup_validation_tools.sh`
```bash
#!/bin/bash
# Unified Validation Tools Setup Script for Linux/macOS
# Installs and configures all API validation tools

set -e

echo ""
echo "========================================"
echo "  API Validation Tools Setup"
echo "========================================"
echo ""

# Step 1: Install Spectral CLI
echo "[1/3] Installing Spectral CLI..."
echo ""

if [ -f "package.json" ]; then
    echo "  Installing from package.json..."
    npm install
    echo "  [OK] Spectral CLI installed"
else
    echo "  [ERROR] package.json not found"
    echo "  Run this from repository root"
    exit 1
fi

# Verify Spectral installation
if npx @stoplight/spectral-cli --version &> /dev/null; then
    spectral_version=$(npx @stoplight/spectral-cli --version)
    echo "  [OK] Spectral CLI version: $spectral_version"
else
    echo "  [ERROR] Spectral CLI installation failed"
    exit 1
fi

# Step 2: Setup Postman CLI
echo ""
echo "[2/3] Setting up Postman CLI..."
echo ""

./dev-tools/setup_postman_local.sh || {
    echo "  [WARNING] Postman setup incomplete"
    echo "  You can complete it later by running:"
    echo "    ./dev-tools/setup_postman_local.sh"
}

# Step 3: Verify all tools
echo ""
echo "[3/3] Verifying validation tools..."
echo ""

all_good=true

# Check Spectral
if npx @stoplight/spectral-cli --version &> /dev/null; then
    echo "  [OK] Spectral CLI"
else
    echo "  [ERROR] Spectral CLI not working"
    all_good=false
fi

# Check Postman
if command -v postman &> /dev/null; then
    echo "  [OK] Postman CLI"
else
    echo "  [WARNING] Postman CLI not installed"
    echo "    Install from: https://www.postman.com/downloads/postman-cli/"
fi

# Check environment variables
if [ -n "$POSTMAN_WORKSPACE_ID" ]; then
    echo "  [OK] POSTMAN_WORKSPACE_ID configured"
else
    echo "  [WARNING] POSTMAN_WORKSPACE_ID not configured"
    echo "    Run: ./dev-tools/setup_postman_local.sh"
fi

echo ""
if [ "$all_good" = true ]; then
    echo "========================================"
    echo "  Setup Complete!"
    echo "========================================"
    echo ""
    echo "You can now run validation:"
    echo "  python dev-tools/run_precommit_tests.py --verbose"
else
    echo "========================================"
    echo "  Setup Incomplete"
    echo "========================================"
    echo ""
    echo "Please fix the errors above and try again"
fi
echo ""
```

**Step 5.3: Update main setup scripts**

**File:** `scripts/setup-local-dev.ps1`

**Location:** After SDK setup (around line 200), add:

```powershell
# ============================================
# Step 5: Validation Tools Setup
# ============================================
if (-not $SkipValidation) {
    Write-Host "[5/5] Setting up validation tools..." -ForegroundColor Yellow
    Write-Host ""

    .\dev-tools\setup_validation_tools.ps1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  [WARNING] Validation tools setup incomplete" -ForegroundColor Yellow
    }
}
```

**File:** `scripts/setup-local-dev.sh`

**Location:** After SDK setup, add:

```bash
# ============================================
# Step 5: Validation Tools Setup
# ============================================
if [ "$skip_validation" != "true" ]; then
    echo "[5/5] Setting up validation tools..."
    echo ""

    ./dev-tools/setup_validation_tools.sh || {
        echo "  [WARNING] Validation tools setup incomplete"
    }
fi
```

**Verification:**
```bash
# Windows
.\scripts\setup-local-dev.ps1

# Linux/macOS
./scripts/setup-local-dev.sh
```

**Rollback:**
```bash
git checkout scripts/setup-local-dev.ps1 scripts/setup-local-dev.sh
git clean -fd dev-tools/setup_validation_tools.*
```

---

### Phase 6: Update Documentation

**Files to Modify:**
1. `README.md`
2. `dev-tools/docs/PRE_COMMIT_VALIDATION.md`

**Changes Required:**

**File:** `README.md`

**Location:** After "Quick Setup" section (around line 120)

**Add new section:**
```markdown
### 🔍 API Validation Setup

The project includes comprehensive API validation with 100+ rules:
- **Spectral Linting**: Google API Design Guidelines (100+ rules)
- **Postman Governance**: Security and governance rules
- **Structural Validation**: OpenAPI 3.0 schema compliance

**One-command setup:**
```bash
# Windows
.\dev-tools\setup_validation_tools.ps1

# Linux/macOS
./dev-tools/setup_validation_tools.sh
```

**Manual setup:**
1. Install Spectral CLI: `npm install` (from repository root)
2. Setup Postman: `.\dev-tools\setup_postman_local.ps1`
3. Configure `.env` with your Postman credentials

**Run validation:**
```bash
python dev-tools/run_precommit_tests.py --verbose
```

See [VALIDATION_SETUP_IMPLEMENTATION_PLAN.md](dev-tools/docs/VALIDATION_SETUP_IMPLEMENTATION_PLAN.md) for details.
```

**File:** `dev-tools/docs/PRE_COMMIT_VALIDATION.md`

**Location:** Add new section at end

**Add:**
```markdown
## Validation Tools Setup

### Required Tools

1. **Spectral CLI** - Lints OpenAPI specs against Google API Design Guidelines
   - Install: `npm install` (from repository root)
   - Verify: `npx @stoplight/spectral-cli --version`

2. **Postman CLI** - Validates against Postman governance rules
   - Install: See https://www.postman.com/downloads/postman-cli/
   - Verify: `postman --version`

### Environment Variables

Create `.env` file in repository root:
```bash
POSTMAN_API_KEY=your-api-key-here
POSTMAN_WORKSPACE_ID=your-workspace-id-here
```

Get credentials from:
- API Key: https://go.postman.co/settings/me/api-keys
- Workspace ID: From your Postman workspace URL

### Automated Setup

Run the setup script:
```bash
# Windows
.\dev-tools\setup_validation_tools.ps1

# Linux/macOS
./dev-tools/setup_validation_tools.sh
```

### Troubleshooting

**Spectral CLI not found:**
```bash
npm install
npx @stoplight/spectral-cli --version
```

**Postman validation skipped:**
```bash
# Check environment variable
echo $env:POSTMAN_WORKSPACE_ID  # Windows
echo $POSTMAN_WORKSPACE_ID      # Linux/macOS

# Run setup
.\dev-tools\setup_postman_local.ps1  # Windows
./dev-tools/setup_postman_local.sh   # Linux/macOS
```

**Pre-commit tests failing:**
```bash
# Run with verbose output
python dev-tools/run_precommit_tests.py --verbose

# Check test logs
cat dev-tools/commit-testing-log/latest_report.md
```
```

**Verification:**
- Review README.md for clarity
- Verify all links work
- Test setup instructions on clean environment

**Rollback:**
```bash
git checkout README.md dev-tools/docs/PRE_COMMIT_VALIDATION.md
```

---

## Execution Order

**CRITICAL: Follow this exact order to avoid dependency issues**

1. ✅ **Phase 1** - Add Spectral CLI dependency (creates package.json)
2. ✅ **Phase 3** - Configure Postman (creates .env.example and setup scripts)
3. ✅ **Phase 5** - Create unified setup scripts (depends on Phase 1 & 3)
4. ✅ **Phase 4** - Update pre-commit runner (depends on Phase 3 for env vars)
5. ✅ **Phase 2** - Update CI/CD (depends on Phase 1 for package.json)
6. ✅ **Phase 6** - Update documentation (final step, references all previous)

**Why this order:**
- Phase 1 must be first (creates package.json needed by Phase 5)
- Phase 3 must be before Phase 5 (setup scripts call Postman setup)
- Phase 4 needs Phase 3 (uses environment variable patterns)
- Phase 2 should be after Phase 1 (CI/CD uses package.json)
- Phase 6 is last (documents everything)

---

## Testing Strategy

### Unit Testing (Per Phase)

**After Phase 1:**
```bash
npx @stoplight/spectral-cli --version
npx @stoplight/spectral-cli lint sdk/openapi.json --ruleset core-api/scripts/api_validation/.spectral-google.yaml
```

**After Phase 2:**
- Push to GitHub
- Check Actions tab for workflow run
- Verify "Run Spectral Linting" step executes

**After Phase 3:**
```bash
.\dev-tools\setup_postman_local.ps1
python dev-tools/validate_spec.py --spec-file sdk/openapi.json
```

**After Phase 4:**
```bash
python dev-tools/run_precommit_tests.py --verbose
# Should show Spectral and Postman tests running
```

**After Phase 5:**
```bash
.\dev-tools\setup_validation_tools.ps1
# Should complete all setup steps
```

### Integration Testing (Full System)

**Test 1: Clean Environment Setup**
```bash
# Start from clean state
git clean -fdx
git checkout .

# Run full setup
.\scripts\setup-local-dev.ps1

# Verify validation works
python dev-tools/run_precommit_tests.py --verbose
```

**Test 2: Pre-commit Hook**
```bash
# Make a trivial change
echo "# test" >> README.md

# Commit (should trigger validation)
git add README.md
git commit -m "test: verify pre-commit validation"

# Should see Spectral and Postman validation running
```

**Test 3: CI/CD Pipeline**
```bash
# Push to GitHub
git push origin main

# Check GitHub Actions
# Verify all validation steps pass
```

---

## Rollback Strategy

### Emergency Rollback (Revert Everything)

```bash
# Revert all changes
git checkout .
git clean -fdx

# Remove created files
rm -rf node_modules package.json package-lock.json .env

# Restore from backup (if needed)
git stash pop  # If you stashed before starting
```

### Selective Rollback (Per Phase)

**Phase 1 Rollback:**
```bash
git checkout package.json package-lock.json .gitignore
rm -rf node_modules
```

**Phase 2 Rollback:**
```bash
git checkout .github/workflows/deploy-and-version.yml
```

**Phase 3 Rollback:**
```bash
git checkout .env.example
git clean -fd dev-tools/setup_postman_local.*
rm .env
```

**Phase 4 Rollback:**
```bash
git checkout dev-tools/run_precommit_tests.py
```

**Phase 5 Rollback:**
```bash
git checkout scripts/setup-local-dev.ps1 scripts/setup-local-dev.sh
git clean -fd dev-tools/setup_validation_tools.*
```

**Phase 6 Rollback:**
```bash
git checkout README.md dev-tools/docs/PRE_COMMIT_VALIDATION.md
```

---

## Success Criteria

### Phase 1 Success
- ✅ `package.json` exists in repository root
- ✅ `node_modules/@stoplight/spectral-cli` directory exists
- ✅ `npx @stoplight/spectral-cli --version` returns version number
- ✅ Can run: `npx @stoplight/spectral-cli lint sdk/openapi.json --ruleset core-api/scripts/api_validation/.spectral-google.yaml`

### Phase 2 Success
- ✅ GitHub Actions workflow includes "Install Node.js dependencies" step
- ✅ GitHub Actions workflow includes "Run Spectral Linting" step
- ✅ Workflow run shows Spectral linting executing (check Actions tab)
- ✅ Spectral output shows rule violations (if any exist in spec)

### Phase 3 Success
- ✅ `.env.example` file exists with template
- ✅ `dev-tools/setup_postman_local.ps1` script exists and runs
- ✅ `dev-tools/setup_postman_local.sh` script exists and runs
- ✅ Running setup script creates `.env` file
- ✅ Can authenticate with Postman CLI using credentials from `.env`

### Phase 4 Success
- ✅ Pre-commit tests check for required environment variables
- ✅ Tests skip gracefully when env vars missing (with clear message)
- ✅ Tests run when env vars present
- ✅ Verbose output shows which tests were skipped and why

### Phase 5 Success
- ✅ `dev-tools/setup_validation_tools.ps1` script exists and runs
- ✅ `dev-tools/setup_validation_tools.sh` script exists and runs
- ✅ Running script installs Spectral CLI
- ✅ Running script sets up Postman CLI
- ✅ Running script verifies all tools installed correctly
- ✅ Main setup scripts (`scripts/setup-local-dev.*`) call validation setup

### Phase 6 Success
- ✅ README.md includes validation setup section
- ✅ PRE_COMMIT_VALIDATION.md includes troubleshooting guide
- ✅ All documentation links work
- ✅ Instructions are clear and complete

### Overall Success
- ✅ **Local Development**: Running `python dev-tools/run_precommit_tests.py --verbose` shows:
  - ✅ Spectral linting executing with 100+ rules
  - ✅ Postman governance validation executing
  - ✅ All tests passing (or showing expected violations)

- ✅ **CI/CD**: GitHub Actions workflow shows:
  - ✅ Spectral linting step executing
  - ✅ Postman validation step executing
  - ✅ All validation passing

- ✅ **Pre-commit Hooks**: Making a commit triggers:
  - ✅ Spectral validation
  - ✅ Postman validation (if env vars set)
  - ✅ Clear error messages if validation fails

---

## Estimated Time

- **Phase 1**: 10 minutes (create package.json, install Spectral)
- **Phase 2**: 5 minutes (add one line to CI/CD workflow)
- **Phase 3**: 20 minutes (create Postman setup scripts and test)
- **Phase 4**: 15 minutes (update pre-commit runner)
- **Phase 5**: 20 minutes (create unified setup scripts)
- **Phase 6**: 15 minutes (update documentation)
- **Testing**: 30 minutes (full integration testing)
- **Buffer**: 10 minutes

**Total**: ~2 hours (reduced from 2.5 hours due to simplified Phase 2)

---

## Dependencies Between Phases

```
Phase 1 (Spectral CLI)
    ↓
    ├─→ Phase 5 (Unified Setup) ←─┐
    │                              │
    └─→ Phase 2 (CI/CD)            │
                                   │
Phase 3 (Postman Setup)            │
    ↓                              │
    ├─→ Phase 4 (Pre-commit) ──────┘
    │
    └─→ Phase 5 (Unified Setup)

Phase 5 (Unified Setup)
    ↓
Phase 6 (Documentation)
```

---

## Post-Implementation Checklist

After completing all phases:

- [ ] Run full setup on clean environment
- [ ] Verify Spectral linting shows rule violations (if any)
- [ ] Verify Postman validation works locally
- [ ] Make a test commit and verify pre-commit hooks work
- [ ] Push to GitHub and verify CI/CD pipeline works
- [ ] Create memory in mx CLI documenting completion
- [ ] Update team on new validation requirements
- [ ] Add validation status badge to README (optional)

---

## Known Issues and Limitations

1. **Postman CLI Windows Installation**: May require manual PATH configuration
2. **Spectral Performance**: First run may be slow (downloads dependencies)
3. **Environment Variables**: Must be set in each terminal session (unless using .env loader)
4. **CI/CD Rate Limits**: Postman API has rate limits (should not be an issue for normal use)

---

## Support and Troubleshooting

**Common Issues:**

1. **"Spectral CLI not found"**
   - Solution: Run `npm install` from repository root
   - Verify: `npx @stoplight/spectral-cli --version`

2. **"Postman workspace not found"**
   - Solution: Check `POSTMAN_WORKSPACE_ID` in `.env`
   - Verify: `echo $env:POSTMAN_WORKSPACE_ID` (Windows) or `echo $POSTMAN_WORKSPACE_ID` (Linux/macOS)

3. **"Pre-commit tests failing"**
   - Solution: Run with `--verbose` flag to see detailed output
   - Check: `dev-tools/commit-testing-log/latest_report.md`

4. **"CI/CD validation failing"**
   - Solution: Check GitHub Actions logs for specific error
   - Verify: GitHub Secrets are set correctly

**Getting Help:**
- Check documentation: `dev-tools/docs/PRE_COMMIT_VALIDATION.md`
- Review logs: `dev-tools/commit-testing-log/`
- Run verbose tests: `python dev-tools/run_precommit_tests.py --verbose`

---

## Appendix: File Locations Reference

**New Files Created:**
```
.env.example                                    # Environment variable template
package.json                                    # Node.js dependencies (Spectral CLI)
package-lock.json                               # Locked dependency versions
dev-tools/setup_postman_local.ps1              # Postman setup (Windows)
dev-tools/setup_postman_local.sh               # Postman setup (Linux/macOS)
dev-tools/setup_validation_tools.ps1           # Unified setup (Windows)
dev-tools/setup_validation_tools.sh            # Unified setup (Linux/macOS)
dev-tools/docs/VALIDATION_SETUP_IMPLEMENTATION_PLAN.md  # This document
```

**Modified Files:**
```
.gitignore                                      # Add node_modules, .env
.github/workflows/deploy-and-version.yml       # Add Spectral validation
dev-tools/run_precommit_tests.py               # Add env var checking
scripts/setup-local-dev.ps1                    # Add validation setup step
scripts/setup-local-dev.sh                     # Add validation setup step
README.md                                       # Add validation setup section
dev-tools/docs/PRE_COMMIT_VALIDATION.md        # Add troubleshooting guide
```

**User-Created Files (Not in Git):**
```
.env                                            # User's Postman credentials
node_modules/                                   # npm dependencies
dev-tools/commit-testing-log/                  # Test reports
```

---

## End of Implementation Plan

This plan provides a complete, step-by-step guide to implementing comprehensive API validation for the Spearmint project. Follow the phases in order, verify each step, and use the rollback strategies if needed.

**Next Steps:**
1. Review this plan with the team
2. Schedule implementation time (~2.5 hours)
3. Execute phases in order
4. Test thoroughly
5. Document any issues encountered
6. Create memory in mx CLI when complete

