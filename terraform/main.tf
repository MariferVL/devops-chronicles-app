terraform {
  required_version = ">= 1.11.2"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.91"
    }
  }

}

provider "aws" {
  region = var.aws_region
}

resource "aws_ssm_parameter" "db_host" {
  name  = "/devops/DB_HOST"
  type  = "String"
  value = var.db_host
  overwrite = true
}

resource "aws_ssm_parameter" "db_user" {
  name  = "/devops/DB_USER"
  type  = "String"
  value = var.db_user
  overwrite = true
}

resource "aws_ssm_parameter" "db_pass" {
  name  = "/devops/DB_PASS"
  type  = "SecureString"
  value = var.db_pass
  overwrite = true
}

resource "aws_ssm_parameter" "db_name" {
  name  = "/devops/DB_NAME"
  type  = "String"
  value = var.db_name
  overwrite = true
}

resource "aws_ssm_parameter" "db_root_pass" {
  name  = "/devops/DB_ROOT_PASS"
  type  = "SecureString"
  value = var.db_root_pass
  overwrite = true
}

resource "aws_ssm_parameter" "flask_env" {
  name  = "/devops/FLASK_ENV"
  type  = "String"
  value = var.flask_env
  overwrite = true
}

resource "aws_security_group" "devops_sg" {
  name        = "devops-sg"
  description = "Allow SSH, App and DB traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "devops_rds" {
  allocated_storage      = var.rds_allocated_storage
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"
  db_name                   = var.db_name
  username               = var.db_user
  password               = var.db_pass
  parameter_group_name   = "default.mysql8.0"
  skip_final_snapshot    = true
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.devops_sg.id]
  storage_type = "gp3"
}

resource "aws_key_pair" "devops_key" {
  key_name   = "devops-key"
  public_key = var.pub_key_content
}

resource "aws_instance" "devops_instance" {
  ami                    = "ami-04b4f1a9cf54c11d0"
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.devops_key.key_name
  security_groups        = [aws_security_group.devops_sg.name]

  tags = {
    Name = "DevOpsChroniclesInstance"
  }
}

output "instance_public_ip" {
  value = aws_instance.devops_instance.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.devops_rds.address
}
