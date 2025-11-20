# E2E Testing with Playwright

This directory contains end-to-end (E2E) tests for the Financial Analysis Tool frontend using Playwright.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Structure](#test-structure)
- [Writing Tests](#writing-tests)
- [Debugging](#debugging)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The test suite covers:

- **Dashboard Tests** (`dashboard.spec.ts`) - Financial metrics display, recent transactions, loading states, data verification
- **Transaction List Tests** (`transaction-list.spec.ts`) - Search, pagination, sorting, row clicks, layout verification
- **Transaction CRUD Tests** (`transaction-crud.spec.ts`) - Create, read, update, delete operations with validation
- **Navigation Tests** (`navigation.spec.ts`) - Sidebar navigation, routing, browser history
- **Error Handling Tests** (`error-handling.spec.ts`) - API failures, validation errors, empty states
- **Visual Regression Tests** (`visual-regression.spec.ts`) - Screenshot-based layout and styling verification

## 🛡️ Critical Bug Prevention

The test suite includes specific tests to prevent critical bugs that were discovered in production:

### 1. Field Name Mismatch (Blank Page Bug)

**Problem:** Backend returns `transaction_id` and `transaction_date`, but frontend expected `id` and `date`, causing a blank page.

**Prevention Tests:**
- `transaction-list.spec.ts` → "should load actual transaction data from API (prevents blank page bug)"
- `transaction-list.spec.ts` → "should display Date column with actual dates (prevents field mapping bug)"
- `dashboard.spec.ts` → "should display actual financial data from API (prevents blank page bug)"

**What they verify:**
- DataGrid has rows with actual data (not empty)
- Date column displays valid dates in MM/DD/YYYY format
- No "undefined" or empty values appear in cells
- All required fields are properly mapped from backend to frontend

### 2. Layout Cut-off Bug

**Problem:** Main content area was missing `margin-left: 240px`, causing sidebar to overlap and hide the Date column.

**Prevention Tests:**
- `transaction-list.spec.ts` → "should display Date column without being cut off (prevents layout bug)"
- `transaction-list.spec.ts` → "should not have sidebar overlapping main content (prevents overlap bug)"
- `visual-regression.spec.ts` → "should display Date column in viewport (prevents cut-off bug)"

**What they verify:**
- Date column header has `x >= 0` (visible in viewport)
- Main content starts at `x >= 240px` (after sidebar)
- No horizontal scrolling required for main content
- All DataGrid columns are within viewport

### 3. Transfer Display Bug

**Problem:** Transfer transactions showed as "Income" (green) or "Expense" (red) instead of "Transfer" (gray).

**Prevention Tests:**
- `transaction-list.spec.ts` → "should correctly identify and display Transfer transactions"
- `visual-regression.spec.ts` → "should display transfer chips correctly (prevents display bug)"
- `visual-regression.spec.ts` → "should render transaction type chips with correct colors"

**What they verify:**
- Transfer chips display "Transfer" text (not "Income" or "Expense")
- Transfer chips use `MuiChip-colorDefault` (gray color)
- Transfer chips do NOT use `MuiChip-colorSuccess` (green) or `MuiChip-colorError` (red)
- `is_transfer` flag is properly checked in the UI

## ✅ Prerequisites

Before running tests, ensure you have:

1. **Node.js** (v18 or higher)
2. **Backend API running** on `http://localhost:8000`
3. **Frontend dev server** (automatically started by Playwright)

## 📦 Installation

Playwright is already installed as a dev dependency. If you need to reinstall:

```bash
npm install -D @playwright/test
npx playwright install chromium
```

## 🚀 Running Tests

### Run All Tests (Headless)

```bash
npm run test:e2e
```

This runs all tests in headless mode (no browser window visible).

### Run Tests with UI Mode

```bash
npm run test:e2e:ui
```

Opens Playwright's interactive UI for running and debugging tests.

### Run Tests in Headed Mode

```bash
npm run test:e2e:headed
```

Runs tests with the browser window visible.

### Run Specific Test File

```bash
npx playwright test dashboard.spec.ts
```

### Run Tests Matching a Pattern

```bash
npx playwright test --grep "should create"
```

### Run Only Critical Bug Prevention Tests

```bash
npx playwright test --grep "Critical Bug Prevention"
```

Runs only the tests designed to catch the three critical bugs (field mapping, layout cut-off, transfer display).

### Run Visual Regression Tests

```bash
npx playwright test visual-regression.spec.ts
```

### Update Visual Regression Baselines

When you intentionally change the UI, update screenshot baselines:

```bash
npx playwright test visual-regression.spec.ts --update-snapshots
```

### Debug Mode

```bash
npm run test:e2e:debug
```

Opens Playwright Inspector for step-by-step debugging.

### View Test Report

```bash
npm run test:e2e:report
```

Opens the HTML test report in your browser.

## 📁 Test Structure

```
tests/
├── dashboard.spec.ts           # Dashboard page tests
├── transaction-list.spec.ts    # Transaction list tests
├── transaction-crud.spec.ts    # CRUD operation tests
├── navigation.spec.ts          # Navigation and routing tests
├── error-handling.spec.ts      # Error handling tests
├── fixtures/
│   └── test-data.ts           # Test data and fixtures
├── utils/
│   └── test-helpers.ts        # Reusable test utilities
└── README.md                  # This file
```

## ✍️ Writing Tests

### Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';
import { navigateTo, waitForPageLoad } from './utils/test-helpers';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await navigateTo(page, '/your-page');
  });

  test('should do something', async ({ page }) => {
    // Arrange
    await page.getByRole('button', { name: 'Click Me' }).click();
    
    // Act
    await page.getByLabel('Input Field').fill('test value');
    
    // Assert
    await expect(page.getByText('Success')).toBeVisible();
  });
});
```

### Using Test Helpers

The `utils/test-helpers.ts` file provides reusable functions:

```typescript
import {
  navigateTo,           // Navigate to a page and wait for load
  waitForPageLoad,      // Wait for loading spinners to disappear
  clickSidebarItem,     // Click sidebar navigation
  waitForToast,         // Wait for toast notification
  fillFormField,        // Fill form field by label
  selectRadio,          // Select radio button
  clickButton,          // Click button by text
  waitForDialog,        // Wait for dialog to open
  waitForDataGrid,      // Wait for MUI DataGrid to load
  searchDataGrid,       // Search in DataGrid
} from './utils/test-helpers';
```

### Using Test Fixtures

The `fixtures/test-data.ts` file provides test data:

```typescript
import {
  testTransactions,           // Sample transaction data
  invalidTransactions,        // Invalid data for validation tests
  generateTestTransaction,    // Generate unique test transaction
  generateUniqueDescription,  // Generate unique description
} from './fixtures/test-data';

