from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    user_id: int = Field(..., description="MovieLens userId")
    movie_id: int = Field(..., description="MovieLens movieId")


class PredictionResponse(BaseModel):
    predicted_rating: float
    user_id: int
    movie_id: int
    model_name: str
    model_version: str
    request_id: str
    latency_ms: float


class RecommendationRequest(BaseModel):
    user_id: int = Field(..., description="MovieLens userId")
    top_n: int = Field(default=10, ge=1, le=50)
    genre: str | None = Field(default=None, description="Optional MovieLens genre filter")


class RecommendationItem(BaseModel):
    rank: int
    movie_id: int
    title: str
    genres: str
    predicted_rating: float


class RecommendationResponse(BaseModel):
    user_id: int
    top_n: int
    returned_count: int
    genre: str | None = None
    recommendations: list[RecommendationItem]
    model_name: str
    model_version: str
    request_id: str
    latency_ms: float


class MovieMetadataResponse(BaseModel):
    movie_id: int
    title: str
    genres: str


class VersionResponse(BaseModel):
    service_name: str
    service_version: str
    model_name: str
    model_version: str


class ModelInfoResponse(BaseModel):
    model_name: str
    model_version: str
    model_run_id: str
    model_artifact_path: str
    model_sha256: str
    checksum_validation: str
    artifact_manifest_status: str
    artifact_manifest_version: str
    model_registry_enabled: str
    registered_model_name: str
    model_alias: str


class ErrorResponse(BaseModel):
    error_code: str
    detail: str
    request_id: str | None = None
