resource "kubernetes_config_map_v1" "model_registry" {
  metadata {
    name      = "model-registry-config"
    namespace = var.namespace
    labels    = merge(var.labels, { "app.kubernetes.io/name" = "model-registry" })
  }

  data = {
    REGISTERED_MODEL_NAME = var.registered_model_name
    MODEL_ALIAS           = var.model_alias
    MODEL_ARTIFACT_PATH   = var.model_artifact_path
    USE_MODEL_REGISTRY    = var.use_model_registry ? "true" : "false"
  }
}
