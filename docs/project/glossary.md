# Glossary

## Purpose

This glossary defines common terms used in Lumina Rec.

| Term | Meaning |
|---|---|
| MLflow | Tool used to track experiments, metrics, parameters, and artifacts |
| MinIO | Local S3 compatible object storage used for model artifacts |
| Postgres | Database used as the MLflow metadata backend |
| FastAPI | Python web framework used for the inference API |
| PyTorch | Machine learning framework used to train the recommender |
| Matrix factorization | Recommendation model technique using user and movie embeddings |
| MovieLens | Public dataset used for recommender system training |
| Artifact | File produced by training, such as model, metadata, or mappings |
| Approved model | Model selected for inference serving |
| MODEL_RUN_ID | MLflow run ID used to load approved artifacts |
| MODEL_SHA256 | Approved model checksum |
| `/predict` | Endpoint that predicts a rating for one user and movie |
| `/recommend` | Endpoint that returns top N movie recommendations |
| `/movies/{movie_id}` | Endpoint that returns movie title and genres |
| RMSE | Root mean squared error, used to evaluate rating prediction accuracy |
| Locust | Load testing tool |
| Prometheus metrics | Metrics format exposed by `/metrics` |