provider "aws" {
  region     = "us-east-1"
  access_key = "AKIA4CFLOWDEMO7Q3X9Z"
  secret_key = "cf/DEMOsecret9Qz3XvLm7Rt2Kp8Wn4Yb6Hd1Jf5Sg0"
}

resource "aws_s3_bucket" "settlements" {
  bucket = "cardflow-settlements-prod"
  acl    = "public-read"
}

resource "aws_security_group" "db" {
  name = "cardflow-db"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "cardflow" {
  identifier          = "cardflow-prod"
  engine              = "postgres"
  engine_version      = "11.5"
  instance_class      = "db.t3.medium"
  allocated_storage   = 100
  username            = "cardflow"
  password            = "Pa55w0rd-cardflow-prod"
  storage_encrypted   = false
  publicly_accessible = true
  skip_final_snapshot = true
  vpc_security_group_ids = [aws_security_group.db.id]
}
