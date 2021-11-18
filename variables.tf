variable "prefix" {
  description = "The prefix used for all resources in this environment"
}
variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default     = "uksouth"
}
variable "FLASK_APP" {
  description = "App Location"
  sensitive   = true
}
variable "LOGIN_DISABLED" {
  description = "Default LOGIN_DISABLED value"
  sensitive   = true
}
variable "AUTH_CLIENTID" {
  description = "OAuth ClientID"
  sensitive   = true
}
variable "AUTH_SECRET" {
  description = "OAuth Secret"
  sensitive   = true
}
variable "AUTH_REDIRECT_URL" {
  description = "OAuth Redirect URL"
  sensitive   = true
}
variable "AUTH_TOKEN_URL" {
  description = "OAuth Token URL"
  sensitive   = true
}
variable "AUTH_API_URL" {
  description = "OAuth API URL"
  sensitive   = true
}
variable "APP_SECRET" {
  description = "Application Secret"
  sensitive   = true
}