variable "region" {
  type      = string
  sensitive = true
}

variable "AZ" {
  type      = string
  sensitive = true
}

variable "server_ami" {
  type      = string
  sensitive = true
}

variable "vpc_cidr" {
  type      = string
  sensitive = true
}

variable "public_subnet_cidr" {
  type      = string
  sensitive = true
}

variable "private_subnet_cidr" {
  type      = string
  sensitive = true
}

variable "key_name" {
  type      = string
  sensitive = true
}

variable "api_instance_type" {
  type      = string
  sensitive = true
}

variable "api_ssh_allow" {
  type      = string
  sensitive = true
}

variable "token" {
  type      = string
  sensitive = true
}

variable "public_dns" {
  type      = string
  sensitive = true
}