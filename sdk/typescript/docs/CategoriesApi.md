# CategoriesApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**applyCategoryRulesApiCategoryRulesApplyPost**](CategoriesApi.md#applycategoryrulesapicategoryrulesapplypost) | **POST** /api/category-rules/apply | Apply Category Rules |
| [**createCategoryApiCategoriesPost**](CategoriesApi.md#createcategoryapicategoriespost) | **POST** /api/categories | Create Category |
| [**createCategoryRuleApiCategoryRulesPost**](CategoriesApi.md#createcategoryruleapicategoryrulespost) | **POST** /api/category-rules | Create Category Rule |
| [**deleteCategoryApiCategoriesCategoryIdDelete**](CategoriesApi.md#deletecategoryapicategoriescategoryiddelete) | **DELETE** /api/categories/{category_id} | Delete Category |
| [**deleteCategoryRuleApiCategoryRulesRuleIdDelete**](CategoriesApi.md#deletecategoryruleapicategoryrulesruleiddelete) | **DELETE** /api/category-rules/{rule_id} | Delete Category Rule |
| [**getCategoryApiCategoriesCategoryIdGet**](CategoriesApi.md#getcategoryapicategoriescategoryidget) | **GET** /api/categories/{category_id} | Get Category |
| [**getCategoryRuleApiCategoryRulesRuleIdGet**](CategoriesApi.md#getcategoryruleapicategoryrulesruleidget) | **GET** /api/category-rules/{rule_id} | Get Category Rule |
| [**getChildCategoriesApiCategoriesCategoryIdChildrenGet**](CategoriesApi.md#getchildcategoriesapicategoriescategoryidchildrenget) | **GET** /api/categories/{category_id}/children | Get Child Categories |
| [**getRootCategoriesApiCategoriesRootGet**](CategoriesApi.md#getrootcategoriesapicategoriesrootget) | **GET** /api/categories/root | Get Root Categories |
| [**listCategoriesApiCategoriesGet**](CategoriesApi.md#listcategoriesapicategoriesget) | **GET** /api/categories | List Categories |
| [**listCategoryRulesApiCategoryRulesGet**](CategoriesApi.md#listcategoryrulesapicategoryrulesget) | **GET** /api/category-rules | List Category Rules |
| [**testCategoryRuleApiCategoryRulesTestPost**](CategoriesApi.md#testcategoryruleapicategoryrulestestpost) | **POST** /api/category-rules/test | Test Category Rule |
| [**updateCategoryApiCategoriesCategoryIdPut**](CategoriesApi.md#updatecategoryapicategoriescategoryidput) | **PUT** /api/categories/{category_id} | Update Category |
| [**updateCategoryRuleApiCategoryRulesRuleIdPut**](CategoriesApi.md#updatecategoryruleapicategoryrulesruleidput) | **PUT** /api/category-rules/{rule_id} | Update Category Rule |



## applyCategoryRulesApiCategoryRulesApplyPost

> ApplyCategoryRulesResponse applyCategoryRulesApiCategoryRulesApplyPost(applyCategoryRulesRequest)

Apply Category Rules

Apply category rules to transactions.  Args:     request: Apply rules request     db: Database session  Returns:     ApplyCategoryRulesResponse: Application results

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { ApplyCategoryRulesApiCategoryRulesApplyPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // ApplyCategoryRulesRequest
    applyCategoryRulesRequest: ...,
  } satisfies ApplyCategoryRulesApiCategoryRulesApplyPostRequest;

  try {
    const data = await api.applyCategoryRulesApiCategoryRulesApplyPost(body);
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
| **applyCategoryRulesRequest** | [ApplyCategoryRulesRequest](ApplyCategoryRulesRequest.md) |  | |

### Return type

[**ApplyCategoryRulesResponse**](ApplyCategoryRulesResponse.md)

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


## createCategoryApiCategoriesPost

> CategoryResponse createCategoryApiCategoriesPost(categoryCreate)

Create Category

Create a new category.  Args:     category: Category data     db: Database session      Returns:     CategoryResponse: Created category

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { CreateCategoryApiCategoriesPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // CategoryCreate
    categoryCreate: ...,
  } satisfies CreateCategoryApiCategoriesPostRequest;

  try {
    const data = await api.createCategoryApiCategoriesPost(body);
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
| **categoryCreate** | [CategoryCreate](CategoryCreate.md) |  | |

### Return type

[**CategoryResponse**](CategoryResponse.md)

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


## createCategoryRuleApiCategoryRulesPost

> CategoryRuleResponse createCategoryRuleApiCategoryRulesPost(categoryRuleCreate)

Create Category Rule

Create a new category rule.  Args:     rule: Category rule data     db: Database session  Returns:     CategoryRuleResponse: Created category rule

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { CreateCategoryRuleApiCategoryRulesPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // CategoryRuleCreate
    categoryRuleCreate: ...,
  } satisfies CreateCategoryRuleApiCategoryRulesPostRequest;

  try {
    const data = await api.createCategoryRuleApiCategoryRulesPost(body);
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
| **categoryRuleCreate** | [CategoryRuleCreate](CategoryRuleCreate.md) |  | |

### Return type

[**CategoryRuleResponse**](CategoryRuleResponse.md)

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


## deleteCategoryApiCategoriesCategoryIdDelete

> SuccessResponse deleteCategoryApiCategoriesCategoryIdDelete(categoryId, force)

Delete Category

Delete category.  Args:     category_id: Category ID     force: Force delete     db: Database session      Returns:     SuccessResponse: Success message

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { DeleteCategoryApiCategoriesCategoryIdDeleteRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // number
    categoryId: 56,
    // boolean | Force delete even if category has transactions or children (optional)
    force: true,
  } satisfies DeleteCategoryApiCategoriesCategoryIdDeleteRequest;

  try {
    const data = await api.deleteCategoryApiCategoriesCategoryIdDelete(body);
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
| **categoryId** | `number` |  | [Defaults to `undefined`] |
| **force** | `boolean` | Force delete even if category has transactions or children | [Optional] [Defaults to `false`] |

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


## deleteCategoryRuleApiCategoryRulesRuleIdDelete

> SuccessResponse deleteCategoryRuleApiCategoryRulesRuleIdDelete(ruleId)

Delete Category Rule

Delete category rule.  Args:     rule_id: Rule ID     db: Database session  Returns:     SuccessResponse: Success message

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { DeleteCategoryRuleApiCategoryRulesRuleIdDeleteRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // number
    ruleId: 56,
  } satisfies DeleteCategoryRuleApiCategoryRulesRuleIdDeleteRequest;

  try {
    const data = await api.deleteCategoryRuleApiCategoryRulesRuleIdDelete(body);
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
| **ruleId** | `number` |  | [Defaults to `undefined`] |

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


## getCategoryApiCategoriesCategoryIdGet

> CategoryResponse getCategoryApiCategoriesCategoryIdGet(categoryId)

Get Category

Get category by ID.  Args:     category_id: Category ID     db: Database session      Returns:     CategoryResponse: Category data

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { GetCategoryApiCategoriesCategoryIdGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // number
    categoryId: 56,
  } satisfies GetCategoryApiCategoriesCategoryIdGetRequest;

  try {
    const data = await api.getCategoryApiCategoriesCategoryIdGet(body);
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
| **categoryId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**CategoryResponse**](CategoryResponse.md)

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


## getCategoryRuleApiCategoryRulesRuleIdGet

> CategoryRuleResponse getCategoryRuleApiCategoryRulesRuleIdGet(ruleId)

Get Category Rule

Get category rule by ID.  Args:     rule_id: Rule ID     db: Database session  Returns:     CategoryRuleResponse: Category rule data

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { GetCategoryRuleApiCategoryRulesRuleIdGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // number
    ruleId: 56,
  } satisfies GetCategoryRuleApiCategoryRulesRuleIdGetRequest;

  try {
    const data = await api.getCategoryRuleApiCategoryRulesRuleIdGet(body);
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
| **ruleId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**CategoryRuleResponse**](CategoryRuleResponse.md)

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


## getChildCategoriesApiCategoriesCategoryIdChildrenGet

> CategoryListResponse getChildCategoriesApiCategoriesCategoryIdChildrenGet(categoryId)

Get Child Categories

Get child categories of a parent category.  Args:     category_id: Parent category ID     db: Database session      Returns:     CategoryListResponse: List of child categories

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { GetChildCategoriesApiCategoriesCategoryIdChildrenGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // number
    categoryId: 56,
  } satisfies GetChildCategoriesApiCategoriesCategoryIdChildrenGetRequest;

  try {
    const data = await api.getChildCategoriesApiCategoriesCategoryIdChildrenGet(body);
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
| **categoryId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**CategoryListResponse**](CategoryListResponse.md)

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


## getRootCategoriesApiCategoriesRootGet

> CategoryListResponse getRootCategoriesApiCategoriesRootGet(categoryType)

Get Root Categories

Get root categories (categories without parent).  Args:     category_type: Category type filter     db: Database session      Returns:     CategoryListResponse: List of root categories

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { GetRootCategoriesApiCategoriesRootGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // string | Category type filter (optional)
    categoryType: categoryType_example,
  } satisfies GetRootCategoriesApiCategoriesRootGetRequest;

  try {
    const data = await api.getRootCategoriesApiCategoriesRootGet(body);
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
| **categoryType** | `string` | Category type filter | [Optional] [Defaults to `undefined`] |

### Return type

[**CategoryListResponse**](CategoryListResponse.md)

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


## listCategoriesApiCategoriesGet

> CategoryListResponse listCategoriesApiCategoriesGet(categoryType, parentCategoryId, includeTransferCategories, searchText)

List Categories

List categories with optional filters.  Args:     category_type: Category type filter     parent_category_id: Parent category ID filter     include_transfer_categories: Include transfer categories     search_text: Search text     db: Database session      Returns:     CategoryListResponse: List of categories

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { ListCategoriesApiCategoriesGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // string | Category type filter (optional)
    categoryType: categoryType_example,
    // number | Parent category ID filter (null for root categories) (optional)
    parentCategoryId: 56,
    // boolean | Include transfer categories (optional)
    includeTransferCategories: true,
    // string | Search in category name or description (optional)
    searchText: searchText_example,
  } satisfies ListCategoriesApiCategoriesGetRequest;

  try {
    const data = await api.listCategoriesApiCategoriesGet(body);
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
| **categoryType** | `string` | Category type filter | [Optional] [Defaults to `undefined`] |
| **parentCategoryId** | `number` | Parent category ID filter (null for root categories) | [Optional] [Defaults to `undefined`] |
| **includeTransferCategories** | `boolean` | Include transfer categories | [Optional] [Defaults to `true`] |
| **searchText** | `string` | Search in category name or description | [Optional] [Defaults to `undefined`] |

### Return type

[**CategoryListResponse**](CategoryListResponse.md)

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


## listCategoryRulesApiCategoryRulesGet

> CategoryRuleListResponse listCategoryRulesApiCategoryRulesGet(activeOnly, categoryId)

List Category Rules

List all category rules.  Args:     active_only: Only return active rules     category_id: Filter by category     db: Database session  Returns:     CategoryRuleListResponse: List of category rules

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { ListCategoryRulesApiCategoryRulesGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // boolean | Only return active rules (optional)
    activeOnly: true,
    // number | Filter by category ID (optional)
    categoryId: 56,
  } satisfies ListCategoryRulesApiCategoryRulesGetRequest;

  try {
    const data = await api.listCategoryRulesApiCategoryRulesGet(body);
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
| **categoryId** | `number` | Filter by category ID | [Optional] [Defaults to `undefined`] |

### Return type

[**CategoryRuleListResponse**](CategoryRuleListResponse.md)

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


## testCategoryRuleApiCategoryRulesTestPost

> TestCategoryRuleResponse testCategoryRuleApiCategoryRulesTestPost(testCategoryRuleRequest)

Test Category Rule

Test a category rule against existing transactions.  Args:     request: Test rule request     db: Database session  Returns:     TestCategoryRuleResponse: Test results

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { TestCategoryRuleApiCategoryRulesTestPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // TestCategoryRuleRequest
    testCategoryRuleRequest: ...,
  } satisfies TestCategoryRuleApiCategoryRulesTestPostRequest;

  try {
    const data = await api.testCategoryRuleApiCategoryRulesTestPost(body);
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
| **testCategoryRuleRequest** | [TestCategoryRuleRequest](TestCategoryRuleRequest.md) |  | |

### Return type

[**TestCategoryRuleResponse**](TestCategoryRuleResponse.md)

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


## updateCategoryApiCategoriesCategoryIdPut

> CategoryResponse updateCategoryApiCategoriesCategoryIdPut(categoryId, categoryUpdate)

Update Category

Update category.  Args:     category_id: Category ID     category: Updated category data     db: Database session      Returns:     CategoryResponse: Updated category

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { UpdateCategoryApiCategoriesCategoryIdPutRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // number
    categoryId: 56,
    // CategoryUpdate
    categoryUpdate: ...,
  } satisfies UpdateCategoryApiCategoriesCategoryIdPutRequest;

  try {
    const data = await api.updateCategoryApiCategoriesCategoryIdPut(body);
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
| **categoryId** | `number` |  | [Defaults to `undefined`] |
| **categoryUpdate** | [CategoryUpdate](CategoryUpdate.md) |  | |

### Return type

[**CategoryResponse**](CategoryResponse.md)

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


## updateCategoryRuleApiCategoryRulesRuleIdPut

> CategoryRuleResponse updateCategoryRuleApiCategoryRulesRuleIdPut(ruleId, categoryRuleUpdate)

Update Category Rule

Update category rule.  Args:     rule_id: Rule ID     rule: Updated rule data     db: Database session  Returns:     CategoryRuleResponse: Updated category rule

### Example

```ts
import {
  Configuration,
  CategoriesApi,
} from '@spearmint-money/sdk';
import type { UpdateCategoryRuleApiCategoryRulesRuleIdPutRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new CategoriesApi();

  const body = {
    // number
    ruleId: 56,
    // CategoryRuleUpdate
    categoryRuleUpdate: ...,
  } satisfies UpdateCategoryRuleApiCategoryRulesRuleIdPutRequest;

  try {
    const data = await api.updateCategoryRuleApiCategoryRulesRuleIdPut(body);
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
| **ruleId** | `number` |  | [Defaults to `undefined`] |
| **categoryRuleUpdate** | [CategoryRuleUpdate](CategoryRuleUpdate.md) |  | |

### Return type

[**CategoryRuleResponse**](CategoryRuleResponse.md)

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

