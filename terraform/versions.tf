terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

data "aws_ami" "aws_ubuntu" {
  most_recent = true
  owners = [
    "amazon"]

  filter {
    name = "name"
    values = [
      "Ubuntu"]


  }
}

//В файле main.tf воспользуйтесь блоком data "aws_ami для поиска ami образа последнего Ubuntu.
//В файле main.tf создайте рессурс ec2 instance. Постарайтесь указать как можно больше параметров для его определения. Минимальный набор параметров указан в первом блоке Example Usage, но желательно, указать большее количество параметров.
//Добавьте data-блоки aws_caller_identity и aws_region.

