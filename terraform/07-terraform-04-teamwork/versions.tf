terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}



terraform {
  backend "s3" {
    #count = local.ubuntu_instance_workspace_states_map[terraform.workspace]
    bucket = "kaa-terraform-states"
    key = "test-module/terraform.tfstate"
    region = "eu-west-3"
  }
}


