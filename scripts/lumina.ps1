param(
    [Parameter(Mandatory = $true)]
    [ValidateSet(
        "up",
        "down",
        "ps",
        "logs",
        "train",
        "test",
        "build-inference",
        "health",
        "ready",
        "metrics",
        "predict",
        "recommend",
        "movie",
        "load-test",
        "wait"
    )]
    [string]$Task
)

function Wait-ForInferenceApi {
    $maxAttempts = 30
    $delaySeconds = 2

    for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
        try {
            $response = Invoke-WebRequest `
                -Uri http://localhost:8001/health `
                -UseBasicParsing `
                -TimeoutSec 5

            if ($response.StatusCode -eq 200) {
                Write-Host "Inference API is ready."
                return
            }
        }
        catch {
            Write-Host "Waiting for inference API... attempt $attempt of $maxAttempts"
            Start-Sleep -Seconds $delaySeconds
        }
    }

    throw "Inference API did not become ready in time."
}

switch ($Task) {
    "up" {
        docker compose up -d --build
        Wait-ForInferenceApi
    }

    "down" {
        docker compose down
    }

    "ps" {
        docker compose ps
    }

    "logs" {
        docker compose logs --tail=100
    }

    "train" {
        python .\ml\training\train.py
    }

    "test" {
        pytest .\tests\inference\test_api.py
    }

    "build-inference" {
        docker compose build inference
    }

    "wait" {
        Wait-ForInferenceApi
    }

    "health" {
        Wait-ForInferenceApi
        Invoke-WebRequest -Uri http://localhost:8001/health -UseBasicParsing
    }

    "ready" {
        Wait-ForInferenceApi
        Invoke-WebRequest -Uri http://localhost:8001/ready -UseBasicParsing
    }

    "metrics" {
        Wait-ForInferenceApi
        Invoke-WebRequest -Uri http://localhost:8001/metrics -UseBasicParsing
    }

    "predict" {
        Wait-ForInferenceApi

        Invoke-RestMethod `
            -Uri http://localhost:8001/predict `
            -Method Post `
            -Headers @{ "x-api-key" = "local-dev-api-key" } `
            -ContentType "application/json" `
            -Body '{"user_id":1,"movie_id":1}'
    }

    "recommend" {
        Wait-ForInferenceApi

        Invoke-RestMethod `
            -Uri http://localhost:8001/recommend `
            -Method Post `
            -Headers @{ "x-api-key" = "local-dev-api-key" } `
            -ContentType "application/json" `
            -Body '{"user_id":1,"top_n":10}'
    }

    "movie" {
        Wait-ForInferenceApi

        Invoke-RestMethod `
            -Uri http://localhost:8001/movies/1 `
            -Method Get
    }

    "load-test" {
        Wait-ForInferenceApi

        New-Item -ItemType Directory -Path .\tests\load -Force | Out-Null

        locust `
            -f .\tests\load\locustfile.py `
            --host http://localhost:8001 `
            --headless `
            -u 10 `
            -r 2 `
            -t 60s `
            --html .\tests\load\load_test_report.html
    }
}