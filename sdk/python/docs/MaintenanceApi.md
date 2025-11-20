# spearmint_sdk.MaintenanceApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**fix_classifications_api_maintenance_fix_classifications_post**](MaintenanceApi.md#fix_classifications_api_maintenance_fix_classifications_post) | **POST** /api/maintenance/fix/classifications | Fix System Classifications
[**fix_reimbursements_api_maintenance_fix_reimbursements_post**](MaintenanceApi.md#fix_reimbursements_api_maintenance_fix_reimbursements_post) | **POST** /api/maintenance/fix/reimbursements | Fix Reimbursement Links
[**fix_transfers_api_maintenance_fix_transfers_post**](MaintenanceApi.md#fix_transfers_api_maintenance_fix_transfers_post) | **POST** /api/maintenance/fix/transfers | Fix Transfer Links


# **fix_classifications_api_maintenance_fix_classifications_post**
> FixResult fix_classifications_api_maintenance_fix_classifications_post()

Fix System Classifications

Repair incorrect system classifications.
    - Fixes 'Insurance Reimbursement' cash flow settings
    - Removes duplicate/legacy classifications ('STANDARD', 'REIMB_RECEIVED')

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.fix_result import FixResult
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
    api_instance = spearmint_sdk.MaintenanceApi(api_client)

    try:
        # Fix System Classifications
        api_response = api_instance.fix_classifications_api_maintenance_fix_classifications_post()
        print("The response of MaintenanceApi->fix_classifications_api_maintenance_fix_classifications_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintenanceApi->fix_classifications_api_maintenance_fix_classifications_post: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**FixResult**](FixResult.md)

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

# **fix_reimbursements_api_maintenance_fix_reimbursements_post**
> FixResult fix_reimbursements_api_maintenance_fix_reimbursements_post()

Fix Reimbursement Links

Links reimbursement expenses to income.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.fix_result import FixResult
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
    api_instance = spearmint_sdk.MaintenanceApi(api_client)

    try:
        # Fix Reimbursement Links
        api_response = api_instance.fix_reimbursements_api_maintenance_fix_reimbursements_post()
        print("The response of MaintenanceApi->fix_reimbursements_api_maintenance_fix_reimbursements_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintenanceApi->fix_reimbursements_api_maintenance_fix_reimbursements_post: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**FixResult**](FixResult.md)

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

# **fix_transfers_api_maintenance_fix_transfers_post**
> FixResult fix_transfers_api_maintenance_fix_transfers_post()

Fix Transfer Links

Attempts to link orphaned transfers based on amount and date proximity.

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.fix_result import FixResult
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
    api_instance = spearmint_sdk.MaintenanceApi(api_client)

    try:
        # Fix Transfer Links
        api_response = api_instance.fix_transfers_api_maintenance_fix_transfers_post()
        print("The response of MaintenanceApi->fix_transfers_api_maintenance_fix_transfers_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintenanceApi->fix_transfers_api_maintenance_fix_transfers_post: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**FixResult**](FixResult.md)

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

