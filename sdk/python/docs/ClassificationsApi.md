# spearmint_sdk.ClassificationsApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**apply_classification_rules_api_classification_rules_apply_post**](ClassificationsApi.md#apply_classification_rules_api_classification_rules_apply_post) | **POST** /api/classification-rules/apply | Apply Classification Rules
[**auto_classify_transactions_api_transactions_auto_classify_post**](ClassificationsApi.md#auto_classify_transactions_api_transactions_auto_classify_post) | **POST** /api/transactions/auto-classify | Auto-Classify Transactions
[**bulk_classify_transactions_api_transactions_classify_bulk_post**](ClassificationsApi.md#bulk_classify_transactions_api_transactions_classify_bulk_post) | **POST** /api/transactions/classify/bulk | Bulk Classify Transactions
[**classify_transaction_api_transactions_transaction_id_classify_post**](ClassificationsApi.md#classify_transaction_api_transactions_transaction_id_classify_post) | **POST** /api/transactions/{transaction_id}/classify | Classify Transaction
[**create_classification_api_classifications_post**](ClassificationsApi.md#create_classification_api_classifications_post) | **POST** /api/classifications | Create Classification
[**create_classification_rule_api_classification_rules_post**](ClassificationsApi.md#create_classification_rule_api_classification_rules_post) | **POST** /api/classification-rules | Create Classification Rule
[**delete_classification_api_classifications_classification_id_delete**](ClassificationsApi.md#delete_classification_api_classifications_classification_id_delete) | **DELETE** /api/classifications/{classification_id} | Delete Classification
[**delete_classification_rule_api_classification_rules_rule_id_delete**](ClassificationsApi.md#delete_classification_rule_api_classification_rules_rule_id_delete) | **DELETE** /api/classification-rules/{rule_id} | Delete Classification Rule
[**get_classification_api_classifications_classification_id_get**](ClassificationsApi.md#get_classification_api_classifications_classification_id_get) | **GET** /api/classifications/{classification_id} | Get Classification Details
[**get_classification_rule_api_classification_rules_rule_id_get**](ClassificationsApi.md#get_classification_rule_api_classification_rules_rule_id_get) | **GET** /api/classification-rules/{rule_id} | Get Classification Rule
[**list_classification_rules_api_classification_rules_get**](ClassificationsApi.md#list_classification_rules_api_classification_rules_get) | **GET** /api/classification-rules | List Classification Rules
[**list_classifications_api_classifications_get**](ClassificationsApi.md#list_classifications_api_classifications_get) | **GET** /api/classifications | List All Classifications
[**test_classification_rule_api_classification_rules_test_post**](ClassificationsApi.md#test_classification_rule_api_classification_rules_test_post) | **POST** /api/classification-rules/test | Test Classification Rule
[**update_classification_api_classifications_classification_id_put**](ClassificationsApi.md#update_classification_api_classifications_classification_id_put) | **PUT** /api/classifications/{classification_id} | Update Classification
[**update_classification_rule_api_classification_rules_rule_id_put**](ClassificationsApi.md#update_classification_rule_api_classification_rules_rule_id_put) | **PUT** /api/classification-rules/{rule_id} | Update Classification Rule


# **apply_classification_rules_api_classification_rules_apply_post**
> ApplyRulesResponse apply_classification_rules_api_classification_rules_apply_post(apply_rules_request)

Apply Classification Rules

Apply classification rules to existing transactions.

    By default, this is a dry-run that previews changes without applying them.
    Set dry_run=False to actually apply the rules.

    Rules are applied in priority order (lower number = higher priority).
    Only active rules are applied unless specific rule_ids are provided.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.apply_rules_request import ApplyRulesRequest
from spearmint_sdk.models.apply_rules_response import ApplyRulesResponse
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    apply_rules_request = spearmint_sdk.ApplyRulesRequest() # ApplyRulesRequest | 

    try:
        # Apply Classification Rules
        api_response = api_instance.apply_classification_rules_api_classification_rules_apply_post(apply_rules_request)
        print("The response of ClassificationsApi->apply_classification_rules_api_classification_rules_apply_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->apply_classification_rules_api_classification_rules_apply_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **apply_rules_request** | [**ApplyRulesRequest**](ApplyRulesRequest.md)|  | 

### Return type

[**ApplyRulesResponse**](ApplyRulesResponse.md)

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

# **auto_classify_transactions_api_transactions_auto_classify_post**
> AutoClassifyResponse auto_classify_transactions_api_transactions_auto_classify_post(auto_classify_request)

Auto-Classify Transactions

Automatically classify transactions using pattern-based rules.

    This applies all active classification rules to transactions.
    Can be run on specific transactions or all unclassified transactions.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.auto_classify_request import AutoClassifyRequest
from spearmint_sdk.models.auto_classify_response import AutoClassifyResponse
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    auto_classify_request = spearmint_sdk.AutoClassifyRequest() # AutoClassifyRequest | 

    try:
        # Auto-Classify Transactions
        api_response = api_instance.auto_classify_transactions_api_transactions_auto_classify_post(auto_classify_request)
        print("The response of ClassificationsApi->auto_classify_transactions_api_transactions_auto_classify_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->auto_classify_transactions_api_transactions_auto_classify_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **auto_classify_request** | [**AutoClassifyRequest**](AutoClassifyRequest.md)|  | 

### Return type

[**AutoClassifyResponse**](AutoClassifyResponse.md)

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

# **bulk_classify_transactions_api_transactions_classify_bulk_post**
> BulkClassifyResponse bulk_classify_transactions_api_transactions_classify_bulk_post(bulk_classify_request)

Bulk Classify Transactions

Classify multiple transactions at once.
    
    Useful for applying the same classification to multiple transactions.
    Returns counts of successful and failed classifications.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.bulk_classify_request import BulkClassifyRequest
from spearmint_sdk.models.bulk_classify_response import BulkClassifyResponse
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    bulk_classify_request = spearmint_sdk.BulkClassifyRequest() # BulkClassifyRequest | 

    try:
        # Bulk Classify Transactions
        api_response = api_instance.bulk_classify_transactions_api_transactions_classify_bulk_post(bulk_classify_request)
        print("The response of ClassificationsApi->bulk_classify_transactions_api_transactions_classify_bulk_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->bulk_classify_transactions_api_transactions_classify_bulk_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bulk_classify_request** | [**BulkClassifyRequest**](BulkClassifyRequest.md)|  | 

### Return type

[**BulkClassifyResponse**](BulkClassifyResponse.md)

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

# **classify_transaction_api_transactions_transaction_id_classify_post**
> ClassificationResponse classify_transaction_api_transactions_transaction_id_classify_post(transaction_id, classify_transaction_request)

Classify Transaction

Manually classify a specific transaction.
    
    This sets the classification for a single transaction.
    The classification determines how the transaction is treated in financial calculations.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.classification_response import ClassificationResponse
from spearmint_sdk.models.classify_transaction_request import ClassifyTransactionRequest
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    transaction_id = 56 # int | Transaction ID
    classify_transaction_request = spearmint_sdk.ClassifyTransactionRequest() # ClassifyTransactionRequest | 

    try:
        # Classify Transaction
        api_response = api_instance.classify_transaction_api_transactions_transaction_id_classify_post(transaction_id, classify_transaction_request)
        print("The response of ClassificationsApi->classify_transaction_api_transactions_transaction_id_classify_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->classify_transaction_api_transactions_transaction_id_classify_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**| Transaction ID | 
 **classify_transaction_request** | [**ClassifyTransactionRequest**](ClassifyTransactionRequest.md)|  | 

### Return type

[**ClassificationResponse**](ClassificationResponse.md)

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

# **create_classification_api_classifications_post**
> ClassificationResponse create_classification_api_classifications_post(classification_create)

Create Classification

Create a new custom classification.
    
    Note: System classifications cannot be created through the API.
    Custom classifications can be used for specialized transaction handling.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.classification_create import ClassificationCreate
from spearmint_sdk.models.classification_response import ClassificationResponse
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    classification_create = spearmint_sdk.ClassificationCreate() # ClassificationCreate | 

    try:
        # Create Classification
        api_response = api_instance.create_classification_api_classifications_post(classification_create)
        print("The response of ClassificationsApi->create_classification_api_classifications_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->create_classification_api_classifications_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **classification_create** | [**ClassificationCreate**](ClassificationCreate.md)|  | 

### Return type

[**ClassificationResponse**](ClassificationResponse.md)

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

# **create_classification_rule_api_classification_rules_post**
> ClassificationRuleResponse create_classification_rule_api_classification_rules_post(classification_rule_create)

Create Classification Rule

Create a new classification rule.

    Rules use pattern matching to automatically classify transactions.
    Patterns support SQL LIKE syntax (% for wildcard).

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.classification_rule_create import ClassificationRuleCreate
from spearmint_sdk.models.classification_rule_response import ClassificationRuleResponse
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    classification_rule_create = spearmint_sdk.ClassificationRuleCreate() # ClassificationRuleCreate | 

    try:
        # Create Classification Rule
        api_response = api_instance.create_classification_rule_api_classification_rules_post(classification_rule_create)
        print("The response of ClassificationsApi->create_classification_rule_api_classification_rules_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->create_classification_rule_api_classification_rules_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **classification_rule_create** | [**ClassificationRuleCreate**](ClassificationRuleCreate.md)|  | 

### Return type

[**ClassificationRuleResponse**](ClassificationRuleResponse.md)

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

# **delete_classification_api_classifications_classification_id_delete**
> delete_classification_api_classifications_classification_id_delete(classification_id)

Delete Classification

Delete a custom classification.
    
    Note: System classifications cannot be deleted.
    Transactions using this classification will be set to 'Standard Transaction'.

### Example


```python
import spearmint_sdk
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    classification_id = 56 # int | Classification ID

    try:
        # Delete Classification
        api_instance.delete_classification_api_classifications_classification_id_delete(classification_id)
    except Exception as e:
        print("Exception when calling ClassificationsApi->delete_classification_api_classifications_classification_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **classification_id** | **int**| Classification ID | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_classification_rule_api_classification_rules_rule_id_delete**
> delete_classification_rule_api_classification_rules_rule_id_delete(rule_id)

Delete Classification Rule

Delete a classification rule.

### Example


```python
import spearmint_sdk
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    rule_id = 56 # int | Rule ID

    try:
        # Delete Classification Rule
        api_instance.delete_classification_rule_api_classification_rules_rule_id_delete(rule_id)
    except Exception as e:
        print("Exception when calling ClassificationsApi->delete_classification_rule_api_classification_rules_rule_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **rule_id** | **int**| Rule ID | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_classification_api_classifications_classification_id_get**
> ClassificationResponse get_classification_api_classifications_classification_id_get(classification_id)

Get Classification Details

Get detailed information about a specific classification by ID.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.classification_response import ClassificationResponse
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    classification_id = 56 # int | Classification ID

    try:
        # Get Classification Details
        api_response = api_instance.get_classification_api_classifications_classification_id_get(classification_id)
        print("The response of ClassificationsApi->get_classification_api_classifications_classification_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->get_classification_api_classifications_classification_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **classification_id** | **int**| Classification ID | 

### Return type

[**ClassificationResponse**](ClassificationResponse.md)

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

# **get_classification_rule_api_classification_rules_rule_id_get**
> ClassificationRuleResponse get_classification_rule_api_classification_rules_rule_id_get(rule_id)

Get Classification Rule

Get detailed information about a specific classification rule.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.classification_rule_response import ClassificationRuleResponse
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    rule_id = 56 # int | Rule ID

    try:
        # Get Classification Rule
        api_response = api_instance.get_classification_rule_api_classification_rules_rule_id_get(rule_id)
        print("The response of ClassificationsApi->get_classification_rule_api_classification_rules_rule_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->get_classification_rule_api_classification_rules_rule_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **rule_id** | **int**| Rule ID | 

### Return type

[**ClassificationRuleResponse**](ClassificationRuleResponse.md)

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

# **list_classification_rules_api_classification_rules_get**
> ClassificationRuleListResponse list_classification_rules_api_classification_rules_get(active_only=active_only)

List Classification Rules

Get a list of all classification rules.

    Rules are applied in priority order (lower number = higher priority).
    Active rules are automatically applied during auto-classification.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.classification_rule_list_response import ClassificationRuleListResponse
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    active_only = False # bool | Only return active rules (optional) (default to False)

    try:
        # List Classification Rules
        api_response = api_instance.list_classification_rules_api_classification_rules_get(active_only=active_only)
        print("The response of ClassificationsApi->list_classification_rules_api_classification_rules_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->list_classification_rules_api_classification_rules_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **active_only** | **bool**| Only return active rules | [optional] [default to False]

### Return type

[**ClassificationRuleListResponse**](ClassificationRuleListResponse.md)

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

# **list_classifications_api_classifications_get**
> ClassificationListResponse list_classifications_api_classifications_get(system_only=system_only)

List All Classifications

Get a list of all transaction classifications.
    
    Classifications determine how transactions are treated in financial calculations:
    - Standard transactions are included in all calculations
    - Transfers are excluded to prevent double-counting
    - Credit card payments/receipts are handled specially
    - Reimbursements and refunds are excluded from income
    
    System classifications cannot be deleted but can be viewed.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.classification_list_response import ClassificationListResponse
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    system_only = False # bool | Only return system classifications (optional) (default to False)

    try:
        # List All Classifications
        api_response = api_instance.list_classifications_api_classifications_get(system_only=system_only)
        print("The response of ClassificationsApi->list_classifications_api_classifications_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->list_classifications_api_classifications_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **system_only** | **bool**| Only return system classifications | [optional] [default to False]

### Return type

[**ClassificationListResponse**](ClassificationListResponse.md)

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

# **test_classification_rule_api_classification_rules_test_post**
> TestRuleResponse test_classification_rule_api_classification_rules_test_post(test_rule_request)

Test Classification Rule

Test a classification rule without applying it.

    Returns the number of transactions that would match the rule
    and a sample of matching transaction IDs.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.test_rule_request import TestRuleRequest
from spearmint_sdk.models.test_rule_response import TestRuleResponse
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    test_rule_request = spearmint_sdk.TestRuleRequest() # TestRuleRequest | 

    try:
        # Test Classification Rule
        api_response = api_instance.test_classification_rule_api_classification_rules_test_post(test_rule_request)
        print("The response of ClassificationsApi->test_classification_rule_api_classification_rules_test_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->test_classification_rule_api_classification_rules_test_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_rule_request** | [**TestRuleRequest**](TestRuleRequest.md)|  | 

### Return type

[**TestRuleResponse**](TestRuleResponse.md)

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

# **update_classification_api_classifications_classification_id_put**
> ClassificationResponse update_classification_api_classifications_classification_id_put(classification_id, classification_update)

Update Classification

Update an existing classification.
    
    Note: System classifications cannot be modified.
    Only custom classifications can be updated.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.classification_response import ClassificationResponse
from spearmint_sdk.models.classification_update import ClassificationUpdate
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    classification_id = 56 # int | Classification ID
    classification_update = spearmint_sdk.ClassificationUpdate() # ClassificationUpdate | 

    try:
        # Update Classification
        api_response = api_instance.update_classification_api_classifications_classification_id_put(classification_id, classification_update)
        print("The response of ClassificationsApi->update_classification_api_classifications_classification_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->update_classification_api_classifications_classification_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **classification_id** | **int**| Classification ID | 
 **classification_update** | [**ClassificationUpdate**](ClassificationUpdate.md)|  | 

### Return type

[**ClassificationResponse**](ClassificationResponse.md)

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

# **update_classification_rule_api_classification_rules_rule_id_put**
> ClassificationRuleResponse update_classification_rule_api_classification_rules_rule_id_put(rule_id, classification_rule_update)

Update Classification Rule

Update an existing classification rule.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.classification_rule_response import ClassificationRuleResponse
from spearmint_sdk.models.classification_rule_update import ClassificationRuleUpdate
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
    api_instance = spearmint_sdk.ClassificationsApi(api_client)
    rule_id = 56 # int | Rule ID
    classification_rule_update = spearmint_sdk.ClassificationRuleUpdate() # ClassificationRuleUpdate | 

    try:
        # Update Classification Rule
        api_response = api_instance.update_classification_rule_api_classification_rules_rule_id_put(rule_id, classification_rule_update)
        print("The response of ClassificationsApi->update_classification_rule_api_classification_rules_rule_id_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ClassificationsApi->update_classification_rule_api_classification_rules_rule_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **rule_id** | **int**| Rule ID | 
 **classification_rule_update** | [**ClassificationRuleUpdate**](ClassificationRuleUpdate.md)|  | 

### Return type

[**ClassificationRuleResponse**](ClassificationRuleResponse.md)

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

