//переменная типа Instance зависимая от текущего workspace
//locals {
//  ubuntu_instance_workspace_type_map = {
//    stage = "t3.nano"
//    prod = "t2.micro"
//    default = "t2.micro"
//  }
//}
//
////переменная кол-ва Instance зависимая от текущего workspace
//locals {
//  ubuntu_instance_workspace_count_map = {
//    //stage = "t3.nano"
//    stage = 1
//    prod = 0
//    default = 0
//  }
//}
//
//
//locals {
//  ubuntu_instance_workspace_states_map = {
//    stage = 0
//    prod = 0
//    default = 1
//  }
//}
//
////переменная имени группы от текущего workspace
//locals {
//  ubuntu_instance_workspace_group_map = {
//    stage = "Group_stage"
//    prod = "Group_prod"
//    default = "Group_default"
//  }
//}
//
//
//
//// Перечень security_group VPC для каждого workspace
//locals {
//  ubuntu_instance_workspace_sgvpc__map = {
//    stage = "sg-vpcid-stage"
//    prod = "sg-vpcid-prod"
//    default = "sg-vpcid-default"
//  }
//}
