# Домашнее задание к занятию "3.4. Файловые системы"

>1. Узнайте о [sparse](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B7%D1%80%D0%B5%D0%B6%D1%91%D0%BD%D0%BD%D1%8B%D0%B9_%D1%84%D0%B0%D0%B9%D0%BB) (разряженных) файлах. 

Своими словами, файлы в которых для экономии места последовательности нулевых бит не записывается на диск, информация о размещениях данной последовательности хранится в метаданных файла (что требует поддержки со стороны ФС).

>2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?

Нет, не могут, так как они все ссылаются на один Inode, а метаданные «файла», в том числе и права доступа/владельцы хранятся в Inode.

>3. Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:
 
    ```bash
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-20.04"
      config.vm.provider :virtualbox do |vb|
        lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
        lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
        vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
        vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
      end
    end
    ``` 
> Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.

>4. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.

**# fdisk /dev/sdb**
_Command (m for help): n  
Partition type  
   p   primary (0 primary, 0 extended, 4 free)  
   e   extended (container for logical partitions)  
Select (default p): p  
Partition number (1-4, default 1): 1  
First sector (2048-5242879, default 2048):  
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242879, default 5242879): +2G  
Created a new partition 1 of type 'Linux' and of size 2 GiB._  

_Command (m for help): n  
Partition type  
   p   primary (1 primary, 0 extended, 3 free)  
   e   extended (container for logical partitions)  
Select (default p): p  
Partition number (2-4, default 2): 2  
First sector (4196352-5242879, default 4196352):  
Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242879, default 5242879):  
Created a new partition 2 of type 'Linux' and of size 511 MiB.  
Command (m for help): w  
The partition table has been altered.  
Calling ioctl() to re-read partition table.  
Syncing disks_.  


>5. Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.

**# sfdisk -d /dev/sdb | sfdisk /dev/sdc**   

>6. Соберите `mdadm` RAID1 на паре разделов 2 Гб.

**mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1**

>7. Соберите `mdadm` RAID0 на второй паре маленьких разделов.

**mdadm --create --verbose /dev/md1 --level=0 --raid-devices=2 /dev/sdb2 /dev/sdc2**

>8. Создайте 2 независимых PV на получившихся md-устройствах.

**pvcreate /dev/md0  
pvcreate /dev/md1**  


>9. Создайте общую volume-group на этих двух PV.

**vgcreate vg_01 /dev/md0 /dev/md1  
vgdisplay**  
_VG Name               vg_01_  


>10. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.

**lvcreate -L100 -n md0_1 vg_01 /dev/md1 
lvdisplay**
_LV Path                /dev/vg_01/md0_1 …_


>11. Создайте `mkfs.ext4` ФС на получившемся LV.

**mkfs.ext4 /dev/vg_01/md0_1  
blkid**  
_/dev/mapper/vg_01-md0_1: UUID="65f9ef9a-b1b2-4414-a31e-d3bdd5c93891" TYPE="ext4"_


>12. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.

**mkdir /tmp/new  
mount /dev/mapper/vg_01-md0_1 /tmp/new**  


>13. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.

**wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz.**

>14. Прикрепите вывод `lsblk`.

**NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT   
sda                    8:0    0   64G  0 disk    
├─sda1                 8:1    0  512M  0 part  /boot/efi  
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /  
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]  
sdb                    8:16   0  2.5G  0 disk  
├─sdb1                 8:17   0    2G  0 part  
│ └─md0                9:0    0    2G  0 raid1  
└─sdb2                 8:18   0  511M  0 part  
  └─md1                9:1    0 1018M  0 raid0  
    └─vg_01-md0_1    253:2    0  100M  0 lvm   /tmp/new  
sdc                    8:32   0  2.5G  0 disk  
├─sdc1                 8:33   0    2G  0 part  
│ └─md0                9:0    0    2G  0 raid1  
└─sdc2                 8:34   0  511M  0 part  
  └─md1                9:1    0 1018M  0 raid0  
    └─vg_01-md0_1    253:2    0  100M  0 lvm   /tmp/new**  


>15. Протестируйте целостность файла:


**# gzip -t /tmp/new/test.gz**  
**# echo $?**  
**0**

    
    
    

>16. Используя pvmove, переместите содержимое PV с RAID0 на RAID1.

**pvmove -n md0_1 /dev/md1 /dev/md0  
или  
pvmove /dev/md1 /dev/md0**  

Так как всего 2 тома, то последний аргумент /dev/md0 можно было не указывать  


>17. Сделайте `--fail` на устройство в вашем RAID1 md.

**mdadm --fail /dev/md0 /dev/sdb1**

>18. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.


[ 6243.423948] md/raid1:md0: Disk failure on sdb1, disabling device. 
               md/raid1:md0: Operation continuing on 1 devices.  



>19. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

**# gzip -t /tmp/new/test.gz**  
**# echo $?**  
**0**



