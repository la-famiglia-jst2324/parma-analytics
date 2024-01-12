
/* ---------------------------------- Service Image --------------------------------- */

# Note: Generally it is NOT best practise to build images in Terraform. We are still
# doing it here for simplicity. In industry, you should think twice before doing this.
resource "null_resource" "docker_build" {

  provisioner "local-exec" {
    working_dir = path.module
    command     = "IMG=${var.region}-docker.pkg.dev/${var.project}/parma-registry/parma-analytics:${var.env}-$(git rev-parse --short HEAD) && docker build -t $IMG ./../../ && docker push $IMG && echo $IMG > .image.name"
  }

  triggers = {
    always_run = timestamp()
  }
}

# get output from docker_build
data "local_file" "image_name" {
  filename   = "${path.module}/.image.name"
  depends_on = [null_resource.docker_build]
}


/* ------------------------------------ Cloud Run ----------------------------------- */

resource "google_cloud_run_service" "parma_analytics_cloud_run" {
  name     = "parma-analytics-${var.env}"
  location = var.region

  template {
    spec {
      containers {
        image = data.local_file.image_name.content
        ports {
          container_port = 8080
        }
        env {
          name  = "POSTGRES_HOST"
          value = google_sql_database_instance.parma_db_instance.public_ip_address
        }
        env {
          name  = "POSTGRES_PORT"
          value = "5432"
        }
        env {
          name  = "POSTGRES_USER"
          value = "postgres"
        }
        env {
          name  = "POSTGRES_PASSWORD"
          value = var.db_root_password
        }
        env {
          name  = "POSTGRES_DB"
          value = google_sql_database.parma_db.name
        }

        env {
          name  = "FIREBASE_ADMINSDK_CERTIFICATE"
          value = var.firebase_adminsdk_certificate
        }

        env {
          name  = "GCP_SECRET_MANAGER_CERTIFICATE"
          value = var.gcp_secret_manager_certificate
        }

        env {
          name  = "SENDGRID_API_KEY"
          value = var.sendgrid_api_key
        }

        env {
          name  = "SENDGRID_FROM_EMAIL"
          value = var.sendgrid_from_email
        }

        env {
          name  = "SENDGRID_NOTIFICATION_TEMPLATE_ID"
          value = var.sendgrid_notification_template_id
        }

        env {
          name  = "SENDGRID_REPORT_TEMPLATE_ID"
          value = var.sendgrid_report_template_id
        }

        env {
          name  = "CHATGPT_API_KEY"
          value = var.chatgpt_api_key
        }
        env {
          name  = "DEPLOYMENT_ENV"
          value = var.env
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

/* ---------------------------- Cloud Run domain mapping ---------------------------- */

# initial setup of DNS mapping in cloud console

/* --------------------------------------- IAM -------------------------------------- */

data "google_iam_policy" "noauth" {
  binding {
    role    = "roles/run.invoker"
    members = ["allUsers"]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.parma_analytics_cloud_run.location
  project  = google_cloud_run_service.parma_analytics_cloud_run.project
  service  = google_cloud_run_service.parma_analytics_cloud_run.name

  policy_data = data.google_iam_policy.noauth.policy_data
}
