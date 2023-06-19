locals {
  resource_group_name = data.azurerm_resource_group.this.name
  location            = var.location == null ? data.azurerm_resource_group.this.location : var.location
  webapp_name         = "wa-cvbia-fastapi"
}
