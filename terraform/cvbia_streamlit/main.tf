data "azurerm_resource_group" "this" {
  name = var.resource_group_name
}

resource "azurerm_service_plan" "this" {
  name                = "spcvbia-streamlit"
  resource_group_name = local.resource_group_name
  location            = local.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "this" {
  name                = local.webapp_name
  resource_group_name = local.resource_group_name
  location            = local.location
  service_plan_id     = azurerm_service_plan.this.id

  app_settings = {
    WEBSITES_PORT : 80,
    WEBSITES_CONTAINER_START_TIME_LIMIT : 1800,
    DOCKER_ENABLE_CI : true,
  }

  logs {
    application_logs {
      file_system_level = "Verbose"
    }
    http_logs {
      file_system {
        retention_in_days = 7
        retention_in_mb   = 35
      }
    }
  }

  identity {
    type = "SystemAssigned"
  }

  site_config {
    container_registry_use_managed_identity = true

    application_stack {
      docker_image     = "cvbia.azurecr.io/cvbia"
      docker_image_tag = "latest"
    }
  }
}
