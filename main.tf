provider "aws" {
  region  = "us-east-1"
}
terraform {
  backend "s3" {
    key = "terraform.tfstate"
    bucket = "vakar-dogs-config"
    region = "us-east-1"
    encrypt = "true"
  }
}
