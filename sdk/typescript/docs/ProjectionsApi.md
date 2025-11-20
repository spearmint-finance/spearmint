# ProjectionsApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**getScenariosApiProjectionsScenariosGet**](ProjectionsApi.md#getscenariosapiprojectionsscenariosget) | **GET** /api/projections/scenarios | Get Scenario Analysis |
| [**projectCashflowApiProjectionsCashflowGet**](ProjectionsApi.md#projectcashflowapiprojectionscashflowget) | **GET** /api/projections/cashflow | Project Future Cash Flow |
| [**projectExpensesApiProjectionsExpensesGet**](ProjectionsApi.md#projectexpensesapiprojectionsexpensesget) | **GET** /api/projections/expenses | Project Future Expenses |
| [**projectIncomeApiProjectionsIncomeGet**](ProjectionsApi.md#projectincomeapiprojectionsincomeget) | **GET** /api/projections/income | Project Future Income |
| [**validateProjectionApiProjectionsValidatePost**](ProjectionsApi.md#validateprojectionapiprojectionsvalidatepost) | **POST** /api/projections/validate | Validate Projection Accuracy |



## getScenariosApiProjectionsScenariosGet

> CashflowProjectionResponse getScenariosApiProjectionsScenariosGet(startDate, endDate, projectionDays, method)

Get Scenario Analysis

Get detailed scenario analysis for cash flow projections

### Example

```ts
import {
  Configuration,
  ProjectionsApi,
} from '@spearmint-money/sdk';
import type { GetScenariosApiProjectionsScenariosGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ProjectionsApi();

  const body = {
    // Date | Start of historical period (optional)
    startDate: 2013-10-20,
    // Date | End of historical period (optional)
    endDate: 2013-10-20,
    // number | Number of days to project (optional)
    projectionDays: 56,
    // ProjectionMethodEnum | Projection method (optional)
    method: ...,
  } satisfies GetScenariosApiProjectionsScenariosGetRequest;

  try {
    const data = await api.getScenariosApiProjectionsScenariosGet(body);
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
| **startDate** | `Date` | Start of historical period | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End of historical period | [Optional] [Defaults to `undefined`] |
| **projectionDays** | `number` | Number of days to project | [Optional] [Defaults to `90`] |
| **method** | `ProjectionMethodEnum` | Projection method | [Optional] [Defaults to `undefined`] [Enum: linear_regression, moving_average, exponential_smoothing, weighted_average] |

### Return type

[**CashflowProjectionResponse**](CashflowProjectionResponse.md)

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


## projectCashflowApiProjectionsCashflowGet

> CashflowProjectionResponse projectCashflowApiProjectionsCashflowGet(startDate, endDate, projectionDays, method, confidenceLevel, includeScenarios)

Project Future Cash Flow

Generate cash flow projections with scenario analysis

### Example

```ts
import {
  Configuration,
  ProjectionsApi,
} from '@spearmint-money/sdk';
import type { ProjectCashflowApiProjectionsCashflowGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ProjectionsApi();

  const body = {
    // Date | Start of historical period (default: 1 year ago) (optional)
    startDate: 2013-10-20,
    // Date | End of historical period (default: today) (optional)
    endDate: 2013-10-20,
    // number | Number of days to project forward (optional)
    projectionDays: 56,
    // ProjectionMethodEnum | Projection algorithm to use (optional)
    method: ...,
    // number | Confidence level for intervals (optional)
    confidenceLevel: 8.14,
    // boolean | Include best/worst case scenarios (optional)
    includeScenarios: true,
  } satisfies ProjectCashflowApiProjectionsCashflowGetRequest;

  try {
    const data = await api.projectCashflowApiProjectionsCashflowGet(body);
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
| **startDate** | `Date` | Start of historical period (default: 1 year ago) | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End of historical period (default: today) | [Optional] [Defaults to `undefined`] |
| **projectionDays** | `number` | Number of days to project forward | [Optional] [Defaults to `90`] |
| **method** | `ProjectionMethodEnum` | Projection algorithm to use | [Optional] [Defaults to `undefined`] [Enum: linear_regression, moving_average, exponential_smoothing, weighted_average] |
| **confidenceLevel** | `number` | Confidence level for intervals | [Optional] [Defaults to `0.95`] |
| **includeScenarios** | `boolean` | Include best/worst case scenarios | [Optional] [Defaults to `true`] |

### Return type

[**CashflowProjectionResponse**](CashflowProjectionResponse.md)

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


## projectExpensesApiProjectionsExpensesGet

> ExpenseProjectionResponse projectExpensesApiProjectionsExpensesGet(startDate, endDate, projectionDays, method, confidenceLevel)

Project Future Expenses

Generate expense projections based on historical data using statistical methods

### Example

```ts
import {
  Configuration,
  ProjectionsApi,
} from '@spearmint-money/sdk';
import type { ProjectExpensesApiProjectionsExpensesGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ProjectionsApi();

  const body = {
    // Date | Start of historical period (default: 1 year ago) (optional)
    startDate: 2013-10-20,
    // Date | End of historical period (default: today) (optional)
    endDate: 2013-10-20,
    // number | Number of days to project forward (optional)
    projectionDays: 56,
    // ProjectionMethodEnum | Projection algorithm to use (optional)
    method: ...,
    // number | Confidence level for intervals (optional)
    confidenceLevel: 8.14,
  } satisfies ProjectExpensesApiProjectionsExpensesGetRequest;

  try {
    const data = await api.projectExpensesApiProjectionsExpensesGet(body);
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
| **startDate** | `Date` | Start of historical period (default: 1 year ago) | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End of historical period (default: today) | [Optional] [Defaults to `undefined`] |
| **projectionDays** | `number` | Number of days to project forward | [Optional] [Defaults to `90`] |
| **method** | `ProjectionMethodEnum` | Projection algorithm to use | [Optional] [Defaults to `undefined`] [Enum: linear_regression, moving_average, exponential_smoothing, weighted_average] |
| **confidenceLevel** | `number` | Confidence level for intervals | [Optional] [Defaults to `0.95`] |

### Return type

[**ExpenseProjectionResponse**](ExpenseProjectionResponse.md)

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


## projectIncomeApiProjectionsIncomeGet

> IncomeProjectionResponse projectIncomeApiProjectionsIncomeGet(startDate, endDate, projectionDays, method, confidenceLevel)

Project Future Income

Generate income projections based on historical data using statistical methods

### Example

```ts
import {
  Configuration,
  ProjectionsApi,
} from '@spearmint-money/sdk';
import type { ProjectIncomeApiProjectionsIncomeGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ProjectionsApi();

  const body = {
    // Date | Start of historical period (default: 1 year ago) (optional)
    startDate: 2013-10-20,
    // Date | End of historical period (default: today) (optional)
    endDate: 2013-10-20,
    // number | Number of days to project forward (optional)
    projectionDays: 56,
    // ProjectionMethodEnum | Projection algorithm to use (optional)
    method: ...,
    // number | Confidence level for intervals (optional)
    confidenceLevel: 8.14,
  } satisfies ProjectIncomeApiProjectionsIncomeGetRequest;

  try {
    const data = await api.projectIncomeApiProjectionsIncomeGet(body);
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
| **startDate** | `Date` | Start of historical period (default: 1 year ago) | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End of historical period (default: today) | [Optional] [Defaults to `undefined`] |
| **projectionDays** | `number` | Number of days to project forward | [Optional] [Defaults to `90`] |
| **method** | `ProjectionMethodEnum` | Projection algorithm to use | [Optional] [Defaults to `undefined`] [Enum: linear_regression, moving_average, exponential_smoothing, weighted_average] |
| **confidenceLevel** | `number` | Confidence level for intervals | [Optional] [Defaults to `0.95`] |

### Return type

[**IncomeProjectionResponse**](IncomeProjectionResponse.md)

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


## validateProjectionApiProjectionsValidatePost

> AccuracyMetrics validateProjectionApiProjectionsValidatePost(validationRequest)

Validate Projection Accuracy

Calculate accuracy metrics for projection validation

### Example

```ts
import {
  Configuration,
  ProjectionsApi,
} from '@spearmint-money/sdk';
import type { ValidateProjectionApiProjectionsValidatePostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ProjectionsApi();

  const body = {
    // ValidationRequest
    validationRequest: ...,
  } satisfies ValidateProjectionApiProjectionsValidatePostRequest;

  try {
    const data = await api.validateProjectionApiProjectionsValidatePost(body);
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
| **validationRequest** | [ValidationRequest](ValidationRequest.md) |  | |

### Return type

[**AccuracyMetrics**](AccuracyMetrics.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

