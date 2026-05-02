Write-Host "Checking Lumina Rec Docker services..."

docker compose ps

Write-Host ""
Write-Host "Checking MLflow..."

try {
    $mlflow = Invoke-WebRequest -Uri http://localhost:5000 -UseBasicParsing -TimeoutSec 5
    Write-Host "MLflow status: $($mlflow.StatusCode)"
}
catch {
    Write-Host "MLflow check failed."
    Write-Host $_.Exception.Message
}

Write-Host ""
Write-Host "Checking inference health..."

try {
    $health = Invoke-RestMethod -Uri http://localhost:8001/health -Method Get -TimeoutSec 5
    Write-Host "Inference health: $($health.status)"
}
catch {
    Write-Host "Inference health check failed."
    Write-Host $_.Exception.Message
}

Write-Host ""
Write-Host "Checking inference readiness..."

try {
    $ready = Invoke-RestMethod -Uri http://localhost:8001/ready -Method Get -TimeoutSec 5
    $ready
}
catch {
    Write-Host "Inference readiness check failed."
    Write-Host $_.Exception.Message
}