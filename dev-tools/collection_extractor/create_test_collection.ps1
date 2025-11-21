param(
    [string]$ApiKey = $env:POSTMAN_API_KEY,
    [string]$WorkspaceId = "20c3490b-76d5-4d25-8d3d-5f8a22d3ad39",
    [string]$CollectionName = "Test Collection - $(Get-Date -Format 'yyyy-MM-dd HHmmss')"
)

if (-not $ApiKey) {
    Write-Error "Postman API key not found. Set POSTMAN_API_KEY environment variable or pass -ApiKey parameter"
    exit 1
}

$body = @{
    collection = @{
        info = @{
            name = $CollectionName
            description = "Test collection created programmatically via Postman API"
            schema = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        }
        variable = @(
            @{
                key = "baseUrl"
                value = "https://api.example.com"
                description = "Base URL for API requests"
            }
        )
        item = @(
            @{
                name = "Get Users"
                request = @{
                    method = "GET"
                    url = "{{baseUrl}}/users"
                    header = @(
                        @{
                            key = "Accept"
                            value = "application/json"
                        }
                    )
                }
            },
            @{
                name = "Create User"
                request = @{
                    method = "POST"
                    url = "{{baseUrl}}/users"
                    header = @(
                        @{
                            key = "Content-Type"
                            value = "application/json"
                        }
                    )
                    body = @{
                        mode = "raw"
                        raw = '{"name": "John Doe", "email": "john@example.com"}'
                        options = @{
                            raw = @{
                                language = "json"
                            }
                        }
                    }
                }
            },
            @{
                name = "Get User by ID"
                request = @{
                    method = "GET"
                    url = "{{baseUrl}}/users/:userId"
                    header = @()
                }
            }
        )
    }
} | ConvertTo-Json -Depth 20

Write-Host "Creating collection: $CollectionName" -ForegroundColor Cyan
Write-Host "Workspace ID: $WorkspaceId" -ForegroundColor Gray
Write-Host ""

try {
    $response = Invoke-RestMethod `
        -Uri "https://api.getpostman.com/collections?workspace=$WorkspaceId" `
        -Method POST `
        -Headers @{
            "X-Api-Key" = $ApiKey
            "Content-Type" = "application/json"
        } `
        -Body $body `
        -ErrorAction Stop

    Write-Host "Success - Collection created!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Collection Details:" -ForegroundColor Cyan
    Write-Host "  ID:   $($response.collection.id)"
    Write-Host "  Name: $($response.collection.name)"
    Write-Host "  UID:  $($response.collection.uid)"
    Write-Host ""
    Write-Host "Access at:" -ForegroundColor Yellow
    Write-Host "  https://app.postman.com/workspace/$WorkspaceId/collections/$($response.collection.id)"
    
} catch {
    $statusCode = $_.Exception.Response.StatusCode.Value__
    Write-Host "Failed to create collection - HTTP $statusCode" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Yellow
    
    try {
        $errorBody = $_.Exception.Response.Content | ConvertFrom-Json
        if ($errorBody.error) {
            Write-Host "Details: $($errorBody.error | ConvertTo-Json)" -ForegroundColor Yellow
        }
    } catch {
        # Ignore JSON parsing errors
    }
    
    exit 1
}

