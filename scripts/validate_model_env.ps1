Write-Host "Validating model environment values..."

$requiredPatterns = @(
    "MODEL_RUN_ID",
    "MODEL_SHA256",
    "MODEL_ARTIFACT_PATH",
    "MLFLOW_TRACKING_URI",
    "MLFLOW_S3_ENDPOINT_URL",
    "LUMINA_API_KEY",
    "LUMINA_RATE_LIMIT"
)

foreach ($pattern in $requiredPatterns) {
    Select-String -Path .\.env -Pattern $pattern
}

Write-Host ""
Write-Host "Docker Compose resolved model values:"

docker compose config | Select-String "MODEL_RUN_ID|MODEL_SHA256|MODEL_ARTIFACT_PATH|USE_MODEL_REGISTRY|REGISTERED_MODEL_NAME|MODEL_ALIAS"