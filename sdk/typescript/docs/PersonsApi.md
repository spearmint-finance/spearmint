# PersonsApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createPersonApiPersonsPost**](PersonsApi.md#createpersonapipersonspost) | **POST** /api/persons/ | Create Person |
| [**createPersonApiPersonsPost_0**](PersonsApi.md#createpersonapipersonspost_0) | **POST** /api/persons/ | Create Person |
| [**listPersonsApiPersonsGet**](PersonsApi.md#listpersonsapipersonsget) | **GET** /api/persons/ | List Persons |
| [**listPersonsApiPersonsGet_0**](PersonsApi.md#listpersonsapipersonsget_0) | **GET** /api/persons/ | List Persons |



## createPersonApiPersonsPost

> PersonRead createPersonApiPersonsPost(personCreate)

Create Person

### Example

```ts
import {
  Configuration,
  PersonsApi,
} from '@spearmint-money/sdk';
import type { CreatePersonApiPersonsPostRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new PersonsApi();

  const body = {
    // PersonCreate
    personCreate: ...,
  } satisfies CreatePersonApiPersonsPostRequest;

  try {
    const data = await api.createPersonApiPersonsPost(body);
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
| **personCreate** | [PersonCreate](PersonCreate.md) |  | |

### Return type

[**PersonRead**](PersonRead.md)

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


## createPersonApiPersonsPost_0

> PersonRead createPersonApiPersonsPost_0(personCreate)

Create Person

### Example

```ts
import {
  Configuration,
  PersonsApi,
} from '@spearmint-money/sdk';
import type { CreatePersonApiPersonsPost0Request } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new PersonsApi();

  const body = {
    // PersonCreate
    personCreate: ...,
  } satisfies CreatePersonApiPersonsPost0Request;

  try {
    const data = await api.createPersonApiPersonsPost_0(body);
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
| **personCreate** | [PersonCreate](PersonCreate.md) |  | |

### Return type

[**PersonRead**](PersonRead.md)

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


## listPersonsApiPersonsGet

> Array&lt;PersonRead&gt; listPersonsApiPersonsGet()

List Persons

### Example

```ts
import {
  Configuration,
  PersonsApi,
} from '@spearmint-money/sdk';
import type { ListPersonsApiPersonsGetRequest } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new PersonsApi();

  try {
    const data = await api.listPersonsApiPersonsGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**Array&lt;PersonRead&gt;**](PersonRead.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## listPersonsApiPersonsGet_0

> Array&lt;PersonRead&gt; listPersonsApiPersonsGet_0()

List Persons

### Example

```ts
import {
  Configuration,
  PersonsApi,
} from '@spearmint-money/sdk';
import type { ListPersonsApiPersonsGet0Request } from '@spearmint-money/sdk';

async function example() {
  console.log("🚀 Testing @spearmint-money/sdk SDK...");
  const api = new PersonsApi();

  try {
    const data = await api.listPersonsApiPersonsGet_0();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**Array&lt;PersonRead&gt;**](PersonRead.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

