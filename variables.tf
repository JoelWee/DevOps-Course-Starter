variable "prefix" {
  description = "The prefix used for all resources in this environment"
  default     = "SoftwirePilot_JoelWee"
}

variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default     = "uksouth"
}

variable "oauth_client_id" {
  description = "oauth_client_id"
}

variable "oauth_client_secret" {
  description = "oauth_client_secret"
}

variable "secret_key" {
  description = "Key for signing session cookie"
}

