# Azure provider
provider "azurerm" {
  features{}
}

# Resource group
resource "azurerm_resource_group" "rg" {
  name     = "rg-terraform"
  location = "East US"
}
