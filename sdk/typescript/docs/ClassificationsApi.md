# ClassificationsApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**applyClassificationRulesApiClassificationRulesApplyPost**](ClassificationsApi.md#applyclassificationrulesapiclassificationrulesapplypost) | **POST** /api/classification-rules/apply | Apply Classification Rules |
| [**autoClassifyTransactionsApiTransactionsAutoClassifyPost**](ClassificationsApi.md#autoclassifytransactionsapitransactionsautoclassifypost) | **POST** /api/transactions/auto-classify | Auto-Classify Transactions |
| [**bulkClassifyTransactionsApiTransactionsClassifyBulkPost**](ClassificationsApi.md#bulkclassifytransactionsapitransactionsclassifybulkpost) | **POST** /api/transactions/classify/bulk | Bulk Classify Transactions |
| [**classifyTransactionApiTransactionsTransactionIdClassifyPost**](ClassificationsApi.md#classifytransactionapitransactionstransactionidclassifypost) | **POST** /api/transactions/{transaction_id}/classify | Classify Transaction |
| [**createClassificationApiClassificationsPost**](ClassificationsApi.md#createclassificationapiclassificationspost) | **POST** /api/classifications | Create Classification |
| [**createClassificationRuleApiClassificationRulesPost**](ClassificationsApi.md#createclassificationruleapiclassificationrulespost) | **POST** /api/classification-rules | Create Classification Rule |
| [**deleteClassificationApiClassificationsClassificationIdDelete**](ClassificationsApi.md#deleteclassificationapiclassificationsclassificationiddelete) | **DELETE** /api/classifications/{classification_id} | Delete Classification |
| [**deleteClassificationRuleApiClassificationRulesRuleIdDelete**](ClassificationsApi.md#deleteclassificationruleapiclassificationrulesruleiddelete) | **DELETE** /api/classification-rules/{rule_id} | Delete Classification Rule |
| [**getClassificationApiClassificationsClassificationIdGet**](ClassificationsApi.md#getclassificationapiclassificationsclassificationidget) | **GET** /api/classifications/{classification_id} | Get Classification Details |
| [**getClassificationRuleApiClassificationRulesRuleIdGet**](ClassificationsApi.md#getclassificationruleapiclassificationrulesruleidget) | **GET** /api/classification-rules/{rule_id} | Get Classification Rule |
| [**listClassificationRulesApiClassificationRulesGet**](ClassificationsApi.md#listclassificationrulesapiclassificationrulesget) | **GET** /api/classification-rules | List Classification Rules |
| [**listClassificationsApiClassificationsGet**](ClassificationsApi.md#listclassificationsapiclassificationsget) | **GET** /api/classifications | List All Classifications |
| [**testClassificationRuleApiClassificationRulesTestPost**](ClassificationsApi.md#testclassificationruleapiclassificationrulestestpost) | **POST** /api/classification-rules/test | Test Classification Rule |
| [**updateClassificationApiClassificationsClassificationIdPut**](ClassificationsApi.md#updateclassificationapiclassificationsclassificationidput) | **PUT** /api/classifications/{classification_id} | Update Classification |
| [**updateClassificationRuleApiClassificationRulesRuleIdPut**](ClassificationsApi.md#updateclassificationruleapiclassificationrulesruleidput) | **PUT** /api/classification-rules/{rule_id} | Update Classification Rule |



## applyClassificationRulesApiClassificationRulesApplyPost

> ApplyRulesResponse applyClassificationRulesApiClassificationRulesApplyPost(applyRulesRequest)

Apply Classification Rules

Apply classification rules to existing transactions.      By default, this is a dry-run that previews changes without applying them.     Set dry_run&#x3D;False to actually apply the rules.      Rules are applied in priority order (lower number &#x3D; higher priority).     Only active rules are applied unless specific rule_ids are provided.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { ApplyClassificationRulesApiClassificationRulesApplyPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // ApplyRulesRequest
    applyRulesRequest: ...,
  } satisfies ApplyClassificationRulesApiClassificationRulesApplyPostRequest;

  try {
    const data = await api.applyClassificationRulesApiClassificationRulesApplyPost(body);
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
| **applyRulesRequest** | [ApplyRulesRequest](ApplyRulesRequest.md) |  | |

### Return type

[**ApplyRulesResponse**](ApplyRulesResponse.md)

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


## autoClassifyTransactionsApiTransactionsAutoClassifyPost

> AutoClassifyResponse autoClassifyTransactionsApiTransactionsAutoClassifyPost(autoClassifyRequest)

Auto-Classify Transactions

Automatically classify transactions using pattern-based rules.      This applies all active classification rules to transactions.     Can be run on specific transactions or all unclassified transactions.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { AutoClassifyTransactionsApiTransactionsAutoClassifyPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // AutoClassifyRequest
    autoClassifyRequest: ...,
  } satisfies AutoClassifyTransactionsApiTransactionsAutoClassifyPostRequest;

  try {
    const data = await api.autoClassifyTransactionsApiTransactionsAutoClassifyPost(body);
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
| **autoClassifyRequest** | [AutoClassifyRequest](AutoClassifyRequest.md) |  | |

### Return type

[**AutoClassifyResponse**](AutoClassifyResponse.md)

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


## bulkClassifyTransactionsApiTransactionsClassifyBulkPost

> BulkClassifyResponse bulkClassifyTransactionsApiTransactionsClassifyBulkPost(bulkClassifyRequest)

Bulk Classify Transactions

Classify multiple transactions at once.          Useful for applying the same classification to multiple transactions.     Returns counts of successful and failed classifications.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { BulkClassifyTransactionsApiTransactionsClassifyBulkPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // BulkClassifyRequest
    bulkClassifyRequest: ...,
  } satisfies BulkClassifyTransactionsApiTransactionsClassifyBulkPostRequest;

  try {
    const data = await api.bulkClassifyTransactionsApiTransactionsClassifyBulkPost(body);
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
| **bulkClassifyRequest** | [BulkClassifyRequest](BulkClassifyRequest.md) |  | |

### Return type

[**BulkClassifyResponse**](BulkClassifyResponse.md)

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


## classifyTransactionApiTransactionsTransactionIdClassifyPost

> ClassificationResponse classifyTransactionApiTransactionsTransactionIdClassifyPost(transactionId, classifyTransactionRequest)

Classify Transaction

Manually classify a specific transaction.          This sets the classification for a single transaction.     The classification determines how the transaction is treated in financial calculations.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { ClassifyTransactionApiTransactionsTransactionIdClassifyPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // number | Transaction ID
    transactionId: 56,
    // ClassifyTransactionRequest
    classifyTransactionRequest: ...,
  } satisfies ClassifyTransactionApiTransactionsTransactionIdClassifyPostRequest;

  try {
    const data = await api.classifyTransactionApiTransactionsTransactionIdClassifyPost(body);
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
| **transactionId** | `number` | Transaction ID | [Defaults to `undefined`] |
| **classifyTransactionRequest** | [ClassifyTransactionRequest](ClassifyTransactionRequest.md) |  | |

### Return type

[**ClassificationResponse**](ClassificationResponse.md)

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


## createClassificationApiClassificationsPost

> ClassificationResponse createClassificationApiClassificationsPost(classificationCreate)

Create Classification

Create a new custom classification.          Note: System classifications cannot be created through the API.     Custom classifications can be used for specialized transaction handling.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { CreateClassificationApiClassificationsPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // ClassificationCreate
    classificationCreate: ...,
  } satisfies CreateClassificationApiClassificationsPostRequest;

  try {
    const data = await api.createClassificationApiClassificationsPost(body);
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
| **classificationCreate** | [ClassificationCreate](ClassificationCreate.md) |  | |

### Return type

[**ClassificationResponse**](ClassificationResponse.md)

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


## createClassificationRuleApiClassificationRulesPost

> ClassificationRuleResponse createClassificationRuleApiClassificationRulesPost(classificationRuleCreate)

Create Classification Rule

Create a new classification rule.      Rules use pattern matching to automatically classify transactions.     Patterns support SQL LIKE syntax (% for wildcard).

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { CreateClassificationRuleApiClassificationRulesPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // ClassificationRuleCreate
    classificationRuleCreate: ...,
  } satisfies CreateClassificationRuleApiClassificationRulesPostRequest;

  try {
    const data = await api.createClassificationRuleApiClassificationRulesPost(body);
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
| **classificationRuleCreate** | [ClassificationRuleCreate](ClassificationRuleCreate.md) |  | |

### Return type

[**ClassificationRuleResponse**](ClassificationRuleResponse.md)

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


## deleteClassificationApiClassificationsClassificationIdDelete

> deleteClassificationApiClassificationsClassificationIdDelete(classificationId)

Delete Classification

Delete a custom classification.          Note: System classifications cannot be deleted.     Transactions using this classification will be set to \&#39;Standard Transaction\&#39;.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { DeleteClassificationApiClassificationsClassificationIdDeleteRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // number | Classification ID
    classificationId: 56,
  } satisfies DeleteClassificationApiClassificationsClassificationIdDeleteRequest;

  try {
    const data = await api.deleteClassificationApiClassificationsClassificationIdDelete(body);
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
| **classificationId** | `number` | Classification ID | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **204** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## deleteClassificationRuleApiClassificationRulesRuleIdDelete

> deleteClassificationRuleApiClassificationRulesRuleIdDelete(ruleId)

Delete Classification Rule

Delete a classification rule.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { DeleteClassificationRuleApiClassificationRulesRuleIdDeleteRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // number | Rule ID
    ruleId: 56,
  } satisfies DeleteClassificationRuleApiClassificationRulesRuleIdDeleteRequest;

  try {
    const data = await api.deleteClassificationRuleApiClassificationRulesRuleIdDelete(body);
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
| **ruleId** | `number` | Rule ID | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **204** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getClassificationApiClassificationsClassificationIdGet

> ClassificationResponse getClassificationApiClassificationsClassificationIdGet(classificationId)

Get Classification Details

Get detailed information about a specific classification by ID.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { GetClassificationApiClassificationsClassificationIdGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // number | Classification ID
    classificationId: 56,
  } satisfies GetClassificationApiClassificationsClassificationIdGetRequest;

  try {
    const data = await api.getClassificationApiClassificationsClassificationIdGet(body);
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
| **classificationId** | `number` | Classification ID | [Defaults to `undefined`] |

### Return type

[**ClassificationResponse**](ClassificationResponse.md)

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


## getClassificationRuleApiClassificationRulesRuleIdGet

> ClassificationRuleResponse getClassificationRuleApiClassificationRulesRuleIdGet(ruleId)

Get Classification Rule

Get detailed information about a specific classification rule.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { GetClassificationRuleApiClassificationRulesRuleIdGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // number | Rule ID
    ruleId: 56,
  } satisfies GetClassificationRuleApiClassificationRulesRuleIdGetRequest;

  try {
    const data = await api.getClassificationRuleApiClassificationRulesRuleIdGet(body);
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
| **ruleId** | `number` | Rule ID | [Defaults to `undefined`] |

### Return type

[**ClassificationRuleResponse**](ClassificationRuleResponse.md)

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


## listClassificationRulesApiClassificationRulesGet

> ClassificationRuleListResponse listClassificationRulesApiClassificationRulesGet(activeOnly)

List Classification Rules

Get a list of all classification rules.      Rules are applied in priority order (lower number &#x3D; higher priority).     Active rules are automatically applied during auto-classification.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { ListClassificationRulesApiClassificationRulesGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // boolean | Only return active rules (optional)
    activeOnly: true,
  } satisfies ListClassificationRulesApiClassificationRulesGetRequest;

  try {
    const data = await api.listClassificationRulesApiClassificationRulesGet(body);
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
| **activeOnly** | `boolean` | Only return active rules | [Optional] [Defaults to `false`] |

### Return type

[**ClassificationRuleListResponse**](ClassificationRuleListResponse.md)

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


## listClassificationsApiClassificationsGet

> ClassificationListResponse listClassificationsApiClassificationsGet(systemOnly)

List All Classifications

Get a list of all transaction classifications.          Classifications determine how transactions are treated in financial calculations:     - Standard transactions are included in all calculations     - Transfers are excluded to prevent double-counting     - Credit card payments/receipts are handled specially     - Reimbursements and refunds are excluded from income          System classifications cannot be deleted but can be viewed.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { ListClassificationsApiClassificationsGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // boolean | Only return system classifications (optional)
    systemOnly: true,
  } satisfies ListClassificationsApiClassificationsGetRequest;

  try {
    const data = await api.listClassificationsApiClassificationsGet(body);
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
| **systemOnly** | `boolean` | Only return system classifications | [Optional] [Defaults to `false`] |

### Return type

[**ClassificationListResponse**](ClassificationListResponse.md)

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


## testClassificationRuleApiClassificationRulesTestPost

> TestRuleResponse testClassificationRuleApiClassificationRulesTestPost(testRuleRequest)

Test Classification Rule

Test a classification rule without applying it.      Returns the number of transactions that would match the rule     and a sample of matching transaction IDs.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { TestClassificationRuleApiClassificationRulesTestPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // TestRuleRequest
    testRuleRequest: ...,
  } satisfies TestClassificationRuleApiClassificationRulesTestPostRequest;

  try {
    const data = await api.testClassificationRuleApiClassificationRulesTestPost(body);
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
| **testRuleRequest** | [TestRuleRequest](TestRuleRequest.md) |  | |

### Return type

[**TestRuleResponse**](TestRuleResponse.md)

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


## updateClassificationApiClassificationsClassificationIdPut

> ClassificationResponse updateClassificationApiClassificationsClassificationIdPut(classificationId, classificationUpdate)

Update Classification

Update an existing classification.          Note: System classifications cannot be modified.     Only custom classifications can be updated.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { UpdateClassificationApiClassificationsClassificationIdPutRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // number | Classification ID
    classificationId: 56,
    // ClassificationUpdate
    classificationUpdate: ...,
  } satisfies UpdateClassificationApiClassificationsClassificationIdPutRequest;

  try {
    const data = await api.updateClassificationApiClassificationsClassificationIdPut(body);
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
| **classificationId** | `number` | Classification ID | [Defaults to `undefined`] |
| **classificationUpdate** | [ClassificationUpdate](ClassificationUpdate.md) |  | |

### Return type

[**ClassificationResponse**](ClassificationResponse.md)

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


## updateClassificationRuleApiClassificationRulesRuleIdPut

> ClassificationRuleResponse updateClassificationRuleApiClassificationRulesRuleIdPut(ruleId, classificationRuleUpdate)

Update Classification Rule

Update an existing classification rule.

### Example

```ts
import {
  Configuration,
  ClassificationsApi,
} from '@spearmint-money/sdk';
import type { UpdateClassificationRuleApiClassificationRulesRuleIdPutRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ClassificationsApi();

  const body = {
    // number | Rule ID
    ruleId: 56,
    // ClassificationRuleUpdate
    classificationRuleUpdate: ...,
  } satisfies UpdateClassificationRuleApiClassificationRulesRuleIdPutRequest;

  try {
    const data = await api.updateClassificationRuleApiClassificationRulesRuleIdPut(body);
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
| **ruleId** | `number` | Rule ID | [Defaults to `undefined`] |
| **classificationRuleUpdate** | [ClassificationRuleUpdate](ClassificationRuleUpdate.md) |  | |

### Return type

[**ClassificationRuleResponse**](ClassificationRuleResponse.md)

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

