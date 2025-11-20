# spearmint_sdk.SplitsApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_transaction_split_api_transactions_transaction_id_splits_post**](SplitsApi.md#create_transaction_split_api_transactions_transaction_id_splits_post) | **POST** /api/transactions/{transaction_id}/splits | Create Transaction Split
[**create_transaction_split_api_transactions_transaction_id_splits_post_0**](SplitsApi.md#create_transaction_split_api_transactions_transaction_id_splits_post_0) | **POST** /api/transactions/{transaction_id}/splits | Create Transaction Split
[**get_transaction_splits_api_transactions_transaction_id_splits_get**](SplitsApi.md#get_transaction_splits_api_transactions_transaction_id_splits_get) | **GET** /api/transactions/{transaction_id}/splits | Get Transaction Splits
[**get_transaction_splits_api_transactions_transaction_id_splits_get_0**](SplitsApi.md#get_transaction_splits_api_transactions_transaction_id_splits_get_0) | **GET** /api/transactions/{transaction_id}/splits | Get Transaction Splits


# **create_transaction_split_api_transactions_transaction_id_splits_post**
> TransactionSplitRead create_transaction_split_api_transactions_transaction_id_splits_post(transaction_id, transaction_split_create)

Create Transaction Split

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.transaction_split_create import TransactionSplitCreate
from spearmint_sdk.models.transaction_split_read import TransactionSplitRead
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
    api_instance = spearmint_sdk.SplitsApi(api_client)
    transaction_id = 56 # int | 
    transaction_split_create = spearmint_sdk.TransactionSplitCreate() # TransactionSplitCreate | 

    try:
        # Create Transaction Split
        api_response = api_instance.create_transaction_split_api_transactions_transaction_id_splits_post(transaction_id, transaction_split_create)
        print("The response of SplitsApi->create_transaction_split_api_transactions_transaction_id_splits_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SplitsApi->create_transaction_split_api_transactions_transaction_id_splits_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 
 **transaction_split_create** | [**TransactionSplitCreate**](TransactionSplitCreate.md)|  | 

### Return type

[**TransactionSplitRead**](TransactionSplitRead.md)

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

# **create_transaction_split_api_transactions_transaction_id_splits_post_0**
> TransactionSplitRead create_transaction_split_api_transactions_transaction_id_splits_post_0(transaction_id, transaction_split_create)

Create Transaction Split

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.transaction_split_create import TransactionSplitCreate
from spearmint_sdk.models.transaction_split_read import TransactionSplitRead
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
    api_instance = spearmint_sdk.SplitsApi(api_client)
    transaction_id = 56 # int | 
    transaction_split_create = spearmint_sdk.TransactionSplitCreate() # TransactionSplitCreate | 

    try:
        # Create Transaction Split
        api_response = api_instance.create_transaction_split_api_transactions_transaction_id_splits_post_0(transaction_id, transaction_split_create)
        print("The response of SplitsApi->create_transaction_split_api_transactions_transaction_id_splits_post_0:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SplitsApi->create_transaction_split_api_transactions_transaction_id_splits_post_0: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 
 **transaction_split_create** | [**TransactionSplitCreate**](TransactionSplitCreate.md)|  | 

### Return type

[**TransactionSplitRead**](TransactionSplitRead.md)

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

# **get_transaction_splits_api_transactions_transaction_id_splits_get**
> List[TransactionSplitRead] get_transaction_splits_api_transactions_transaction_id_splits_get(transaction_id)

Get Transaction Splits

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.transaction_split_read import TransactionSplitRead
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
    api_instance = spearmint_sdk.SplitsApi(api_client)
    transaction_id = 56 # int | 

    try:
        # Get Transaction Splits
        api_response = api_instance.get_transaction_splits_api_transactions_transaction_id_splits_get(transaction_id)
        print("The response of SplitsApi->get_transaction_splits_api_transactions_transaction_id_splits_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SplitsApi->get_transaction_splits_api_transactions_transaction_id_splits_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 

### Return type

[**List[TransactionSplitRead]**](TransactionSplitRead.md)

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

# **get_transaction_splits_api_transactions_transaction_id_splits_get_0**
> List[TransactionSplitRead] get_transaction_splits_api_transactions_transaction_id_splits_get_0(transaction_id)

Get Transaction Splits

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.transaction_split_read import TransactionSplitRead
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
    api_instance = spearmint_sdk.SplitsApi(api_client)
    transaction_id = 56 # int | 

    try:
        # Get Transaction Splits
        api_response = api_instance.get_transaction_splits_api_transactions_transaction_id_splits_get_0(transaction_id)
        print("The response of SplitsApi->get_transaction_splits_api_transactions_transaction_id_splits_get_0:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SplitsApi->get_transaction_splits_api_transactions_transaction_id_splits_get_0: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **int**|  | 

### Return type

[**List[TransactionSplitRead]**](TransactionSplitRead.md)

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

