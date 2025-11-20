# spearmint_sdk.ImportApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_import_detail_api_import_history_import_id_get**](ImportApi.md#get_import_detail_api_import_history_import_id_get) | **GET** /api/import/history/{import_id} | Get Import Detail
[**get_import_history_api_import_history_get**](ImportApi.md#get_import_history_api_import_history_get) | **GET** /api/import/history | Get Import History
[**get_import_status_api_import_status_import_id_get**](ImportApi.md#get_import_status_api_import_status_import_id_get) | **GET** /api/import/status/{import_id} | Get Import Status
[**import_from_file_path_api_import_file_path_post**](ImportApi.md#import_from_file_path_api_import_file_path_post) | **POST** /api/import/file-path | Import From File Path
[**import_transactions_api_import_post**](ImportApi.md#import_transactions_api_import_post) | **POST** /api/import | Import Transactions


# **get_import_detail_api_import_history_import_id_get**
> ImportHistoryDetailResponse get_import_detail_api_import_history_import_id_get(import_id)

Get Import Detail

Get detailed information about a specific import.

Returns detailed information including error logs and full statistics.

Args:
    import_id: Import ID
    db: Database session

Returns:
    ImportHistoryDetailResponse: Detailed import information

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.import_history_detail_response import ImportHistoryDetailResponse
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
    api_instance = spearmint_sdk.ImportApi(api_client)
    import_id = 56 # int | 

    try:
        # Get Import Detail
        api_response = api_instance.get_import_detail_api_import_history_import_id_get(import_id)
        print("The response of ImportApi->get_import_detail_api_import_history_import_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ImportApi->get_import_detail_api_import_history_import_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **import_id** | **int**|  | 

### Return type

[**ImportHistoryDetailResponse**](ImportHistoryDetailResponse.md)

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

# **get_import_history_api_import_history_get**
> ImportHistoryResponse get_import_history_api_import_history_get(limit=limit, offset=offset)

Get Import History

Get import history.

Returns a list of past imports with statistics including:
- Import date and file name
- Total rows, successful rows, failed rows
- Classification statistics
- Success rate

Args:
    limit: Maximum number of imports to return
    offset: Number of imports to skip (for pagination)
    db: Database session

Returns:
    ImportHistoryResponse: List of import history items

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.import_history_response import ImportHistoryResponse
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
    api_instance = spearmint_sdk.ImportApi(api_client)
    limit = 50 # int | Maximum number of imports to return (optional) (default to 50)
    offset = 0 # int | Number of imports to skip (optional) (default to 0)

    try:
        # Get Import History
        api_response = api_instance.get_import_history_api_import_history_get(limit=limit, offset=offset)
        print("The response of ImportApi->get_import_history_api_import_history_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ImportApi->get_import_history_api_import_history_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| Maximum number of imports to return | [optional] [default to 50]
 **offset** | **int**| Number of imports to skip | [optional] [default to 0]

### Return type

[**ImportHistoryResponse**](ImportHistoryResponse.md)

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

# **get_import_status_api_import_status_import_id_get**
> ImportStatusResponse get_import_status_api_import_status_import_id_get(import_id)

Get Import Status

Get real-time import status.

This endpoint provides progress tracking for ongoing imports.
For completed imports, it returns the final status.

Args:
    import_id: Import ID
    db: Database session

Returns:
    ImportStatusResponse: Import status and progress

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.import_status_response import ImportStatusResponse
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
    api_instance = spearmint_sdk.ImportApi(api_client)
    import_id = 56 # int | 

    try:
        # Get Import Status
        api_response = api_instance.get_import_status_api_import_status_import_id_get(import_id)
        print("The response of ImportApi->get_import_status_api_import_status_import_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ImportApi->get_import_status_api_import_status_import_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **import_id** | **int**|  | 

### Return type

[**ImportStatusResponse**](ImportStatusResponse.md)

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

# **import_from_file_path_api_import_file_path_post**
> ImportResponse import_from_file_path_api_import_file_path_post(file_path, import_request)

Import From File Path

Import transactions from file path (for local development).

Args:
    file_path: Path to Excel file
    request: Import request parameters
    db: Database session
    
Returns:
    ImportResponse: Import result

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.import_request import ImportRequest
from spearmint_sdk.models.import_response import ImportResponse
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
    api_instance = spearmint_sdk.ImportApi(api_client)
    file_path = 'file_path_example' # str | 
    import_request = spearmint_sdk.ImportRequest() # ImportRequest | 

    try:
        # Import From File Path
        api_response = api_instance.import_from_file_path_api_import_file_path_post(file_path, import_request)
        print("The response of ImportApi->import_from_file_path_api_import_file_path_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ImportApi->import_from_file_path_api_import_file_path_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_path** | **str**|  | 
 **import_request** | [**ImportRequest**](ImportRequest.md)|  | 

### Return type

[**ImportResponse**](ImportResponse.md)

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

# **import_transactions_api_import_post**
> ImportResponse import_transactions_api_import_post(file, mode=mode, skip_duplicates=skip_duplicates)

Import Transactions

Import transactions from Excel file.

Args:
    file: Uploaded Excel file
    mode: Import mode (full, incremental, update)
    skip_duplicates: Whether to skip duplicates
    db: Database session
    
Returns:
    ImportResponse: Import result

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.import_response import ImportResponse
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
    api_instance = spearmint_sdk.ImportApi(api_client)
    file = None # bytearray | Excel file to import
    mode = 'incremental' # str | Import mode (optional) (default to 'incremental')
    skip_duplicates = True # bool | Skip duplicate transactions (optional) (default to True)

    try:
        # Import Transactions
        api_response = api_instance.import_transactions_api_import_post(file, mode=mode, skip_duplicates=skip_duplicates)
        print("The response of ImportApi->import_transactions_api_import_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ImportApi->import_transactions_api_import_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **bytearray**| Excel file to import | 
 **mode** | **str**| Import mode | [optional] [default to &#39;incremental&#39;]
 **skip_duplicates** | **bool**| Skip duplicate transactions | [optional] [default to True]

### Return type

[**ImportResponse**](ImportResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

