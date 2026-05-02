Write-Host "Running Lumina Rec full local validation..."

Write-Host ""
Write-Host "1. Checking Docker services..."
docker compose ps

Write-Host ""
Write-Host "2. Checking readiness..."
.\scripts\lumina.ps1 ready

Write-Host ""
Write-Host "3. Checking prediction..."
.\scripts\lumina.ps1 predict

Write-Host ""
Write-Host "4. Checking recommendation..."
.\scripts\lumina.ps1 recommend

Write-Host ""
Write-Host "5. Checking movie metadata lookup..."
.\scripts\lumina.ps1 movie

Write-Host ""
Write-Host "6. Running tests..."
.\scripts\lumina.ps1 test

Write-Host ""
Write-Host "7. Checking Git status..."
git status

Write-Host ""
Write-Host "Validation complete."