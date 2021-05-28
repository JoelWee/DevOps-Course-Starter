terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }

  backend "azurerm" {
    resource_group_name  = "SoftwirePilot_JoelWee_ProjectExercise"
    storage_account_name = "joelweetfstate"
    container_name       = "tfstate-container"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "${var.prefix}_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
  name                = "terraformed-asp"
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
  name                = "terraformed-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|j0elwee/devops-trg:latest"
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGO_URI"                  = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
    "OAUTH_CLIENT_ID"            = var.oauth_client_id
    "OAUTH_CLIENT_SECRET"        = var.oauth_client_secret
    "SECRET_KEY"                 = var.secret_key
    "LOGGLY_TOKEN"               = var.loggly_token
    "LOG_LEVEL" = "DEBUG"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "cosmosdb-account"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 10
    max_staleness_prefix    = 200
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }

  capabilities { name = "EnableMongo" }
  capabilities { name = "MongoDBv3.4" }
  capabilities { name = "EnableServerless" }
}


resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "cosmos-mongo-db"
  resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name

  lifecycle { prevent_destroy = true }
}
