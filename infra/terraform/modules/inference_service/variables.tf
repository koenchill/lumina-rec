variable "namespace" {
  type        = string
  description = "Kubernetes namespace for inference"
}

variable "create_namespace" {
  type        = bool
  description = "Whether this module creates the namespace"
  default     = true
}

variable "image" {
  type        = string
  description = "Container image for inference"
  default     = "lumina-rec-inference:latest"
}

variable "replicas" {
  type        = number
  description = "Desired replica count"
  default     = 1
}

variable "mlflow_tracking_uri" {
  type        = string
  description = "MLflow tracking URI reachable from the pod"
}

variable "mlflow_s3_endpoint_url" {
  type        = string
  description = "S3-compatible endpoint for artifacts"
}

variable "aws_access_key_id" {
  type        = string
  description = "Access key for artifact storage"
}

variable "aws_secret_access_key" {
  type        = string
  description = "Secret key for artifact storage"
  sensitive   = true
}

variable "lumina_api_key" {
  type        = string
  description = "API key for protected endpoints"
  sensitive   = true
}

variable "lumina_rate_limit" {
  type        = string
  description = "Rate limit string for SlowAPI"
  default     = "300/minute"
}

variable "model_run_id" {
  type        = string
  description = "Approved MLflow run ID"
}

variable "model_sha256" {
  type        = string
  description = "Approved model checksum"
}

variable "model_artifact_path" {
  type    = string
  default = "approved_model"
}

variable "registered_model_name" {
  type    = string
  default = "lumina-rec-movielens-mf"
}

variable "model_alias" {
  type    = string
  default = "approved"
}

variable "use_model_registry" {
  type    = bool
  default = false
}

variable "labels" {
  type    = map(string)
  default = {}
}
