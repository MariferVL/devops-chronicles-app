variable "aws_region" {
  description = "The AWS region where the infrastructure will be deployed"
  type        = string
  default     = "us-east-1"
}

variable "db_host" {
  description = "Database host"
  type        = string
}

variable "db_user" {
  description = "Database user"
  type        = string
}

variable "db_pass" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "db_root_pass" {
  description = "Database root password"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "flask_env" {
  description = "Flask environment setting (e.g., production, development, staging)"
  type        = string
}

variable "rds_allocated_storage" {
  description = "Allocated storage for RDS (in GB)"
  type        = number
}

variable "pub_key_content" {
  description = "The content of the public SSH key"
  type        = string
}