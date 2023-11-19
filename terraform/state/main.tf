# Terraform code to handle remote state in storage bucket.
# to be run manually

terraform {
  required_version = "1.5.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6"
    }
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

/* --------------------------------------- KMS -------------------------------------- */

resource "google_kms_key_ring" "tf_state_bucket" {
  name     = "tf-state"
  location = "europe-west1"
}

resource "google_kms_crypto_key" "tf_state_bucket" {
  name            = "tf-state"
  key_ring        = google_kms_key_ring.tf_state_bucket.id
  rotation_period = "100000s"
}

/* --------------------------------------- IAM -------------------------------------- */

data "google_storage_project_service_account" "gcs_account" {
}

resource "google_kms_crypto_key_iam_binding" "binding" {
  crypto_key_id = google_kms_crypto_key.tf_state_bucket.id
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"

  members = ["serviceAccount:${data.google_storage_project_service_account.gcs_account.email_address}"]
}

/* --------------------------------------- GCS -------------------------------------- */

resource "google_storage_bucket" "tf_state" {
  name          = "la-famiglia-jst2324-tf-state"
  force_destroy = false
  location      = "EUROPE-WEST1"
  storage_class = "STANDARD"
  versioning {
    enabled = true
  }
  encryption {
    default_kms_key_name = google_kms_crypto_key.tf_state_bucket.id
  }

  # Ensure the KMS crypto-key IAM binding for the service account exists prior to the
  # bucket attempting to utilise the crypto-key.
  depends_on = [google_kms_crypto_key_iam_binding.binding]
}

/* ------------------------------- Container Registry ------------------------------- */

resource "google_artifact_registry_repository" "parma_registry" {
  location      = "europe-west1"
  repository_id = "parma-registry"
  description   = "Parma Analytics Container Registry"
  format        = "DOCKER"
}
