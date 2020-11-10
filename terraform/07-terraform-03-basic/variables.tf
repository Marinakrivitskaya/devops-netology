//переменная типа Instance зависимая от текущего workspace
locals {
  ubuntu_instance_workspace_type_map = {
    //stage = "t3.nano"
    stage = "t3.micro"
    prod = "t2.micro"
    default = "t2.micro"
  }
}

//переменная кол-ва Instance зависимая от текущего workspace
locals {
  ubuntu_instance_workspace_count_map = {
    //stage = "t3.nano"
    stage = 1
    prod = 2
    default = 0
  }
}

//переменная имени группы от текущего workspace
locals {
  ubuntu_instance_workspace_group_map = {
    stage = "Group_stage"
    prod = "Group_prod"
    default = "Group_default"
  }
}


// В default создается политики и s3_backend,
// в остальных Workspace - это игнорируется
locals {
  ubuntu_instance_workspace_states_map = {
    stage = 0
    prod = 0
    default = 1
  }
}


// Перечень security_group VPC для каждого workspace
locals {
  ubuntu_instance_workspace_sgvpc__map = {
    stage = "sg-vpcid-stage"
    prod = "sg-vpcid-prod"
    default = "sg-vpcid-default"
  }
}
