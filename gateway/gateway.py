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

config = configparser.RawConfigParser() # On créé un nouvel objet "config"
config.read('config.cfg') # On lit le fichier de paramètres

serialPort = serial_rx_tx.SerialPort()

# Récupération CONFIG SERIAL
port = config.get('SERIAL','port')
baudrate = config.get('SERIAL','baudrate')
bytesize = config.get('SERIAL','bytesize')
parity = config.get('SERIAL','parity')
stopbits = config.get('SERIAL','stopbits')

# Récupération CONFIG DATABASE
paramMysql = {
    'host'   : config.get('MYSQL','host'),
    'user'   : config.get('MYSQL','user'),
    'passwd' : config.get('MYSQL','passwd'),
    'db'     : config.get('MYSQL','db')
}
db = mysql.connect(**paramMysql)        # name of the data base
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


def Temp(msg):
 tab = msg.split()
 capteur = int(tab[0])
 temp = float(tab[1])
 hum = float(tab[2])
 vbat = float(tab[3])
 values = ( capteur, temp, hum, vbat)
 print("capteur : {} temp : {} hum : {} vbat : {}".format(capteur, temp, hum, vbat))
 # Commande SQL
 query = "INSERT INTO Date_Temp_hum_tension (capteur, temp, hum, tension) VALUES(%s, %s, %s, %s)"
 cur.execute(query,values)
 db.commit()
 #print(cur.rowcount, "record inserted")
 
def Analyse_Trames(m):
 #Pour capteur température "TH"
 if m[:2]=="TH":
   Temp(m[2:])
 # Pour autres capteurs
 # ...
 else :
   print(m)


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



 
