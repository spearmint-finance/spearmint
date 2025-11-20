# ReportsApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**getBalanceReportApiReportsBalancesGet**](ReportsApi.md#getbalancereportapireportsbalancesget) | **GET** /api/reports/balances | Generate Balance Sheet / Net Worth Report |
| [**getExpenseDetailReportApiReportsExpensesGet**](ReportsApi.md#getexpensedetailreportapireportsexpensesget) | **GET** /api/reports/expenses | Generate Expense Detail Report |
| [**getIncomeDetailReportApiReportsIncomeGet**](ReportsApi.md#getincomedetailreportapireportsincomeget) | **GET** /api/reports/income | Generate Income Detail Report |
| [**getReconciliationReportApiReportsReconciliationGet**](ReportsApi.md#getreconciliationreportapireportsreconciliationget) | **GET** /api/reports/reconciliation | Generate Reconciliation Report |
| [**getSummaryReportApiReportsSummaryGet**](ReportsApi.md#getsummaryreportapireportssummaryget) | **GET** /api/reports/summary | Generate Summary Report |



## getBalanceReportApiReportsBalancesGet

> BalanceReportResponse getBalanceReportApiReportsBalancesGet()

Generate Balance Sheet / Net Worth Report

Generate a report of all account balances and net worth.

### Example

```ts
import {
  Configuration,
  ReportsApi,
} from '@spearmint-money/sdk';
import type { GetBalanceReportApiReportsBalancesGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ReportsApi();

  try {
    const data = await api.getBalanceReportApiReportsBalancesGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**BalanceReportResponse**](BalanceReportResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getExpenseDetailReportApiReportsExpensesGet

> ExpenseDetailReportResponse getExpenseDetailReportApiReportsExpensesGet(startDate, endDate, mode, format)

Generate Expense Detail Report

Generate a detailed expense report showing:     - Total expenses for the period     - Transaction count and averages     - Complete breakdown by category with percentages          Useful for understanding spending patterns and identifying areas for optimization.

### Example

```ts
import {
  Configuration,
  ReportsApi,
} from '@spearmint-money/sdk';
import type { GetExpenseDetailReportApiReportsExpensesGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ReportsApi();

  const body = {
    // Date | Start date (default: 30 days ago) (optional)
    startDate: 2013-10-20,
    // Date | End date (default: today) (optional)
    endDate: 2013-10-20,
    // SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum | Analysis mode: \'analysis\' excludes transfers, \'complete\' includes all (optional)
    mode: ...,
    // ReportFormatEnum | Export format: \'json\' or \'csv\' (optional)
    format: ...,
  } satisfies GetExpenseDetailReportApiReportsExpensesGetRequest;

  try {
    const data = await api.getExpenseDetailReportApiReportsExpensesGet(body);
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
| **startDate** | `Date` | Start date (default: 30 days ago) | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date (default: today) | [Optional] [Defaults to `undefined`] |
| **mode** | `SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum` | Analysis mode: \&#39;analysis\&#39; excludes transfers, \&#39;complete\&#39; includes all | [Optional] [Defaults to `undefined`] [Enum: analysis, complete] |
| **format** | `ReportFormatEnum` | Export format: \&#39;json\&#39; or \&#39;csv\&#39; | [Optional] [Defaults to `undefined`] [Enum: json, csv] |

### Return type

[**ExpenseDetailReportResponse**](ExpenseDetailReportResponse.md)

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


## getIncomeDetailReportApiReportsIncomeGet

> IncomeDetailReportResponse getIncomeDetailReportApiReportsIncomeGet(startDate, endDate, mode, format)

Generate Income Detail Report

Generate a detailed income report showing:     - Total income for the period     - Transaction count and averages     - Complete breakdown by category with percentages          Useful for understanding income sources and patterns.

### Example

```ts
import {
  Configuration,
  ReportsApi,
} from '@spearmint-money/sdk';
import type { GetIncomeDetailReportApiReportsIncomeGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ReportsApi();

  const body = {
    // Date | Start date (default: 30 days ago) (optional)
    startDate: 2013-10-20,
    // Date | End date (default: today) (optional)
    endDate: 2013-10-20,
    // SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum | Analysis mode: \'analysis\' excludes transfers, \'complete\' includes all (optional)
    mode: ...,
    // ReportFormatEnum | Export format: \'json\' or \'csv\' (optional)
    format: ...,
  } satisfies GetIncomeDetailReportApiReportsIncomeGetRequest;

  try {
    const data = await api.getIncomeDetailReportApiReportsIncomeGet(body);
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
| **startDate** | `Date` | Start date (default: 30 days ago) | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date (default: today) | [Optional] [Defaults to `undefined`] |
| **mode** | `SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum` | Analysis mode: \&#39;analysis\&#39; excludes transfers, \&#39;complete\&#39; includes all | [Optional] [Defaults to `undefined`] [Enum: analysis, complete] |
| **format** | `ReportFormatEnum` | Export format: \&#39;json\&#39; or \&#39;csv\&#39; | [Optional] [Defaults to `undefined`] [Enum: json, csv] |

### Return type

[**IncomeDetailReportResponse**](IncomeDetailReportResponse.md)

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


## getReconciliationReportApiReportsReconciliationGet

> ReconciliationReportResponse getReconciliationReportApiReportsReconciliationGet(startDate, endDate, format)

Generate Reconciliation Report

Generate a reconciliation report showing ALL transactions including transfers.          This report uses COMPLETE mode to show:     - All transactions in the period (including transfers, credit card payments, etc.)     - Complete transaction details for reconciliation     - Summary statistics          Useful for:     - Bank reconciliation     - Verifying all transactions are accounted for     - Auditing purposes     - Complete financial picture

### Example

```ts
import {
  Configuration,
  ReportsApi,
} from '@spearmint-money/sdk';
import type { GetReconciliationReportApiReportsReconciliationGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ReportsApi();

  const body = {
    // Date | Start date (default: 30 days ago) (optional)
    startDate: 2013-10-20,
    // Date | End date (default: today) (optional)
    endDate: 2013-10-20,
    // ReportFormatEnum | Export format: \'json\' or \'csv\' (optional)
    format: ...,
  } satisfies GetReconciliationReportApiReportsReconciliationGetRequest;

  try {
    const data = await api.getReconciliationReportApiReportsReconciliationGet(body);
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
| **startDate** | `Date` | Start date (default: 30 days ago) | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date (default: today) | [Optional] [Defaults to `undefined`] |
| **format** | `ReportFormatEnum` | Export format: \&#39;json\&#39; or \&#39;csv\&#39; | [Optional] [Defaults to `undefined`] [Enum: json, csv] |

### Return type

[**ReconciliationReportResponse**](ReconciliationReportResponse.md)

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


## getSummaryReportApiReportsSummaryGet

> SummaryReportResponse getSummaryReportApiReportsSummaryGet(startDate, endDate, mode, format)

Generate Summary Report

Generate a comprehensive financial summary report including:     - Income summary with top categories     - Expense summary with top categories     - Cash flow summary     - Financial health indicators          The report can be generated in JSON or CSV format.

### Example

```ts
import {
  Configuration,
  ReportsApi,
} from '@spearmint-money/sdk';
import type { GetSummaryReportApiReportsSummaryGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ReportsApi();

  const body = {
    // Date | Start date (default: 30 days ago) (optional)
    startDate: 2013-10-20,
    // Date | End date (default: today) (optional)
    endDate: 2013-10-20,
    // SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum | Analysis mode: \'analysis\' excludes transfers, \'complete\' includes all (optional)
    mode: ...,
    // ReportFormatEnum | Export format: \'json\' or \'csv\' (optional)
    format: ...,
  } satisfies GetSummaryReportApiReportsSummaryGetRequest;

  try {
    const data = await api.getSummaryReportApiReportsSummaryGet(body);
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
| **startDate** | `Date` | Start date (default: 30 days ago) | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date (default: today) | [Optional] [Defaults to `undefined`] |
| **mode** | `SrcFinancialAnalysisApiSchemasReportAnalysisModeEnum` | Analysis mode: \&#39;analysis\&#39; excludes transfers, \&#39;complete\&#39; includes all | [Optional] [Defaults to `undefined`] [Enum: analysis, complete] |
| **format** | `ReportFormatEnum` | Export format: \&#39;json\&#39; or \&#39;csv\&#39; | [Optional] [Defaults to `undefined`] [Enum: json, csv] |

### Return type

[**SummaryReportResponse**](SummaryReportResponse.md)

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

