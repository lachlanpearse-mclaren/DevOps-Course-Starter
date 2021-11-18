terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }
}
provider "azurerm" {
  features {}
}
data "azurerm_resource_group" "main" {
  name = "McLaren1_LachlanPearse_ProjectExercise"
}

data "azurerm_cosmosdb_account" "main" {
  name                = "lp-projectexercise-db"
  resource_group_name = data.azurerm_resource_group.main.name
  capabilities { name = "EnableServerless" }
}

data "azurerm_cosmosdb_mongo_database" "main" {
  name                = "todo_app"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = data.azurerm_cosmosdb_account.main.name

}

resource "azurerm_app_service_plan" "main" {
  name                = "lp-unit12-project-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true
  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "main" {
  name                = "lp-unit12-projectexercise-todo"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|lachiexyz/todo-app:latest"
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "FLASK_APP"           = var.FLASK_APP
    "MONGO_DB_CONNECTION" = var.MONGO_DB_CONNECTION
    "MONGO_DB_NAME"       = var.MONGO_DB_NAME
    "LOGIN_DISABLED"      = var.LOGIN_DISABLED
    "AUTH_CLIENTID"       = var.AUTH_CLIENTID
    "AUTH_SECRET"         = var.AUTH_SECRET
    "AUTH_REDIRECT_URL"   = var.AUTH_REDIRECT_URL
    "AUTH_TOKEN_URL"      = var.AUTH_TOKEN_URL
    "AUTH_API_URL"        = var.AUTH_API_URL
    "APP_SECRET"          = var.APP_SECRET  
  }
}

