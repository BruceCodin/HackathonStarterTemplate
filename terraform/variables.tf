# variables.tf - Variables for our terraform file 

# main.tf confirguration
variable "aws_region" {
  description = "AWS region for deploying resources"
  type        = string
  default     = "eu-west-2"
}

# rds.tf confirguration 
variable "db_identifier" {
  type    = string
  default = "tamagotchi-database"
}

variable "db_instance_class" {
  type    = string
  default = "db.t3.micro"
}

variable "db_name" {
  type    = string
  default = "tamagotchi"
}

variable "db_username" {
  type    = string
  default = "postgres"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "Master password for the DB"
}

variable "allocated_storage" {
  type    = number
  default = 20
}

variable "engine_version" {
  type    = string
  default = "16.2"
}

variable "db_port" {
  type    = number
  default = 5432
}

variable "subnet_group_name" {
  type    = string
  default = "hackathon-db-subnet-group"
}

variable "security_group_name" {
  type    = string
  default = "hackathon-db-public-sg"
}
