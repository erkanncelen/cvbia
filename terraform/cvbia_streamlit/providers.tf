terraform {
  required_version = ">= 1.3"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "cvbia_test"
    storage_account_name = "sacvbia"
    container_name       = "tfstate"
    key                  = "webapp-streamlit/terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}
