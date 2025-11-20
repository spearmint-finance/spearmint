# ScenariosApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**previewScenarioApiScenariosPreviewPost**](ScenariosApi.md#previewscenarioapiscenariospreviewpost) | **POST** /api/scenarios/preview | Preview Scenario |
| [**previewScenarioApiScenariosPreviewPost_0**](ScenariosApi.md#previewscenarioapiscenariospreviewpost_0) | **POST** /api/scenarios/preview | Preview Scenario |



## previewScenarioApiScenariosPreviewPost

> ScenarioPreviewResponse previewScenarioApiScenariosPreviewPost(scenarioPreviewRequest)

Preview Scenario

Simulate a scenario without saving it (deterministic, fast preview).

### Example

```ts
import {
  Configuration,
  ScenariosApi,
} from '@spearmint-money/sdk';
import type { PreviewScenarioApiScenariosPreviewPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ScenariosApi();

  const body = {
    // ScenarioPreviewRequest
    scenarioPreviewRequest: ...,
  } satisfies PreviewScenarioApiScenariosPreviewPostRequest;

  try {
    const data = await api.previewScenarioApiScenariosPreviewPost(body);
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
| **scenarioPreviewRequest** | [ScenarioPreviewRequest](ScenarioPreviewRequest.md) |  | |

### Return type

[**ScenarioPreviewResponse**](ScenarioPreviewResponse.md)

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


## previewScenarioApiScenariosPreviewPost_0

> ScenarioPreviewResponse previewScenarioApiScenariosPreviewPost_0(scenarioPreviewRequest)

Preview Scenario

Simulate a scenario without saving it (deterministic, fast preview).

### Example

```ts
import {
  Configuration,
  ScenariosApi,
} from '@spearmint-money/sdk';
import type { PreviewScenarioApiScenariosPreviewPost0Request } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new ScenariosApi();

  const body = {
    // ScenarioPreviewRequest
    scenarioPreviewRequest: ...,
  } satisfies PreviewScenarioApiScenariosPreviewPost0Request;

  try {
    const data = await api.previewScenarioApiScenariosPreviewPost_0(body);
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
| **scenarioPreviewRequest** | [ScenarioPreviewRequest](ScenarioPreviewRequest.md) |  | |

### Return type

[**ScenarioPreviewResponse**](ScenarioPreviewResponse.md)

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

