# ✅ OpenAPI Spec Validation - Implementation Complete!

## 🎯 What Was Added

I've successfully integrated **Postman API Governance and Security validation** into both your **pre-commit hooks** and **CI/CD pipeline**!

---

## 📦 New Files Created

### 1. **`dev-tools/validate_spec.py`**
Python script that validates OpenAPI specs using Postman CLI:
- ✅ Validates against Postman governance rules
- ✅ Validates against Postman security rules (OWASP)
- ✅ Supports OpenAPI 2.0, 3.0, and 3.1
- ✅ Configurable fail severity (HINT, INFO, WARNING, ERROR)
- ✅ JSON output for CI/CD integration
- ✅ Human-readable console output

### 2. **`dev-tools/setup_spec_validation.sh`** (Linux/macOS)
Automated setup script that:
- ✅ Installs Postman CLI
- ✅ Authenticates with Postman API
- ✅ Configures workspace ID
- ✅ Installs pre-commit hooks

### 3. **`dev-tools/setup_spec_validation.ps1`** (Windows)
Windows PowerShell version of the setup script

### 4. **`dev-tools/docs/SPEC_VALIDATION.md`**
Comprehensive documentation covering:
- ✅ What gets validated (syntax, governance, security)
- ✅ Pre-commit setup and usage
- ✅ CI/CD integration details
- ✅ Manual validation commands
- ✅ Troubleshooting guide
- ✅ Configuring governance rules in Postman

---

## 🔧 Modified Files

### 1. **`.pre-commit-config.yaml`**
Added new hook:
```yaml
- id: openapi-spec-validation
  name: OpenAPI Spec Validation (Postman)
  entry: python dev-tools/validate_spec.py --spec-file sdk/openapi.json --fail-severity WARNING
  language: system
  files: ^sdk/openapi\.json$
  stages: [commit, push]
```

**Triggers on:** Changes to `sdk/openapi.json`  
**Fail severity:** WARNING or higher

### 2. **`.github/workflows/deploy-and-version.yml`**
Added new job: `validate-spec`

**What it does:**
1. ✅ Downloads OpenAPI spec artifact from `build-sdk` job
2. ✅ Installs Postman CLI
3. ✅ Authenticates with Postman API
4. ✅ Runs `postman spec lint` command
5. ✅ Uploads validation results as artifact (30-day retention)
6. ✅ Adds summary to GitHub Actions output
7. ✅ **Blocks deployment** if violations found

**Updated dependency chain:**
```
test → build-gateway ↘
                      → validate-spec → bump-version → publish-sdk
test → build-sdk    ↗                                → create-collection
                                                      → publish-spec
```

Now **all three jobs** (build-gateway, build-sdk, validate-spec) must succeed before version bump!

---

## 🚀 How to Use

### **Pre-commit Validation** (Local Development)

#### Setup (One-time):
```bash
# Linux/macOS
./dev-tools/setup_spec_validation.sh

# Windows
.\dev-tools\setup_spec_validation.ps1
```

#### Usage:
```bash
# Automatic - runs on commit
git add sdk/openapi.json
git commit -m "Update API spec"
# ↑ Validation runs automatically!

# Manual - run all hooks
pre-commit run --all-files

# Manual - run only spec validation
pre-commit run openapi-spec-validation

# Bypass (not recommended)
git commit --no-verify
```

---

### **CI/CD Validation** (Automatic)

**Triggers:** Every push to `main` that changes API code

**What happens:**
1. Tests run
2. Gateway builds
3. SDK builds (generates OpenAPI spec)
4. **Spec validates** ← NEW!
5. Version bumps (only if all succeed)
6. SDK publishes to npm
7. Collection creates in Postman
8. Spec publishes to Postman Spec Hub

**View results:**
- Go to GitHub Actions → Click workflow run
- See "OpenAPI Spec Validation Results" summary
- Download `spec-validation-results` artifact for full details

---

### **Manual Validation** (Anytime)

