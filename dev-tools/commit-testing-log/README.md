# Commit Testing Log

This directory contains detailed logs from pre-commit validation tests.

## Overview

Every time you commit changes, the pre-commit hooks run a comprehensive test suite that validates:
1. **OpenAPI Generation** - Generates the OpenAPI spec from the FastAPI application
2. **OpenAPI Spec Validation** - Validates the spec against Postman governance rules

All test results are logged here with detailed information about each test run.

## Files

### Latest Reports (Tracked in Git)
- `latest_report.json` - Most recent test results in JSON format
- `latest_report.md` - Most recent test results in human-readable Markdown format

### Timestamped Reports (Not Tracked in Git)
- `test_report_YYYYMMDD_HHMMSS.json` - Full test results with timestamp
- `test_report_YYYYMMDD_HHMMSS.md` - Human-readable report with timestamp
- `spec_validation_YYYYMMDD_HHMMSS.json` - Detailed Postman validation results

## Report Contents

Each report includes:
- **Timestamp** - When the tests were run
- **Summary** - Total, passed, failed, and skipped test counts
- **Test Details** - For each test:
  - Test name and description
  - Command executed
  - Status (passed/failed/skipped)
  - Exit code
  - Duration
  - Full stdout and stderr output

## Usage

### Automatic (Pre-Commit Hook)
Reports are automatically generated when you commit:
```bash
git commit -m "Your commit message"
```

### Manual Test Run
You can run the test suite manually:
```bash
python dev-tools/run_precommit_tests.py
```

### View Latest Results
```bash
# View in terminal (Markdown)
cat dev-tools/commit-testing-log/latest_report.md

# View JSON
cat dev-tools/commit-testing-log/latest_report.json
```

## Troubleshooting

If tests fail:
1. Check `latest_report.md` for detailed error messages
2. Review the specific test's stdout/stderr output
3. Fix the issues identified
4. Re-run the tests or commit again

## Configuration

The test suite is configured in:
- `.pre-commit-config.yaml` - Pre-commit hook configuration
- `dev-tools/run_precommit_tests.py` - Test runner script
- `dev-tools/validate_spec.py` - Spec validation script
- `core-api/scripts/api_validation/api_validation.py` - OpenAPI generation script

