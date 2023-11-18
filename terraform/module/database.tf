
resource "google_sql_database_instance" "parma_db_instance" {
  name             = "parma-${var.env}-db-instance"
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
  name      = "parma-${var.env}-db"
  instance  = google_sql_database_instance.parma_db_instance.name
  charset   = "UTF8"
  collation = "en_US.UTF8"

}
