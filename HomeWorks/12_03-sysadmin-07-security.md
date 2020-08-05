# Домашнее задание к занятию "3.7. Элементы безопасности информационных систем"


>1. Установите [Hashicorp Vault](https://learn.hashicorp.com/vault) в виртуальной машине Vagrant/VirtualBox.  

Дополнительно к стандартной инструкции на Ubunto 20:  
**#snap install vault  #потребовалось дополнительно после установки по инструкции** 
**#snap install jq  #apt install jq – предлагал нестабильную версию**  


>2. Запустить Vault-сервер в dev-режиме.  

**#vault server -dev**   
**#export VAULT_ADDR='http://127.0.0.1:8200'**  
**#export VAULT_TOKEN='s.5LGogjJTcokwJWwRIjw4orrd '**  


>3. Используя [PKI Secrets Engine](https://www.vaultproject.io/docs/secrets/pki), создайте Root CA и Intermediate CA.  
Обратите внимание на [дополнительные материалы](https://learn.hashicorp.com/vault/secrets-management/sm-pki-engine) по созданию CA в Vault, если с изначальной инструкцией возникнут сложности.


**#vault secrets enable pki**  

 Увеличиваем до 1 года мах. срок сертификата  
**#vault secrets tune -max-lease-ttl=8760h pki**   

Создаем корневой сертификат на 1 год  
**#vault write pki/root/generate/internal common_name=avia-example.com ttl=8760h > CA_cert.crt**  

**# openssl x509 -in CA_cert.crt -text**  
**# openssl x509 -in CA_intermediate.cert.pem -text**   

	
Конфигурируем корневой ЦС (CA) и список отзыва (CRL):  
**#vault write pki/config/urls \ **  

issuing_certificates="http://127.0.0.1:8200/v1/pki/ca" \   
crl_distribution_points="http://127.0.0.1:8200/v1/pki/crl"  

Включаем secrets engine для промежуточного сертификата и   
Настраиваем мах. срок действия ,   
**#vault secrets enable -path=pki_int pki**  
**#vault secrets tune -max-lease-ttl=8760h pki_int**  

Создаем реквест для промежуточного сертификата:   
	#vault write -format=json pki_int/intermediate/generate/internal \  
common_name="avia-example.com Intermediate Authority" \  
| jq -r '.data.csr' > pki_intermediate.csr  

Обрабатываем реквест - подписываем промежуточный сертификат корневым:	
**#vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.csr format=pem_bundle ttl="8760h" |   jq -r '.data.certificate' > intermediate.cert.pem**

Импортируем его в хранилище
**#vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem**

>4. Согласно этой же инструкции, подпишите Intermediate CA csr на сертификат для любого тестового домена (`example.ru`).  


Создаем роль\ политику для выпуска сертификатов, говорим, что подписываться будут промежуточным сервером сертификации - pki_int     

 **#vault write pki_int/roles/avia-example-dot-com \ **         
        **allowed_domains="avia-example.com" \ **    
        **allow_subdomains=true \  **   
       ** max_ttl="4380h"**     

**# vault list pki_int/roles/**  

_ Keys   
avia-example-com_  

Выпускаем сертификат, подписываем промежуточным:   
**#vault write pki_int/issue/avia-example-dot-com common_name="web.avia-example.com" ttl="72h" > nginx.cert**   
	_…  
	serial_number       17:81:a3:fb:33:16:c9:b0:3e:1e:de:62:12:08:93:b6:74:6c:1c:63_  


>5. Поднимите на localhost nginx, сконфигурируйте default vhost для использования подписанного Vault Intermediate CA сертификата и выбранного вами домена. Сертификат из Vault подложить в nginx руками.


Руками из файла nginx.cert достал часть сертификата  и положил в web.avia-example.com.crt и часть приватного ключа и положил в web.avia-example.com.key
(хотя можно было разобрать _| tee_   
 _>(jq -r .data.certificate > ca.pem) \_  
 _>(jq -r .data.private_key > ca-key.pem)_  
 Уже потом увидел пример  
)

/etc/nginx/sites-enabled/
         listen 443 ssl default_server;
                listen [::]:443 ssl default_server;
         ssl_certificate /root/certs/web.avia-example.com.crt;
         ssl_certificate_key /root/certs/web.avia-example.com.key;

>6. Модифицировав `/etc/hosts` и [системный trust-store](http://manpages.ubuntu.com/manpages/focal/en/man8/update-ca-certificates.8.html), добейтесь безошибочной с точки зрения HTTPS работы curl на ваш тестовый домен (отдающийся с localhost).

etc/hosts
127.0.1.1<----->web.avia-example.com

**# curl https://web.avia-example.com**
curl: (60) SSL certificate problem: unable to get local issuer certificate
More details here: https://curl.haxx.se/docs/sslcerts.html




Подложил корневой  и промежуточный сертификат в хранилище доверенных. И обновил список.
**# ln -s /root/HCvault/CA_cert.crt /usr/local/share/ca-certificates/CA_cert.crt**
**#ln -s /root/HCvault/intermediate.cert.pem  /usr/local/share/ca-certificates/ intermediate.cert.crt**
**#update-ca-certificates --fresh**

**# curl https://web.avia-example.com**
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body { …


>7. Ознакомьтесь(https://letsencrypt.org/ru/docs/client-options/) с протоколом ACME и CA Let's encrypt. Если у вас есть во владении доменное имя с платным TLS-сертификатом, который возможно заменить на LE, или же без HTTPS вообще, попробуйте воспользоваться одним из предложенных клиентов, чтобы сделать веб-сайт безопасным (или перестать платить за коммерческий сертификат).  
Ознакомился

>8.Дополнительное задание вне зачета. Вместо ручного подкладывания сертификата в nginx, воспользуйтесь [Consul](https://medium.com/hashicorp-engineering/pki-as-a-service-with-hashicorp-vault-a8d075ece9a) для автоматического подтягивания сертификата из Vault.  

Получилось в точности по инструкции с учетом небольших корректировок по версии ОС. 

Это проигнорировал, 
_setopt – используется в  zsh,_

Не задолось с установкой Токена в root:
VAULT_UI=true vault server -dev -dev-root-token-id="root"
Сделал со сгенерированным сервером.

Также изменил:
**/etc/systemd/system/ consul-template.service**

__ [Unit]
Description=consul-template
Requires=network-online.target
After=network-online.target

[Service]
EnvironmentFile=-/etc/default/consul-template
Restart=on-failure
ExecStart=/usr/sbin/consul-template $OPTIONS -config='/etc/consul-template.d/pki-demo.hcl'
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target__

Также пока не добавил корневой и промежуточный сертификат получил ошибки. 
Не успел вызвать уже истек =), несколько секунд между вызовами. 
root@ubuntu20:/etc/nginx/certs# curl https://web.avia-example.com
<!DOCTYPE html>
<html>
<head>
….
root@ubuntu20:/etc/nginx/certs# curl https://web.avia-example.com
curl: (60) SSL certificate problem: certificate has expired
More details here: https://curl.haxx.se/docs/sslcerts.html

