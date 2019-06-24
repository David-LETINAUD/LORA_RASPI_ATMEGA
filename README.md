# LORA_RASPI_ATMEGA
## Installation
### Environnement python
sudo apt-get install python  
sudo apt-get install python-configparser  
sudo apt-get install python-mysqldb
sudo apt-get install python-pymssql


### Installation serveur mysql et phpmyadmin
https://raspbian-france.fr/installer-serveur-web-raspberry-lamp/
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