// Example usage
const transaction = generateTestTransaction('Income');
await fillFormField(page, 'Description', transaction.description);
```

### Best Practices

1. **Use Semantic Selectors**
   ```typescript
   // Good - semantic and stable
   await page.getByRole('button', { name: 'Submit' });
   await page.getByLabel('Email');
   await page.getByText('Welcome');
   
   // Avoid - brittle and implementation-dependent
   await page.locator('#submit-btn');
   await page.locator('.css-class-name');
   ```

2. **Wait for Elements Properly**
   ```typescript
   // Good - auto-waiting
   await expect(page.getByText('Success')).toBeVisible();
   
   // Avoid - manual waits
   await page.waitForTimeout(1000);
   ```

3. **Test Isolation**
   - Each test should be independent
   - Use `beforeEach` for setup
   - Clean up test data if needed

4. **Descriptive Test Names**
   ```typescript
   // Good
   test('should display validation error for empty description', ...)
   
   // Avoid
   test('test 1', ...)
   ```

## 🐛 Debugging

### Debug a Specific Test

```bash
npx playwright test dashboard.spec.ts --debug
```

### Debug with UI Mode

```bash
npm run test:e2e:ui
```

Features:
- Watch mode
- Time travel debugging
- Pick locator tool
- Step through tests

### View Traces

When a test fails, Playwright captures a trace. View it with:

```bash
npx playwright show-trace trace.zip
```

### Screenshots and Videos

Failed tests automatically capture:
- Screenshots (in `test-results/`)
- Videos (in `test-results/`)

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Install Playwright
        run: |
          cd frontend
          npx playwright install --with-deps chromium
      
      - name: Start backend
        run: |
          # Start your backend API
          python -m uvicorn main:app &
      
      - name: Run tests
        run: |
          cd frontend
          npm run test:e2e
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report/
```

