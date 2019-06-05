#!/usr/bin/env python
# -*- coding: utf-8 -*

import signal
import sys
import _thread
import time
import configparser # Permet de parser le fichier de parametres
import serial_rx_tx # Serial port
import MySQLdb as mysql# Database

# https://www.quennec.fr/trucs-astuces/langages/python/python-utiliser-un-fichier-de-param%C3%A8tres

MY_SERVER_ADDRESS=0 # de 0 à 9

config = configparser.RawConfigParser() # On créé un nouvel objet "config"
config.read('config.cfg') # On lit le fichier de paramètres

serialPort = serial_rx_tx.SerialPort()
serialPort.Send("test\n")

# Récupération CONFIG SERIAL
port = config.get('SERIAL','port')
baudrate = config.get('SERIAL','baudrate')
bytesize = config.get('SERIAL','bytesize')
parity = config.get('SERIAL','parity')
stopbits = config.get('SERIAL','stopbits')

# Récupération CONFIG DATABASE
param_db = {
    'host'   : config.get('DATABASE','host'),
    'user'   : config.get('DATABASE','user'),
    'passwd' : config.get('DATABASE','passwd'),
    'db'     : config.get('DATABASE','db')
}
temp_table = config.get('DATABASE','temp_table')
temp_query = "INSERT INTO {} (capteur, temp, hum, tension) VALUES(%s, %s, %s, %s)".format(temp_table)

db = mysql.connect(**param_db)        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
#cur.execute("SHOW TABLES")
#print(cur.fetchall())

# Lors de la fermeture du programme
def fermer_prog(signal,frame):
 serialPort.Close()
 db.close()
 sys.stdout.flush()
 print("Exit")
 sys.exit(0)

signal.signal(signal.SIGINT, fermer_prog)

def insert_db(query,values):
 cur.execute(query,values)
 db.commit()
 #print(cur.rowcount, "record inserted")

def Temp(msg):
 tab = msg.split()
 capteur = int(tab[0])
 temp = float(tab[1])
 hum = float(tab[2])
 vbat = float(tab[3])
 values = ( capteur, temp, hum, vbat)
 print("capteur : {} temp : {} hum : {} vbat : {}".format(capteur, temp, hum, vbat))

 # Si valeur improbable : trame corrompu rendre code erreur
 if capteur < 0 or capteur > 255:
  return 1
 elif vbat < 0 or vbat > 10:
  return 2
 elif hum < 0 or hum > 100:
  return 3
 elif temp < -50 or vbat > 99:
  return 4

 # Commande SQL
 insert_db(temp_query,values)
 # Pas d'erreur
 return 0
 
 
def Analyse_Trames(m):
 r = -1
 capteur_type = m[1:3]
 addr_capt = m[3]
 if m[0]==str(MY_SERVER_ADDRESS):
  print("Server addr")   
  #Pour capteur température "TH"
  if capteur_type=="TH":
   r = Temp(m[3:])   
  # Pour autres capteurs
  # ...
  
 if r==-1 :
   print(m)
   
 elif r == 0:
  print("OK")
  #Envoie d'un acquittement si recu et pas d'erreurs
  serialPort.Send("{}{}{} A".format(addr_capt,capteur_type,MY_SERVER_ADDRESS))
 elif r!=1:
  #Si erreurs : demande de renvoie
  print("erreur")
  serialPort.Send("{}{}{} E".format(addr_capt,capteur_type,MY_SERVER_ADDRESS))
 

# serial data callback function
def OnReceiveSerialData(message):
 str_message = message.decode("utf-8")
 #print(str_message)
 Analyse_Trames(str_message)

# Ouverture du port de communication série avec l'arduino
serialPort.Open(port,baudrate,bytesize,parity,stopbits)
# Register the callback above with the serial port object
serialPort.RegisterReceiveCallback(OnReceiveSerialData)

print("START")
while 1:
 #x=serialPort.readline()
 #print(x)
 time.sleep(10) 



 
