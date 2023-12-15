resource "google_cloud_scheduler_job" "schedule_job" {
  depends_on = []
  name       = "schedule-job-${var.env}"
  schedule   = "0,30 * * * *" # Every full and half hour

  http_target {
    uri         = "https://analytics.${var.api_subdomain}${var.base_domain}/schedule"
    http_method = "GET"
  }

  project = var.project
  region  = var.region
}
