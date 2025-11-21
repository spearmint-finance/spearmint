# Setup script for OpenAPI spec validation with Postman (Windows)
# This script installs and configures the Postman CLI for spec validation

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "OpenAPI Spec Validation Setup (Windows)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Postman CLI is installed
try {
    $version = postman --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Postman CLI is already installed" -ForegroundColor Green
        Write-Host "  Version: $version"
    } else {
        throw "Not installed"
    }
} catch {
    Write-Host "Installing Postman CLI..." -ForegroundColor Yellow
    
    try {
        Invoke-WebRequest -Uri "https://dl-cli.pstmn.io/install/win64.ps1" -UseBasicParsing | Invoke-Expression
        Write-Host "✓ Postman CLI installed successfully" -ForegroundColor Green
        Write-Host "  Please restart your PowerShell terminal and run this script again" -ForegroundColor Yellow
        exit 0
    } catch {
        Write-Host "❌ Failed to install Postman CLI" -ForegroundColor Red
        Write-Host "Please install manually from:" -ForegroundColor Yellow
        Write-Host "https://learning.postman.com/docs/postman-cli/postman-cli-installation/" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""

# Check if user is logged in
Write-Host "Checking Postman authentication..." -ForegroundColor Cyan
try {
    postman login --help 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Postman CLI is ready" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Postman CLI not found in PATH" -ForegroundColor Red
    Write-Host "Please restart your terminal or add Postman CLI to your PATH" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Prompt for API key
Write-Host "To validate specs, you need to login to Postman." -ForegroundColor Cyan
Write-Host ""
$hasKey = Read-Host "Do you have a Postman API key? (y/n)"

if ($hasKey -eq "y" -or $hasKey -eq "Y") {
    $apiKey = Read-Host "Enter your Postman API key" -AsSecureString
    $apiKeyPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey)
    )
    
    if ($apiKeyPlain) {
        Write-Host "Logging in to Postman..." -ForegroundColor Cyan
        postman login --with-api-key $apiKeyPlain
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Successfully logged in to Postman" -ForegroundColor Green
        } else {
            Write-Host "❌ Login failed" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "❌ No API key provided" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host ""
    Write-Host "To get a Postman API key:" -ForegroundColor Yellow
    Write-Host "1. Go to https://postman.co/settings/me/api-keys"
    Write-Host "2. Click 'Generate API Key'"
    Write-Host "3. Copy the key and run this script again"
    Write-Host ""
    Write-Host "Or login manually with:" -ForegroundColor Yellow
    Write-Host "  postman login --with-api-key YOUR_API_KEY"
    exit 0
}

Write-Host ""

# Prompt for workspace ID
Write-Host "To apply workspace-specific governance rules, you need a workspace ID." -ForegroundColor Cyan
Write-Host ""
$setWorkspace = Read-Host "Do you want to set a workspace ID? (y/n)"

if ($setWorkspace -eq "y" -or $setWorkspace -eq "Y") {
    $workspaceId = Read-Host "Enter your Postman workspace ID"
    
    if ($workspaceId) {
        # Set environment variable
        [Environment]::SetEnvironmentVariable("POSTMAN_WORKSPACE_ID", $workspaceId, "User")
        Write-Host "✓ Set POSTMAN_WORKSPACE_ID environment variable" -ForegroundColor Green
        Write-Host "  Please restart your terminal for changes to take effect" -ForegroundColor Yellow
        
        # Also set for current session
        $env:POSTMAN_WORKSPACE_ID = $workspaceId
    }
} else {
    Write-Host "Skipping workspace ID setup" -ForegroundColor Yellow
    Write-Host "Validation will use 'All workspaces' governance rules"
}

Write-Host ""

# Install pre-commit if not installed
try {
    pre-commit --version 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ pre-commit is already installed" -ForegroundColor Green
    }
} catch {
    Write-Host "Installing pre-commit..." -ForegroundColor Yellow
    pip install pre-commit
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ pre-commit installed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install pre-commit" -ForegroundColor Red
        Write-Host "Please install manually with: pip install pre-commit" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""

# Install pre-commit hooks
Write-Host "Installing pre-commit hooks..." -ForegroundColor Cyan
pre-commit install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Pre-commit hooks installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install pre-commit hooks" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test the validation:"
Write-Host "   python dev-tools/validate_spec.py --spec-file sdk/openapi.json"
Write-Host ""
Write-Host "2. Run pre-commit hooks manually:"
Write-Host "   pre-commit run --all-files"
Write-Host ""
Write-Host "3. Commit changes to trigger automatic validation:"
Write-Host "   git add ."
Write-Host "   git commit -m 'Your commit message'"
Write-Host ""
Write-Host "For more information, see:" -ForegroundColor Cyan
Write-Host "  dev-tools/docs/SPEC_VALIDATION.md"
Write-Host ""

