#!/usr/bin/env python3.5
# -*- coding: utf-8 -*

import signal
import time
import sys
import serial_rx_tx # Serial port


from config import *
from capteurs import *


# Lors de la fermeture du programme
def fermer_prog(signal,frame):
 serialPort.Close()
 db.close()
 sys.stdout.flush()
 print("Exit")
 sys.exit(0)

signal.signal(signal.SIGINT, fermer_prog)

# ex de trame temperature : 0TH1 21.59 51.18 3.53
# 0 : @Server | "TH" : TYPE de capteur (Temp Hum) | 1 : @capteur | 21.59 : Temperature | 51.18 : Humidite | 3.53 : Tension batterie
def Analyse_Trames(m):
 r = -1
 capteur_type = m[1:3]
 addr_capt = m[3]
 if m[0]==str(MY_SERVER_ADDRESS):
  #Pour capteur temperature "TH"
  if capteur_type=="TH":
   r = Temp_sensor_packet(m[3:]) 
  # Pour autres capteurs
  #if capteur_type=="PR":
  # ...
  
 #if r==-1 :
  # print(m)
   
 if r > 0:
  # Envoie d'un acquittement si recu et pas d erreurs
  
  #Si recu et enregistrer dans la BDD alors
  print (capteurs[r].ack )
  
  serialPort.Send("{}{}{} A".format(addr_capt,capteur_type,MY_SERVER_ADDRESS))
 elif r<0:
  #Si erreur : demande de renvoie
  serialPort.Send("{}{}{} E".format(addr_capt,capteur_type,MY_SERVER_ADDRESS))
 

# A la réception d une trame
def OnReceiveSerialData(message):
 str_message = message.decode("utf-8")
 print(str_message) # Affiche la trame reçue
 Analyse_Trames(str_message)


# Port serie
serialPort = serial_rx_tx.SerialPort()
# Ouverture du port de communication serie avec l arduino
serialPort.Open(port,baudrate,bytesize,parity,stopbits)
# Register the callback above with the serial port object
serialPort.RegisterReceiveCallback(OnReceiveSerialData)


print("START")
while 1:
 #x=serialPort.readline()
 #print("t")
 
 for key,value in capteurs.items():
  #print( key,value.ack, value.time_cycle )
  
  if (value.time_cycle==1):
    value.time_cycle=0
    value.ack=0
  elif (value.ack==1):
    value.time_cycle=1
    
 time.sleep(60)  # en secondes



 
