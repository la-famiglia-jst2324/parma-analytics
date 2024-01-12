terraform {
  required_version = "1.5.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
  backend "gcs" {
    bucket      = "la-famiglia-jst2324-tf-state"
    prefix      = "terraform/state/staging"
    credentials = "../.secrets/la-famiglia-parma-ai.json"
  }
}

locals {
  project = "la-famiglia-parma-ai"
  region  = "europe-west1"
}

provider "google" {
  credentials = file("../.secrets/la-famiglia-parma-ai.json")
  project     = local.project
  region      = local.region
}

module "main" {
  source           = "../module"
  env              = "staging"
  project          = local.project
  region           = local.region
  db_root_password = var.db_root_password
  base_domain      = var.base_domain
  api_subdomain    = "staging."

  firebase_adminsdk_certificate  = var.firebase_adminsdk_certificate
  gcp_secret_manager_certificate = var.gcp_secret_manager_certificate

  sendgrid_api_key                  = var.sendgrid_api_key
  sendgrid_from_email               = var.sendgrid_from_email
  sendgrid_notification_template_id = var.sendgrid_notification_template_id
  sendgrid_report_template_id       = var.sendgrid_report_template_id

  chatgpt_api_key = var.chatgpt_api_key
}
