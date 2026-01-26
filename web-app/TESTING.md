# Playwright E2E Testing - Quick Start Guide

## 🚀 Quick Start

### 1. Prerequisites

Make sure you have:
- ✅ Backend API running on `http://localhost:8000`
- ✅ Node.js installed (v18+)
- ✅ Playwright installed (`npm install`)

### 2. Start the Backend

In a separate terminal:

```bash
# From project root
scripts\start_api.bat
```

Verify it's running:
```bash
curl http://localhost:8000/api/health
```

### 3. Run Tests

```bash
# Run all tests (headless)
npm run test:e2e

# Run with UI (recommended for development)
npm run test:e2e:ui

# Run in headed mode (see browser)
npm run test:e2e:headed

# Debug mode
npm run test:e2e:debug
```

### 4. View Results

```bash
# Open HTML report
npm run test:e2e:report
```

## 📊 Test Coverage

### ✅ Implemented Tests (5 test files, 80+ tests)

1. **Dashboard Tests** (`dashboard.spec.ts`) - 14 tests
   - Display dashboard title and metrics
   - Financial overview cards (Income, Expenses, Cash Flow)
   - Financial health indicators
   - Currency formatting
   - Recent transactions
   - Loading states
   - Responsive design
   - Navigation

2. **Transaction List Tests** (`transaction-list.spec.ts`) - 20+ tests
   - Page display and layout
   - DataGrid rendering
   - Search functionality
   - Pagination controls
   - Sorting
   - Row clicks
   - Color-coded amounts
   - Transaction type chips
   - Empty states

3. **Transaction CRUD Tests** (`transaction-crud.spec.ts`) - 25+ tests
   - **Create:** New transactions with validation
   - **Read:** View transaction details
   - **Update:** Edit transactions
   - **Delete:** Delete with confirmation
   - Form validation (required fields, min values, length)
   - Success/error toast notifications
   - Dialog interactions

4. **Navigation Tests** (`navigation.spec.ts`) - 20+ tests
   - Sidebar navigation
   - All menu items (Dashboard, Transactions, Analysis, etc.)
   - Active state highlighting
   - Browser back/forward buttons
   - URL routing
   - Layout consistency
   - Multiple navigation flows

5. **Error Handling Tests** (`error-handling.spec.ts`) - 15+ tests
   - Network errors (API unavailable)
   - Retry functionality
   - Form validation errors
   - API error responses (404, 500)
   - Empty states
   - Loading states
   - Toast error messages

## 🎯 Test Results

### Expected Results (with backend running)

```
✓ Dashboard tests: 14/14 passing
✓ Transaction List tests: 20/20 passing
✓ Transaction CRUD tests: 25/25 passing
✓ Navigation tests: 20/20 passing
✓ Error Handling tests: 15/15 passing

Total: 94+ tests passing
```

### Common Failures (without backend)

If backend is not running, you'll see failures like:
- ❌ "Element not found" - Dashboard elements
- ❌ "Timeout" - Waiting for API responses
- ❌ "Navigation failed" - API calls failing

**Solution:** Start the backend API first!

## 📁 Test Structure

```
frontend/
├── tests/
│   ├── dashboard.spec.ts           # Dashboard tests
│   ├── transaction-list.spec.ts    # List view tests
│   ├── transaction-crud.spec.ts    # CRUD operations
│   ├── navigation.spec.ts          # Navigation tests
│   ├── error-handling.spec.ts      # Error scenarios
│   ├── fixtures/
│   │   └── test-data.ts           # Test data
│   ├── utils/
│   │   └── test-helpers.ts        # Helper functions
│   └── README.md                  # Detailed docs
├── playwright.config.ts            # Playwright config
├── package.json                    # Test scripts
└── TESTING.md                     # This file
```

## 🛠️ Available Commands

