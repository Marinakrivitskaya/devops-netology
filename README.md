# devops-netology
Andrey Krylov
05/07/2020



7.1. Инфраструктура как код  https://github.com/syatihoko/devops-netology/blob/master/HomeWorks2/11-11-terraform-07-01-intro.md

13-terraform-07-03-basic.md  https://github.com/syatihoko/devops-netology/blob/master/HomeWorks2/13-terraform-07-03-basic.md
14-terraform-07-04-teamwork.md   https://github.com/syatihoko/devops-netology/blob/master/HomeWorks2/14-terraform-07-04-teamwork.md
15_Введение в Golang.md    https://github.com/syatihoko/devops-netology/blob/master/HomeWorks2/15_%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B2%20Golang.md
16-terraform-07-06-provider.md    https://github.com/syatihoko/devops-netology/blob/master/HomeWorks2/16-terraform-07-06-provider.md
https://learn.hashicorp.com/collections/terraform/providers
https://github.com/syatihoko/my_terraform-providr-hashicups/tree/boilerplate/hashicups












##Git ignored files in Root Directory

    logs/
    + standard set of rules
    #/**.*.log #Ignore logs-files in root dir. and in subdirs.
    .idea/  #Pycharm files

##Git ignored files in Directory terraform:

    All files in subdirectories /.terraform/ (**/.terraform/*)
    *.tfstate
    *.tfstate.*
    crash.log
    override.tf
    override.tf.json
    *_override.tf
    *_override.tf.json
    .terraformrc
    terraform.rc
    
