locals {
  resource_group_name = data.azurerm_resource_group.this.name
  location            = var.location == null ? data.azurerm_resource_group.this.location : var.location
  webapp_name         = "wa-cvbia-slackbot"
  key_vault_id = "kvwebappslackbot"
  dropbox_app_token_secret_name = "dropbox_app"
  dropbox_refresh_token_secret_name = "dropbox_refresh_token"
}
