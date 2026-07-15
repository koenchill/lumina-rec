locals {
  labels = {
    "app.kubernetes.io/part-of"    = "lumina-rec"
    "app.kubernetes.io/managed-by" = "terraform"
    "environment"                  = "dev"
  }
}

module "model_registry" {
  source = "../../modules/model_registry"

  namespace             = var.namespace
  registered_model_name = var.registered_model_name
  model_alias           = var.model_alias
  model_artifact_path   = var.model_artifact_path
  use_model_registry    = var.use_model_registry
  labels                = local.labels

  depends_on = [module.inference_service]
}

module "inference_service" {
  source = "../../modules/inference_service"

  namespace              = var.namespace
  create_namespace       = true
  image                  = var.inference_image
  replicas               = var.replicas
  mlflow_tracking_uri    = var.mlflow_tracking_uri
  mlflow_s3_endpoint_url = var.mlflow_s3_endpoint_url
  aws_access_key_id      = var.aws_access_key_id
  aws_secret_access_key  = var.aws_secret_access_key
  lumina_api_key         = var.lumina_api_key
  lumina_rate_limit      = var.lumina_rate_limit
  model_run_id           = var.model_run_id
  model_sha256           = var.model_sha256
  model_artifact_path    = var.model_artifact_path
  registered_model_name  = var.registered_model_name
  model_alias            = var.model_alias
  use_model_registry     = var.use_model_registry
  labels                 = local.labels
}
