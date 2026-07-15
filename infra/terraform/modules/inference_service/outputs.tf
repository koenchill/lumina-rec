output "namespace" {
  value = var.namespace
}

output "service_name" {
  value = kubernetes_service_v1.inference.metadata[0].name
}

output "deployment_name" {
  value = kubernetes_deployment_v1.inference.metadata[0].name
}

output "config_map_name" {
  value = kubernetes_config_map_v1.inference.metadata[0].name
}

output "secret_name" {
  value = kubernetes_secret_v1.inference.metadata[0].name
}
