#Requires -Version 5.1
<#
.SYNOPSIS
    Extract a Postman collection by ID and generate a detailed API overview report.

.DESCRIPTION
    Fetches a Postman collection from the API, saves the raw JSON, and generates
    a comprehensive overview report showing all endpoints, HTTP methods, and structure.

.PARAMETER CollectionId
    The Postman collection ID (UID) to extract. Can be found in collection URLs.

.PARAMETER ApiKey
    Postman API key. If not provided, will attempt to use POSTMAN_API_KEY env var.

.PARAMETER OutputDir
    Directory to save collection JSON and report. Defaults to current directory.

.PARAMETER SkipReport
    If specified, only downloads the collection JSON without generating the report.

.EXAMPLE
    .\extract_collection.ps1 -CollectionId "19931619-c8ba23fd-94d7-4737-8ca6-1743b4952531"
    
.EXAMPLE
    .\extract_collection.ps1 -CollectionId "19931619-c8ba23fd-94d7-4737-8ca6-1743b4952531" -OutputDir "./exports"

#>

param(
    [Parameter(Mandatory=$true, HelpMessage="Postman collection ID")]
    [string]$CollectionId,

    [Parameter(Mandatory=$false, HelpMessage="Postman API key (or use POSTMAN_API_KEY env var)")]
    [string]$ApiKey,

    [Parameter(Mandatory=$false, HelpMessage="Output directory for files")]
    [string]$OutputDir = ".",

    [switch]$SkipReport
)

$ErrorActionPreference = "Stop"

# Get API key from parameter or environment variable
if (-not $ApiKey) {
    $ApiKey = $env:POSTMAN_API_KEY
    if (-not $ApiKey) {
        Write-Error "API key not provided and POSTMAN_API_KEY environment variable not set."
        exit 1
    }
}

# Create output directory if it doesn't exist
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$OutputDir = (Get-Item $OutputDir).FullName

# Fetch collection from Postman API
Write-Host "Fetching collection: $CollectionId" -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod `
        -Uri "https://api.getpostman.com/collections/$CollectionId" `
        -Headers @{"X-Api-Key" = $ApiKey} `
        -ErrorAction Stop

    $collectionJson = $response | ConvertTo-Json -Depth 50
    $collectionName = $response.collection.info.name
    
    $safeCollectionName = $collectionName -replace '[^\w\s-]', '' -replace '\s+', '_'
    $jsonFile = Join-Path $OutputDir "${safeCollectionName}_collection.json"
    
    $collectionJson | Out-File -FilePath $jsonFile -Encoding utf8
    Write-Host "Collection saved: $jsonFile" -ForegroundColor Green
    
} catch {
    Write-Error "Failed to fetch collection: $($_.Exception.Message)"
    exit 1
}

# Generate report if not skipped
if (-not $SkipReport) {
    Write-Host "Generating API overview report..." -ForegroundColor Cyan
    
    $pythonScript = Join-Path (Split-Path $PSCommandPath) "analyze_collection.py"
    
    if (-not (Test-Path $pythonScript)) {
        Write-Error "Python analyzer not found at: $pythonScript"
        exit 1
    }
    
    & python $pythonScript -i $jsonFile -o $OutputDir
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Report generation complete!" -ForegroundColor Green
    } else {
        Write-Error "Report generation failed"
        exit 1
    }
}
