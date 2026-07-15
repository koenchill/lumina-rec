variable "namespace" {
  type        = string
  description = "Kubernetes namespace for registry metadata"
}

variable "registered_model_name" {
  type        = string
  description = "Logical registered model name"
}

variable "model_alias" {
  type        = string
  description = "Approved model alias"
}

variable "model_artifact_path" {
  type        = string
  description = "Artifact folder name inside the MLflow run"
  default     = "approved_model"
}

variable "use_model_registry" {
  type        = bool
  description = "Whether inference should resolve models by registry alias"
  default     = false
}

variable "labels" {
  type        = map(string)
  description = "Common Kubernetes labels"
  default     = {}
}
