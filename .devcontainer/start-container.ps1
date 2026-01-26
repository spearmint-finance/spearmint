# Start Spearmint Dev Container
# Run this script before opening in VS Code

Write-Host "Starting Spearmint Dev Container..." -ForegroundColor Cyan

# Change to project directory
Set-Location $PSScriptRoot\..

# Start container
docker compose -f .devcontainer/docker-compose.yml up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Container started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Open VS Code"
    Write-Host "  2. Press Ctrl+Shift+P"
    Write-Host "  3. Select 'Dev Containers: Attach to Running Container'"
    Write-Host "  4. Choose 'devcontainer-app-1'"
    Write-Host ""
} else {
    Write-Host "Failed to start container. Check Docker Desktop is running." -ForegroundColor Red
}
