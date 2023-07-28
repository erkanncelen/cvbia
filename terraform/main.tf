data "azurerm_resource_group" "this" {
  name = var.resource_group_name
}

data "azurerm_client_config" "this" {}

data "azurerm_key_vault" "this" {
  name = local.key_vault_name
  resource_group_name = local.resource_group_name
}

data "azurerm_key_vault_secret" "dropbox_app_keyvault_secret" {
  name         = local.dropbox_app_token_secret_name
  key_vault_id = data.azurerm_key_vault.this.id
}

data "azurerm_key_vault_secret" "dropbox_refresh_token_keyvault_secret" {
  name         = local.dropbox_refresh_token_secret_name
  key_vault_id = data.azurerm_key_vault.this.id
}

data "azurerm_key_vault_secret" "slack_bot_token" {
  name         = local.slack_bot_token
  key_vault_id = data.azurerm_key_vault.this.id
}

data "azurerm_key_vault_secret" "slack_app_token" {
  name         = local.slack_app_token
  key_vault_id = data.azurerm_key_vault.this.id
}

resource "azuread_application" "this" {
  display_name     = "azuread-app-spcvbia-streamlit"
  # "oauth2AllowIdTokenImplicitFlow": true,
  # https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/~/Manifest/appId/6159b30e-4413-497b-bd20-95356e6ffd6e
}

resource "azurerm_service_plan" "streamlit" {
  name                = "spcvbia-streamlit"
  resource_group_name = local.resource_group_name
  location            = local.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "streamlit" {
  name                = local.webapp_name_streamlit
  resource_group_name = local.resource_group_name
  location            = local.location
  service_plan_id     = azurerm_service_plan.streamlit.id

  app_settings = {
    WEBSITES_PORT : 80,
    WEBSITES_CONTAINER_START_TIME_LIMIT : 1800,
    DOCKER_ENABLE_CI : true,
    DROPBOX_APP_KEY: data.azurerm_key_vault_secret.dropbox_app_keyvault_secret.value,
    DROPBOX_REFRESH_TOKEN: data.azurerm_key_vault_secret.dropbox_refresh_token_keyvault_secret.value
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
      docker_image     = var.docker_image_streamlit
      docker_image_tag = "latest"
    }
  }

  auth_settings_v2  {
    auth_enabled           = true
    unauthenticated_action = "Return401"
    require_authentication = true
    require_https          = true
    # default_provider = "aad"

    active_directory_v2  {
        client_id = azuread_application.this.application_id
        client_secret_setting_name = "AzureAdClientSecret" # This should be allowed optional
        tenant_auth_endpoint = "https://login.microsoftonline.com/${data.azurerm_client_config.this.tenant_id}"
    }
    
    login {
        token_store_enabled = true
    }
  }
}

resource "azurerm_service_plan" "slackbot" {
  name                = "spcvbia-slackbot"
  resource_group_name = local.resource_group_name
  location            = local.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "slackbot" {
  name                = local.webapp_name_slackbot
  resource_group_name = local.resource_group_name
  location            = local.location
  service_plan_id     = azurerm_service_plan.slackbot.id

  app_settings = {
    WEBSITES_PORT : 8000,
    WEBSITES_CONTAINER_START_TIME_LIMIT : 1800,
    DOCKER_ENABLE_CI : true,
    DROPBOX_APP_KEY: data.azurerm_key_vault_secret.dropbox_app_keyvault_secret.value,
    DROPBOX_REFRESH_TOKEN: data.azurerm_key_vault_secret.dropbox_refresh_token_keyvault_secret.value,
    SLACK_BOT_TOKEN: data.azurerm_key_vault_secret.slack_bot_token.value,
    SLACK_APP_TOKEN: data.azurerm_key_vault_secret.slack_app_token.value
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
      docker_image     = var.docker_image_slackbot
      docker_image_tag = "latest"
    }
  }
}