```bash
# Basic validation
python dev-tools/validate_spec.py --spec-file sdk/openapi.json

# With workspace-specific rules
python dev-tools/validate_spec.py \
  --spec-file sdk/openapi.json \
  --workspace-id "your-workspace-id"

# Fail on warnings
python dev-tools/validate_spec.py \
  --spec-file sdk/openapi.json \
  --fail-severity WARNING

# Save results to file
python dev-tools/validate_spec.py \
  --spec-file sdk/openapi.json \
  --output-file validation-results.json
```

---

## 🔍 What Gets Validated?

### **Syntax Validation** (All Plans)
- Missing required fields
- Wrong data types
- Incorrect nesting
- Malformed field names
- Invalid JSON/YAML

### **Governance Rules** (Enterprise Plans)
- API design standards
- Naming conventions
- Required descriptions/examples
- HTTP status code requirements
- Path structure rules
- Custom team rules

### **Security Rules** (Enterprise Plans)
- OWASP API Security Top 10
- Authentication requirements
- Missing security schemes
- Sensitive data exposure
- Rate limiting requirements

---

## 🔐 Required Secrets (Already Configured)

Your GitHub Actions already has these secrets:
- ✅ `POSTMAN_API_KEY` - For Postman API access
- ✅ `POSTMAN_WORKSPACE_ID` - Your workspace ID

---

## 📊 Example Validation Output

**Console:**
```
🔍 Validating spec: sdk/openapi.json
   Workspace ID: 12345678-workspace-id
   Fail severity: WARNING
   Output format: JSON

================================================================================
VALIDATION RESULTS
================================================================================

❌ FAILED - Found 2 violation(s)

Violations:
--------------------------------------------------------------------------------

1. WARNING - Line 42
   File: openapi.json
   Path: paths./api/endpoint.get.responses
   Issue: Operation should return a 2xx HTTP status code

2. ERROR - Line 108
   File: openapi.json
   Path: paths./api/users/{id}/
   Issue: There should be no trailing slashes on paths

================================================================================
```

**GitHub Actions Summary:**
```markdown
## 📋 OpenAPI Spec Validation Results

❌ **FAILED** - Found 2 violation(s)

### Violations:
1. **WARNING** - Line 42
   - File: `openapi.json`
   - Path: `paths./api/endpoint.get.responses`
   - Issue: Operation should return a 2xx HTTP status code

2. **ERROR** - Line 108
   - File: `openapi.json`
   - Path: `paths./api/users/{id}/`
   - Issue: There should be no trailing slashes on paths
```

---

## 🎓 Next Steps

1. **Run the setup script** to configure your local environment:
   ```bash
   ./dev-tools/setup_spec_validation.sh  # Linux/macOS
   .\dev-tools\setup_spec_validation.ps1  # Windows
   ```

2. **Test the validation** manually:
   ```bash
   python dev-tools/validate_spec.py --spec-file sdk/openapi.json
   ```

3. **Watch the workflow** run on GitHub Actions to see validation in action!

4. **Configure governance rules** in Postman (Enterprise plans):
   - Go to Postman → API Governance → Configure Rules
   - Enable/disable rules or create custom rules
   - Apply to specific workspaces

---

## 📚 Documentation

- **Full guide:** `dev-tools/docs/SPEC_VALIDATION.md`
- **Spec publishing:** `dev-tools/docs/SPEC_PUBLISHING.md`
- **Postman CLI docs:** https://learning.postman.com/docs/postman-cli/postman-cli-overview/
- **API Governance:** https://learning.postman.com/docs/api-governance/api-governance-overview/

---

## ✨ Benefits

✅ **Catch issues early** - Validate before committing  
✅ **Enforce standards** - Consistent API design across team  
✅ **Security compliance** - OWASP security checks  
✅ **Block bad deploys** - CI/CD fails on violations  
✅ **Automated** - No manual checks needed  
✅ **Configurable** - Adjust severity and rules  
✅ **Documented** - Clear violation messages  

---

**Questions?** See `dev-tools/docs/SPEC_VALIDATION.md` for detailed documentation!

