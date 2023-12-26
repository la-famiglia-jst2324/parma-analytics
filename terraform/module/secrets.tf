resource "google_kms_key_ring" "enc_key" {
  name     = "parma-secrets"
  location = "europe-west1"
}

resource "google_kms_crypto_key" "enc_key" {
  name            = "parma-secrets-key"
  key_ring        = google_kms_key_ring.enc_key.id
  rotation_period = "7776000s"  # 90 days
}
