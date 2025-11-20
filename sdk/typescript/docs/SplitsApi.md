# SplitsApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createTransactionSplitApiTransactionsTransactionIdSplitsPost**](SplitsApi.md#createtransactionsplitapitransactionstransactionidsplitspost) | **POST** /api/transactions/{transaction_id}/splits | Create Transaction Split |
| [**createTransactionSplitApiTransactionsTransactionIdSplitsPost_0**](SplitsApi.md#createtransactionsplitapitransactionstransactionidsplitspost_0) | **POST** /api/transactions/{transaction_id}/splits | Create Transaction Split |
| [**getTransactionSplitsApiTransactionsTransactionIdSplitsGet**](SplitsApi.md#gettransactionsplitsapitransactionstransactionidsplitsget) | **GET** /api/transactions/{transaction_id}/splits | Get Transaction Splits |
| [**getTransactionSplitsApiTransactionsTransactionIdSplitsGet_0**](SplitsApi.md#gettransactionsplitsapitransactionstransactionidsplitsget_0) | **GET** /api/transactions/{transaction_id}/splits | Get Transaction Splits |



## createTransactionSplitApiTransactionsTransactionIdSplitsPost

> TransactionSplitRead createTransactionSplitApiTransactionsTransactionIdSplitsPost(transactionId, transactionSplitCreate)

Create Transaction Split

### Example

```ts
import {
  Configuration,
  SplitsApi,
} from '@spearmint-money/sdk';
import type { CreateTransactionSplitApiTransactionsTransactionIdSplitsPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new SplitsApi();

  const body = {
    // number
    transactionId: 56,
    // TransactionSplitCreate
    transactionSplitCreate: ...,
  } satisfies CreateTransactionSplitApiTransactionsTransactionIdSplitsPostRequest;

  try {
    const data = await api.createTransactionSplitApiTransactionsTransactionIdSplitsPost(body);
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
| **transactionSplitCreate** | [TransactionSplitCreate](TransactionSplitCreate.md) |  | |

### Return type

[**TransactionSplitRead**](TransactionSplitRead.md)

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


## createTransactionSplitApiTransactionsTransactionIdSplitsPost_0

> TransactionSplitRead createTransactionSplitApiTransactionsTransactionIdSplitsPost_0(transactionId, transactionSplitCreate)

Create Transaction Split

### Example

```ts
import {
  Configuration,
  SplitsApi,
} from '@spearmint-money/sdk';
import type { CreateTransactionSplitApiTransactionsTransactionIdSplitsPost0Request } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new SplitsApi();

  const body = {
    // number
    transactionId: 56,
    // TransactionSplitCreate
    transactionSplitCreate: ...,
  } satisfies CreateTransactionSplitApiTransactionsTransactionIdSplitsPost0Request;

  try {
    const data = await api.createTransactionSplitApiTransactionsTransactionIdSplitsPost_0(body);
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
| **transactionSplitCreate** | [TransactionSplitCreate](TransactionSplitCreate.md) |  | |

### Return type

[**TransactionSplitRead**](TransactionSplitRead.md)

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


## getTransactionSplitsApiTransactionsTransactionIdSplitsGet

> Array&lt;TransactionSplitRead&gt; getTransactionSplitsApiTransactionsTransactionIdSplitsGet(transactionId)

Get Transaction Splits

### Example

```ts
import {
  Configuration,
  SplitsApi,
} from '@spearmint-money/sdk';
import type { GetTransactionSplitsApiTransactionsTransactionIdSplitsGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new SplitsApi();

  const body = {
    // number
    transactionId: 56,
  } satisfies GetTransactionSplitsApiTransactionsTransactionIdSplitsGetRequest;

  try {
    const data = await api.getTransactionSplitsApiTransactionsTransactionIdSplitsGet(body);
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

[**Array&lt;TransactionSplitRead&gt;**](TransactionSplitRead.md)

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


## getTransactionSplitsApiTransactionsTransactionIdSplitsGet_0

> Array&lt;TransactionSplitRead&gt; getTransactionSplitsApiTransactionsTransactionIdSplitsGet_0(transactionId)

Get Transaction Splits

### Example

```ts
import {
  Configuration,
  SplitsApi,
} from '@spearmint-money/sdk';
import type { GetTransactionSplitsApiTransactionsTransactionIdSplitsGet0Request } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new SplitsApi();

  const body = {
    // number
    transactionId: 56,
  } satisfies GetTransactionSplitsApiTransactionsTransactionIdSplitsGet0Request;

  try {
    const data = await api.getTransactionSplitsApiTransactionsTransactionIdSplitsGet_0(body);
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

[**Array&lt;TransactionSplitRead&gt;**](TransactionSplitRead.md)

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

