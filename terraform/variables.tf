variable "resource_group_name" {
  type        = string
  description = "Name of the resource group"
  default     = "cvbia_test"
}

variable "location" {
  description = "Location of deployed resource. If not provided, the resource group location will be used"
  type        = string
  default     = null
}

variable "docker_repository" {
  type        = string
  default     = "docker.io"
  description = "Docker image name"
}

variable "docker_image_streamlit" {
  type        = string
  default     = "cvbia.azurecr.io/cvbia_streamlit"
  description = "Azure container registry image name"
}

variable "docker_image_slackbot" {
  type        = string
  default     = "cvbia.azurecr.io/cvbia_slackbot"
  description = "Azure container registry image name"
}
