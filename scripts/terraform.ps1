param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("init", "plan", "apply", "destroy", "output", "fmt", "write-tfvars")]
    [string]$Task
)

$ErrorActionPreference = "Stop"

# Ensure winget-installed terraform is visible in fresh shells.
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
    [System.Environment]::GetEnvironmentVariable("Path", "User")

$RepoRoot = Split-Path -Parent $PSScriptRoot
$DevDir = Join-Path $RepoRoot "infra\terraform\environments\dev"
$EnvFile = Join-Path $RepoRoot ".env"
$TfVars = Join-Path $DevDir "terraform.tfvars"

function Get-DotEnvValue {
    param([string]$Path, [string]$Key)

    if (-not (Test-Path $Path)) {
        throw ".env not found at $Path"
    }

    $line = Get-Content $Path |
        Where-Object { $_ -match "^\s*$Key\s*=" } |
        Select-Object -First 1

    if (-not $line) {
        throw "Missing $Key in .env"
    }

    return ($line -split "=", 2)[1].Trim().Trim('"').Trim("'")
}

function Write-TfVarsFromEnv {
    $modelRunId = Get-DotEnvValue -Path $EnvFile -Key "MODEL_RUN_ID"
    $modelSha = Get-DotEnvValue -Path $EnvFile -Key "MODEL_SHA256"
    $apiKey = Get-DotEnvValue -Path $EnvFile -Key "LUMINA_API_KEY"
    $awsSecret = Get-DotEnvValue -Path $EnvFile -Key "AWS_SECRET_ACCESS_KEY"
    $artifactPath = Get-DotEnvValue -Path $EnvFile -Key "MODEL_ARTIFACT_PATH"

    @"
kube_context = "docker-desktop"
namespace    = "lumina-rec"

inference_image = "lumina-rec-inference:latest"
replicas        = 1

mlflow_tracking_uri    = "http://host.docker.internal:5000"
mlflow_s3_endpoint_url = "http://host.docker.internal:9000"
aws_access_key_id      = "minio"
aws_secret_access_key  = "$awsSecret"

lumina_api_key    = "$apiKey"
lumina_rate_limit = "300/minute"

model_run_id        = "$modelRunId"
model_sha256        = "$modelSha"
model_artifact_path = "$artifactPath"

registered_model_name = "lumina-rec-movielens-mf"
model_alias           = "approved"
use_model_registry    = false
"@ | Set-Content -Path $TfVars -Encoding utf8

    Write-Host "Wrote $TfVars from .env (do not commit)."
}

function Ensure-TfVars {
    if (-not (Test-Path $TfVars)) {
        Write-TfVarsFromEnv
    }
}

function Invoke-Terraform {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)

    Push-Location $DevDir
    try {
        & terraform @Args
        if ($LASTEXITCODE -ne 0) {
            throw "terraform $($Args -join ' ') failed with exit code $LASTEXITCODE"
        }
    }
    finally {
        Pop-Location
    }
}

switch ($Task) {
    "write-tfvars" {
        Write-TfVarsFromEnv
    }

    "init" {
        Ensure-TfVars
        Invoke-Terraform init
    }

    "fmt" {
        Push-Location (Join-Path $RepoRoot "infra\terraform")
        try {
            terraform fmt -recursive
        }
        finally {
            Pop-Location
        }
    }

    "plan" {
        Ensure-TfVars
        Invoke-Terraform plan
    }

    "apply" {
        Ensure-TfVars
        Write-Host "Ensure Compose MLflow/MinIO/Postgres are up before apply."
        docker compose -f (Join-Path $RepoRoot "docker-compose.yml") up -d postgres minio minio-init mlflow
        Invoke-Terraform apply -auto-approve
        Write-Host ""
        Write-Host "Applied. Port-forward with:"
        Write-Host "  kubectl -n lumina-rec port-forward svc/inference 8002:8000"
    }

    "destroy" {
        Ensure-TfVars
        Invoke-Terraform destroy -auto-approve
    }

    "output" {
        Invoke-Terraform output
    }
}
