
output "analytics_api_url_root" {
  value = "https://analytics.${var.api_subdomain}${var.base_domain}"
}