### Environment Variables

Configure test behavior with environment variables:

```bash
# Run in CI mode (no retries, single worker)
CI=true npm run test:e2e

# Custom base URL
PLAYWRIGHT_BASE_URL=http://localhost:3000 npm run test:e2e
```

## 🔧 Troubleshooting

### Tests Fail with "Timeout"

**Problem:** Tests timeout waiting for elements.

**Solutions:**
1. Ensure backend API is running on `http://localhost:8000`
2. Increase timeout in `playwright.config.ts`:
   ```typescript
   use: {
     actionTimeout: 15000,
     navigationTimeout: 45000,
   }
   ```
3. Check network tab in debug mode

### "Element not found" Errors

**Problem:** Selectors don't match elements.

**Solutions:**
1. Use Playwright Inspector to pick correct selectors:
   ```bash
   npm run test:e2e:debug
   ```
2. Use more flexible selectors:
   ```typescript
   // Instead of exact match
   page.getByRole('button', { name: 'Submit', exact: false })
   ```

### Tests Pass Locally but Fail in CI

**Problem:** Environment differences.

**Solutions:**
1. Ensure same Node.js version
2. Check for timing issues (add proper waits)
3. Use `CI=true` locally to test CI behavior
4. Review CI logs and artifacts

### Backend Not Available

**Problem:** Tests can't connect to backend.

**Solutions:**
1. Start backend manually:
   ```bash
   cd ..
   start_api.bat
   ```
2. Verify backend is running:
   ```bash
   curl http://localhost:8000/api/health
   ```
3. Check `playwright.config.ts` base URL

### Flaky Tests

**Problem:** Tests pass/fail inconsistently.

**Solutions:**
1. Add proper waits:
   ```typescript
   await waitForPageLoad(page);
   await expect(element).toBeVisible();
   ```
2. Increase retries in `playwright.config.ts`:
   ```typescript
   retries: 2
   ```
3. Use `test.slow()` for slow tests:
   ```typescript
   test.slow();
   ```

### Browser Not Installed

**Problem:** "Executable doesn't exist" error.

**Solution:**
```bash
npx playwright install chromium
```

## 📊 Test Coverage

Current test coverage:

- ✅ Dashboard display and metrics
- ✅ Transaction list with search/filter/pagination
- ✅ Transaction CRUD operations
- ✅ Form validation
- ✅ Navigation and routing
- ✅ Error handling and recovery
- ✅ Toast notifications
- ✅ Loading states
- ✅ Empty states

## 🎓 Learning Resources

- [Playwright Documentation](https://playwright.dev)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [Debugging Guide](https://playwright.dev/docs/debug)
- [Selectors Guide](https://playwright.dev/docs/selectors)

## 📝 Contributing

When adding new tests:

1. Follow existing test structure
2. Use test helpers and fixtures
3. Add descriptive test names
4. Ensure tests are isolated
5. Update this README if needed

## 🆘 Getting Help

If you encounter issues:

1. Check this README's troubleshooting section
2. Review Playwright documentation
3. Check test output and traces
4. Ask the team for help

---

**Happy Testing! 🎉**

