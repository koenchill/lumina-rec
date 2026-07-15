locals {
  common_labels = merge(
    {
      "app.kubernetes.io/part-of" = "lumina-rec"
    },
    var.labels,
  )
}

resource "kubernetes_namespace_v1" "this" {
  count = var.create_namespace ? 1 : 0

  metadata {
    name   = var.namespace
    labels = local.common_labels
  }
}

resource "kubernetes_secret_v1" "inference" {
  metadata {
    name      = "inference-secrets"
    namespace = var.namespace
    labels    = merge(local.common_labels, { "app.kubernetes.io/name" = "inference" })
  }

  data = {
    LUMINA_API_KEY        = var.lumina_api_key
    MODEL_RUN_ID          = var.model_run_id
    MODEL_SHA256          = var.model_sha256
    AWS_SECRET_ACCESS_KEY = var.aws_secret_access_key
  }

  type = "Opaque"

  depends_on = [kubernetes_namespace_v1.this]
}

resource "kubernetes_config_map_v1" "inference" {
  metadata {
    name      = "inference-config"
    namespace = var.namespace
    labels    = merge(local.common_labels, { "app.kubernetes.io/name" = "inference" })
  }

  data = {
    MLFLOW_TRACKING_URI    = var.mlflow_tracking_uri
    MLFLOW_S3_ENDPOINT_URL = var.mlflow_s3_endpoint_url
    AWS_ACCESS_KEY_ID      = var.aws_access_key_id
    MODEL_ARTIFACT_PATH    = var.model_artifact_path
    USE_MODEL_REGISTRY     = var.use_model_registry ? "true" : "false"
    REGISTERED_MODEL_NAME  = var.registered_model_name
    MODEL_ALIAS            = var.model_alias
    LUMINA_RATE_LIMIT      = var.lumina_rate_limit
    PYTHONPATH             = "/app/src:/app"
  }

  depends_on = [kubernetes_namespace_v1.this]
}

resource "kubernetes_deployment_v1" "inference" {
  metadata {
    name      = "inference"
    namespace = var.namespace
    labels    = merge(local.common_labels, { "app.kubernetes.io/name" = "inference" })
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        "app.kubernetes.io/name" = "inference"
      }
    }

    template {
      metadata {
        labels = merge(local.common_labels, { "app.kubernetes.io/name" = "inference" })
      }

      spec {
        container {
          name              = "inference"
          image             = var.image
          image_pull_policy = "IfNotPresent"

          port {
            name           = "http"
            container_port = 8000
          }

          env_from {
            config_map_ref {
              name = kubernetes_config_map_v1.inference.metadata[0].name
            }
          }

          env_from {
            secret_ref {
              name = kubernetes_secret_v1.inference.metadata[0].name
            }
          }

          readiness_probe {
            http_get {
              path = "/ready"
              port = "http"
            }
            initial_delay_seconds = 20
            period_seconds        = 10
            timeout_seconds       = 5
            failure_threshold     = 12
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = "http"
            }
            initial_delay_seconds = 30
            period_seconds        = 20
            timeout_seconds       = 5
            failure_threshold     = 3
          }

          resources {
            requests = {
              cpu    = "100m"
              memory = "512Mi"
            }
            limits = {
              cpu    = "2"
              memory = "2Gi"
            }
          }
        }
      }
    }
  }

  depends_on = [
    kubernetes_config_map_v1.inference,
    kubernetes_secret_v1.inference,
  ]
}

resource "kubernetes_service_v1" "inference" {
  metadata {
    name      = "inference"
    namespace = var.namespace
    labels    = merge(local.common_labels, { "app.kubernetes.io/name" = "inference" })
  }

  spec {
    type = "ClusterIP"

    selector = {
      "app.kubernetes.io/name" = "inference"
    }

    port {
      name        = "http"
      port        = 8000
      target_port = "http"
    }
  }

  depends_on = [kubernetes_deployment_v1.inference]
}
