output "config_map_name" {
  description = "Name of the model registry ConfigMap"
  value       = kubernetes_config_map_v1.model_registry.metadata[0].name
}

output "registered_model_name" {
  value = var.registered_model_name
}

output "model_alias" {
  value = var.model_alias
}

output "model_artifact_path" {
  value = var.model_artifact_path
}

output "use_model_registry" {
  value = var.use_model_registry
}
