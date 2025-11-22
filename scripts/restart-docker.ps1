# restart-docker.ps1
# Script to update and restart the local Docker Compose cluster

param(
    [switch]$Build,      # Force rebuild of images
    [switch]$Clean,      # Remove volumes and clean start
    [switch]$Logs,       # Show logs after starting
    [switch]$Help        # Show help
)

function Show-Help {
    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host "  Spearmint Docker Compose - Update & Restart Script" -ForegroundColor Cyan
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Yellow
    Write-Host "  .\scripts\restart-docker.ps1 [OPTIONS]"
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Yellow
    Write-Host "  -Build       Force rebuild of all Docker images"
    Write-Host "  -Clean       Remove volumes and perform clean start (WARNING: deletes data)"
    Write-Host "  -Logs        Show logs after starting services"
    Write-Host "  -Help        Show this help message"
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "  .\scripts\restart-docker.ps1                # Quick restart"
    Write-Host "  .\scripts\restart-docker.ps1 -Build         # Rebuild and restart"
    Write-Host "  .\scripts\restart-docker.ps1 -Clean         # Clean restart (deletes data)"
    Write-Host "  .\scripts\restart-docker.ps1 -Build -Logs   # Rebuild and show logs"
    Write-Host ""
    Write-Host "SERVICES:" -ForegroundColor Yellow
    Write-Host "  - gateway    (API Gateway)      http://localhost:8080"
    Write-Host "  - core-api   (Backend API)      http://localhost:8000"
    Write-Host "  - web-app    (Frontend)         http://localhost:80"
    Write-Host "  - db         (PostgreSQL)       localhost:5432"
    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host ""
    exit 0
}

if ($Help) {
    Show-Help
}

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  Spearmint Docker Compose - Update & Restart" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if docker-compose is available
Write-Host "Checking Docker Compose..." -ForegroundColor Yellow
try {
    $dockerComposeVersion = docker compose version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Compose not found"
    }
    Write-Host "✓ Docker Compose found: $dockerComposeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Docker Compose is not installed or not in PATH" -ForegroundColor Red
    Write-Host "  Please install Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Step 1: Stop running containers
Write-Host "Step 1: Stopping running containers..." -ForegroundColor Yellow
docker compose down
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to stop containers" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Containers stopped" -ForegroundColor Green
Write-Host ""

# Step 2: Clean volumes if requested
if ($Clean) {
    Write-Host "Step 2: Removing volumes (CLEAN MODE)..." -ForegroundColor Yellow
    Write-Host "  WARNING: This will delete all database data!" -ForegroundColor Red
    $confirmation = Read-Host "  Are you sure? (yes/no)"
    if ($confirmation -eq "yes") {
        docker compose down -v
        if ($LASTEXITCODE -ne 0) {
            Write-Host "✗ Failed to remove volumes" -ForegroundColor Red
            exit 1
        }
        Write-Host "✓ Volumes removed" -ForegroundColor Green
    } else {
        Write-Host "  Skipping volume removal" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Step 3: Pull latest images (if not building)
if (-not $Build) {
    Write-Host "Step 3: Pulling latest images..." -ForegroundColor Yellow
    docker compose pull
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠ Warning: Failed to pull some images (may not exist in registry)" -ForegroundColor Yellow
    } else {
        Write-Host "✓ Images pulled" -ForegroundColor Green
    }
    Write-Host ""
}

# Step 4: Build images if requested
if ($Build) {
    Write-Host "Step 3: Building Docker images..." -ForegroundColor Yellow
    docker compose build --no-cache
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to build images" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Images built" -ForegroundColor Green
    Write-Host ""
}

# Step 5: Start services
Write-Host "Step 4: Starting services..." -ForegroundColor Yellow
docker compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to start services" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Services started" -ForegroundColor Green
Write-Host ""

# Step 6: Show status
Write-Host "Step 5: Checking service status..." -ForegroundColor Yellow
docker compose ps
Write-Host ""

# Step 7: Show access URLs
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  Services are now running!" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access your services at:" -ForegroundColor Yellow
Write-Host "  - API Gateway:     http://localhost:8080" -ForegroundColor White
Write-Host "  - API Docs:        http://localhost:8080/api/docs" -ForegroundColor White
Write-Host "  - Frontend:        http://localhost:80" -ForegroundColor White
Write-Host "  - Core API:        http://localhost:8000" -ForegroundColor White
Write-Host "  - PostgreSQL:      localhost:5432" -ForegroundColor White
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  - View logs:       docker compose logs -f" -ForegroundColor White
Write-Host "  - Stop services:   docker compose down" -ForegroundColor White
Write-Host "  - Restart service: docker compose restart <service-name>" -ForegroundColor White
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 8: Show logs if requested
if ($Logs) {
    Write-Host "Showing logs (press Ctrl+C to exit)..." -ForegroundColor Yellow
    Write-Host ""
    docker compose logs -f
}

