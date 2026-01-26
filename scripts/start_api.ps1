# Start the FastAPI backend server

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Spearmint API Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "[WARNING] Virtual environment not detected" -ForegroundColor Yellow
    Write-Host "Attempting to activate .venv..." -ForegroundColor Yellow
    
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        & .venv\Scripts\Activate.ps1
        Write-Host "[OK] Virtual environment activated" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Virtual environment not found at .venv" -ForegroundColor Red
        Write-Host "Please create it with: python -m venv .venv" -ForegroundColor Yellow
        Write-Host "Then activate it with: .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "[OK] Virtual environment activated" -ForegroundColor Green
}

Write-Host ""

# Set PYTHONPATH to include core-api directory
$env:PYTHONPATH = "$PWD\core-api;$env:PYTHONPATH"

# Navigate to core-api directory
Push-Location core-api

try {
    # Start the API server with uvicorn
    Write-Host "Starting API server..." -ForegroundColor Yellow
    Write-Host ""
    uvicorn src.financial_analysis.api.main:app --host 0.0.0.0 --port 8000 --reload
} finally {
    # Return to root directory
    Pop-Location
}

