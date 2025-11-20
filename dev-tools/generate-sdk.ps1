# generate-sdk.ps1

Write-Host "Checking if API Gateway is up..."
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080/api/health" -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "API is up. Generating SDKs with LibLab..."
        Set-Location "../sdk"
        liblab build
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SDK Generation Complete!" -ForegroundColor Green
        } else {
            Write-Host "SDK Generation Failed." -ForegroundColor Red
        }
    }
} catch {
    Write-Host "Error: API Gateway is not accessible at http://localhost:8080" -ForegroundColor Red
    Write-Host "Please run 'docker-compose up -d' first."
}
