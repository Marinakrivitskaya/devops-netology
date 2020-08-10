# Домашнее задание к занятию "4.1. Командная оболочка Bash: Практические навыки"

>1. Есть скрипт:
```bash  
	a=1
	b=2
	c=a+b
	d=$a+$b
	e=$(($a+$b))
```
	
	* Какие значения переменным c,d,e будут присвоены?
	* Почему?


c=a+b, так как мы определили строку, не указав, что a и b переменные.  
d=1+2, опять строка состоящая из значений переменных и между ними символом +  
e=3, наша операция по сложению заключена в конструкцию $(( )), что указывает, что это выражение и переменные нужно рассматривать как числовые.  

	
	

>2. На нашем локальном сервере упал сервис и мы написали скрипт, который постоянно проверяет его доступность, записывая дату проверок до тех пор, пока сервис не станет доступным. В скрипте допущена ошибка, из-за которой выполнение не может завершиться, при этом место на Жёстком Диске постоянно уменьшается. Что необходимо сделать, чтобы его исправить:
  
```bash  
while ((1==1)       
do   
curl https://localhost:4757     
if (($? != 0))    
then   
date >> curl.log  
fi   
done   
``` 
  
	
1)В первой строчке пропущена правая кавычка.    
2)Лучше добавить информацию какой интерпретатор #!/usr/bin/env bash	    
3)Чтобы скрипт завершился нужно добавить в условие if     
then break      
4) date > curl.log   (если я правильно понял нам нужна только последняя дата, когда сайт ещё не работал)   
5)ещё можно в вывод curl https://localhost:4757 перенаправить в > /dev/null 2>&1    
	
	
>3. Необходимо написать скрипт, который проверяет доступность трёх IP: 192.168.0.1, 173.194.222.113, 87.250.250.242 и записывает результат в файл log. Проверять доступность необходимо пять раз для каждого узла.


```bash
 #!/usr/bin/env bash  

addr_list=("192.168.0.1" "173.194.222.113" "87.250.250.242") 
declare -i chk_site   
date >> curl.log   

for i in ${addr_list[@]}   
do    
    chk_site=0   
    ip_addr=$i   
    for j in {1..5}  
    do  
<------>curl --connect-timeout 2 $ip_addr > /dev/null 2>&1  
<------>if (($? == 0))  
<------>then  
<------>    let "chk_site += 1"  
<------>fi  
    done  
echo "Site $ip_addr: $chk_site out of 5 successful checks" >> curl.log  
done  
``` 


>4. Необходимо дописать скрипт из предыдущего задания так, чтобы он выполнялся до тех пор, пока один из узлов не окажется недоступным. Если любой из узлов недоступен - IP этого узла пишется в файл error, скрипт прерывается  


```bash
#!/usr/bin/env bash  

addr_list=("192.168.0.1" "173.194.222.113" "87.250.250.242")  
declare -i chk_site  
date >> curl.log  

while true  
do  
  
for i in ${addr_list[@]}  
do  
    chk_site=0  
    ip_addr=$i   
    for j in {1..5} 
    do  
<------>curl --connect-timeout 1 $ip_addr > /dev/null 2>&1  
<------>if (($? == 0))   
<------>then   
<------>    let "chk_site += 1"   
<------>else  
<------>    echo $ip_addr not available > error.log  
<------>    break 3 # break 3-loops  
<------>fi  
    done   
echo "Site $ip_addr: $chk_site out of 5 successful checks" >> curl.log   
done    

done   
``` 



>5. (Задание со звёздочкой) Мы хотим, чтобы у нас были красивые сообщения для коммитов в репозиторий. Для этого нужно написать локальный хук для git, который будет проверять, что сообщение в коммите содержит код текущего задания в квадратных скобках и количество символов в сообщении не превышает 30. Пример сообщения: \[04-script-01-bash\] сломал хук

Используем хук commit-msg  

```bash
message_file=$1  
#echo message_file = $message_file  

##result=$(grep -c -E '^(\[)[A-Za-z0-9.,!?:…-]{1,30}(\])$' $message_file)   
result=$(grep -c -E '^(\[04-script-01-bash])[A-Za-z0-9.,!?:…-]{0,30}' $message_file)   
#echo result = $result   

if ((result == 1))   
then   
    echo [GIT_POLICY] Ok   
    exit 0   
else   
    echo [GIT_POLICY] Your message is not formatted correctly     
    exit 1   
fi   
``` 


Тестирование:  
 
 #git commit -m "\[04-script-01-bash\]"   
[GIT_POLICY] Your message is not formatted correctly   

 #git commit -m "04-script-01-bash"   
[GIT_POLICY] Your message is not formatted correctly   

 #git commit -m "[04-script-01-bash1111122222333334444455555]"   
[GIT_POLICY] Your message is not formatted correctly   

 #git commit -m "[04-script-01-bash]"  
[GIT_POLICY] Ok  
[master 0217194] [04-script-01-bash]  
 1 file changed, 1 insertion(+), 1 deletion(-)   
