# rds terraform set up

# Get the default VPC (Virtual Private Cloud) - Cohort 20 VPC
data "aws_vpc" "cohort_vpc" {
  id = "vpc-01b7a51a09d27de04"
}

# Get all subnets in the VPC - Cohort 20 Subnets
data "aws_subnets" "cohort_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.cohort_vpc.id]
  }
}

# Subnet group
resource "aws_db_subnet_group" "tamagotchi_subnet_group" {
  name       = var.subnet_group_name
  subnet_ids = data.aws_subnets.cohort_subnets.ids

  tags = {
    Name = var.subnet_group_name
  }
}

# Security group (PUBLIC)
resource "aws_security_group" "tamagotchi_db_sg" {
  name        = var.security_group_name
  description = "Allow PUBLIC PostgreSQL access (hackathon only)"
  vpc_id      = data.aws_vpc.cohort_vpc.id

  ingress {
    from_port   = var.db_port
    to_port     = var.db_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.security_group_name
  }
}


# RDS instance
resource "aws_db_instance" "hackathon_db" {
  identifier        = var.db_identifier
  engine            = "postgres"
  instance_class    = var.db_instance_class
  allocated_storage = var.allocated_storage
  storage_type      = "gp2"

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.tamagotchi_db_sg.id]
  db_subnet_group_name = aws_db_subnet_group.tamagotchi_subnet_group.name

  publicly_accessible  = true
  skip_final_snapshot  = true
  deletion_protection  = false
  apply_immediately    = true
  backup_retention_period = 0

  tags = {
    Name = var.db_identifier
  }
}

# Outputs
output "db_endpoint" {
  value       = aws_db_instance.hackathon_db.endpoint
  description = "The connection endpoint for the RDS instance"
}

output "db_name" {
  value       = aws_db_instance.hackathon_db.db_name
  description = "The database name"
}