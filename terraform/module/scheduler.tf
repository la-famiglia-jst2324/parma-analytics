resource "google_cloud_scheduler_job" "schedule_job" {
  name     = "schedule-job-${var.env}"
  schedule = "0 12 * * *"  # Cron Expression for Every Day at Midday

  http_target {
    uri         = "https://analytics.${var.api_subdomain}${var.base_domain}/schedule"
    http_method = "GET"
  }

  project = var.project
  region  = var.region
}
