# AnalysisApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**getCashFlowAnalysisApiAnalysisCashflowGet**](AnalysisApi.md#getcashflowanalysisapianalysiscashflowget) | **GET** /api/analysis/cashflow | Get Cash Flow Analysis |
| [**getCashFlowTrendsApiAnalysisCashflowTrendsGet**](AnalysisApi.md#getcashflowtrendsapianalysiscashflowtrendsget) | **GET** /api/analysis/cashflow/trends | Get Cash Flow Trends |
| [**getCategoryBreakdownApiAnalysisCategoryBreakdownGet**](AnalysisApi.md#getcategorybreakdownapianalysiscategorybreakdownget) | **GET** /api/analysis/category-breakdown | Get Category Breakdown |
| [**getExpenseAnalysisApiAnalysisExpensesGet**](AnalysisApi.md#getexpenseanalysisapianalysisexpensesget) | **GET** /api/analysis/expenses | Get Expense Analysis |
| [**getExpenseCategoryTrendsApiAnalysisExpensesCategoryTrendsGet**](AnalysisApi.md#getexpensecategorytrendsapianalysisexpensescategorytrendsget) | **GET** /api/analysis/expenses/category-trends | Get Expense Category Trends |
| [**getExpenseTrendsApiAnalysisExpensesTrendsGet**](AnalysisApi.md#getexpensetrendsapianalysisexpensestrendsget) | **GET** /api/analysis/expenses/trends | Get Expense Trends |
| [**getFinancialHealthApiAnalysisHealthGet**](AnalysisApi.md#getfinancialhealthapianalysishealthget) | **GET** /api/analysis/health | Get Financial Health |
| [**getFinancialSummaryApiAnalysisSummaryGet**](AnalysisApi.md#getfinancialsummaryapianalysissummaryget) | **GET** /api/analysis/summary | Get Financial Summary |
| [**getIncomeAnalysisApiAnalysisIncomeGet**](AnalysisApi.md#getincomeanalysisapianalysisincomeget) | **GET** /api/analysis/income | Get Income Analysis |
| [**getIncomeExpenseComparisonApiAnalysisIncomeExpenseGet**](AnalysisApi.md#getincomeexpensecomparisonapianalysisincomeexpenseget) | **GET** /api/analysis/income-expense | Get Income Expense Comparison |
| [**getIncomeTrendsApiAnalysisIncomeTrendsGet**](AnalysisApi.md#getincometrendsapianalysisincometrendsget) | **GET** /api/analysis/income/trends | Get Income Trends |



## getCashFlowAnalysisApiAnalysisCashflowGet

> CashFlowResponse getCashFlowAnalysisApiAnalysisCashflowGet(startDate, endDate, mode)

Get Cash Flow Analysis

Get cash flow analysis for a period.  Args:     start_date: Start date for analysis     end_date: End date for analysis     mode: Analysis mode (analysis or complete)     db: Database session      Returns:     CashFlowResponse: Cash flow analysis results

### Example

```ts
import {
  Configuration,
  AnalysisApi,
} from '@spearmint-money/sdk';
import type { GetCashFlowAnalysisApiAnalysisCashflowGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new AnalysisApi();

  const body = {
    // Date | Start date for analysis (optional)
    startDate: 2013-10-20,
    // Date | End date for analysis (optional)
    endDate: 2013-10-20,
    // SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    mode: ...,
  } satisfies GetCashFlowAnalysisApiAnalysisCashflowGetRequest;

  try {
    const data = await api.getCashFlowAnalysisApiAnalysisCashflowGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **startDate** | `Date` | Start date for analysis | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date for analysis | [Optional] [Defaults to `undefined`] |
| **mode** | `SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum` | Analysis mode | [Optional] [Defaults to `undefined`] [Enum: analysis, with_capital, complete] |

### Return type

[**CashFlowResponse**](CashFlowResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getCashFlowTrendsApiAnalysisCashflowTrendsGet

> CashFlowTrendsResponse getCashFlowTrendsApiAnalysisCashflowTrendsGet(startDate, endDate, period, mode)

Get Cash Flow Trends

Get cash flow trends over time.  Args:     start_date: Start date for analysis     end_date: End date for analysis     period: Period granularity (daily, weekly, monthly, etc.)     mode: Analysis mode     db: Database session      Returns:     CashFlowTrendsResponse: Cash flow trend data

### Example

```ts
import {
  Configuration,
  AnalysisApi,
} from '@spearmint-money/sdk';
import type { GetCashFlowTrendsApiAnalysisCashflowTrendsGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new AnalysisApi();

  const body = {
    // Date | Start date for analysis (optional)
    startDate: 2013-10-20,
    // Date | End date for analysis (optional)
    endDate: 2013-10-20,
    // TimePeriodEnum | Period granularity (optional)
    period: ...,
    // SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    mode: ...,
  } satisfies GetCashFlowTrendsApiAnalysisCashflowTrendsGetRequest;

  try {
    const data = await api.getCashFlowTrendsApiAnalysisCashflowTrendsGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **startDate** | `Date` | Start date for analysis | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date for analysis | [Optional] [Defaults to `undefined`] |
| **period** | `TimePeriodEnum` | Period granularity | [Optional] [Defaults to `undefined`] [Enum: daily, weekly, monthly, quarterly, yearly] |
| **mode** | `SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum` | Analysis mode | [Optional] [Defaults to `undefined`] [Enum: analysis, with_capital, complete] |

### Return type

[**CashFlowTrendsResponse**](CashFlowTrendsResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getCategoryBreakdownApiAnalysisCategoryBreakdownGet

> CategoryBreakdownResponse getCategoryBreakdownApiAnalysisCategoryBreakdownGet(startDate, endDate, mode)

Get Category Breakdown

Get detailed category breakdown for income and expenses.  This endpoint provides a comprehensive breakdown of all categories including: - Income categories with totals, counts, and percentages - Expense categories with totals, counts, and percentages - Percentage of total for each category type - Percentage of all transactions  Args:     start_date: Start date for analysis     end_date: End date for analysis     mode: Analysis mode (analysis or complete)     db: Database session  Returns:     CategoryBreakdownResponse: Detailed category breakdown

### Example

```ts
import {
  Configuration,
  AnalysisApi,
} from '@spearmint-money/sdk';
import type { GetCategoryBreakdownApiAnalysisCategoryBreakdownGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new AnalysisApi();

  const body = {
    // Date | Start date for analysis (optional)
    startDate: 2013-10-20,
    // Date | End date for analysis (optional)
    endDate: 2013-10-20,
    // SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    mode: ...,
  } satisfies GetCategoryBreakdownApiAnalysisCategoryBreakdownGetRequest;

  try {
    const data = await api.getCategoryBreakdownApiAnalysisCategoryBreakdownGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **startDate** | `Date` | Start date for analysis | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date for analysis | [Optional] [Defaults to `undefined`] |
| **mode** | `SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum` | Analysis mode | [Optional] [Defaults to `undefined`] [Enum: analysis, with_capital, complete] |

### Return type

[**CategoryBreakdownResponse**](CategoryBreakdownResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getExpenseAnalysisApiAnalysisExpensesGet

> ExpenseAnalysisResponse getExpenseAnalysisApiAnalysisExpensesGet(startDate, endDate, mode, topN)

Get Expense Analysis

Get expense analysis for a period.  Args:     start_date: Start date for analysis     end_date: End date for analysis     mode: Analysis mode (analysis or complete)     top_n: Number of top categories to return     db: Database session      Returns:     ExpenseAnalysisResponse: Expense analysis results

### Example

```ts
import {
  Configuration,
  AnalysisApi,
} from '@spearmint-money/sdk';
import type { GetExpenseAnalysisApiAnalysisExpensesGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new AnalysisApi();

  const body = {
    // Date | Start date for analysis (optional)
    startDate: 2013-10-20,
    // Date | End date for analysis (optional)
    endDate: 2013-10-20,
    // SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    mode: ...,
    // number | Number of top categories to return (optional)
    topN: 56,
  } satisfies GetExpenseAnalysisApiAnalysisExpensesGetRequest;

  try {
    const data = await api.getExpenseAnalysisApiAnalysisExpensesGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **startDate** | `Date` | Start date for analysis | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date for analysis | [Optional] [Defaults to `undefined`] |
| **mode** | `SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum` | Analysis mode | [Optional] [Defaults to `undefined`] [Enum: analysis, with_capital, complete] |
| **topN** | `number` | Number of top categories to return | [Optional] [Defaults to `10`] |

### Return type

[**ExpenseAnalysisResponse**](ExpenseAnalysisResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getExpenseCategoryTrendsApiAnalysisExpensesCategoryTrendsGet

> any getExpenseCategoryTrendsApiAnalysisExpensesCategoryTrendsGet(startDate, endDate, period, mode, topN)

Get Expense Category Trends

Get expense trends broken down by category for stacked charts.  Returns expense amounts for each category for each time period, allowing for accurate stacked bar charts that show actual expenses per period rather than proportional distributions.

### Example

```ts
import {
  Configuration,
  AnalysisApi,
} from '@spearmint-money/sdk';
import type { GetExpenseCategoryTrendsApiAnalysisExpensesCategoryTrendsGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new AnalysisApi();

  const body = {
    // Date | Start date for analysis (optional)
    startDate: 2013-10-20,
    // Date | End date for analysis (optional)
    endDate: 2013-10-20,
    // TimePeriodEnum | Period granularity (optional)
    period: ...,
    // SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    mode: ...,
    // number | Number of top categories to include (optional)
    topN: 56,
  } satisfies GetExpenseCategoryTrendsApiAnalysisExpensesCategoryTrendsGetRequest;

  try {
    const data = await api.getExpenseCategoryTrendsApiAnalysisExpensesCategoryTrendsGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **startDate** | `Date` | Start date for analysis | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date for analysis | [Optional] [Defaults to `undefined`] |
| **period** | `TimePeriodEnum` | Period granularity | [Optional] [Defaults to `undefined`] [Enum: daily, weekly, monthly, quarterly, yearly] |
| **mode** | `SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum` | Analysis mode | [Optional] [Defaults to `undefined`] [Enum: analysis, with_capital, complete] |
| **topN** | `number` | Number of top categories to include | [Optional] [Defaults to `8`] |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getExpenseTrendsApiAnalysisExpensesTrendsGet

> TrendsResponse getExpenseTrendsApiAnalysisExpensesTrendsGet(startDate, endDate, period, mode)

Get Expense Trends

Get expense trends over time.  Args:     start_date: Start date for analysis     end_date: End date for analysis     period: Period granularity (daily, weekly, monthly, etc.)     mode: Analysis mode     db: Database session      Returns:     TrendsResponse: Expense trend data

### Example

```ts
import {
  Configuration,
  AnalysisApi,
} from '@spearmint-money/sdk';
import type { GetExpenseTrendsApiAnalysisExpensesTrendsGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new AnalysisApi();

  const body = {
    // Date | Start date for analysis (optional)
    startDate: 2013-10-20,
    // Date | End date for analysis (optional)
    endDate: 2013-10-20,
    // TimePeriodEnum | Period granularity (optional)
    period: ...,
    // SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    mode: ...,
  } satisfies GetExpenseTrendsApiAnalysisExpensesTrendsGetRequest;

  try {
    const data = await api.getExpenseTrendsApiAnalysisExpensesTrendsGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **startDate** | `Date` | Start date for analysis | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date for analysis | [Optional] [Defaults to `undefined`] |
| **period** | `TimePeriodEnum` | Period granularity | [Optional] [Defaults to `undefined`] [Enum: daily, weekly, monthly, quarterly, yearly] |
| **mode** | `SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum` | Analysis mode | [Optional] [Defaults to `undefined`] [Enum: analysis, with_capital, complete] |

### Return type

[**TrendsResponse**](TrendsResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getFinancialHealthApiAnalysisHealthGet

> FinancialHealthResponse getFinancialHealthApiAnalysisHealthGet(startDate, endDate, mode)

Get Financial Health

Get financial health indicators.  Args:     start_date: Start date for analysis     end_date: End date for analysis     mode: Analysis mode (analysis, with_capital, or complete)     db: Database session  Returns:     FinancialHealthResponse: Financial health indicators

### Example

```ts
import {
  Configuration,
  AnalysisApi,
} from '@spearmint-money/sdk';
import type { GetFinancialHealthApiAnalysisHealthGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new AnalysisApi();

  const body = {
    // Date | Start date for analysis (optional)
    startDate: 2013-10-20,
    // Date | End date for analysis (optional)
    endDate: 2013-10-20,
    // SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    mode: ...,
  } satisfies GetFinancialHealthApiAnalysisHealthGetRequest;

  try {
    const data = await api.getFinancialHealthApiAnalysisHealthGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **startDate** | `Date` | Start date for analysis | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date for analysis | [Optional] [Defaults to `undefined`] |
| **mode** | `SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum` | Analysis mode | [Optional] [Defaults to `undefined`] [Enum: analysis, with_capital, complete] |

### Return type

[**FinancialHealthResponse**](FinancialHealthResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getFinancialSummaryApiAnalysisSummaryGet

> FinancialSummaryResponse getFinancialSummaryApiAnalysisSummaryGet(startDate, endDate, mode, topN, recentCount)

Get Financial Summary

Get comprehensive financial summary.  This endpoint provides a complete financial overview including: - Total income, expenses, and net cash flow - Top income and expense categories - Recent transactions - Financial health indicators  Args:     start_date: Start date for analysis     end_date: End date for analysis     mode: Analysis mode (analysis or complete)     top_n: Number of top categories to return     recent_count: Number of recent transactions to return     db: Database session  Returns:     FinancialSummaryResponse: Comprehensive financial summary

### Example

```ts
import {
  Configuration,
  AnalysisApi,
} from '@spearmint-money/sdk';
import type { GetFinancialSummaryApiAnalysisSummaryGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new AnalysisApi();

  const body = {
    // Date | Start date for analysis (optional)
    startDate: 2013-10-20,
    // Date | End date for analysis (optional)
    endDate: 2013-10-20,
    // SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    mode: ...,
    // number | Number of top categories to return (optional)
    topN: 56,
    // number | Number of recent transactions to return (optional)
    recentCount: 56,
  } satisfies GetFinancialSummaryApiAnalysisSummaryGetRequest;

  try {
    const data = await api.getFinancialSummaryApiAnalysisSummaryGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **startDate** | `Date` | Start date for analysis | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date for analysis | [Optional] [Defaults to `undefined`] |
| **mode** | `SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum` | Analysis mode | [Optional] [Defaults to `undefined`] [Enum: analysis, with_capital, complete] |
| **topN** | `number` | Number of top categories to return | [Optional] [Defaults to `5`] |
| **recentCount** | `number` | Number of recent transactions to return | [Optional] [Defaults to `10`] |

### Return type

[**FinancialSummaryResponse**](FinancialSummaryResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getIncomeAnalysisApiAnalysisIncomeGet

> IncomeAnalysisResponse getIncomeAnalysisApiAnalysisIncomeGet(startDate, endDate, mode)

Get Income Analysis

Get income analysis for a period.  Args:     start_date: Start date for analysis     end_date: End date for analysis     mode: Analysis mode (analysis or complete)     db: Database session      Returns:     IncomeAnalysisResponse: Income analysis results

### Example

```ts
import {
  Configuration,
  AnalysisApi,
} from '@spearmint-money/sdk';
import type { GetIncomeAnalysisApiAnalysisIncomeGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new AnalysisApi();

  const body = {
    // Date | Start date for analysis (optional)
    startDate: 2013-10-20,
    // Date | End date for analysis (optional)
    endDate: 2013-10-20,
    // SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    mode: ...,
  } satisfies GetIncomeAnalysisApiAnalysisIncomeGetRequest;

  try {
    const data = await api.getIncomeAnalysisApiAnalysisIncomeGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **startDate** | `Date` | Start date for analysis | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date for analysis | [Optional] [Defaults to `undefined`] |
| **mode** | `SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum` | Analysis mode | [Optional] [Defaults to `undefined`] [Enum: analysis, with_capital, complete] |

### Return type

[**IncomeAnalysisResponse**](IncomeAnalysisResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getIncomeExpenseComparisonApiAnalysisIncomeExpenseGet

> IncomeExpenseComparisonResponse getIncomeExpenseComparisonApiAnalysisIncomeExpenseGet(startDate, endDate, mode, topN)

Get Income Expense Comparison

Get combined income and expense comparison.  This endpoint provides a side-by-side comparison of income and expenses including: - Detailed income analysis - Detailed expense analysis - Cash flow summary - Comparison metrics (ratios, percentages)  Args:     start_date: Start date for analysis     end_date: End date for analysis     mode: Analysis mode (analysis or complete)     top_n: Number of top categories to return     db: Database session  Returns:     IncomeExpenseComparisonResponse: Income vs expense comparison

### Example

```ts
import {
  Configuration,
  AnalysisApi,
} from '@spearmint-money/sdk';
import type { GetIncomeExpenseComparisonApiAnalysisIncomeExpenseGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new AnalysisApi();

  const body = {
    // Date | Start date for analysis (optional)
    startDate: 2013-10-20,
    // Date | End date for analysis (optional)
    endDate: 2013-10-20,
    // SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    mode: ...,
    // number | Number of top categories to return (optional)
    topN: 56,
  } satisfies GetIncomeExpenseComparisonApiAnalysisIncomeExpenseGetRequest;

  try {
    const data = await api.getIncomeExpenseComparisonApiAnalysisIncomeExpenseGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **startDate** | `Date` | Start date for analysis | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date for analysis | [Optional] [Defaults to `undefined`] |
| **mode** | `SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum` | Analysis mode | [Optional] [Defaults to `undefined`] [Enum: analysis, with_capital, complete] |
| **topN** | `number` | Number of top categories to return | [Optional] [Defaults to `10`] |

### Return type

[**IncomeExpenseComparisonResponse**](IncomeExpenseComparisonResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getIncomeTrendsApiAnalysisIncomeTrendsGet

> TrendsResponse getIncomeTrendsApiAnalysisIncomeTrendsGet(startDate, endDate, period, mode)

Get Income Trends

Get income trends over time.  Args:     start_date: Start date for analysis     end_date: End date for analysis     period: Period granularity (daily, weekly, monthly, etc.)     mode: Analysis mode     db: Database session      Returns:     TrendsResponse: Income trend data

### Example

```ts
import {
  Configuration,
  AnalysisApi,
} from '@spearmint-money/sdk';
import type { GetIncomeTrendsApiAnalysisIncomeTrendsGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new AnalysisApi();

  const body = {
    // Date | Start date for analysis (optional)
    startDate: 2013-10-20,
    // Date | End date for analysis (optional)
    endDate: 2013-10-20,
    // TimePeriodEnum | Period granularity (optional)
    period: ...,
    // SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum | Analysis mode (optional)
    mode: ...,
  } satisfies GetIncomeTrendsApiAnalysisIncomeTrendsGetRequest;

  try {
    const data = await api.getIncomeTrendsApiAnalysisIncomeTrendsGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **startDate** | `Date` | Start date for analysis | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date for analysis | [Optional] [Defaults to `undefined`] |
| **period** | `TimePeriodEnum` | Period granularity | [Optional] [Defaults to `undefined`] [Enum: daily, weekly, monthly, quarterly, yearly] |
| **mode** | `SrcFinancialAnalysisApiSchemasAnalysisAnalysisModeEnum` | Analysis mode | [Optional] [Defaults to `undefined`] [Enum: analysis, with_capital, complete] |

### Return type

[**TrendsResponse**](TrendsResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

