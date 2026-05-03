$latestRunPath = ".\reports\latest_training_run.json"
$approvedModelPath = ".\configs\approved_model.json"

if (-not (Test-Path $latestRunPath)) {
    throw "Missing latest training run file: $latestRunPath"
}

$latestRun = Get-Content $latestRunPath | ConvertFrom-Json

$approvedPayload = [ordered]@{
    model_name = $latestRun.model_name
    model_version = $latestRun.model_version
    model_run_id = $latestRun.model_run_id
    model_sha256 = $latestRun.model_sha256
    model_artifact_path = $latestRun.model_artifact_path
    test_rmse = $latestRun.test_rmse
    registered_model_name = $latestRun.registered_model_name
    model_alias = $latestRun.model_alias
}

$approvedPayload |
    ConvertTo-Json -Depth 5 |
    Set-Content $approvedModelPath

Write-Host "Promoted latest training run to approved model config."
Write-Host "Approved model config: $approvedModelPath"
Write-Host "MODEL_RUN_ID=$($latestRun.model_run_id)"
Write-Host "MODEL_SHA256=$($latestRun.model_sha256)"
Write-Host "TEST_RMSE=$($latestRun.test_rmse)"