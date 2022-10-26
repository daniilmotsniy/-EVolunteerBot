resource "aws_vpc" "vpc_main" {
  cidr_block           = var.vpc_cidr
  instance_tenancy     = "default"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    "Name"    = "HelpServiceVPC"
    "Public"  = "true"
  }
}

resource "aws_subnet" "public" {
  availability_zone       = var.AZ
  vpc_id                  = aws_vpc.vpc_main.id
  cidr_block              = var.public_subnet_cidr
  map_public_ip_on_launch = true

  tags = {
    "Name"         = "HelpServicePublic"
    "Availability" = "Public"
  }
}

# resource "aws_subnet" "private" {
#   availability_zone       = var.AZ
#   vpc_id                  = aws_vpc.vpc_main.id
#   cidr_block              = var.private_subnet_cidr
#   map_public_ip_on_launch = false

#   tags = {
#     "Name"         = "HelpServicePrivate"
#     "Availability" = "Private"
#   }
# }

resource "aws_internet_gateway" "internet-gw" {
  vpc_id = aws_vpc.vpc_main.id

  tags = {
    Name = "internet-gw"
  }
}

resource "aws_route_table" "public-rt" {
  vpc_id = aws_vpc.vpc_main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet-gw.id
  }
}

resource "aws_route_table_association" "public-rta" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public-rt.id
}
