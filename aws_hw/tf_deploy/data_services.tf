terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "input_bucket" {
  bucket = var.input_bucket
  acl = "private"
  force_destroy = "true"

  tags = {
    Name = "Input bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket" "output_bucket" {
  bucket = var.output_bucket
  acl = "private"
  force_destroy = "true"

  tags = {
    Name = "Output bucket"
    Environment = "Dev"
  }
}

resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

resource "aws_security_group" "postgres_rds_security_group" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"

  ingress {
    description = "postgres"
    from_port   = 5432
    to_port     = 5432
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
    Name = "Allow connect to postgres"
  }
}

resource "aws_db_instance" "database" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "12.4"
  instance_class       = "db.t2.micro"
  name                 = var.db_name
  username             = var.db_username
  password             = var.db_password
  publicly_accessible  = "true"
  skip_final_snapshot  = "true"
  vpc_security_group_ids = ["sg-085b0da8f40f8d9c2"]
}

output "db_host" {
  value = aws_db_instance.database.endpoint
  description = "Database instance endpoint"
}
