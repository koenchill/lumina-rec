Write-Host "Creating MinIO alias..."

docker compose exec minio mc alias set local http://localhost:9000 minio minio123

Write-Host "Creating mlflow-artifacts bucket if missing..."

docker compose exec minio mc mb --ignore-existing local/mlflow-artifacts

Write-Host "Current MinIO buckets:"

docker compose exec minio mc ls local