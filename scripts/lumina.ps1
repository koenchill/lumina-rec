param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("up", "down", "ps", "logs", "train", "test", "build-inference", "health", "ready", "metrics", "predict", "load-test")]
)

switch ($Task) {
    "up" {
        docker compose up -d --build
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

    "health" {
        Invoke-WebRequest -Uri http://localhost:8001/health -UseBasicParsing
    }

    "ready" {
        Invoke-WebRequest -Uri http://localhost:8001/ready -UseBasicParsing
    }

    "metrics" {
        Invoke-WebRequest -Uri http://localhost:8001/metrics -UseBasicParsing
    }

    "predict" {
        Invoke-RestMethod `
            -Uri http://localhost:8001/predict `
            -Method Post `
            -ContentType "application/json" `
            -Body '{"features":[1,2,3,4,5,6,7,8,9,10]}'
    }
}