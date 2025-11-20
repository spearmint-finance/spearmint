# spearmint_sdk.ProjectionsApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_scenarios_api_projections_scenarios_get**](ProjectionsApi.md#get_scenarios_api_projections_scenarios_get) | **GET** /api/projections/scenarios | Get Scenario Analysis
[**project_cashflow_api_projections_cashflow_get**](ProjectionsApi.md#project_cashflow_api_projections_cashflow_get) | **GET** /api/projections/cashflow | Project Future Cash Flow
[**project_expenses_api_projections_expenses_get**](ProjectionsApi.md#project_expenses_api_projections_expenses_get) | **GET** /api/projections/expenses | Project Future Expenses
[**project_income_api_projections_income_get**](ProjectionsApi.md#project_income_api_projections_income_get) | **GET** /api/projections/income | Project Future Income
[**validate_projection_api_projections_validate_post**](ProjectionsApi.md#validate_projection_api_projections_validate_post) | **POST** /api/projections/validate | Validate Projection Accuracy


# **get_scenarios_api_projections_scenarios_get**
> CashflowProjectionResponse get_scenarios_api_projections_scenarios_get(start_date=start_date, end_date=end_date, projection_days=projection_days, method=method)

Get Scenario Analysis

Get detailed scenario analysis for cash flow projections

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.cashflow_projection_response import CashflowProjectionResponse
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
    api_instance = spearmint_sdk.ProjectionsApi(api_client)
    start_date = '2013-10-20' # date | Start of historical period (optional)
    end_date = '2013-10-20' # date | End of historical period (optional)
    projection_days = 90 # int | Number of days to project (optional) (default to 90)
    method = spearmint_sdk.ProjectionMethodEnum() # ProjectionMethodEnum | Projection method (optional)

    try:
        # Get Scenario Analysis
        api_response = api_instance.get_scenarios_api_projections_scenarios_get(start_date=start_date, end_date=end_date, projection_days=projection_days, method=method)
        print("The response of ProjectionsApi->get_scenarios_api_projections_scenarios_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectionsApi->get_scenarios_api_projections_scenarios_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start of historical period | [optional] 
 **end_date** | **date**| End of historical period | [optional] 
 **projection_days** | **int**| Number of days to project | [optional] [default to 90]
 **method** | [**ProjectionMethodEnum**](.md)| Projection method | [optional] 

### Return type

[**CashflowProjectionResponse**](CashflowProjectionResponse.md)

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

# **project_cashflow_api_projections_cashflow_get**
> CashflowProjectionResponse project_cashflow_api_projections_cashflow_get(start_date=start_date, end_date=end_date, projection_days=projection_days, method=method, confidence_level=confidence_level, include_scenarios=include_scenarios)

Project Future Cash Flow

Generate cash flow projections with scenario analysis

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.cashflow_projection_response import CashflowProjectionResponse
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
    api_instance = spearmint_sdk.ProjectionsApi(api_client)
    start_date = '2013-10-20' # date | Start of historical period (default: 1 year ago) (optional)
    end_date = '2013-10-20' # date | End of historical period (default: today) (optional)
    projection_days = 90 # int | Number of days to project forward (optional) (default to 90)
    method = spearmint_sdk.ProjectionMethodEnum() # ProjectionMethodEnum | Projection algorithm to use (optional)
    confidence_level = 0.95 # float | Confidence level for intervals (optional) (default to 0.95)
    include_scenarios = True # bool | Include best/worst case scenarios (optional) (default to True)

    try:
        # Project Future Cash Flow
        api_response = api_instance.project_cashflow_api_projections_cashflow_get(start_date=start_date, end_date=end_date, projection_days=projection_days, method=method, confidence_level=confidence_level, include_scenarios=include_scenarios)
        print("The response of ProjectionsApi->project_cashflow_api_projections_cashflow_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectionsApi->project_cashflow_api_projections_cashflow_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start of historical period (default: 1 year ago) | [optional] 
 **end_date** | **date**| End of historical period (default: today) | [optional] 
 **projection_days** | **int**| Number of days to project forward | [optional] [default to 90]
 **method** | [**ProjectionMethodEnum**](.md)| Projection algorithm to use | [optional] 
 **confidence_level** | **float**| Confidence level for intervals | [optional] [default to 0.95]
 **include_scenarios** | **bool**| Include best/worst case scenarios | [optional] [default to True]

### Return type

[**CashflowProjectionResponse**](CashflowProjectionResponse.md)

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

# **project_expenses_api_projections_expenses_get**
> ExpenseProjectionResponse project_expenses_api_projections_expenses_get(start_date=start_date, end_date=end_date, projection_days=projection_days, method=method, confidence_level=confidence_level)

Project Future Expenses

Generate expense projections based on historical data using statistical methods

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.expense_projection_response import ExpenseProjectionResponse
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
    api_instance = spearmint_sdk.ProjectionsApi(api_client)
    start_date = '2013-10-20' # date | Start of historical period (default: 1 year ago) (optional)
    end_date = '2013-10-20' # date | End of historical period (default: today) (optional)
    projection_days = 90 # int | Number of days to project forward (optional) (default to 90)
    method = spearmint_sdk.ProjectionMethodEnum() # ProjectionMethodEnum | Projection algorithm to use (optional)
    confidence_level = 0.95 # float | Confidence level for intervals (optional) (default to 0.95)

    try:
        # Project Future Expenses
        api_response = api_instance.project_expenses_api_projections_expenses_get(start_date=start_date, end_date=end_date, projection_days=projection_days, method=method, confidence_level=confidence_level)
        print("The response of ProjectionsApi->project_expenses_api_projections_expenses_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectionsApi->project_expenses_api_projections_expenses_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start of historical period (default: 1 year ago) | [optional] 
 **end_date** | **date**| End of historical period (default: today) | [optional] 
 **projection_days** | **int**| Number of days to project forward | [optional] [default to 90]
 **method** | [**ProjectionMethodEnum**](.md)| Projection algorithm to use | [optional] 
 **confidence_level** | **float**| Confidence level for intervals | [optional] [default to 0.95]

### Return type

[**ExpenseProjectionResponse**](ExpenseProjectionResponse.md)

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

# **project_income_api_projections_income_get**
> IncomeProjectionResponse project_income_api_projections_income_get(start_date=start_date, end_date=end_date, projection_days=projection_days, method=method, confidence_level=confidence_level)

Project Future Income

Generate income projections based on historical data using statistical methods

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.income_projection_response import IncomeProjectionResponse
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
    api_instance = spearmint_sdk.ProjectionsApi(api_client)
    start_date = '2013-10-20' # date | Start of historical period (default: 1 year ago) (optional)
    end_date = '2013-10-20' # date | End of historical period (default: today) (optional)
    projection_days = 90 # int | Number of days to project forward (optional) (default to 90)
    method = spearmint_sdk.ProjectionMethodEnum() # ProjectionMethodEnum | Projection algorithm to use (optional)
    confidence_level = 0.95 # float | Confidence level for intervals (optional) (default to 0.95)

    try:
        # Project Future Income
        api_response = api_instance.project_income_api_projections_income_get(start_date=start_date, end_date=end_date, projection_days=projection_days, method=method, confidence_level=confidence_level)
        print("The response of ProjectionsApi->project_income_api_projections_income_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectionsApi->project_income_api_projections_income_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **date**| Start of historical period (default: 1 year ago) | [optional] 
 **end_date** | **date**| End of historical period (default: today) | [optional] 
 **projection_days** | **int**| Number of days to project forward | [optional] [default to 90]
 **method** | [**ProjectionMethodEnum**](.md)| Projection algorithm to use | [optional] 
 **confidence_level** | **float**| Confidence level for intervals | [optional] [default to 0.95]

### Return type

[**IncomeProjectionResponse**](IncomeProjectionResponse.md)

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

# **validate_projection_api_projections_validate_post**
> AccuracyMetrics validate_projection_api_projections_validate_post(validation_request)

Validate Projection Accuracy

Calculate accuracy metrics for projection validation

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.accuracy_metrics import AccuracyMetrics
from spearmint_sdk.models.validation_request import ValidationRequest
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
    api_instance = spearmint_sdk.ProjectionsApi(api_client)
    validation_request = spearmint_sdk.ValidationRequest() # ValidationRequest | 

    try:
        # Validate Projection Accuracy
        api_response = api_instance.validate_projection_api_projections_validate_post(validation_request)
        print("The response of ProjectionsApi->validate_projection_api_projections_validate_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectionsApi->validate_projection_api_projections_validate_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **validation_request** | [**ValidationRequest**](ValidationRequest.md)|  | 

### Return type

[**AccuracyMetrics**](AccuracyMetrics.md)

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

