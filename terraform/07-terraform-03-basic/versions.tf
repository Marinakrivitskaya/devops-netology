terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}


#s3_bucket для хранения backend s3
resource "aws_s3_bucket" "kaa-terraform-states" {
  bucket = "kaa-terraform-states"
  acl = "private"

  tags = {
    Name = "Terraform-states"
    Environment = "Test"
  }
}


terraform {
  backend "s3" {
    bucket = "kaa-terraform-states"
    key = "main-infra/terraform.tfstate"
    region = "eu-west-3"
  }
}


//
//data "terraform_remote_state" "network" {
//  backend = "s3"
//  config = {
//    bucket = "terraform-state-prod"
//    key    = "network/terraform.tfstate"
//    region = "eu-west-3"
//  }
//}



//
//Создайте s3 бакет, iam роль и пользователя от которого будет работать терраформ.
//Можно создать отдельного пользователя, а можно использовать созданного в рамках предыдущего задания,
//просто добавьте ему необходимы права, как описано здесь.
//https://www.terraform.io/docs/backends/types/s3.html
//Зарегистрируйте бэкэнд в терраформ проекте как описано по ссылке выше.




//terraform {
//  backend "s3" {
//    bucket = "mybucket"
//    key    = "path/to/my/key"
//    region = "us-east-1"
//  }
//}
//
//terraform import aws_iam_policy.Terraform_policy  arn:aws:iam::250629965860:policy/Terraform_policy
//terraform import aws_iam_policy.administrator  arn:aws:iam::250629965860:policy UsersManageOwnCredentials

//Задача 2. Инициализируем проект и создаем воркспейсы.
//Выполните terraform init:
//если был создан бэкэнд в S3, то терраформ создат файл стейтов в S3 и запись в таблице dynamodb.
//иначе будет создан локальный файл со стейтами.
//Создайте два воркспейса stage и prod.
//В уже созданный aws_instance добавьте зависимость типа инстанса от вокспейса, что бы в разных ворскспейсах использовались разные instance_type.
//Добавим count. Для stage должен создаться один экземпляр ec2, а для prod два.
//Создайте рядом еще один aws_instance, но теперь определите их количество при помощи for_each, а не count.
//Что бы при изменении типа инстанса не возникло ситуации, когда не будет ни одного инстанса добавьте параметр жизненного цикла create_before_destroy = true в один из рессурсов aws_instance.
//При желании поэкспериментируйте с другими параметрами и рессурсами.
//В виде результата работы пришлите:
//
//Вывод команды terraform workspace list.
//Вывод команды terraform plan для воркспейса prod.