```bash
# Run all tests
npm run test:e2e

# Interactive UI mode (best for development)
npm run test:e2e:ui

# Headed mode (see browser)
npm run test:e2e:headed

# Debug mode (step through tests)
npm run test:e2e:debug

# View HTML report
npm run test:e2e:report

# Run specific test file
npx playwright test dashboard.spec.ts

# Run tests matching pattern
npx playwright test --grep "should create"

# Run in specific browser
npx playwright test --project=chromium
```

## 🐛 Debugging

### Debug a Failing Test

```bash
# Run specific test in debug mode
npx playwright test dashboard.spec.ts --debug

# Or use UI mode
npm run test:e2e:ui
```

### View Test Artifacts

Failed tests automatically capture:
- **Screenshots** - `test-results/*/test-failed-*.png`
- **Videos** - `test-results/*/video.webm`
- **Traces** - View with `npx playwright show-trace trace.zip`

### Common Issues

**Issue:** Tests timeout
**Fix:** Ensure backend is running on port 8000

**Issue:** "Element not found"
**Fix:** Use Playwright Inspector to find correct selectors
```bash
npm run test:e2e:debug
```

**Issue:** Flaky tests
**Fix:** Add proper waits using test helpers
```typescript
await waitForPageLoad(page);
await expect(element).toBeVisible();
```

## 📝 Writing New Tests

### 1. Create Test File

```typescript
// tests/my-feature.spec.ts
import { test, expect } from '@playwright/test';
import { navigateTo, waitForPageLoad } from './utils/test-helpers';

test.describe('My Feature', () => {
  test.beforeEach(async ({ page }) => {
    await navigateTo(page, '/my-page');
  });

  test('should do something', async ({ page }) => {
    // Your test code
    await expect(page.getByText('Expected Text')).toBeVisible();
  });
});
```

### 2. Use Test Helpers

```typescript
import {
  navigateTo,
  waitForPageLoad,
  clickButton,
  fillFormField,
  waitForToast,
  waitForDialog,
} from './utils/test-helpers';

// Navigate and wait
await navigateTo(page, '/transactions');

// Fill form
await fillFormField(page, 'Description', 'Test');

// Click button
await clickButton(page, 'Submit');

// Wait for success
await waitForToast(page, 'Success', 'success');
```

### 3. Use Test Data

```typescript
import { generateTestTransaction } from './fixtures/test-data';

const transaction = generateTestTransaction('Income');
await fillFormField(page, 'Description', transaction.description);
```

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
- name: Run E2E Tests
  run: |
    cd frontend
    npm run test:e2e
```

### Environment Variables

```bash
# CI mode (no retries, single worker)
CI=true npm run test:e2e

# Custom base URL
PLAYWRIGHT_BASE_URL=http://localhost:3000 npm run test:e2e
```

## 📊 Test Metrics

- **Total Tests:** 94+
- **Test Files:** 5
- **Helper Functions:** 20+
- **Test Fixtures:** 10+
- **Coverage Areas:** Dashboard, Transactions, Navigation, Errors
- **Execution Time:** ~2-3 minutes (all tests)
- **Browser:** Chromium (can add Firefox, WebKit)

## ✅ Best Practices

1. **Always start backend first**
2. **Use semantic selectors** (getByRole, getByLabel)
3. **Wait for elements properly** (auto-waiting)
4. **Keep tests isolated** (independent)
5. **Use test helpers** (reusable functions)
6. **Add descriptive names** (clear intent)
7. **Check test artifacts** (screenshots, videos)

## 🎓 Learning Resources

- [Playwright Docs](https://playwright.dev)
- [Test Helpers](./tests/utils/test-helpers.ts)
- [Test Data](./tests/fixtures/test-data.ts)
- [Detailed README](./tests/README.md)

## 🆘 Getting Help

1. Check [tests/README.md](./tests/README.md) for detailed docs
2. Review test output and artifacts
3. Use Playwright Inspector (`npm run test:e2e:debug`)
4. Check Playwright documentation

---

**Happy Testing! 🎉**

For more detailed information, see [tests/README.md](./tests/README.md)

