# spearmint_sdk.ScenariosApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**preview_scenario_api_scenarios_preview_post**](ScenariosApi.md#preview_scenario_api_scenarios_preview_post) | **POST** /api/scenarios/preview | Preview Scenario
[**preview_scenario_api_scenarios_preview_post_0**](ScenariosApi.md#preview_scenario_api_scenarios_preview_post_0) | **POST** /api/scenarios/preview | Preview Scenario


# **preview_scenario_api_scenarios_preview_post**
> ScenarioPreviewResponse preview_scenario_api_scenarios_preview_post(scenario_preview_request)

Preview Scenario

Simulate a scenario without saving it (deterministic, fast preview).

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.scenario_preview_request import ScenarioPreviewRequest
from spearmint_sdk.models.scenario_preview_response import ScenarioPreviewResponse
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
    api_instance = spearmint_sdk.ScenariosApi(api_client)
    scenario_preview_request = spearmint_sdk.ScenarioPreviewRequest() # ScenarioPreviewRequest | 

    try:
        # Preview Scenario
        api_response = api_instance.preview_scenario_api_scenarios_preview_post(scenario_preview_request)
        print("The response of ScenariosApi->preview_scenario_api_scenarios_preview_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScenariosApi->preview_scenario_api_scenarios_preview_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scenario_preview_request** | [**ScenarioPreviewRequest**](ScenarioPreviewRequest.md)|  | 

### Return type

[**ScenarioPreviewResponse**](ScenarioPreviewResponse.md)

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

# **preview_scenario_api_scenarios_preview_post_0**
> ScenarioPreviewResponse preview_scenario_api_scenarios_preview_post_0(scenario_preview_request)

Preview Scenario

Simulate a scenario without saving it (deterministic, fast preview).

### Example


```python
import spearmint_sdk
from spearmint_sdk.models.scenario_preview_request import ScenarioPreviewRequest
from spearmint_sdk.models.scenario_preview_response import ScenarioPreviewResponse
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
    api_instance = spearmint_sdk.ScenariosApi(api_client)
    scenario_preview_request = spearmint_sdk.ScenarioPreviewRequest() # ScenarioPreviewRequest | 

    try:
        # Preview Scenario
        api_response = api_instance.preview_scenario_api_scenarios_preview_post_0(scenario_preview_request)
        print("The response of ScenariosApi->preview_scenario_api_scenarios_preview_post_0:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScenariosApi->preview_scenario_api_scenarios_preview_post_0: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scenario_preview_request** | [**ScenarioPreviewRequest**](ScenarioPreviewRequest.md)|  | 

### Return type

[**ScenarioPreviewResponse**](ScenarioPreviewResponse.md)

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

