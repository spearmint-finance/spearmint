# RelationshipsApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createRelationshipApiRelationshipsPost**](RelationshipsApi.md#createrelationshipapirelationshipspost) | **POST** /api/relationships | Create Relationship |
| [**deleteRelationshipApiRelationshipsRelationshipIdDelete**](RelationshipsApi.md#deleterelationshipapirelationshipsrelationshipiddelete) | **DELETE** /api/relationships/{relationship_id} | Delete Relationship |
| [**detectAllRelationshipsApiRelationshipsDetectAllPost**](RelationshipsApi.md#detectallrelationshipsapirelationshipsdetectallpost) | **POST** /api/relationships/detect/all | Detect All Relationships |
| [**detectCreditCardPairsApiRelationshipsDetectCreditCardsPost**](RelationshipsApi.md#detectcreditcardpairsapirelationshipsdetectcreditcardspost) | **POST** /api/relationships/detect/credit-cards | Detect Credit Card Pairs |
| [**detectDividendReinvestmentPairsApiRelationshipsDetectDividendReinvestmentsPost**](RelationshipsApi.md#detectdividendreinvestmentpairsapirelationshipsdetectdividendreinvestmentspost) | **POST** /api/relationships/detect/dividend-reinvestments | Detect Dividend Reinvestment Pairs |
| [**detectReimbursementPairsApiRelationshipsDetectReimbursementsPost**](RelationshipsApi.md#detectreimbursementpairsapirelationshipsdetectreimbursementspost) | **POST** /api/relationships/detect/reimbursements | Detect Reimbursement Pairs |
| [**detectTransferPairsApiRelationshipsDetectTransfersPost**](RelationshipsApi.md#detecttransferpairsapirelationshipsdetecttransferspost) | **POST** /api/relationships/detect/transfers | Detect Transfer Pairs |
| [**getRelatedTransactionsApiTransactionsTransactionIdRelationshipsGet**](RelationshipsApi.md#getrelatedtransactionsapitransactionstransactionidrelationshipsget) | **GET** /api/transactions/{transaction_id}/relationships | Get Related Transactions |



## createRelationshipApiRelationshipsPost

> RelationshipResponse createRelationshipApiRelationshipsPost(relationshipCreateRequest)

Create Relationship

Manually create a relationship between two transactions.  Args:     request: Relationship creation request     db: Database session  Returns:     RelationshipResponse: Created relationship

### Example

```ts
import {
  Configuration,
  RelationshipsApi,
} from '@spearmint-money/sdk';
import type { CreateRelationshipApiRelationshipsPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new RelationshipsApi();

  const body = {
    // RelationshipCreateRequest
    relationshipCreateRequest: ...,
  } satisfies CreateRelationshipApiRelationshipsPostRequest;

  try {
    const data = await api.createRelationshipApiRelationshipsPost(body);
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
| **relationshipCreateRequest** | [RelationshipCreateRequest](RelationshipCreateRequest.md) |  | |

### Return type

[**RelationshipResponse**](RelationshipResponse.md)

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


## deleteRelationshipApiRelationshipsRelationshipIdDelete

> SuccessResponse deleteRelationshipApiRelationshipsRelationshipIdDelete(relationshipId)

Delete Relationship

Delete a relationship between transactions.  Args:     relationship_id: Relationship ID to delete     db: Database session  Returns:     SuccessResponse: Success confirmation

### Example

```ts
import {
  Configuration,
  RelationshipsApi,
} from '@spearmint-money/sdk';
import type { DeleteRelationshipApiRelationshipsRelationshipIdDeleteRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new RelationshipsApi();

  const body = {
    // number
    relationshipId: 56,
  } satisfies DeleteRelationshipApiRelationshipsRelationshipIdDeleteRequest;

  try {
    const data = await api.deleteRelationshipApiRelationshipsRelationshipIdDelete(body);
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
| **relationshipId** | `number` |  | [Defaults to `undefined`] |

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


## detectAllRelationshipsApiRelationshipsDetectAllPost

> DetectAllRelationshipsResponse detectAllRelationshipsApiRelationshipsDetectAllPost(autoLink, dateToleranceDays)

Detect All Relationships

Run all relationship detection algorithms.  Detects transfer pairs, credit card payments, reimbursements, and dividend reinvestments in a single operation.  Args:     auto_link: If True, automatically create relationships for high-confidence matches (&gt;&#x3D;0.8)     date_tolerance_days: Maximum days between related transactions (for transfers)     db: Database session  Returns:     DetectAllRelationshipsResponse: Summary of all detected relationships

### Example

```ts
import {
  Configuration,
  RelationshipsApi,
} from '@spearmint-money/sdk';
import type { DetectAllRelationshipsApiRelationshipsDetectAllPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new RelationshipsApi();

  const body = {
    // boolean | Automatically create relationships for high-confidence matches (optional)
    autoLink: true,
    // number | Maximum days between related transactions (optional)
    dateToleranceDays: 56,
  } satisfies DetectAllRelationshipsApiRelationshipsDetectAllPostRequest;

  try {
    const data = await api.detectAllRelationshipsApiRelationshipsDetectAllPost(body);
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
| **autoLink** | `boolean` | Automatically create relationships for high-confidence matches | [Optional] [Defaults to `false`] |
| **dateToleranceDays** | `number` | Maximum days between related transactions | [Optional] [Defaults to `3`] |

### Return type

[**DetectAllRelationshipsResponse**](DetectAllRelationshipsResponse.md)

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


## detectCreditCardPairsApiRelationshipsDetectCreditCardsPost

> CreditCardPairsResponse detectCreditCardPairsApiRelationshipsDetectCreditCardsPost(dateToleranceDays, autoLink)

Detect Credit Card Pairs

Detect credit card payment/receipt pairs.  Identifies matching pairs of credit card payments (from bank account) and receipts (to credit card company) to prevent double-counting in analysis.  Args:     date_tolerance_days: Maximum days between payment and receipt (default: 5)     auto_link: If True, automatically create relationships for high-confidence matches (&gt;&#x3D;0.8)     db: Database session      Returns:     CreditCardPairsResponse: Detected credit card pairs with confidence scores

### Example

```ts
import {
  Configuration,
  RelationshipsApi,
} from '@spearmint-money/sdk';
import type { DetectCreditCardPairsApiRelationshipsDetectCreditCardsPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new RelationshipsApi();

  const body = {
    // number | Maximum days between payment and receipt (optional)
    dateToleranceDays: 56,
    // boolean | Automatically create relationships for high-confidence matches (optional)
    autoLink: true,
  } satisfies DetectCreditCardPairsApiRelationshipsDetectCreditCardsPostRequest;

  try {
    const data = await api.detectCreditCardPairsApiRelationshipsDetectCreditCardsPost(body);
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
| **dateToleranceDays** | `number` | Maximum days between payment and receipt | [Optional] [Defaults to `5`] |
| **autoLink** | `boolean` | Automatically create relationships for high-confidence matches | [Optional] [Defaults to `false`] |

### Return type

[**CreditCardPairsResponse**](CreditCardPairsResponse.md)

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


## detectDividendReinvestmentPairsApiRelationshipsDetectDividendReinvestmentsPost

> DividendReinvestmentPairsResponse detectDividendReinvestmentPairsApiRelationshipsDetectDividendReinvestmentsPost(dateToleranceDays, amountTolerance, autoLink)

Detect Dividend Reinvestment Pairs

Detect dividend reinvestment pairs (dividend income + automatic reinvestment).  Identifies dividend income transactions that were automatically reinvested in the same security. Links the dividend (income) with the reinvestment (expense).  Args:     date_tolerance_days: Maximum days between dividend and reinvestment (default: 1)     amount_tolerance: Maximum amount difference to consider a match (default: 0.01)     auto_link: If True, automatically create relationships for high-confidence matches (&gt;&#x3D;0.8)     db: Database session  Returns:     DividendReinvestmentPairsResponse: Detected dividend reinvestment pairs with confidence scores

### Example

```ts
import {
  Configuration,
  RelationshipsApi,
} from '@spearmint-money/sdk';
import type { DetectDividendReinvestmentPairsApiRelationshipsDetectDividendReinvestmentsPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new RelationshipsApi();

  const body = {
    // number | Maximum days between dividend and reinvestment (optional)
    dateToleranceDays: 56,
    // number | Maximum amount difference (optional)
    amountTolerance: 8.14,
    // boolean | Automatically create relationships for high-confidence matches (optional)
    autoLink: true,
  } satisfies DetectDividendReinvestmentPairsApiRelationshipsDetectDividendReinvestmentsPostRequest;

  try {
    const data = await api.detectDividendReinvestmentPairsApiRelationshipsDetectDividendReinvestmentsPost(body);
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
| **dateToleranceDays** | `number` | Maximum days between dividend and reinvestment | [Optional] [Defaults to `1`] |
| **amountTolerance** | `number` | Maximum amount difference | [Optional] [Defaults to `0.01`] |
| **autoLink** | `boolean` | Automatically create relationships for high-confidence matches | [Optional] [Defaults to `false`] |

### Return type

[**DividendReinvestmentPairsResponse**](DividendReinvestmentPairsResponse.md)

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


## detectReimbursementPairsApiRelationshipsDetectReimbursementsPost

> ReimbursementPairsResponse detectReimbursementPairsApiRelationshipsDetectReimbursementsPost(dateToleranceDays, autoLink)

Detect Reimbursement Pairs

Detect reimbursement pairs (expense paid + reimbursement received).  Identifies expenses that were later reimbursed to properly track out-of-pocket costs vs. reimbursed amounts.  Args:     date_tolerance_days: Maximum days between expense and reimbursement (default: 30)     auto_link: If True, automatically create relationships for high-confidence matches (&gt;&#x3D;0.8)     db: Database session      Returns:     ReimbursementPairsResponse: Detected reimbursement pairs with confidence scores

### Example

```ts
import {
  Configuration,
  RelationshipsApi,
} from '@spearmint-money/sdk';
import type { DetectReimbursementPairsApiRelationshipsDetectReimbursementsPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new RelationshipsApi();

  const body = {
    // number | Maximum days between expense and reimbursement (optional)
    dateToleranceDays: 56,
    // boolean | Automatically create relationships for high-confidence matches (optional)
    autoLink: true,
  } satisfies DetectReimbursementPairsApiRelationshipsDetectReimbursementsPostRequest;

  try {
    const data = await api.detectReimbursementPairsApiRelationshipsDetectReimbursementsPost(body);
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
| **dateToleranceDays** | `number` | Maximum days between expense and reimbursement | [Optional] [Defaults to `30`] |
| **autoLink** | `boolean` | Automatically create relationships for high-confidence matches | [Optional] [Defaults to `false`] |

### Return type

[**ReimbursementPairsResponse**](ReimbursementPairsResponse.md)

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


## detectTransferPairsApiRelationshipsDetectTransfersPost

> TransferPairsResponse detectTransferPairsApiRelationshipsDetectTransfersPost(dateToleranceDays, amountTolerance, autoLink)

Detect Transfer Pairs

Detect potential transfer pairs (same amount, within date range).  Transfer pairs are transactions that represent money moving between accounts, such as transfers from checking to savings or between different banks.  Args:     date_tolerance_days: Maximum days between transactions (default: 3)     amount_tolerance: Maximum amount difference to consider a match (default: 0.01)     auto_link: If True, automatically create relationships for high-confidence matches (&gt;&#x3D;0.8)     db: Database session      Returns:     TransferPairsResponse: Detected transfer pairs with confidence scores

### Example

```ts
import {
  Configuration,
  RelationshipsApi,
} from '@spearmint-money/sdk';
import type { DetectTransferPairsApiRelationshipsDetectTransfersPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new RelationshipsApi();

  const body = {
    // number | Maximum days between transactions (optional)
    dateToleranceDays: 56,
    // number | Maximum amount difference (optional)
    amountTolerance: 8.14,
    // boolean | Automatically create relationships for high-confidence matches (optional)
    autoLink: true,
  } satisfies DetectTransferPairsApiRelationshipsDetectTransfersPostRequest;

  try {
    const data = await api.detectTransferPairsApiRelationshipsDetectTransfersPost(body);
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
| **dateToleranceDays** | `number` | Maximum days between transactions | [Optional] [Defaults to `3`] |
| **amountTolerance** | `number` | Maximum amount difference | [Optional] [Defaults to `0.01`] |
| **autoLink** | `boolean` | Automatically create relationships for high-confidence matches | [Optional] [Defaults to `false`] |

### Return type

[**TransferPairsResponse**](TransferPairsResponse.md)

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


## getRelatedTransactionsApiTransactionsTransactionIdRelationshipsGet

> RelatedTransactionsResponse getRelatedTransactionsApiTransactionsTransactionIdRelationshipsGet(transactionId)

Get Related Transactions

Get all transactions related to a given transaction.  Args:     transaction_id: Transaction ID     db: Database session  Returns:     RelatedTransactionsResponse: Related transactions with relationship info

### Example

```ts
import {
  Configuration,
  RelationshipsApi,
} from '@spearmint-money/sdk';
import type { GetRelatedTransactionsApiTransactionsTransactionIdRelationshipsGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new RelationshipsApi();

  const body = {
    // number
    transactionId: 56,
  } satisfies GetRelatedTransactionsApiTransactionsTransactionIdRelationshipsGetRequest;

  try {
    const data = await api.getRelatedTransactionsApiTransactionsTransactionIdRelationshipsGet(body);
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

[**RelatedTransactionsResponse**](RelatedTransactionsResponse.md)

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

