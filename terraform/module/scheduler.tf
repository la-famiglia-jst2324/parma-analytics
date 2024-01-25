# Data sourcing modules scheduler
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

# Weekly reports
resource "google_cloud_scheduler_job" "weekly_reports_schedule_job" {
  depends_on = []
  name       = "weekly-reports-schedule-job-${var.env}"
  schedule   = "0 8 * * 1" # Every Monday at 8 AM

  http_target {
    uri         = "https://analytics.${var.api_subdomain}${var.base_domain}/weekly-reports"
    http_method = "GET"
  }

  project = var.project
  region  = var.region
}
