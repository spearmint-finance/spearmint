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

# Try to load from sdk/.env if not already set
if (-not $env:LIBLAB_TOKEN) {
    $envFile = "sdk\.env"
    if (Test-Path $envFile) {
        Write-Host "Loading LIBLAB_TOKEN from sdk\.env..." -ForegroundColor Gray
        try {
            # Read and parse .env file
            Get-Content $envFile -ErrorAction Stop | ForEach-Object {
                $line = $_.Trim()
                # Skip empty lines and comments
                if ($line -and -not $line.StartsWith('#')) {
                    # Split on first = sign
                    $parts = $line -split '=', 2
                    if ($parts.Length -eq 2) {
                        $key = $parts[0].Trim()
                        $value = $parts[1].Trim()
                        if ($key -eq 'LIBLAB_TOKEN') {
                            $env:LIBLAB_TOKEN = $value
                            Write-Host "  Token loaded successfully" -ForegroundColor Gray
                        }
                    }
                }
            }
        } catch {
            Write-Host "  [WARNING] Failed to read sdk\.env: $_" -ForegroundColor Yellow
        }
    }
}

# Verify token is set
if (-not $env:LIBLAB_TOKEN) {
    Write-Host "[ERROR] LIBLAB_TOKEN environment variable not set" -ForegroundColor Red
    Write-Host "" -ForegroundColor Yellow
    Write-Host "Option 1: Create sdk\.env file with:" -ForegroundColor Yellow
    Write-Host "  LIBLAB_TOKEN=your-token-here" -ForegroundColor White
    Write-Host "" -ForegroundColor Yellow
    Write-Host "Option 2: Set environment variable:" -ForegroundColor Yellow
    Write-Host "  `$env:LIBLAB_TOKEN = 'your-token'" -ForegroundColor White
    Write-Host ""
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
Write-Host "Step 3: Synchronizing SDK version with version.json..." -ForegroundColor Yellow
Write-Host "-------------------------------------------------------" -ForegroundColor Cyan

# Read version from version.json
$versionFile = "version.json"
if (Test-Path $versionFile) {
    try {
        $versionData = Get-Content $versionFile -Raw | ConvertFrom-Json
        $projectVersion = $versionData.version
        Write-Host "Project version from version.json: $projectVersion" -ForegroundColor Gray

        # Update TypeScript SDK package.json
        $tsPackageJson = "sdk\output\typescript\package.json"
        if (Test-Path $tsPackageJson) {
            $tsPackage = Get-Content $tsPackageJson -Raw | ConvertFrom-Json
            $oldVersion = $tsPackage.version
            $tsPackage.version = $projectVersion
            $tsPackage | ConvertTo-Json -Depth 10 | Set-Content $tsPackageJson
            Write-Host "  Updated TypeScript SDK: $oldVersion -> $projectVersion" -ForegroundColor Green
        } else {
            Write-Host "  [WARNING] TypeScript package.json not found" -ForegroundColor Yellow
        }

        # Update Python SDK version (if needed in the future)
        # TODO: Add Python SDK version sync when needed

        Write-Host "[OK] SDK version synchronized" -ForegroundColor Green
    } catch {
        Write-Host "[WARNING] Failed to sync SDK version: $_" -ForegroundColor Yellow
        Write-Host "You may need to manually update sdk/output/typescript/package.json" -ForegroundColor Yellow
    }
} else {
    Write-Host "[WARNING] version.json not found at repository root" -ForegroundColor Yellow
    Write-Host "SDK version may not match project version" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 4: Building TypeScript SDK..." -ForegroundColor Yellow
Write-Host "-----------------------------------" -ForegroundColor Cyan

Push-Location sdk\output\typescript
try {
    Write-Host "Installing SDK dependencies..." -ForegroundColor Gray
    npm install --silent 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[WARNING] npm install had warnings, continuing..." -ForegroundColor Yellow
    }

    Write-Host "Building SDK (compiling TypeScript to dist/)..." -ForegroundColor Gray
    npm run build 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "npm run build failed"
    }

    Write-Host "Fixing package.json exports for ESM compatibility..." -ForegroundColor Gray
    $packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
    if ($packageJson.exports -and $packageJson.exports.'.' -and $packageJson.exports.'.'.import) {
        $packageJson.exports.'.'.import = "./dist/index.mjs"
        $packageJson | ConvertTo-Json -Depth 10 | Set-Content "package.json"
        Write-Host "  Fixed exports.import to use index.mjs" -ForegroundColor Gray
    }

    Write-Host "[OK] TypeScript SDK built successfully" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Failed to build TypeScript SDK: $_" -ForegroundColor Red
    Write-Host "The SDK source was generated but not compiled." -ForegroundColor Yellow
    Write-Host "You may need to manually run: cd sdk\output\typescript && npm install && npm run build" -ForegroundColor Yellow
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

