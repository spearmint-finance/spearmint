# setup-local-dev.ps1
# One-command setup for local development with SDK hot reload

param(
    [switch]$Help,
    [switch]$SkipBackend,
    [switch]$SkipFrontend,
    [switch]$SkipSDK,
    [switch]$SkipEnv,
    [switch]$StartServers
)

if ($Help) {
    Write-Host ""
    Write-Host "Local Development Setup Script" -ForegroundColor Cyan
    Write-Host "==============================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Sets up complete local development environment with SDK hot reload." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\scripts\setup-local-dev.ps1 [OPTIONS]"
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -SkipBackend    Skip backend setup (Python venv, dependencies, DB)"
    Write-Host "  -SkipFrontend   Skip frontend setup (npm install)"
    Write-Host "  -SkipSDK        Skip SDK generation and linking"
    Write-Host "  -SkipEnv        Skip environment configuration (.env file)"
    Write-Host "  -StartServers   Automatically start backend and frontend servers after setup"
    Write-Host "  -Help           Show this help message"
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  .\scripts\setup-local-dev.ps1                    # Full setup"
    Write-Host "  .\scripts\setup-local-dev.ps1 -StartServers      # Full setup + start servers"
    Write-Host "  .\scripts\setup-local-dev.ps1 -SkipBackend       # Skip backend setup"
    Write-Host "  .\scripts\setup-local-dev.ps1 -SkipSDK           # Skip SDK generation"
    Write-Host ""
    exit 0
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Spearmint Local Development Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"

# Detect repository root and navigate to it if needed
$currentLocation = Get-Location
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if we're in the scripts directory
if ($currentLocation.Path -like "*\scripts") {
    Write-Host "Detected script running from scripts directory, navigating to repository root..." -ForegroundColor Yellow
    Set-Location ..
}

# Verify we're in the repository root by checking for key directories
if (-not (Test-Path "core-api") -or -not (Test-Path "web-app") -or -not (Test-Path "sdk")) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ERROR: Not in repository root!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "This script must be run from the repository root directory." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Current directory: $currentLocation" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Please run:" -ForegroundColor Yellow
    Write-Host "  cd d:\CodingProjects\spearmint" -ForegroundColor Cyan
    Write-Host "  .\scripts\setup-local-dev.ps1" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

$startLocation = Get-Location

# Track what was done for final summary
$setupSteps = @()

try {
    # ============================================
    # Step 1: Backend Setup
    # ============================================
    if (-not $SkipBackend) {
        Write-Host "[1/4] Setting up Backend..." -ForegroundColor Yellow
        Write-Host ""
        
        # Check Python
        Write-Host "  Checking Python installation..." -ForegroundColor Gray
        try {
            $pythonVersion = python --version 2>&1
            Write-Host "  [OK] $pythonVersion" -ForegroundColor Green
        } catch {
            Write-Host "  [ERROR] Python not found. Please install Python 3.10+" -ForegroundColor Red
            exit 1
        }
        
        # Create virtual environment
        if (-not (Test-Path ".venv")) {
            Write-Host "  Creating virtual environment..." -ForegroundColor Gray
            python -m venv .venv
            Write-Host "  [OK] Virtual environment created" -ForegroundColor Green
        } else {
            Write-Host "  [OK] Virtual environment already exists" -ForegroundColor Green
        }
        
        # Activate virtual environment
        Write-Host "  Activating virtual environment..." -ForegroundColor Gray
        & .venv\Scripts\Activate.ps1
        Write-Host "  [OK] Virtual environment activated" -ForegroundColor Green
        
        # Install backend dependencies
        Write-Host "  Installing backend dependencies..." -ForegroundColor Gray
        Push-Location core-api
        pip install -r requirements.txt -q
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install backend dependencies"
        }
        Write-Host "  [OK] Backend dependencies installed" -ForegroundColor Green
        Pop-Location
        
        # Initialize database
        Write-Host "  Initializing database..." -ForegroundColor Gray
        Push-Location core-api
        python -m src.financial_analysis.database.init_db
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to initialize database"
        }
        Write-Host "  [OK] Database initialized" -ForegroundColor Green
        Pop-Location
        
        $setupSteps += "✅ Backend setup complete (Python venv, dependencies, database)"
        Write-Host ""
    } else {
        Write-Host "[1/4] Skipping Backend Setup" -ForegroundColor Gray
        Write-Host ""
    }
    
    # ============================================
    # Step 2: Frontend Setup
    # ============================================
    if (-not $SkipFrontend) {
        Write-Host "[2/4] Setting up Frontend..." -ForegroundColor Yellow
        Write-Host ""
        
        # Check Node.js
        Write-Host "  Checking Node.js installation..." -ForegroundColor Gray
        try {
            $nodeVersion = node --version
            Write-Host "  [OK] Node.js $nodeVersion" -ForegroundColor Green
        } catch {
            Write-Host "  [ERROR] Node.js not found. Please install Node.js 18+" -ForegroundColor Red
            exit 1
        }
        
        # Install frontend dependencies
        Write-Host "  Installing frontend dependencies..." -ForegroundColor Gray
        Push-Location web-app
        npm install
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install frontend dependencies"
        }
        Write-Host "  [OK] Frontend dependencies installed" -ForegroundColor Green
        Pop-Location
        
        $setupSteps += "✅ Frontend setup complete (npm dependencies)"
        Write-Host ""
    } else {
        Write-Host "[2/4] Skipping Frontend Setup" -ForegroundColor Gray
        Write-Host ""
    }

    # ============================================
    # Step 3: SDK Setup
    # ============================================
    if (-not $SkipSDK) {
        Write-Host "[3/4] Setting up SDK..." -ForegroundColor Yellow
        Write-Host ""

        # Check LibLab
        Write-Host "  Checking LibLab installation..." -ForegroundColor Gray
        try {
            $liblabVersion = liblab --version 2>&1
            Write-Host "  [OK] LibLab installed" -ForegroundColor Green
        } catch {
            Write-Host "  [WARNING] LibLab not found. Installing globally..." -ForegroundColor Yellow
            npm install -g liblab
            if ($LASTEXITCODE -ne 0) {
                throw "Failed to install LibLab"
            }
            Write-Host "  [OK] LibLab installed" -ForegroundColor Green
        }

        # Check for LibLab token
        Write-Host "  Checking LibLab token..." -ForegroundColor Gray
        if (-not (Test-Path "sdk\.env")) {
            Write-Host "  [WARNING] sdk\.env not found" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "  LibLab token is required for SDK generation." -ForegroundColor Yellow
            Write-Host "  Please create sdk\.env with your LibLab token:" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "  1. Copy the example file:" -ForegroundColor White
            Write-Host "     Copy-Item sdk\.env.example sdk\.env" -ForegroundColor Gray
            Write-Host ""
            Write-Host "  2. Edit sdk\.env and add your token:" -ForegroundColor White
            Write-Host "     LIBLAB_TOKEN=your-token-here" -ForegroundColor Gray
            Write-Host ""
            Write-Host "  3. Get your token from: https://developers.liblab.com/" -ForegroundColor White
            Write-Host ""
            Write-Host "  Then run this script again." -ForegroundColor Yellow
            Write-Host ""
            throw "LibLab token not configured"
        }
        Write-Host "  [OK] LibLab token configured" -ForegroundColor Green

        # Generate SDK
        Write-Host "  Generating SDK from OpenAPI spec..." -ForegroundColor Gray
        & .\sdk\scripts\generate-sdk.ps1
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to generate SDK"
        }
        Write-Host "  [OK] SDK generated" -ForegroundColor Green

        # Install SDK dependencies
        Write-Host "  Installing SDK dependencies..." -ForegroundColor Gray
        Push-Location sdk\output\typescript
        npm install
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to install SDK dependencies"
        }
        Write-Host "  [OK] SDK dependencies installed" -ForegroundColor Green

        # Create global npm link
        Write-Host "  Creating global npm link..." -ForegroundColor Gray
        npm link
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create npm link"
        }
        Write-Host "  [OK] Global npm link created" -ForegroundColor Green
        Pop-Location

        # Link SDK to web-app
        Write-Host "  Linking SDK to web-app..." -ForegroundColor Gray
        Push-Location web-app
        npm link @spearmint-finance/sdk
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to link SDK to web-app"
        }
        Write-Host "  [OK] SDK linked to web-app" -ForegroundColor Green
        Pop-Location

        # Verify link
        Write-Host "  Verifying SDK link..." -ForegroundColor Gray
        Push-Location web-app
        $linkCheck = npm ls @spearmint-finance/sdk 2>&1 | Out-String
        # Match both forward slashes (Linux/Mac) and backslashes (Windows)
        if ($linkCheck -match "-> \.[\\/]\.\.[\\/]sdk[\\/]output[\\/]typescript") {
            Write-Host "  [OK] SDK link verified" -ForegroundColor Green
        } else {
            Write-Host "  [WARNING] SDK link verification failed" -ForegroundColor Yellow
        }
        Pop-Location

        $setupSteps += "✅ SDK setup complete (generated, linked to web-app)"
        Write-Host ""
    } else {
        Write-Host "[3/4] Skipping SDK Setup" -ForegroundColor Gray
        Write-Host ""
    }

    # ============================================
    # Step 4: Environment Configuration
    # ============================================
    if (-not $SkipEnv) {
        Write-Host "[4/4] Configuring Environment..." -ForegroundColor Yellow
        Write-Host ""

        # Create .env file if it doesn't exist
        if (-not (Test-Path "web-app\.env")) {
            Write-Host "  Creating .env file from template..." -ForegroundColor Gray
            Copy-Item "web-app\.env.example" "web-app\.env"
            Write-Host "  [OK] .env file created" -ForegroundColor Green

            # Configure for Vite Proxy (recommended)
            Write-Host "  Configuring for Vite Proxy (recommended)..." -ForegroundColor Gray
            $envContent = Get-Content "web-app\.env" -Raw
            # Comment out VITE_API_URL to use Vite proxy
            $envContent = $envContent -replace "^VITE_API_URL=", "# VITE_API_URL="
            Set-Content "web-app\.env" $envContent
            Write-Host "  [OK] Configured for Vite Proxy (VITE_API_URL unset)" -ForegroundColor Green

            $setupSteps += "✅ Environment configured (Vite Proxy mode)"
        } else {
            Write-Host "  [OK] .env file already exists" -ForegroundColor Green
            $setupSteps += "✅ Environment already configured"
        }

        Write-Host ""
    } else {
        Write-Host "[4/4] Skipping Environment Configuration" -ForegroundColor Gray
        Write-Host ""
    }

    # ============================================
    # Setup Complete!
    # ============================================
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""

    # Show summary
    Write-Host "Summary:" -ForegroundColor Cyan
    foreach ($step in $setupSteps) {
        Write-Host "  $step" -ForegroundColor White
    }
    Write-Host ""

    # Start servers if requested
    if ($StartServers) {
        Write-Host ""
        Write-Host "Starting Development Servers..." -ForegroundColor Cyan
        Write-Host ""

        # Start backend in new terminal
        Write-Host "  Starting backend API server..." -ForegroundColor Yellow
        $backendPath = Join-Path $startLocation "start_api.ps1"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$startLocation'; .\start_api.ps1"
        Write-Host "  [OK] Backend started in new terminal" -ForegroundColor Green

        # Wait a moment for backend to initialize
        Start-Sleep -Seconds 2

        # Start frontend in new terminal
        Write-Host "  Starting frontend dev server..." -ForegroundColor Yellow
        $webAppPath = Join-Path $startLocation "web-app"
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$webAppPath'; .\start_frontend.bat"
        Write-Host "  [OK] Frontend started in new terminal" -ForegroundColor Green

        Write-Host ""
        Write-Host "Servers are starting up..." -ForegroundColor Cyan
        Write-Host "  Backend:  http://localhost:8000/api/docs" -ForegroundColor White
        Write-Host "  Frontend: http://localhost:5173" -ForegroundColor White
        Write-Host ""
        Write-Host "Note: It may take a few seconds for servers to be ready." -ForegroundColor Gray
        Write-Host "      Check the new terminal windows for server status." -ForegroundColor Gray
        Write-Host ""
    } else {
        # Show next steps
        Write-Host "Next Steps:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "  1. Start Backend (Terminal 1):" -ForegroundColor Yellow
        Write-Host "     .\start_api.ps1" -ForegroundColor White
        Write-Host ""
        Write-Host "  2. Start Frontend (Terminal 2):" -ForegroundColor Yellow
        Write-Host "     cd web-app" -ForegroundColor White
        Write-Host "     .\start_frontend.bat" -ForegroundColor White
        Write-Host ""
        Write-Host "  3. Access the application:" -ForegroundColor Yellow
        Write-Host "     Frontend:  http://localhost:5173" -ForegroundColor White
        Write-Host "     API Docs:  http://localhost:8000/api/docs" -ForegroundColor White
        Write-Host ""
        Write-Host "  4. After API changes, regenerate SDK:" -ForegroundColor Yellow
        Write-Host "     .\sdk\scripts\generate-sdk.ps1" -ForegroundColor White
        Write-Host "     (Frontend will auto-reload!)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "TIP: Run with -StartServers flag to automatically start both servers:" -ForegroundColor Cyan
        Write-Host "     .\scripts\setup-local-dev.ps1 -StartServers" -ForegroundColor White
        Write-Host ""
    }

    Write-Host "Documentation:" -ForegroundColor Cyan
    Write-Host "  - Complete Guide: dev-tools\docs\LOCAL_DEVELOPMENT_GUIDE.md" -ForegroundColor White
    Write-Host "  - Quick Start:    LOCAL_DEVELOPMENT_QUICKSTART.md" -ForegroundColor White
    Write-Host "  - SDK Guide:      LOCAL_SDK_DEVELOPMENT.md" -ForegroundColor White
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  Setup Failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check the error message above and try again." -ForegroundColor Yellow
    Write-Host "For help, run: .\scripts\setup-local-dev.ps1 -Help" -ForegroundColor Yellow
    Write-Host ""
    exit 1
} finally {
    Set-Location $startLocation
}

