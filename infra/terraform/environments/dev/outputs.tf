output "namespace" {
  value = module.inference_service.namespace
}

output "inference_service_name" {
  value = module.inference_service.service_name
}

output "inference_deployment_name" {
  value = module.inference_service.deployment_name
}

output "model_registry_config_map" {
  value = module.model_registry.config_map_name
}

output "port_forward_command" {
  value = "kubectl -n ${module.inference_service.namespace} port-forward svc/${module.inference_service.service_name} 8002:8000"
}
