# Creating Collections Programmatically with Postman API

## Answer

**YES** — You can absolutely create a new collection in a workspace programmatically using the Postman API.

---

## The Endpoint

```
POST https://api.getpostman.com/collections?workspace={{workspaceId}}
```

**Authentication**: Include your Postman API key in the header:
```
X-API-Key: {your_api_key}
```

---

## Basic Request Body Structure

```json
{
  "collection": {
    "info": {
      "name": "My New Collection",
      "description": "Optional description",
      "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
      {
        "name": "Example Request",
        "request": {
          "method": "GET",
          "url": "https://api.example.com/users"
        }
      }
    ]
  }
}
```

---

## Complete Example with PowerShell

```powershell
$ApiKey = $env:POSTMAN_API_KEY
$WorkspaceId = "your-workspace-id"
$CollectionName = "My API Collection"

$body = @{
    collection = @{
        info = @{
            name = $CollectionName
            description = "Created programmatically"
            schema = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        }
        variable = @(
            @{
                key = "baseUrl"
                value = "https://api.example.com"
            }
        )
        item = @(
            @{
                name = "Get Users"
                request = @{
                    method = "GET"
                    url = @{
                        raw = "{{baseUrl}}/users"
                        host = @("{{baseUrl}}")
                        path = @("users")
                    }
                }
            },
            @{
                name = "Create User"
                request = @{
                    method = "POST"
                    url = @{
                        raw = "{{baseUrl}}/users"
                        host = @("{{baseUrl}}")
                        path = @("users")
                    }
                    body = @{
                        mode = "raw"
                        raw = "{`"name`": `"John Doe`"}"
                    }
                }
            }
        )
    }
} | ConvertTo-Json -Depth 20

$response = Invoke-RestMethod `
    -Uri "https://api.getpostman.com/collections?workspace=$WorkspaceId" `
    -Method POST `
    -Headers @{ "X-Api-Key" = $ApiKey } `
    -Body $body `
    -ContentType "application/json"

Write-Host "Collection created successfully!"
Write-Host "Collection ID: $($response.collection.id)"
Write-Host "Collection UID: $($response.collection.uid)"
```

---

## Response Format (Success)

```json
{
  "collection": {
    "id": "12ece9e1-2abf-4edc-8e34-de66e74114d2",
    "name": "Test Collection",
    "uid": "12345678-12ece9e1-2abf-4edc-8e34-de66e74114d2"
  }
}
```

---

## Possible Error Responses

### 400 - Bad Request (Item Already Exists)
```json
{
  "error": {
    "name": "instanceFoundError",
    "message": "The specified item already exists.",
    "details": {
      "item": "collection",
      "id": "12ece9e1-2abf-4edc-8e34-de66e74114d2"
    }
  }
}
```

### 400 - Malformed Request (Missing `info` Property)
```json
{
  "error": {
    "name": "malformedRequestError",
    "message": "Found 1 errors with the supplied collection.",
    "details": [
      ": must have required property 'info'"
    ]
  }
}
```

### 429 - Rate Limit Exceeded
```json
{
  "error": "rateLimited",
  "message": "Rate limit exceeded. Please retry after 1669048687"
}
```

---

## Collection Structure Reference

### Required Fields
- **`collection.info.name`** - Collection name (string)
- **`collection.info.schema`** - Must be the v2.1.0 schema URL
- **`collection.item`** - Array of requests/folders (can be empty)

### Optional Fields
- **`collection.info.description`** - Collection description
- **`collection.variable`** - Collection-level variables
- **`collection.auth`** - Authentication settings (basic, bearer, oauth2, etc.)
- **`collection.event`** - Pre-request and test scripts
- **`collection.item[].request.header`** - Request headers
- **`collection.item[].request.body`** - Request body (raw, formdata, urlencoded, etc.)

---

## Query Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `workspace` | No | Workspace ID where to create the collection. If omitted, creates in your oldest personal workspace. |

---

## Request Headers Required

```
X-Api-Key: {your_postman_api_key}
Content-Type: application/json
```

---

## Rate Limits

- **Standard Rate Limit**: 300 requests per minute per user
- **Specific Endpoint Limits**: GET `/collections` has a limit of 10 calls in 10 seconds

---

## Key Points

1. **Workspace Parameter**: If you don't specify the `workspace` parameter, Postman creates the collection in your oldest personal Internal workspace.

2. **Schema Validation**: The collection must comply with the [Postman Collection v2.1.0 schema](https://schema.postman.com/collection/json/v2.1.0/draft-07/docs/index.html).

3. **IDs vs UIDs**: 
   - **ID**: Unique identifier for the collection (e.g., `12ece9e1-2abf-4edc-8e34-de66e74114d2`)
   - **UID**: Full unique identifier (user ID + item ID, e.g., `12345678-12ece9e1-2abf-4edc-8e34-de66e74114d2`)

4. **Nested Structures**: You can create folders within collections by nesting items and using the `item` array.

---

## Example: Creating a Collection with Folders and Variables

```json
{
  "collection": {
    "info": {
      "name": "REST API",
      "description": "Complete REST API specification",
      "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "variable": [
      {
        "key": "baseUrl",
        "value": "https://api.example.com",
        "description": "Base URL for all requests"
      },
      {
        "key": "apiKey",
        "value": "your-api-key",
        "description": "API Authentication Key"
      }
    ],
    "auth": {
      "type": "apikey",
      "apikey": [
        {
          "key": "value",
          "value": "{{apiKey}}"
        },
        {
          "key": "key",
          "value": "X-API-Key"
        },
        {
          "key": "in",
          "value": "header"
        }
      ]
    },
    "item": [
      {
        "name": "Users",
        "item": [
          {
            "name": "Get All Users",
            "request": {
              "method": "GET",
              "url": "{{baseUrl}}/users"
            }
          },
          {
            "name": "Create User",
            "request": {
              "method": "POST",
              "url": "{{baseUrl}}/users",
              "body": {
                "mode": "raw",
                "raw": "{\"name\": \"John\", \"email\": \"john@example.com\"}"
              }
            }
          }
        ]
      },
      {
        "name": "Products",
        "item": [
          {
            "name": "Get All Products",
            "request": {
              "method": "GET",
              "url": "{{baseUrl}}/products"
            }
          }
        ]
      }
    ]
  }
}
```

---

## Real-World Use Cases

1. **API Scaffolding**: Automatically create collections from OpenAPI specs
2. **Workspace Provisioning**: Create standard collection templates for new team members
3. **CI/CD Integration**: Generate Postman collections as part of your deployment pipeline
4. **API Documentation**: Programmatically build collections that mirror your API structure
5. **Bulk Operations**: Create multiple collections in batch for testing different API versions

---

## Additional Related Endpoints

From the Postman API, you can also:

- **Update a collection**: `PUT /collections/:collectionId`
- **Duplicate a collection**: `POST /collections/:collectionId/duplicates`
- **Add folders to a collection**: `POST /collections/:collectionId/folders`
- **Add requests to a collection**: `POST /collections/:collectionId/requests`
- **Delete a collection**: `DELETE /collections/:collectionId`
- **Sync collection with API schema**: `PUT /collections/:collectionUid/synchronizations?specId={{specId}}`

---

## Documentation

For complete details, refer to the [Postman Collection Format v2.1.0 documentation](https://schema.postman.com/collection/json/v2.1.0/draft-07/docs/index.html).
