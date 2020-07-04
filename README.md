# devops-netology
Andrey Krylov
05/07/2020

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
    
