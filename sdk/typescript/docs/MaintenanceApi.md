# MaintenanceApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**fixClassificationsApiMaintenanceFixClassificationsPost**](MaintenanceApi.md#fixclassificationsapimaintenancefixclassificationspost) | **POST** /api/maintenance/fix/classifications | Fix System Classifications |
| [**fixClassificationsApiMaintenanceFixClassificationsPost_0**](MaintenanceApi.md#fixclassificationsapimaintenancefixclassificationspost_0) | **POST** /api/maintenance/fix/classifications | Fix System Classifications |
| [**fixReimbursementsApiMaintenanceFixReimbursementsPost**](MaintenanceApi.md#fixreimbursementsapimaintenancefixreimbursementspost) | **POST** /api/maintenance/fix/reimbursements | Fix Reimbursement Links |
| [**fixReimbursementsApiMaintenanceFixReimbursementsPost_0**](MaintenanceApi.md#fixreimbursementsapimaintenancefixreimbursementspost_0) | **POST** /api/maintenance/fix/reimbursements | Fix Reimbursement Links |
| [**fixTransfersApiMaintenanceFixTransfersPost**](MaintenanceApi.md#fixtransfersapimaintenancefixtransferspost) | **POST** /api/maintenance/fix/transfers | Fix Transfer Links |
| [**fixTransfersApiMaintenanceFixTransfersPost_0**](MaintenanceApi.md#fixtransfersapimaintenancefixtransferspost_0) | **POST** /api/maintenance/fix/transfers | Fix Transfer Links |



## fixClassificationsApiMaintenanceFixClassificationsPost

> FixResult fixClassificationsApiMaintenanceFixClassificationsPost()

Fix System Classifications

Repair incorrect system classifications.     - Fixes \&#39;Insurance Reimbursement\&#39; cash flow settings     - Removes duplicate/legacy classifications (\&#39;STANDARD\&#39;, \&#39;REIMB_RECEIVED\&#39;)

### Example

```ts
import {
  Configuration,
  MaintenanceApi,
} from '@spearmint-money/sdk';
import type { FixClassificationsApiMaintenanceFixClassificationsPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new MaintenanceApi();

  try {
    const data = await api.fixClassificationsApiMaintenanceFixClassificationsPost();
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

[**FixResult**](FixResult.md)

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


## fixClassificationsApiMaintenanceFixClassificationsPost_0

> FixResult fixClassificationsApiMaintenanceFixClassificationsPost_0()

Fix System Classifications

Repair incorrect system classifications.     - Fixes \&#39;Insurance Reimbursement\&#39; cash flow settings     - Removes duplicate/legacy classifications (\&#39;STANDARD\&#39;, \&#39;REIMB_RECEIVED\&#39;)

### Example

```ts
import {
  Configuration,
  MaintenanceApi,
} from '@spearmint-money/sdk';
import type { FixClassificationsApiMaintenanceFixClassificationsPost0Request } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new MaintenanceApi();

  try {
    const data = await api.fixClassificationsApiMaintenanceFixClassificationsPost_0();
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

[**FixResult**](FixResult.md)

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


## fixReimbursementsApiMaintenanceFixReimbursementsPost

> FixResult fixReimbursementsApiMaintenanceFixReimbursementsPost()

Fix Reimbursement Links

Links reimbursement expenses to income.

### Example

```ts
import {
  Configuration,
  MaintenanceApi,
} from '@spearmint-money/sdk';
import type { FixReimbursementsApiMaintenanceFixReimbursementsPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new MaintenanceApi();

  try {
    const data = await api.fixReimbursementsApiMaintenanceFixReimbursementsPost();
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

[**FixResult**](FixResult.md)

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


## fixReimbursementsApiMaintenanceFixReimbursementsPost_0

> FixResult fixReimbursementsApiMaintenanceFixReimbursementsPost_0()

Fix Reimbursement Links

Links reimbursement expenses to income.

### Example

```ts
import {
  Configuration,
  MaintenanceApi,
} from '@spearmint-money/sdk';
import type { FixReimbursementsApiMaintenanceFixReimbursementsPost0Request } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new MaintenanceApi();

  try {
    const data = await api.fixReimbursementsApiMaintenanceFixReimbursementsPost_0();
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

[**FixResult**](FixResult.md)

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


## fixTransfersApiMaintenanceFixTransfersPost

> FixResult fixTransfersApiMaintenanceFixTransfersPost()

Fix Transfer Links

Attempts to link orphaned transfers based on amount and date proximity.

### Example

```ts
import {
  Configuration,
  MaintenanceApi,
} from '@spearmint-money/sdk';
import type { FixTransfersApiMaintenanceFixTransfersPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new MaintenanceApi();

  try {
    const data = await api.fixTransfersApiMaintenanceFixTransfersPost();
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

[**FixResult**](FixResult.md)

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


## fixTransfersApiMaintenanceFixTransfersPost_0

> FixResult fixTransfersApiMaintenanceFixTransfersPost_0()

Fix Transfer Links

Attempts to link orphaned transfers based on amount and date proximity.

### Example

```ts
import {
  Configuration,
  MaintenanceApi,
} from '@spearmint-money/sdk';
import type { FixTransfersApiMaintenanceFixTransfersPost0Request } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new MaintenanceApi();

  try {
    const data = await api.fixTransfersApiMaintenanceFixTransfersPost_0();
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

[**FixResult**](FixResult.md)

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

