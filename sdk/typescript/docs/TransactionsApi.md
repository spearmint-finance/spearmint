# TransactionsApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createTransactionApiTransactionsPost**](TransactionsApi.md#createtransactionapitransactionspost) | **POST** /api/transactions | Create Transaction |
| [**deleteTransactionApiTransactionsTransactionIdDelete**](TransactionsApi.md#deletetransactionapitransactionstransactioniddelete) | **DELETE** /api/transactions/{transaction_id} | Delete Transaction |
| [**getTransactionApiTransactionsTransactionIdGet**](TransactionsApi.md#gettransactionapitransactionstransactionidget) | **GET** /api/transactions/{transaction_id} | Get Transaction |
| [**listTransactionsApiTransactionsGet**](TransactionsApi.md#listtransactionsapitransactionsget) | **GET** /api/transactions | List Transactions |
| [**updateTransactionApiTransactionsTransactionIdPut**](TransactionsApi.md#updatetransactionapitransactionstransactionidput) | **PUT** /api/transactions/{transaction_id} | Update Transaction |



## createTransactionApiTransactionsPost

> TransactionResponse createTransactionApiTransactionsPost(transactionCreate)

Create Transaction

Create a new transaction.  Args:     transaction: Transaction data     db: Database session      Returns:     TransactionResponse: Created transaction

### Example

```ts
import {
  Configuration,
  TransactionsApi,
} from '@spearmint-money/sdk';
import type { CreateTransactionApiTransactionsPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new TransactionsApi();

  const body = {
    // TransactionCreate
    transactionCreate: ...,
  } satisfies CreateTransactionApiTransactionsPostRequest;

  try {
    const data = await api.createTransactionApiTransactionsPost(body);
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
| **transactionCreate** | [TransactionCreate](TransactionCreate.md) |  | |

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## deleteTransactionApiTransactionsTransactionIdDelete

> SuccessResponse deleteTransactionApiTransactionsTransactionIdDelete(transactionId)

Delete Transaction

Delete transaction.  Args:     transaction_id: Transaction ID     db: Database session      Returns:     SuccessResponse: Success message

### Example

```ts
import {
  Configuration,
  TransactionsApi,
} from '@spearmint-money/sdk';
import type { DeleteTransactionApiTransactionsTransactionIdDeleteRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new TransactionsApi();

  const body = {
    // number
    transactionId: 56,
  } satisfies DeleteTransactionApiTransactionsTransactionIdDeleteRequest;

  try {
    const data = await api.deleteTransactionApiTransactionsTransactionIdDelete(body);
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
| **transactionId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**SuccessResponse**](SuccessResponse.md)

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


## getTransactionApiTransactionsTransactionIdGet

> TransactionResponse getTransactionApiTransactionsTransactionIdGet(transactionId)

Get Transaction

Get transaction by ID.  Args:     transaction_id: Transaction ID     db: Database session      Returns:     TransactionResponse: Transaction data

### Example

```ts
import {
  Configuration,
  TransactionsApi,
} from '@spearmint-money/sdk';
import type { GetTransactionApiTransactionsTransactionIdGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new TransactionsApi();

  const body = {
    // number
    transactionId: 56,
  } satisfies GetTransactionApiTransactionsTransactionIdGetRequest;

  try {
    const data = await api.getTransactionApiTransactionsTransactionIdGet(body);
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
| **transactionId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

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


## listTransactionsApiTransactionsGet

> TransactionListResponse listTransactionsApiTransactionsGet(startDate, endDate, transactionType, categoryId, classificationId, includeInAnalysis, isTransfer, minAmount, maxAmount, searchText, includeCapitalExpenses, includeTransfers, limit, offset, sortBy, sortOrder)

List Transactions

List transactions with optional filters.  Args:     Various filter parameters     db: Database session  Returns:     TransactionListResponse: List of transactions

### Example

```ts
import {
  Configuration,
  TransactionsApi,
} from '@spearmint-money/sdk';
import type { ListTransactionsApiTransactionsGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new TransactionsApi();

  const body = {
    // Date | Start date filter (optional)
    startDate: 2013-10-20,
    // Date | End date filter (optional)
    endDate: 2013-10-20,
    // string | Transaction type filter (optional)
    transactionType: transactionType_example,
    // number | Category ID filter (optional)
    categoryId: 56,
    // number | Classification ID filter (optional)
    classificationId: 56,
    // boolean | Include in analysis filter (optional)
    includeInAnalysis: true,
    // boolean | Is transfer filter (optional)
    isTransfer: true,
    // MinAmount | Minimum amount filter (optional)
    minAmount: ...,
    // MaxAmount | Maximum amount filter (optional)
    maxAmount: ...,
    // string | Search in description, source, notes (optional)
    searchText: searchText_example,
    // boolean | Include non-operating expenses (capital, refunds, reimbursements, etc.) in results (optional)
    includeCapitalExpenses: true,
    // boolean | Include transfers in results (optional)
    includeTransfers: true,
    // number | Maximum number of results (optional)
    limit: 56,
    // number | Number of results to skip (optional)
    offset: 56,
    // string | Field to sort by (optional)
    sortBy: sortBy_example,
    // string | Sort order (optional)
    sortOrder: sortOrder_example,
  } satisfies ListTransactionsApiTransactionsGetRequest;

  try {
    const data = await api.listTransactionsApiTransactionsGet(body);
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
| **startDate** | `Date` | Start date filter | [Optional] [Defaults to `undefined`] |
| **endDate** | `Date` | End date filter | [Optional] [Defaults to `undefined`] |
| **transactionType** | `string` | Transaction type filter | [Optional] [Defaults to `undefined`] |
| **categoryId** | `number` | Category ID filter | [Optional] [Defaults to `undefined`] |
| **classificationId** | `number` | Classification ID filter | [Optional] [Defaults to `undefined`] |
| **includeInAnalysis** | `boolean` | Include in analysis filter | [Optional] [Defaults to `undefined`] |
| **isTransfer** | `boolean` | Is transfer filter | [Optional] [Defaults to `undefined`] |
| **minAmount** | [](.md) | Minimum amount filter | [Optional] [Defaults to `undefined`] |
| **maxAmount** | [](.md) | Maximum amount filter | [Optional] [Defaults to `undefined`] |
| **searchText** | `string` | Search in description, source, notes | [Optional] [Defaults to `undefined`] |
| **includeCapitalExpenses** | `boolean` | Include non-operating expenses (capital, refunds, reimbursements, etc.) in results | [Optional] [Defaults to `true`] |
| **includeTransfers** | `boolean` | Include transfers in results | [Optional] [Defaults to `true`] |
| **limit** | `number` | Maximum number of results | [Optional] [Defaults to `100`] |
| **offset** | `number` | Number of results to skip | [Optional] [Defaults to `0`] |
| **sortBy** | `string` | Field to sort by | [Optional] [Defaults to `&#39;transaction_date&#39;`] |
| **sortOrder** | `string` | Sort order | [Optional] [Defaults to `&#39;desc&#39;`] |

### Return type

[**TransactionListResponse**](TransactionListResponse.md)

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


## updateTransactionApiTransactionsTransactionIdPut

> TransactionResponse updateTransactionApiTransactionsTransactionIdPut(transactionId, transactionUpdate, reapplyRules)

Update Transaction

Update transaction.  Args:     transaction_id: Transaction ID     transaction: Updated transaction data     db: Database session      Returns:     TransactionResponse: Updated transaction

### Example

```ts
import {
  Configuration,
  TransactionsApi,
} from '@spearmint-money/sdk';
import type { UpdateTransactionApiTransactionsTransactionIdPutRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new TransactionsApi();

  const body = {
    // number
    transactionId: 56,
    // TransactionUpdate
    transactionUpdate: ...,
    // boolean | If true, re-apply classification rules (optional)
    reapplyRules: true,
  } satisfies UpdateTransactionApiTransactionsTransactionIdPutRequest;

  try {
    const data = await api.updateTransactionApiTransactionsTransactionIdPut(body);
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
| **transactionId** | `number` |  | [Defaults to `undefined`] |
| **transactionUpdate** | [TransactionUpdate](TransactionUpdate.md) |  | |
| **reapplyRules** | `boolean` | If true, re-apply classification rules | [Optional] [Defaults to `undefined`] |

### Return type

[**TransactionResponse**](TransactionResponse.md)

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

