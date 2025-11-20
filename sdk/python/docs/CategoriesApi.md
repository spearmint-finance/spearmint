# spearmint_sdk.CategoriesApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**apply_category_rules_api_category_rules_apply_post**](CategoriesApi.md#apply_category_rules_api_category_rules_apply_post) | **POST** /api/category-rules/apply | Apply Category Rules
[**create_category_api_categories_post**](CategoriesApi.md#create_category_api_categories_post) | **POST** /api/categories | Create Category
[**create_category_rule_api_category_rules_post**](CategoriesApi.md#create_category_rule_api_category_rules_post) | **POST** /api/category-rules | Create Category Rule
[**delete_category_api_categories_category_id_delete**](CategoriesApi.md#delete_category_api_categories_category_id_delete) | **DELETE** /api/categories/{category_id} | Delete Category
[**delete_category_rule_api_category_rules_rule_id_delete**](CategoriesApi.md#delete_category_rule_api_category_rules_rule_id_delete) | **DELETE** /api/category-rules/{rule_id} | Delete Category Rule
[**get_category_api_categories_category_id_get**](CategoriesApi.md#get_category_api_categories_category_id_get) | **GET** /api/categories/{category_id} | Get Category
[**get_category_rule_api_category_rules_rule_id_get**](CategoriesApi.md#get_category_rule_api_category_rules_rule_id_get) | **GET** /api/category-rules/{rule_id} | Get Category Rule
[**get_child_categories_api_categories_category_id_children_get**](CategoriesApi.md#get_child_categories_api_categories_category_id_children_get) | **GET** /api/categories/{category_id}/children | Get Child Categories
[**get_root_categories_api_categories_root_get**](CategoriesApi.md#get_root_categories_api_categories_root_get) | **GET** /api/categories/root | Get Root Categories
[**list_categories_api_categories_get**](CategoriesApi.md#list_categories_api_categories_get) | **GET** /api/categories | List Categories
[**list_category_rules_api_category_rules_get**](CategoriesApi.md#list_category_rules_api_category_rules_get) | **GET** /api/category-rules | List Category Rules
[**test_category_rule_api_category_rules_test_post**](CategoriesApi.md#test_category_rule_api_category_rules_test_post) | **POST** /api/category-rules/test | Test Category Rule
[**update_category_api_categories_category_id_put**](CategoriesApi.md#update_category_api_categories_category_id_put) | **PUT** /api/categories/{category_id} | Update Category
[**update_category_rule_api_category_rules_rule_id_put**](CategoriesApi.md#update_category_rule_api_category_rules_rule_id_put) | **PUT** /api/category-rules/{rule_id} | Update Category Rule


# **apply_category_rules_api_category_rules_apply_post**
> ApplyCategoryRulesResponse apply_category_rules_api_category_rules_apply_post(apply_category_rules_request)

Apply Category Rules

Apply category rules to transactions.

Args:
    request: Apply rules request
    db: Database session

Returns:
    ApplyCategoryRulesResponse: Application results

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.apply_category_rules_request import ApplyCategoryRulesRequest
from spearmint_sdk.models.apply_category_rules_response import ApplyCategoryRulesResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    apply_category_rules_request = spearmint_sdk.ApplyCategoryRulesRequest() # ApplyCategoryRulesRequest | 

    try:
        # Apply Category Rules
        api_response = api_instance.apply_category_rules_api_category_rules_apply_post(apply_category_rules_request)
        print("The response of CategoriesApi->apply_category_rules_api_category_rules_apply_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->apply_category_rules_api_category_rules_apply_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **apply_category_rules_request** | [**ApplyCategoryRulesRequest**](ApplyCategoryRulesRequest.md)|  | 

### Return type

[**ApplyCategoryRulesResponse**](ApplyCategoryRulesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_category_api_categories_post**
> CategoryResponse create_category_api_categories_post(category_create)

Create Category

Create a new category.

Args:
    category: Category data
    db: Database session
    
Returns:
    CategoryResponse: Created category

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.category_create import CategoryCreate
from spearmint_sdk.models.category_response import CategoryResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    category_create = spearmint_sdk.CategoryCreate() # CategoryCreate | 

    try:
        # Create Category
        api_response = api_instance.create_category_api_categories_post(category_create)
        print("The response of CategoriesApi->create_category_api_categories_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->create_category_api_categories_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **category_create** | [**CategoryCreate**](CategoryCreate.md)|  | 

### Return type

[**CategoryResponse**](CategoryResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_category_rule_api_category_rules_post**
> CategoryRuleResponse create_category_rule_api_category_rules_post(category_rule_create)

Create Category Rule

Create a new category rule.

Args:
    rule: Category rule data
    db: Database session

Returns:
    CategoryRuleResponse: Created category rule

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.category_rule_create import CategoryRuleCreate
from spearmint_sdk.models.category_rule_response import CategoryRuleResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    category_rule_create = spearmint_sdk.CategoryRuleCreate() # CategoryRuleCreate | 

    try:
        # Create Category Rule
        api_response = api_instance.create_category_rule_api_category_rules_post(category_rule_create)
        print("The response of CategoriesApi->create_category_rule_api_category_rules_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->create_category_rule_api_category_rules_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **category_rule_create** | [**CategoryRuleCreate**](CategoryRuleCreate.md)|  | 

### Return type

[**CategoryRuleResponse**](CategoryRuleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_category_api_categories_category_id_delete**
> SuccessResponse delete_category_api_categories_category_id_delete(category_id, force=force)

Delete Category

Delete category.

Args:
    category_id: Category ID
    force: Force delete
    db: Database session
    
Returns:
    SuccessResponse: Success message

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.success_response import SuccessResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    category_id = 56 # int | 
    force = False # bool | Force delete even if category has transactions or children (optional) (default to False)

    try:
        # Delete Category
        api_response = api_instance.delete_category_api_categories_category_id_delete(category_id, force=force)
        print("The response of CategoriesApi->delete_category_api_categories_category_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->delete_category_api_categories_category_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **category_id** | **int**|  | 
 **force** | **bool**| Force delete even if category has transactions or children | [optional] [default to False]

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_category_rule_api_category_rules_rule_id_delete**
> SuccessResponse delete_category_rule_api_category_rules_rule_id_delete(rule_id)

Delete Category Rule

Delete category rule.

Args:
    rule_id: Rule ID
    db: Database session

Returns:
    SuccessResponse: Success message

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.success_response import SuccessResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    rule_id = 56 # int | 

    try:
        # Delete Category Rule
        api_response = api_instance.delete_category_rule_api_category_rules_rule_id_delete(rule_id)
        print("The response of CategoriesApi->delete_category_rule_api_category_rules_rule_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->delete_category_rule_api_category_rules_rule_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **rule_id** | **int**|  | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_category_api_categories_category_id_get**
> CategoryResponse get_category_api_categories_category_id_get(category_id)

Get Category

Get category by ID.

Args:
    category_id: Category ID
    db: Database session
    
Returns:
    CategoryResponse: Category data

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.category_response import CategoryResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    category_id = 56 # int | 

    try:
        # Get Category
        api_response = api_instance.get_category_api_categories_category_id_get(category_id)
        print("The response of CategoriesApi->get_category_api_categories_category_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->get_category_api_categories_category_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **category_id** | **int**|  | 

### Return type

[**CategoryResponse**](CategoryResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_category_rule_api_category_rules_rule_id_get**
> CategoryRuleResponse get_category_rule_api_category_rules_rule_id_get(rule_id)

Get Category Rule

Get category rule by ID.

Args:
    rule_id: Rule ID
    db: Database session

Returns:
    CategoryRuleResponse: Category rule data

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.category_rule_response import CategoryRuleResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    rule_id = 56 # int | 

    try:
        # Get Category Rule
        api_response = api_instance.get_category_rule_api_category_rules_rule_id_get(rule_id)
        print("The response of CategoriesApi->get_category_rule_api_category_rules_rule_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->get_category_rule_api_category_rules_rule_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **rule_id** | **int**|  | 

### Return type

[**CategoryRuleResponse**](CategoryRuleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_child_categories_api_categories_category_id_children_get**
> CategoryListResponse get_child_categories_api_categories_category_id_children_get(category_id)

Get Child Categories

Get child categories of a parent category.

Args:
    category_id: Parent category ID
    db: Database session
    
Returns:
    CategoryListResponse: List of child categories

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.category_list_response import CategoryListResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    category_id = 56 # int | 

    try:
        # Get Child Categories
        api_response = api_instance.get_child_categories_api_categories_category_id_children_get(category_id)
        print("The response of CategoriesApi->get_child_categories_api_categories_category_id_children_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->get_child_categories_api_categories_category_id_children_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **category_id** | **int**|  | 

### Return type

[**CategoryListResponse**](CategoryListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_root_categories_api_categories_root_get**
> CategoryListResponse get_root_categories_api_categories_root_get(category_type=category_type)

Get Root Categories

Get root categories (categories without parent).

Args:
    category_type: Category type filter
    db: Database session
    
Returns:
    CategoryListResponse: List of root categories

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.category_list_response import CategoryListResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    category_type = 'category_type_example' # str | Category type filter (optional)

    try:
        # Get Root Categories
        api_response = api_instance.get_root_categories_api_categories_root_get(category_type=category_type)
        print("The response of CategoriesApi->get_root_categories_api_categories_root_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->get_root_categories_api_categories_root_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **category_type** | **str**| Category type filter | [optional] 

### Return type

[**CategoryListResponse**](CategoryListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_categories_api_categories_get**
> CategoryListResponse list_categories_api_categories_get(category_type=category_type, parent_category_id=parent_category_id, include_transfer_categories=include_transfer_categories, search_text=search_text)

List Categories

List categories with optional filters.

Args:
    category_type: Category type filter
    parent_category_id: Parent category ID filter
    include_transfer_categories: Include transfer categories
    search_text: Search text
    db: Database session
    
Returns:
    CategoryListResponse: List of categories

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.category_list_response import CategoryListResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    category_type = 'category_type_example' # str | Category type filter (optional)
    parent_category_id = 56 # int | Parent category ID filter (null for root categories) (optional)
    include_transfer_categories = True # bool | Include transfer categories (optional) (default to True)
    search_text = 'search_text_example' # str | Search in category name or description (optional)

    try:
        # List Categories
        api_response = api_instance.list_categories_api_categories_get(category_type=category_type, parent_category_id=parent_category_id, include_transfer_categories=include_transfer_categories, search_text=search_text)
        print("The response of CategoriesApi->list_categories_api_categories_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->list_categories_api_categories_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **category_type** | **str**| Category type filter | [optional] 
 **parent_category_id** | **int**| Parent category ID filter (null for root categories) | [optional] 
 **include_transfer_categories** | **bool**| Include transfer categories | [optional] [default to True]
 **search_text** | **str**| Search in category name or description | [optional] 

### Return type

[**CategoryListResponse**](CategoryListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_category_rules_api_category_rules_get**
> CategoryRuleListResponse list_category_rules_api_category_rules_get(active_only=active_only, category_id=category_id)

List Category Rules

List all category rules.

Args:
    active_only: Only return active rules
    category_id: Filter by category
    db: Database session

Returns:
    CategoryRuleListResponse: List of category rules

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.category_rule_list_response import CategoryRuleListResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    active_only = False # bool | Only return active rules (optional) (default to False)
    category_id = 56 # int | Filter by category ID (optional)

    try:
        # List Category Rules
        api_response = api_instance.list_category_rules_api_category_rules_get(active_only=active_only, category_id=category_id)
        print("The response of CategoriesApi->list_category_rules_api_category_rules_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->list_category_rules_api_category_rules_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **active_only** | **bool**| Only return active rules | [optional] [default to False]
 **category_id** | **int**| Filter by category ID | [optional] 

### Return type

[**CategoryRuleListResponse**](CategoryRuleListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_category_rule_api_category_rules_test_post**
> TestCategoryRuleResponse test_category_rule_api_category_rules_test_post(test_category_rule_request)

Test Category Rule

Test a category rule against existing transactions.

Args:
    request: Test rule request
    db: Database session

Returns:
    TestCategoryRuleResponse: Test results

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.test_category_rule_request import TestCategoryRuleRequest
from spearmint_sdk.models.test_category_rule_response import TestCategoryRuleResponse
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    test_category_rule_request = spearmint_sdk.TestCategoryRuleRequest() # TestCategoryRuleRequest | 

    try:
        # Test Category Rule
        api_response = api_instance.test_category_rule_api_category_rules_test_post(test_category_rule_request)
        print("The response of CategoriesApi->test_category_rule_api_category_rules_test_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->test_category_rule_api_category_rules_test_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_category_rule_request** | [**TestCategoryRuleRequest**](TestCategoryRuleRequest.md)|  | 

### Return type

[**TestCategoryRuleResponse**](TestCategoryRuleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_category_api_categories_category_id_put**
> CategoryResponse update_category_api_categories_category_id_put(category_id, category_update)

Update Category

Update category.

Args:
    category_id: Category ID
    category: Updated category data
    db: Database session
    
Returns:
    CategoryResponse: Updated category

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.category_response import CategoryResponse
from spearmint_sdk.models.category_update import CategoryUpdate
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    category_id = 56 # int | 
    category_update = spearmint_sdk.CategoryUpdate() # CategoryUpdate | 

    try:
        # Update Category
        api_response = api_instance.update_category_api_categories_category_id_put(category_id, category_update)
        print("The response of CategoriesApi->update_category_api_categories_category_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->update_category_api_categories_category_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **category_id** | **int**|  | 
 **category_update** | [**CategoryUpdate**](CategoryUpdate.md)|  | 

### Return type

[**CategoryResponse**](CategoryResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_category_rule_api_category_rules_rule_id_put**
> CategoryRuleResponse update_category_rule_api_category_rules_rule_id_put(rule_id, category_rule_update)

Update Category Rule

Update category rule.

Args:
    rule_id: Rule ID
    rule: Updated rule data
    db: Database session

Returns:
    CategoryRuleResponse: Updated category rule

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.category_rule_response import CategoryRuleResponse
from spearmint_sdk.models.category_rule_update import CategoryRuleUpdate
from spearmint_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = spearmint_sdk.Configuration(
    host = "http://localhost:8000"
)


# Enter a context with an instance of the API client
with spearmint_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = spearmint_sdk.CategoriesApi(api_client)
    rule_id = 56 # int | 
    category_rule_update = spearmint_sdk.CategoryRuleUpdate() # CategoryRuleUpdate | 

    try:
        # Update Category Rule
        api_response = api_instance.update_category_rule_api_category_rules_rule_id_put(rule_id, category_rule_update)
        print("The response of CategoriesApi->update_category_rule_api_category_rules_rule_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CategoriesApi->update_category_rule_api_category_rules_rule_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **rule_id** | **int**|  | 
 **category_rule_update** | [**CategoryRuleUpdate**](CategoryRuleUpdate.md)|  | 

### Return type

[**CategoryRuleResponse**](CategoryRuleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

