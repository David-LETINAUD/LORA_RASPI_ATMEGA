# LORA_RASPI_ATMEGA
## Installation
### Environnement python
sudo apt-get install python  
sudo apt-get install python-configparser  
sudo apt-get install python3-mysqldb  
sudo apt-get install python-pymssql

### Config ntp server
Dans le fichier : /etc/systemd/timesyncd.conf  
Ajouter l'adresse des serveurs ntp, dans le champ "NTP"

### Config proxy server
Dans le fichier : /etc/environment
export http_proxy="http://username:password@proxyipaddress:proxyport"  
export https_proxy="http://username:password@proxyipaddress:proxyport"  

### Installation serveur mysql et phpmyadmin 
sudo apt-get install apache2  
sudo apt-get install php    
sudo apt-get install mysql-server php-mysql  
sudo apt-get install phpmyadmin  
Activer mysqli :  
sudo phpenmod mysqli  
sudo /etc/init.d/apache2 restart  

Accès à distance à la base de donnée  
Dans : /etc/mysql/mariadb.conf.d/50-server.cnf  
Modifier : bind-address 127.0.0.1 en bind-address 0.0.0.0  
## Arduino_LORA_low_power_trame
### rf95_client.ino
Programme d'acquisition de mesures et envoie par communication Lora. A installer sur les modules capteurs.

### rf95_server.ino
Programme de réception et émission de trames Lora par le biais d'une connexion série. A installer sur l'arduino connecté au Raspberry pi.

## Gateway
Fichier config et programmes python pour le raspberry.
### gateway.py
Programme python pour réception des données et sauvegarde dans une base de donnée.
### config.cfg
Fichier de config des paramètres de communication série et de la base de donnée.
### serial_rx_tx.py
Classe SerialPort pour la gestion de la communication série.
### heat_index.py
Calcul de la témpérature ressentie.
### config.py
Récupération des paramètres de config.cfg.
### capteurs.py
Gestion des capteurs et extractions des infos et enregitrement dans base de données. 

## Schémas
### Schéma de principe
![alt text](https://github.com/David-LETINAUD/LORA_RASPI_ATMEGA/blob/master/Images/Schema_materiel.PNG)

### Connexion arduino <-> Lora
![alt text](https://github.com/David-LETINAUD/LORA_RASPI_ATMEGA/blob/master/Images/LoRa-com-Arduino-UNO.jpg)
