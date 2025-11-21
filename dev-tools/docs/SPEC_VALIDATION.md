# OpenAPI Spec Validation with Postman Governance Rules

This document describes how OpenAPI spec validation is integrated into the Spearmint development workflow using Postman's governance and security rules.

## Overview

The OpenAPI specification (`sdk/openapi.json`) is automatically validated against Postman's configured governance and security rules in two places:

1. **Pre-commit hooks** - Validates spec before committing changes
2. **CI/CD pipeline** - Validates spec during deployment workflow

## What Gets Validated?

### Syntax Validation (All Plans)
- Missing required fields
- Wrong data types
- Incorrect nesting
- Malformed field names
- Invalid JSON/YAML

### Governance Rules (Enterprise Plans)
- API design standards
- Naming conventions
- Required fields (descriptions, examples, etc.)
- HTTP status code requirements
- Path structure rules
- Custom team-specific rules

### Security Rules (Enterprise Plans)
- OWASP API Security Top 10
- Authentication requirements
- Missing security schemes
- Sensitive data exposure
- Rate limiting requirements

## Pre-commit Validation

### Setup

1. **Install pre-commit** (if not already installed):
   ```bash
   pip install pre-commit
   ```

2. **Install Postman CLI**:
   ```bash
   # Linux/macOS
   curl -o- "https://dl-cli.pstmn.io/install/linux64.sh" | sh
   
   # Windows (PowerShell)
   iwr https://dl-cli.pstmn.io/install/win64.ps1 | iex
   ```

3. **Login to Postman**:
   ```bash
   postman login --with-api-key YOUR_API_KEY
   ```

4. **Set environment variable** (optional, for workspace-specific rules):
   ```bash
   # Linux/macOS
   export POSTMAN_WORKSPACE_ID="your-workspace-id"
   
   # Windows (PowerShell)
   $env:POSTMAN_WORKSPACE_ID="your-workspace-id"
   ```

5. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

### Usage

The spec validation hook runs automatically when you commit changes to:
- `sdk/openapi.json`

**Manual validation:**
```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run only spec validation hook
pre-commit run openapi-spec-validation
```

**Bypass validation** (not recommended):
```bash
git commit --no-verify
```

### Configuration

The pre-commit hook is configured in `.pre-commit-config.yaml`:

```yaml
- id: openapi-spec-validation
  name: OpenAPI Spec Validation (Postman)
  entry: python dev-tools/validate_spec.py --spec-file sdk/openapi.json --fail-severity WARNING
  language: system
  files: ^sdk/openapi\.json$
  stages: [commit, push]
  pass_filenames: false
  verbose: true
```

**Adjust fail severity:**
- `HINT` - Informational suggestions
- `INFO` - Minor issues
- `WARNING` - Potential problems (default)
- `ERROR` - Critical violations only

## CI/CD Validation

### How It Works

The `validate-spec` job in `.github/workflows/deploy-and-version.yml`:

1. Downloads the generated OpenAPI spec artifact
2. Installs Postman CLI
3. Authenticates with Postman API
4. Runs `postman spec lint` command
5. Uploads validation results as artifact
6. Adds summary to GitHub Actions output
7. Fails the build if violations are found

### Required Secrets

The following GitHub secrets must be configured:

- `POSTMAN_API_KEY` - Your Postman API key
- `POSTMAN_WORKSPACE_ID` - Your workspace ID

### Viewing Results

**In GitHub Actions:**
1. Go to Actions tab
2. Click on the workflow run
3. View the "OpenAPI Spec Validation Results" summary
4. Download the `spec-validation-results` artifact for full details

**Validation results artifact:**
```json
{
  "success": false,
  "exit_code": 1,
  "violations": [
    {
      "file": "openapi.json",
      "line number": "42",
      "path": "paths./api/endpoint.get.responses",
      "severity": "WARNING",
      "issue": "Operation should return a 2xx HTTP status code"
    }
  ]
}
```

## Manual Validation

You can run spec validation manually at any time:

```bash
# Basic validation
python dev-tools/validate_spec.py --spec-file sdk/openapi.json

# With workspace-specific rules
python dev-tools/validate_spec.py \
  --spec-file sdk/openapi.json \
  --workspace-id "your-workspace-id"

# Fail on warnings or higher
python dev-tools/validate_spec.py \
  --spec-file sdk/openapi.json \
  --fail-severity WARNING

# Save results to file
python dev-tools/validate_spec.py \
  --spec-file sdk/openapi.json \
  --output-file validation-results.json
```

## Troubleshooting

### "Postman CLI not found"

Install the Postman CLI:
```bash
# Linux/macOS
curl -o- "https://dl-cli.pstmn.io/install/linux64.sh" | sh

# Windows
iwr https://dl-cli.pstmn.io/install/win64.ps1 | iex
```

### "Authentication required"

Login to Postman:
```bash
postman login --with-api-key YOUR_API_KEY
```

### "No violations found but validation failed"

This usually means there's a syntax error in the spec file. Check the error output for details.

### Pre-commit hook not running

Reinstall the hooks:
```bash
pre-commit uninstall
pre-commit install
```

## Configuring Governance Rules in Postman

To configure custom governance rules for your team:

1. Go to Postman web app
2. Navigate to **API Governance** (Enterprise plans only)
3. Click **Configure Rules**
4. Enable/disable rules or create custom rules
5. Apply rules to specific workspaces or "All workspaces"

Rules are automatically applied when running `postman spec lint`.

## References

- [Postman CLI Documentation](https://learning.postman.com/docs/postman-cli/postman-cli-overview/)
- [Postman API Governance](https://learning.postman.com/docs/api-governance/api-governance-overview/)
- [Postman Spec Validation](https://learning.postman.com/docs/design-apis/specifications/validate-a-specification/)
- [Pre-commit Framework](https://pre-commit.com/)

