variable "db_root_password" {
  description = "Password for the root user of the database"
  type        = string
  sensitive   = true
}

variable "base_domain" {
  description = "Base domain for the project"
  type        = string
  sensitive   = false
  default     = "parma.software"
}
