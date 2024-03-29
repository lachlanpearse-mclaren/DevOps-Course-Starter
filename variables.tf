variable "prefix" {
  description = "The prefix used for all resources in this environment"
}
variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default     = "uksouth"
}
variable "AUTH_CLIENTID" {
  description = "OAuth ClientID"
  sensitive   = true
}
variable "AUTH_SECRET" {
  description = "OAuth Secret"
  sensitive   = true
}
variable "APP_SECRET" {
  description = "Application Secret"
  sensitive   = true
}
variable "LOGGLY_TOKEN" {
  description = "Loggly Secure Token"
  sensitive   = true
}