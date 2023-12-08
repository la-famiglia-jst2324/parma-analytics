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
  description = "value"
  type        = string
  sensitive   = true
}

variable "firebase_adminsdk_certificate" {
  description = "value"
  type        = string
  sensitive   = true
}
