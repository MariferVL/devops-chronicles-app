variable "aws_region" {
  description = "The AWS region where the infrastructure will be deployed"
  type        = string
  default     = "us-east-1"
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

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "rds_allocated_storage" {
  description = "Allocated storage for RDS (in GB)"
  type        = number
}

variable "pub_key" {
  description = "Path to the public key file"
  type        = string
}