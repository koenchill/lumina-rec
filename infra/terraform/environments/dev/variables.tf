variable "kubeconfig_path" {
  type        = string
  description = "Path to kubeconfig"
  default     = "~/.kube/config"
}

variable "kube_context" {
  type        = string
  description = "kubectl context to use"
  default     = "docker-desktop"
}

variable "namespace" {
  type        = string
  description = "Kubernetes namespace"
  default     = "lumina-rec"
}

variable "inference_image" {
  type        = string
  description = "Inference container image"
  default     = "lumina-rec-inference:latest"
}

variable "replicas" {
  type    = number
  default = 1
}

variable "mlflow_tracking_uri" {
  type    = string
  default = "http://host.docker.internal:5000"
}

variable "mlflow_s3_endpoint_url" {
  type    = string
  default = "http://host.docker.internal:9000"
}

variable "aws_access_key_id" {
  type    = string
  default = "minio"
}

variable "aws_secret_access_key" {
  type      = string
  sensitive = true
}

variable "lumina_api_key" {
  type      = string
  sensitive = true
}

variable "lumina_rate_limit" {
  type    = string
  default = "300/minute"
}

variable "model_run_id" {
  type = string
}

variable "model_sha256" {
  type = string
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
