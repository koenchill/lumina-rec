$configPath = ".\configs\approved_model.json"
$envPath = ".\.env"

if (-not (Test-Path $configPath)) {
    throw "Missing approved model config: $configPath"
}

if (-not (Test-Path $envPath)) {
    throw "Missing .env file: $envPath"
}

$config = Get-Content $configPath | ConvertFrom-Json
$envContent = Get-Content $envPath

function Set-EnvValue {
    param(
        [string[]]$Lines,
        [string]$Key,
        [string]$Value
    )

    $pattern = "^$Key="
    $replacement = "$Key=$Value"

    if ($Lines -match $pattern) {
        return $Lines | ForEach-Object {
            if ($_ -match $pattern) {
                $replacement
            }
            else {
                $_
            }
        }
    }

    return $Lines + $replacement
}

$envContent = Set-EnvValue $envContent "MODEL_RUN_ID" $config.model_run_id
$envContent = Set-EnvValue $envContent "MODEL_SHA256" $config.model_sha256
$envContent = Set-EnvValue $envContent "MODEL_ARTIFACT_PATH" $config.model_artifact_path
$envContent = Set-EnvValue $envContent "REGISTERED_MODEL_NAME" $config.registered_model_name
$envContent = Set-EnvValue $envContent "MODEL_ALIAS" $config.model_alias

$envContent | Set-Content $envPath

Write-Host "Updated .env from configs/approved_model.json"
Write-Host "MODEL_RUN_ID=$($config.model_run_id)"
Write-Host "MODEL_SHA256=$($config.model_sha256)"
Write-Host "MODEL_ARTIFACT_PATH=$($config.model_artifact_path)"