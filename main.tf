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

}

data "azurerm_cosmosdb_mongo_database" "main" {
  name                = "todo_app"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = data.azurerm_cosmosdb_account.main.name

}

resource "azurerm_app_service_plan" "main" {
  name                = "${var.prefix}-todo-asp"
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
  name                = "${var.prefix}-todo-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|lachiexyz/todo-app:latest"
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "FLASK_APP"                  = var.FLASK_APP
    "MONGO_DB_CONNECTION"        = "mongodb://${data.azurerm_cosmosdb_account.main.name}:${data.azurerm_cosmosdb_account.main.primary_key}@${data.azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@${data.azurerm_cosmosdb_account.main.name}@"
    "MONGO_DB_NAME"              = "${data.azurerm_cosmosdb_mongo_database.main.name}"
    "LOGIN_DISABLED"             = var.LOGIN_DISABLED
    "AUTH_CLIENTID"              = var.AUTH_CLIENTID
    "AUTH_SECRET"                = var.AUTH_SECRET
    "AUTH_REDIRECT_URL"          = var.AUTH_REDIRECT_URL
    "AUTH_TOKEN_URL"             = var.AUTH_TOKEN_URL
    "AUTH_API_URL"               = var.AUTH_API_URL
    "APP_SECRET"                 = var.APP_SECRET
  }
}

