# Raw curl test for Postman spec publishing
# This eliminates any Python script issues

$env:POSTMAN_API_KEY = (Get-Content d:\CodingProjects\spearmint\core-api\.env | Select-String 'POSTMAN_API_KEY' | ForEach-Object { $_ -replace 'POSTMAN_API_KEY=', '' })
$workspaceId = "20c3490b-76d5-4d25-8d3d-5f8a22d3ad39"

# Read the old spec file
$specContent = Get-Content d:\CodingProjects\spearmint\dev-tools\local-debug\old-openapi.json -Raw

# Escape for JSON
$specContentEscaped = $specContent -replace '\\', '\\' -replace '"', '\"' -replace "`r`n", '\n' -replace "`n", '\n' -replace "`t", '\t'

# Build JSON payload
$payload = @"
{
  "name": "Spearmint Finance API - CURL Test v0.0.14",
  "type": "OPENAPI:3.1",
  "files": [
    {
      "path": "old-openapi.json",
      "content": "$specContentEscaped",
      "type": "ROOT"
    }
  ]
}
"@

# Save payload to file for curl
$payload | Out-File -FilePath d:\CodingProjects\spearmint\dev-tools\local-debug\curl-payload.json -Encoding utf8 -NoNewline

Write-Host "Payload file created. Size: $((Get-Item d:\CodingProjects\spearmint\dev-tools\local-debug\curl-payload.json).Length) bytes"
Write-Host ""
Write-Host "Executing curl command..."
Write-Host ""

# Execute curl
curl.exe -X POST "https://api.postman.com/specs?workspaceId=$workspaceId" `
  -H "X-Api-Key: $env:POSTMAN_API_KEY" `
  -H "Content-Type: application/json" `
  -d "@d:\CodingProjects\spearmint\dev-tools\local-debug\curl-payload.json" `
  --verbose
