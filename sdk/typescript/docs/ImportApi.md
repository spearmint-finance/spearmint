# ImportApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**getImportDetailApiImportHistoryImportIdGet**](ImportApi.md#getimportdetailapiimporthistoryimportidget) | **GET** /api/import/history/{import_id} | Get Import Detail |
| [**getImportHistoryApiImportHistoryGet**](ImportApi.md#getimporthistoryapiimporthistoryget) | **GET** /api/import/history | Get Import History |
| [**getImportStatusApiImportStatusImportIdGet**](ImportApi.md#getimportstatusapiimportstatusimportidget) | **GET** /api/import/status/{import_id} | Get Import Status |
| [**importFromFilePathApiImportFilePathPost**](ImportApi.md#importfromfilepathapiimportfilepathpost) | **POST** /api/import/file-path | Import From File Path |
| [**importTransactionsApiImportPost**](ImportApi.md#importtransactionsapiimportpost) | **POST** /api/import | Import Transactions |



## getImportDetailApiImportHistoryImportIdGet

> ImportHistoryDetailResponse getImportDetailApiImportHistoryImportIdGet(importId)

Get Import Detail

Get detailed information about a specific import.  Returns detailed information including error logs and full statistics.  Args:     import_id: Import ID     db: Database session  Returns:     ImportHistoryDetailResponse: Detailed import information

### Example

```ts
import {
  Configuration,
  ImportApi,
} from '@spearmint-money/sdk';
import type { GetImportDetailApiImportHistoryImportIdGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ImportApi();

  const body = {
    // number
    importId: 56,
  } satisfies GetImportDetailApiImportHistoryImportIdGetRequest;

  try {
    const data = await api.getImportDetailApiImportHistoryImportIdGet(body);
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
| **importId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**ImportHistoryDetailResponse**](ImportHistoryDetailResponse.md)

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


## getImportHistoryApiImportHistoryGet

> ImportHistoryResponse getImportHistoryApiImportHistoryGet(limit, offset)

Get Import History

Get import history.  Returns a list of past imports with statistics including: - Import date and file name - Total rows, successful rows, failed rows - Classification statistics - Success rate  Args:     limit: Maximum number of imports to return     offset: Number of imports to skip (for pagination)     db: Database session  Returns:     ImportHistoryResponse: List of import history items

### Example

```ts
import {
  Configuration,
  ImportApi,
} from '@spearmint-money/sdk';
import type { GetImportHistoryApiImportHistoryGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ImportApi();

  const body = {
    // number | Maximum number of imports to return (optional)
    limit: 56,
    // number | Number of imports to skip (optional)
    offset: 56,
  } satisfies GetImportHistoryApiImportHistoryGetRequest;

  try {
    const data = await api.getImportHistoryApiImportHistoryGet(body);
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
| **limit** | `number` | Maximum number of imports to return | [Optional] [Defaults to `50`] |
| **offset** | `number` | Number of imports to skip | [Optional] [Defaults to `0`] |

### Return type

[**ImportHistoryResponse**](ImportHistoryResponse.md)

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


## getImportStatusApiImportStatusImportIdGet

> ImportStatusResponse getImportStatusApiImportStatusImportIdGet(importId)

Get Import Status

Get real-time import status.  This endpoint provides progress tracking for ongoing imports. For completed imports, it returns the final status.  Args:     import_id: Import ID     db: Database session  Returns:     ImportStatusResponse: Import status and progress

### Example

```ts
import {
  Configuration,
  ImportApi,
} from '@spearmint-money/sdk';
import type { GetImportStatusApiImportStatusImportIdGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ImportApi();

  const body = {
    // number
    importId: 56,
  } satisfies GetImportStatusApiImportStatusImportIdGetRequest;

  try {
    const data = await api.getImportStatusApiImportStatusImportIdGet(body);
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
| **importId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**ImportStatusResponse**](ImportStatusResponse.md)

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


## importFromFilePathApiImportFilePathPost

> ImportResponse importFromFilePathApiImportFilePathPost(filePath, importRequest)

Import From File Path

Import transactions from file path (for local development).  Args:     file_path: Path to Excel file     request: Import request parameters     db: Database session      Returns:     ImportResponse: Import result

### Example

```ts
import {
  Configuration,
  ImportApi,
} from '@spearmint-money/sdk';
import type { ImportFromFilePathApiImportFilePathPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ImportApi();

  const body = {
    // string
    filePath: filePath_example,
    // ImportRequest
    importRequest: ...,
  } satisfies ImportFromFilePathApiImportFilePathPostRequest;

  try {
    const data = await api.importFromFilePathApiImportFilePathPost(body);
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
| **filePath** | `string` |  | [Defaults to `undefined`] |
| **importRequest** | [ImportRequest](ImportRequest.md) |  | |

### Return type

[**ImportResponse**](ImportResponse.md)

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


## importTransactionsApiImportPost

> ImportResponse importTransactionsApiImportPost(file, mode, skipDuplicates)

Import Transactions

Import transactions from Excel file.  Args:     file: Uploaded Excel file     mode: Import mode (full, incremental, update)     skip_duplicates: Whether to skip duplicates     db: Database session      Returns:     ImportResponse: Import result

### Example

```ts
import {
  Configuration,
  ImportApi,
} from '@spearmint-money/sdk';
import type { ImportTransactionsApiImportPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ImportApi();

  const body = {
    // Blob | Excel file to import
    file: BINARY_DATA_HERE,
    // string | Import mode (optional)
    mode: mode_example,
    // boolean | Skip duplicate transactions (optional)
    skipDuplicates: true,
  } satisfies ImportTransactionsApiImportPostRequest;

  try {
    const data = await api.importTransactionsApiImportPost(body);
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
| **file** | `Blob` | Excel file to import | [Defaults to `undefined`] |
| **mode** | `string` | Import mode | [Optional] [Defaults to `&#39;incremental&#39;`] |
| **skipDuplicates** | `boolean` | Skip duplicate transactions | [Optional] [Defaults to `true`] |

### Return type

[**ImportResponse**](ImportResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `multipart/form-data`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

