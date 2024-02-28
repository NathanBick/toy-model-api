# Azure provider
provider "azurerm" {
  features{}
}

# Resource group
resource "azurerm_resource_group" "rg" {
  name     = "rg-terraform"
  location = "East US"
}

# netwrk security group
resource "azurerm_network_security_group" "examplesg" {
  name                = "example-security-group"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# virtual network
resource "azurerm_virtual_network" "examplevnet" {
  name                = "example-network"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "examplesubnet" {
  name                 = "example-subnetn"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.examplevnet.name
  address_prefixes     = ["10.0.2.0/24"]
  service_endpoints    = ["Microsoft.Sql", "Microsoft.Storage"]
}


# Azure storage account
resource "azurerm_storage_account" "sa" {
  name                     = "storageterraformtest"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  # disable the blob public access
  enable_https_traffic_only = true
  is_hns_enabled            = true

  network_rules {
    default_action             = "Deny"
    ip_rules                   = ["100.0.0.1"]
    virtual_network_subnet_ids = [azurerm_subnet.examplesubnet.id]
  }

}