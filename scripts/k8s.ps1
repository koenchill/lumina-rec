param(
    [Parameter(Mandatory = $true)]
    [ValidateSet(
        "deps",
        "build",
        "deploy",
        "status",
        "ready",
        "logs",
        "down",
        "restart"
    )]
    [string]$Task
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$K8sDir = Join-Path $RepoRoot "infra\k8s"
$EnvFile = Join-Path $RepoRoot ".env"
$Namespace = "lumina-rec"
$LocalPort = 8002

function Get-DotEnvValue {
    param(
        [string]$Path,
        [string]$Key
    )

    if (-not (Test-Path $Path)) {
        throw ".env not found at $Path. Copy .env.example to .env first."
    }

    $line = Get-Content $Path |
        Where-Object { $_ -match "^\s*$Key\s*=" } |
        Select-Object -First 1

    if (-not $line) {
        throw "Missing $Key in .env"
    }

    return ($line -split "=", 2)[1].Trim().Trim('"').Trim("'")
}

function Assert-KubectlContext {
    $context = kubectl config current-context
    if (-not $context) {
        throw "No kubectl context set. Enable Kubernetes in Docker Desktop first."
    }
    Write-Host "Using kubectl context: $context"
}

function Ensure-ComposeDeps {
    Push-Location $RepoRoot
    try {
        Write-Host "Starting Compose dependencies (postgres, minio, mlflow)..."
        docker compose up -d postgres minio minio-init mlflow
    }
    finally {
        Pop-Location
    }
}

function Apply-InferenceSecret {
    $apiKey = Get-DotEnvValue -Path $EnvFile -Key "LUMINA_API_KEY"
    $modelRunId = Get-DotEnvValue -Path $EnvFile -Key "MODEL_RUN_ID"
    $modelSha = Get-DotEnvValue -Path $EnvFile -Key "MODEL_SHA256"
    $awsSecret = Get-DotEnvValue -Path $EnvFile -Key "AWS_SECRET_ACCESS_KEY"

    kubectl create namespace $Namespace --dry-run=client -o yaml | kubectl apply -f -

    kubectl -n $Namespace create secret generic inference-secrets `
        --from-literal=LUMINA_API_KEY=$apiKey `
        --from-literal=MODEL_RUN_ID=$modelRunId `
        --from-literal=MODEL_SHA256=$modelSha `
        --from-literal=AWS_SECRET_ACCESS_KEY=$awsSecret `
        --dry-run=client -o yaml | kubectl apply -f -
}

function Wait-ForReady {
    Write-Host "Waiting for Deployment rollout..."
    kubectl -n $Namespace rollout status deployment/inference --timeout=180s

    Write-Host "Port-forwarding svc/inference to http://localhost:$LocalPort ..."
    Write-Host "Leave this running, or use another terminal for curl checks."
    Write-Host "Quick check command:"
    Write-Host "  curl.exe http://localhost:$LocalPort/ready"
}

switch ($Task) {
    "deps" {
        Ensure-ComposeDeps
    }

    "build" {
        Push-Location $RepoRoot
        try {
            docker build -t lumina-rec-inference:latest -f services/inference/Dockerfile .
        }
        finally {
            Pop-Location
        }
    }

    "deploy" {
        Assert-KubectlContext
        Ensure-ComposeDeps
        Apply-InferenceSecret
        kubectl apply -k $K8sDir
        kubectl -n $Namespace rollout status deployment/inference --timeout=180s
        Write-Host ""
        Write-Host "Deployed. Start port-forward with:"
        Write-Host "  kubectl -n $Namespace port-forward svc/inference ${LocalPort}:8000"
        Write-Host "Then:"
        Write-Host "  .\scripts\k8s.ps1 ready"
    }

    "restart" {
        Assert-KubectlContext
        Apply-InferenceSecret
        kubectl -n $Namespace rollout restart deployment/inference
        kubectl -n $Namespace rollout status deployment/inference --timeout=180s
    }

    "status" {
        Assert-KubectlContext
        kubectl -n $Namespace get deploy,po,svc
    }

    "ready" {
        $uri = "http://localhost:$LocalPort/ready"
        try {
            $response = Invoke-WebRequest -Uri $uri -UseBasicParsing -TimeoutSec 5
            $response.Content
        }
        catch {
            throw "Ready check failed on $uri. Is port-forward running? kubectl -n $Namespace port-forward svc/inference ${LocalPort}:8000"
        }
    }

    "logs" {
        Assert-KubectlContext
        kubectl -n $Namespace logs deploy/inference --tail=120
    }

    "down" {
        Assert-KubectlContext
        kubectl delete -k $K8sDir --ignore-not-found
        kubectl -n $Namespace delete secret inference-secrets --ignore-not-found
    }
}
