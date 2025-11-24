# Pre-Commit Test Report

**Timestamp:** 2025-11-24T14:40:22.892108

## Summary

- **Total Tests:** 2
- **Passed:** 2
- **Failed:** 0
- **Skipped:** 0

**Overall Status:** [PASSED]

## Test Details

### 1. OpenAPI Generation [PASSED]

**Status:** PASSED

**Description:** Generate OpenAPI spec from FastAPI application

**Command:** `python core-api/scripts/api_validation/api_validation.py --generate --output sdk/openapi.json`

**Duration:** 3.76 seconds

**Exit Code:** 0

**Errors/Warnings:**
```
2025-11-24 14:40:23,135 - INFO - Generating spec locally...
2025-11-24 14:40:25,168 - INFO - \u2705 Spec generated to sdk/openapi.json
2025-11-24 14:40:25,168 - INFO - 2025-11-24 14:40:23 - financial_analysis.api.logging_config - INFO - Logging configured successfully
2025-11-24 14:40:23 - financial_analysis.api.logging_config - INFO - Logging configured successfully
DEBUG: CORS Origins: ['*']
OpenAPI spec generated successfully

2025-11-24 14:40:25,169 - INFO - ================================================================================
2025-11-24 14:40:25,169 - INFO - Starting OpenAPI Validation Pipeline
2025-11-24 14:40:25,169 - INFO - ================================================================================
2025-11-24 14:40:25,169 - INFO - 
--- Structural Validation (before) ---
2025-11-24 14:40:25,169 - INFO - Validating structure: D:\CodingProjects\spearmint\sdk\openapi.json
2025-11-24 14:40:25,934 - INFO - \u2705 Spec at D:\CodingProjects\spearmint\sdk\openapi.json is structurally valid.
2025-11-24 14:40:25,934 - INFO - 
--- Bundling External Refs ---
2025-11-24 14:40:25,934 - INFO - Checking for external $ref files...
2025-11-24 14:40:25,935 - INFO - No external $ref files detected or already absolute URLs.
2025-11-24 14:40:25,935 - INFO - 
--- Spectral Linting ---
2025-11-24 14:40:25,935 - INFO - Linting with Spectral: D:\CodingProjects\spearmint\sdk\openapi.json
2025-11-24 14:40:25,935 - INFO - Using ruleset: D:\CodingProjects\spearmint\.spectral-google.yaml
2025-11-24 14:40:25,936 - WARNING - Ruleset not found: D:\CodingProjects\spearmint\.spectral-google.yaml. Skipping Spectral linting.
2025-11-24 14:40:25,936 - INFO - 
--- Structural Validation (after) ---
2025-11-24 14:40:25,936 - INFO - Validating structure: D:\CodingProjects\spearmint\sdk\openapi.json
2025-11-24 14:40:26,623 - INFO - \u2705 Spec at D:\CodingProjects\spearmint\sdk\openapi.json is structurally valid.
2025-11-24 14:40:26,623 - INFO - 
================================================================================
2025-11-24 14:40:26,623 - INFO - Validation Summary
2025-11-24 14:40:26,623 - INFO - ================================================================================
2025-11-24 14:40:26,623 - INFO - \u2705 PASS: Structural Validation (before)
2025-11-24 14:40:26,623 - INFO - \u2705 PASS: Bundling External Refs
2025-11-24 14:40:26,623 - INFO - \u2705 PASS: Spectral Linting
2025-11-24 14:40:26,623 - INFO - \u2705 PASS: Structural Validation (after)
2025-11-24 14:40:26,623 - INFO - ================================================================================
2025-11-24 14:40:26,623 - INFO - \u2705 All validation steps passed!
2025-11-24 14:40:26,623 - INFO - ================================================================================

```

---

### 2. OpenAPI Spec Validation (Postman) [PASSED]

**Status:** PASSED

**Description:** Validate OpenAPI spec against Postman governance rules

**Command:** `python dev-tools/validate_spec.py --spec-file sdk/openapi.json --fail-severity WARNING --output-file dev-tools\commit-testing-log\spec_validation_20251124_144022.json`

**Duration:** 0.61 seconds

**Exit Code:** 0

**Output:**
```
[OK] Postman CLI found: 1.17.0

[VALIDATING] Spec: D:\CodingProjects\spearmint\sdk\openapi.json
   Workspace ID: Default (All workspaces)
   Fail severity: WARNING
   Output format: JSON

   Running: postman spec lint D:\CodingProjects\spearmint\sdk\openapi.json --fail-severity WARNING --output JSON


[WARNING] Postman workspace not configured or not accessible.
Skipping Postman governance validation.
To enable validation, set POSTMAN_WORKSPACE_ID environment variable.

================================================================================
VALIDATION RESULTS
================================================================================

[PASSED] No governance or security violations found!

Errors/Warnings:
Error: An error occurred while retrieving specification details, Details: The requested resource could not be found.



================================================================================

[OK] Results saved to: dev-tools\commit-testing-log\spec_validation_20251124_144022.json

```

---

