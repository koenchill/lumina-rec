$configPath = ".\configs\approved_model.json"

if (-not (Test-Path $configPath)) {
    throw "Missing approved model config: $configPath"
}

$config = Get-Content $configPath | ConvertFrom-Json

Write-Host "Approved Model Configuration"
Write-Host "----------------------------"
Write-Host "Model name: $($config.model_name)"
Write-Host "Model version: $($config.model_version)"
Write-Host "Model run ID: $($config.model_run_id)"
Write-Host "Model SHA256: $($config.model_sha256)"
Write-Host "Artifact path: $($config.model_artifact_path)"
Write-Host "Test RMSE: $($config.test_rmse)"
Write-Host "Registered model name: $($config.registered_model_name)"
Write-Host "Model alias: $($config.model_alias)"