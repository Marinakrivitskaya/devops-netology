//Используем модуль aws-vpc  https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest

module "ec2_cluster_test" {
  source = "terraform-aws-modules/ec2-instance/aws"
  version                = "~> 2.0"


  #instance_count         = local.ubuntu_instance_workspace_count_map[terraform.workspace]
  count                   = local.ubuntu_instance_workspace_count_map[terraform.workspace]

  name                   = "test_ubuntu_${count.index}"
  #name                   = "test_ubuntu_"

  ami                    = data.aws_ami.aws_ubuntu.id
  instance_type          = local.ubuntu_instance_workspace_type_map[terraform.workspace]

  monitoring             = false


  tags = {
   "Name"      = "test_ubuntu_${count.index}"
   "GroupName" = local.ubuntu_instance_workspace_group_map[terraform.workspace]
  }
 //внешний IP нужен
 associate_public_ip_address = true

 //защитить от удаления
 disable_api_termination = false

 #Обязательно задать
 subnet_id              = "subnet_id"


 //Число IPv6-адресов, которые необходимо связать с основным сетевым интерфейсом
 ipv6_address_count = 0
 //укажите один или несколько IPv6-адресов из диапазона подсети, которые нужно связать с основным сетевым интерфейсом.
 ipv6_addresses = []


 //Управляет маршрутизацией трафика к экземпляру, если адрес назначения не совпадает с экземпляром. Используется для NAT или VPN. По умолчанию true.
 source_dest_check = true

 // владение экземпляром (если экземпляр работает в VPC). Экземпляр с арендой выделенных запусков на однопользовательском оборудовании.
 tenancy = "default"


 volume_tags = {}


 //Параметры Volume
 root_block_device = []
}

