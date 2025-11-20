# spearmint_sdk.PersonsApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_person_api_persons_post**](PersonsApi.md#create_person_api_persons_post) | **POST** /api/persons/ | Create Person
[**create_person_api_persons_post_0**](PersonsApi.md#create_person_api_persons_post_0) | **POST** /api/persons/ | Create Person
[**list_persons_api_persons_get**](PersonsApi.md#list_persons_api_persons_get) | **GET** /api/persons/ | List Persons
[**list_persons_api_persons_get_0**](PersonsApi.md#list_persons_api_persons_get_0) | **GET** /api/persons/ | List Persons


# **create_person_api_persons_post**
> PersonRead create_person_api_persons_post(person_create)

Create Person

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.person_create import PersonCreate
from spearmint_sdk.models.person_read import PersonRead
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
    api_instance = spearmint_sdk.PersonsApi(api_client)
    person_create = spearmint_sdk.PersonCreate() # PersonCreate | 

    try:
        # Create Person
        api_response = api_instance.create_person_api_persons_post(person_create)
        print("The response of PersonsApi->create_person_api_persons_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersonsApi->create_person_api_persons_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **person_create** | [**PersonCreate**](PersonCreate.md)|  | 

### Return type

[**PersonRead**](PersonRead.md)

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

# **create_person_api_persons_post_0**
> PersonRead create_person_api_persons_post_0(person_create)

Create Person

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.person_create import PersonCreate
from spearmint_sdk.models.person_read import PersonRead
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
    api_instance = spearmint_sdk.PersonsApi(api_client)
    person_create = spearmint_sdk.PersonCreate() # PersonCreate | 

    try:
        # Create Person
        api_response = api_instance.create_person_api_persons_post_0(person_create)
        print("The response of PersonsApi->create_person_api_persons_post_0:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersonsApi->create_person_api_persons_post_0: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **person_create** | [**PersonCreate**](PersonCreate.md)|  | 

### Return type

[**PersonRead**](PersonRead.md)

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

# **list_persons_api_persons_get**
> List[PersonRead] list_persons_api_persons_get()

List Persons

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.person_read import PersonRead
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
    api_instance = spearmint_sdk.PersonsApi(api_client)

    try:
        # List Persons
        api_response = api_instance.list_persons_api_persons_get()
        print("The response of PersonsApi->list_persons_api_persons_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersonsApi->list_persons_api_persons_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[PersonRead]**](PersonRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_persons_api_persons_get_0**
> List[PersonRead] list_persons_api_persons_get_0()

List Persons

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.person_read import PersonRead
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
    api_instance = spearmint_sdk.PersonsApi(api_client)

    try:
        # List Persons
        api_response = api_instance.list_persons_api_persons_get_0()
        print("The response of PersonsApi->list_persons_api_persons_get_0:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersonsApi->list_persons_api_persons_get_0: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[PersonRead]**](PersonRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

