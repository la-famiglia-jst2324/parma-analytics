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
}

provider "google" {
  credentials = file("../.secrets/la-famiglia-parma-ai.json")
  project     = var.project
  region      = var.region
}
