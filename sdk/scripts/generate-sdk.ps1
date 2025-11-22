# generate-sdk.ps1
# Generates the SDK locally using LibLab (matches CI/CD workflow process)

param(
    [switch]$SkipSpec,
    [switch]$Help
)

if ($Help) {
    Write-Host ""
    Write-Host "SDK Generation Script" -ForegroundColor Cyan
    Write-Host "=====================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Generates the TypeScript and Python SDKs using LibLab." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\sdk\scripts\generate-sdk.ps1 [OPTIONS]"
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -SkipSpec    Skip OpenAPI spec generation (use existing sdk/openapi.json)"
    Write-Host "  -Help        Show this help message"
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  .\sdk\scripts\generate-sdk.ps1              # Generate spec + SDK"
    Write-Host "  .\sdk\scripts\generate-sdk.ps1 -SkipSpec    # Only generate SDK"
    Write-Host ""
    Write-Host "REQUIREMENTS:" -ForegroundColor Yellow
    Write-Host "  - LibLab CLI installed: npm install -g liblab"
    Write-Host "  - LIBLAB_TOKEN environment variable set"
    Write-Host "  - Python virtual environment activated (if generating spec)"
    Write-Host ""
    exit 0
}

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Spearmint SDK Generation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check LibLab CLI
Write-Host "Checking LibLab CLI..." -ForegroundColor Yellow
try {
    $liblabVersion = liblab --version 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Not found" }
    Write-Host "[OK] LibLab CLI found: $liblabVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] LibLab CLI not found" -ForegroundColor Red
    Write-Host "Install with: npm install -g liblab" -ForegroundColor Yellow
    exit 1
}

# Check LIBLAB_TOKEN
Write-Host "Checking LIBLAB_TOKEN..." -ForegroundColor Yellow
if (-not $env:LIBLAB_TOKEN) {
    Write-Host "[ERROR] LIBLAB_TOKEN environment variable not set" -ForegroundColor Red
    Write-Host "Set it with: `$env:LIBLAB_TOKEN = 'your-token'" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] LIBLAB_TOKEN is set" -ForegroundColor Green
Write-Host ""

# Step 1: Generate OpenAPI Spec (unless skipped)
if (-not $SkipSpec) {
    Write-Host "Step 1: Generating OpenAPI Spec..." -ForegroundColor Yellow
    Write-Host "-----------------------------------" -ForegroundColor Cyan
    
    # Check if we're in a virtual environment
    if (-not $env:VIRTUAL_ENV) {
        Write-Host "[WARNING] Python virtual environment not detected" -ForegroundColor Yellow
        Write-Host "Attempting to activate .venv..." -ForegroundColor Yellow
        
        if (Test-Path ".venv\Scripts\Activate.ps1") {
            & .venv\Scripts\Activate.ps1
        } else {
            Write-Host "[ERROR] Virtual environment not found at .venv" -ForegroundColor Red
            Write-Host "Please activate your virtual environment first" -ForegroundColor Yellow
            exit 1
        }
    }
    
    # Navigate to core-api and generate spec
    Push-Location core-api
    try {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt -q
        pip install -e . -q
        
        Write-Host "Generating OpenAPI spec..." -ForegroundColor Yellow
        $env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"
        python scripts/generate_openapi.py ../sdk/openapi.json
        
        if ($LASTEXITCODE -ne 0) {
            throw "OpenAPI generation failed"
        }
        
        Write-Host "[OK] OpenAPI spec generated successfully" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Failed to generate OpenAPI spec: $_" -ForegroundColor Red
        Pop-Location
        exit 1
    } finally {
        Pop-Location
    }
    Write-Host ""
} else {
    Write-Host "Step 1: Skipping OpenAPI spec generation (using existing)" -ForegroundColor Yellow
    Write-Host ""
}

# Step 2: Build SDK with LibLab
Write-Host "Step 2: Building SDK with LibLab..." -ForegroundColor Yellow
Write-Host "------------------------------------" -ForegroundColor Cyan

Push-Location sdk
try {
    # Ensure config points to local openapi.json
    Write-Host "Updating liblab.config.json..." -ForegroundColor Yellow
    $config = Get-Content liblab.config.json -Raw | ConvertFrom-Json
    $config.specFilePath = "./openapi.json"
    $config | ConvertTo-Json -Depth 10 | Set-Content liblab.config.json
    
    Write-Host "Running liblab build..." -ForegroundColor Yellow
    liblab build
    
    if ($LASTEXITCODE -ne 0) {
        throw "LibLab build failed"
    }
    
    Write-Host "[OK] SDK built successfully" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Failed to build SDK: $_" -ForegroundColor Red
    Pop-Location
    exit 1
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SDK Generation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Output locations:" -ForegroundColor Yellow
Write-Host "  - TypeScript SDK: sdk/output/typescript/" -ForegroundColor White
Write-Host "  - Python SDK:     sdk/output/python/" -ForegroundColor White
Write-Host ""

