variable "env" {
  description = "staging or prod environment"
  type        = string
}

variable "project" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud Region"
  type        = string
}

variable "db_root_password" {
  description = "Password for the root user of the database"
  type        = string
  sensitive   = true
}

variable "firebase_adminsdk_certificate" {
  description = "Certificate for the firebase admin sdk"
  type        = string
  sensitive   = true
}

variable "gcp_secret_manager_certificate" {
  description = "Certificate for the a gcp secret manager service account"
  type        = string
  sensitive   = true
}

variable "base_domain" {
  description = "Base domain for the project"
  type        = string
  sensitive   = false
}

variable "api_subdomain" {
  description = "Subdomain for the API"
  type        = string
  sensitive   = false
}

/* ------------------------ Analytics and Sourcing Auth Flow ------------------------ */

variable "PARMA_SHARED_SECRET_KEY" {
  description = "Shared secret key for the analytics and sourcing auth flow"
  type        = string
  sensitive   = true
}

variable "PARMA_ANALYTICS_SECRET_KEY" {
  description = "Analytics secret key the analytics and sourcing auth flow"
  type        = string
  sensitive   = true
}


/* ------------------------------------ SendGrid ------------------------------------ */

variable "sendgrid_api_key" {
  type      = string
  sensitive = true
}

variable "sendgrid_from_email" {
  type      = string
  sensitive = false
}

variable "sendgrid_notification_template_id" {
  type      = string
  sensitive = false
}

variable "sendgrid_report_template_id" {
  type      = string
  sensitive = false
}

/* ------------------------------------- ChatGpt ------------------------------------ */

variable "chatgpt_api_key" {
  type      = string
  sensitive = true
}
