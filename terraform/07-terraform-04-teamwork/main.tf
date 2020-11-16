provider "aws" {
  region = "eu-west-3"
}

//ищем самый новый образ ubuntu
data "aws_ami" "aws_ubuntu" {

  most_recent = true

  owners = [
    "amazon"]

  filter {
    name = "name"
    values = [
      "*ubuntu*"]
  }
}