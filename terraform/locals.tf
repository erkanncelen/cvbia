locals {
  resource_group_name   = data.azurerm_resource_group.this.name
  location              = var.location == null ? data.azurerm_resource_group.this.location : var.location
  
  webapp_name_streamlit = "wa-cvbia-streamlit"
  webapp_name_slackbot  = "wa-cvbia-slackbot"

  key_vault_name = "kv-cvbia"
  dropbox_app_token_secret_name = "dropbox-app-key"
  dropbox_refresh_token_secret_name = "dropbox-refresh-token"
  slack_bot_token = "slack-bot-token"
  slack_app_token = "slack-app-token"
}
