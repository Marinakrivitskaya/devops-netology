provider "aws" {
  region = "eu-west-3"
}

terraform {
  backend "s3" {
    bucket = "kaa2-terraform-states"
    key = "main-infra/terraform.tfstate"
    region = "eu-west-3"
    //dynamodb_table = "terraform-locks"
  }
}


module "ec2" {
  source = "./modules/ec2"

}