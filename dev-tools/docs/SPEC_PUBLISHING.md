# Publishing OpenAPI Specs to Postman Spec Hub

This document explains how the `publish_spec.py` script works and how it's integrated into the CI/CD pipeline.

## Overview

The `publish_spec.py` script automatically publishes OpenAPI specifications to Postman's Spec Hub whenever the API version is bumped. This keeps your API documentation synchronized across:

- **npm SDK** - Published to npm registry
- **Postman Collection** - Created in workspace
- **OpenAPI Spec** - Published to Spec Hub

---

## Script Location

```
dev-tools/publish_spec.py
```

---

## How It Works

### 1. **Reads the OpenAPI Spec File**
- Supports both JSON and YAML formats
- Validates JSON syntax if it's a `.json` file
- Reads the entire file content as a string

### 2. **Detects OpenAPI Version**
- Automatically detects the spec type from the content:
  - `OPENAPI:3.1` - OpenAPI 3.1.x
  - `OPENAPI:3.0` - OpenAPI 3.0.x
  - `OPENAPI:2.0` - Swagger 2.0
- Works with both JSON and YAML formats

### 3. **Creates the Spec in Postman**
- Uses Postman API endpoint: `POST /specs?workspaceId={workspaceId}`
- Sends the spec content as a file
- Names the spec: `"Spearmint Finance API - v{version} ({Month Year})"`

### 4. **Returns Spec Details**
- Spec ID
- Spec name
- Spec type
- Creation timestamp
- Direct link to view in Postman

---

## Usage

### Command Line

```bash
python dev-tools/publish_spec.py \
  --workspace-id "YOUR_WORKSPACE_ID" \
  --spec-file "sdk/openapi.json" \
  --version "1.0.0" \
  --output-file "spec_info.json"
```

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--workspace-id` | Postman workspace ID | `1f0df51a-8658-4ee8-a2a1-d2567dfa09a9` |
| `--spec-file` | Path to OpenAPI spec file | `sdk/openapi.json` |
| `--version` | API version | `1.0.0` |

### Optional Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--api-key` | Postman API key | Uses `POSTMAN_API_KEY` env var |
| `--spec-name` | Custom spec name | `Spearmint Finance API - v{version} ({date})` |
| `--output-file` | Save spec details to JSON | None |

---

## CI/CD Integration

The script is integrated into the GitHub Actions workflow at `.github/workflows/deploy-and-version.yml`.

### Workflow Job: `publish-spec`

```yaml
publish-spec:
  needs: bump-version
  if: needs.bump-version.outputs.version_changed == 'true'
  runs-on: ubuntu-latest
  steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        ref: main

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Download OpenAPI spec artifact
      uses: actions/download-artifact@v4
      with:
        name: openapi-spec
        path: sdk/

    - name: Publish spec to Postman
      run: |
        python dev-tools/publish_spec.py \
          --workspace-id "${{ secrets.POSTMAN_WORKSPACE_ID }}" \
          --spec-file "sdk/openapi.json" \
          --version "${{ needs.bump-version.outputs.new_version }}" \
          --output-file spec_info.json
      env:
        POSTMAN_API_KEY: ${{ secrets.POSTMAN_API_KEY }}
```

### When It Runs

The `publish-spec` job runs:
- ✅ After the version is bumped
- ✅ Only when the version actually changed
- ✅ In parallel with `publish-sdk` and `create-postman-collection`

---

## Required Secrets

Add these secrets to your GitHub repository:

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `POSTMAN_API_KEY` | Postman API key | [Generate in Postman Settings](https://go.postman.co/settings/me/api-keys) |
| `POSTMAN_WORKSPACE_ID` | Workspace ID | Found in workspace URL: `https://app.postman.com/workspace/{workspace-id}` |

---

## Output

### Console Output

```
Publishing OpenAPI spec to Postman Spec Hub...
Spec name: Spearmint Finance API - v1.0.0 (Nov 2025)
Spec file: sdk/openapi.json
Workspace ID: 1f0df51a-8658-4ee8-a2a1-d2567dfa09a9

✓ Spec published successfully!

Spec Details:
  Name:       Spearmint Finance API - v1.0.0 (Nov 2025)
  ID:         b4fc1bdc-6587-4f9b-95c9-f768146089b4
  Type:       OPENAPI:3.0
  Created At: 2025-11-21T21:30:00.000Z

Access the spec at:
  https://app.postman.com/workspace/1f0df51a-8658-4ee8-a2a1-d2567dfa09a9/specs/b4fc1bdc-6587-4f9b-95c9-f768146089b4
```

### GitHub Actions Outputs

The script sets these outputs for use in subsequent steps:

- `spec_id` - The spec's unique ID
- `spec_name` - The spec's name
- `spec_type` - The spec type (e.g., `OPENAPI:3.0`)

---

## Error Handling

The script handles common errors:

### File Not Found
```
ERROR: Spec file not found: sdk/openapi.json
```

### Invalid JSON
```
ERROR: Invalid JSON in spec file: Expecting property name enclosed in double quotes
```

### API Errors
```
ERROR: Postman API error (HTTP 400): {"error": {"name": "malformedRequestError", ...}}
```

### Network Errors
```
ERROR: Network error: Connection refused
```

---

## Related Documentation

- [Postman API Collection Creation](./POSTMAN_API_COLLECTION_CREATION.md)
- [Postman API Documentation](https://www.postman.com/postman/workspace/postman-public-workspace/documentation/12959542-c8142d51-e97c-46b6-bd77-52bb66712c9a)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)

