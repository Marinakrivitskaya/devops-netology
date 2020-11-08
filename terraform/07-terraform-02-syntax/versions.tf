terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}


//В файле main.tf воспользуйтесь блоком data "aws_ami для поиска ami образа последнего Ubuntu.
//получаем: data.aws_ami.aws_ubuntu
data "aws_ami" "aws_ubuntu" {
  most_recent = true
  # самый новый
  owners = [
    "amazon"]

  filter {
    name = "name"
    values = [
      "*ubuntu*"]
  }
}

//В файле main.tf создайте рессурс ec2 instance. Постарайтесь указать как можно больше параметров для его определения. Минимальный набор параметров указан в первом блоке Example Usage, но желательно, указать большее количество параметров.
resource "aws_instance" "ubuntu_new" {
  provider = aws
  ami = data.aws_ami.aws_ubuntu.id
  instance_type = "t2.micro"
  tags = {
    "Name" = "test_ubuntu1"
    "ClusterName" = "test_Cluster1"
  }

  associate_public_ip_address = true
  //внешний IP нужен



  availability_zone = "eu-west-3a"
  //Зона доступности

  #ERROR: The t2.micro instance type does not support specifying CpuOptions.
  #cpu_core_count               = 1 //меняется, если поддерживается выбраным Type
  #cpu_threads_per_core         = 1
  disable_api_termination = false
  #защитить от удаления
  #ebs_optimized                = false  //если тип экземпляра оптимизирован по умолчанию, то нет необходимости устанавливать это, и нет никакого эффекта для его отключения.
  get_password_data = false
  //Если true, дождитесь, пока данные пароля станут доступными, и получите их.





  ipv6_address_count = 0
  //Число IPv6-адресов, которые необходимо связать с основным сетевым интерфейсом
  ipv6_addresses = []
  //укажите один или несколько IPv6-адресов из диапазона подсети, которые нужно связать с основным сетевым интерфейсом.
  monitoring = false
  #Если true, для запущенного экземпляра EC2 будет включен подробный мониторинг.
  //primary_network_interface_id = "eni-0f1ce5bdae258b015"  //ID primary_network  интерфейса экземпляра.
  //private_dns                  = "ip-172-31-61-141.ec2.internal"  //Частное DNS-имя, назначенное экземпляру. Может использоваться только внутри Amazon EC2 и доступен только в том случае, если вы включили имена хостов DNS для своего VP
  //private_ip                   = "172.31.61.141"   //Частный IP-адрес, присвоенный экземпляру.
  //public_dns                   = "ec2-54-166-19-244.compute-1.amazonaws.com"  //публичное DNS-имя, присвоенное экземпляру. Для EC2-VPC это доступно, только если вы включили DNS-имена хостов для своего VPC.
  //public_ip                    = "54.166.19.244"   //Общедоступный IP-адрес, присвоенный экземпляру, если применимо. ПРИМЕЧАНИЕ. Если вы используете aws_eip с вашим экземпляром, вам следует напрямую ссылаться на адрес EIP, а не использовать public_ip, поскольку это поле изменится после присоединения EIP.


  //связанные группы безопасности.
  security_groups = [
    "default",
  ]
  source_dest_check = true
  //Управляет маршрутизацией трафика к экземпляру, если адрес назначения не совпадает с экземпляром. Используется для NAT или VPN. По умолчанию true.
  //  subnet_id                    = "subnet-1facdf35"   #The VPC subnet ID.
  tenancy = "default"

  // владение экземпляром (если экземпляр работает в VPC). Экземпляр с арендой выделенных запусков на однопользовательском оборудовании.
  //  volume_tags                  = {}
  //  vpc_security_group_ids       = [   #The associated security groups in non-default VPC
  //       "sg-5255f429",
  //  ]

  credit_specification {
    cpu_credits = "standard"
    //Кредитная спецификация экземпляра
  }

  root_block_device {
    delete_on_termination = true
    iops = 100
    volume_size = 8
    volume_type = "gp2"
  }

}


//Данные идентификации
//https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity
data "aws_caller_identity" "current" {}

//Данные региона
//https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/regions
data "aws_region" "current" {}






