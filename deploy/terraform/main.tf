terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "aetheria-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default = "us-east-1"
}

variable "cluster_name" {
  default = "aetheria-prod"
}

variable "db_password" {
  sensitive = true
}

# VPC
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  name    = "aetheria-vpc"
  cidr    = "10.0.0.0/16"
  azs     = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  enable_nat_gateway = true
  single_nat_gateway = false
}

# EKS Cluster
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = "1.29"
  subnet_ids      = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  eks_managed_node_groups = {
    main = {
      desired_size = 3
      max_size     = 15
      min_size     = 2
      instance_types = ["m5.xlarge"]
      labels = {
        role = "aetheria"
      }
    }
    compute = {
      desired_size = 2
      max_size     = 10
      min_size     = 1
      instance_types = ["c5.2xlarge"]
      labels = {
        role = "compute"
      }
      taints = [{
        key    = "dedicated"
        value  = "compute"
        effect = "NO_SCHEDULE"
      }]
    }
  }
}

# RDS PostgreSQL
resource "aws_db_instance" "main" {
  identifier     = "aetheria-postgres"
  engine         = "postgres"
  engine_version = "16"
  instance_class = "db.r5.large"
  allocated_storage = 100
  db_name        = "aetheria"
  username       = "hermes"
  password       = var.db_password
  db_subnet_group_name = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  multi_az       = true
  backup_retention_period = 7
  skip_final_snapshot = true
}

resource "aws_db_subnet_group" "main" {
  name       = "aetheria-db-subnet"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_security_group" "rds" {
  name_prefix = "aetheria-rds-"
  vpc_id      = module.vpc.vpc_id
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = module.vpc.private_subnets_cidr_blocks
  }
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "aetheria-redis"
  engine              = "redis"
  engine_version      = "7.0"
  node_type           = "cache.r5.large"
  num_cache_nodes     = 2
  parameter_group_name = "default.redis7"
  port                = 6379
  subnet_group_name   = aws_elasticache_subnet_group.main.name
  security_group_ids  = [aws_security_group.redis.id]
}

resource "aws_elasticache_subnet_group" "main" {
  name       = "aetheria-redis-subnet"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_security_group" "redis" {
  name_prefix = "aetheria-redis-"
  vpc_id      = module.vpc.vpc_id
  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = module.vpc.private_subnets_cidr_blocks
  }
}

# S3 bucket for reports
resource "aws_s3_bucket" "reports" {
  bucket = "aetheria-reports-${data.aws_caller_identity.current.account_id}"
}

data "aws_caller_identity" "current" {}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "rds_endpoint" {
  value = aws_db_instance.main.endpoint
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.redis.cache_nodes[0].address
}
