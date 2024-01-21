terraform {
  required_version = "1.5.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.12.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
  backend "gcs" {
    bucket      = "la-famiglia-jst2324-tf-state"
    prefix      = "terraform/state/dev"
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

resource "google_sql_database_instance" "parma_db_instance" {
  name             = "parma-dev-db-instance"
  database_version = "POSTGRES_15"

  settings {
    tier = "db-f1-micro"

    disk_autoresize = false
    disk_type       = "PD_SSD"
    disk_size       = "10"

    ip_configuration {
      ipv4_enabled = true
      # ipv4_enabled                                  = false
      # private_network                               = google_compute_network.private_network.id
      # enable_private_path_for_google_cloud_services = true
      authorized_networks {
        name  = "everywhere"
        value = "0.0.0.0/0"
      }
    }
  }

  deletion_protection = "false"
  root_password       = var.db_root_password
}

resource "google_sql_database" "parma_db" {
  name      = "parma-dev-db"
  instance  = google_sql_database_instance.parma_db_instance.name
  charset   = "UTF8"
  collation = "en_US.UTF8"

}
