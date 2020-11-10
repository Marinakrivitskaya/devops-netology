locals {
  ubuntu_instance_names_map = {
    //stage = "t3.nano"
    ubuntu_new2_1 = "PC_For_Test"
    ubuntu_new2_2 = "PC_For_Use"
  }
}


//// создаем  Instance ubuntu 2 через for_each
resource "aws_instance" "ubuntu_new2" {

  //Создавать ресурсы до удаления
  lifecycle {
    create_before_destroy = true
  }


  // Для каждлого значения в local.ubuntu_instance_names_map
  //for_each = local.ubuntu_instance_names_map
  count = 0

  provider = aws
  ami = data.aws_ami.aws_ubuntu.id
  //instance_type = "t2.micro"
  //Значение типа от текущего workspace
  instance_type = local.ubuntu_instance_workspace_type_map
[terraform.workspace]
tags = {
//Для определение имени берем значение ключа из ubuntu_instance_names_map
//"Name" = each.key
//Для определение имени берем значение value из ubuntu_instance_names_map
//"GroupName" = each.value
}

//внешний IP нужен
associate_public_ip_address = true

//Зона доступности
availability_zone = "eu-west-3a"

//защитить от удаления
disable_api_termination = false

//Если true, дождитесь, пока данные пароля станут доступными, и получите их.
get_password_data = false

//Число IPv6-адресов, которые необходимо связать с основным сетевым интерфейсом
ipv6_address_count = 0
//укажите один или несколько IPv6-адресов из диапазона подсети, которые нужно связать с основным сетевым интерфейсом.
ipv6_addresses = []
//Если true, для запущенного экземпляра EC2 будет включен подробный мониторинг.
monitoring = false

//связанные группы безопасности.
security_groups = [
"default",
]
//Управляет маршрутизацией трафика к экземпляру, если адрес назначения не совпадает с экземпляром. Используется для NAT или VPN. По умолчанию true.
source_dest_check = true


// владение экземпляром (если экземпляр работает в VPC). Экземпляр с арендой выделенных запусков на однопользовательском оборудовании.
tenancy = "default"

//Кредитная спецификация экземпляра
credit_specification {
cpu_credits = "standard"

}

//Параметры Volume
root_block_device {
delete_on_termination = true
//iops = 100
//volume_size = 8
volume_type = "gp2"
}

}
