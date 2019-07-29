# -*- coding: utf-8 -*

import signal
import time
import sys

import serial_rx_tx # Serial port

from log_files import logger_info, logger_warning
from config import port,baudrate,bytesize,parity,stopbits
from capteurs import *


logger_info.info("Gateway START")
logger_warning.warning("Gateway START")

ACK_OPTION = True       # RASPBERRY_1 renvoie acknoledge
#ACK_OPTION= False      # RASPBERRY_2 pas de renvoie acknoledge

# Lors de la fermeture du programme
def fermer_prog(signal,frame):
 try:
  serialPort.Close()
  db.close()
  sys.stdout.flush()
  #print("Exit")
 except:
  s=sys.exc_info()[0]
  print("Error closing gateway.py: ",s)
  logger_warning.warning('fermer_prog : {}'.format(s))
 finally:
  logger_info.info("Gateway STOP")
  logger_warning.warning("Gateway STOP")
  sys.exit(0)

signal.signal(signal.SIGINT, fermer_prog)

# ex de trame temperature : 0TH1 21.59 51.18 3.53
# 0 : @Server | "TH" : TYPE de capteur (Temp Hum) | 1 : @capteur | 21.59 : Temperature | 51.18 : Humidite | 3.53 : Tension batterie
def Analyse_Trames(m):
 numero_capt = -1
 capteur_type = m[1:3]
 
 if m[0]==str(MY_SERVER_ADDRESS):
  #Pour capteur temperature "TH"
  if capteur_type=="TH":
   numero_capt = Temp_sensor_packet(m[3:]) 
   #print("Temp_sensor_packet END")
  # Pour autres capteurs
  #if capteur_type=="PR":
  # ...
  
 #if r==-1 :
  # print(m)
   
 if numero_capt > 0:
  # Envoie d'un acquittement si recu et pas d erreurs
  
  #Si recu et enregistrer dans la BDD alors
  if ACK_OPTION :
   serialPort.Send("{} {} {} A".format(numero_capt,capteur_type,MY_SERVER_ADDRESS))
 elif numero_capt<0:
  #Si erreur : demande de renvoie
  if ACK_OPTION :
   serialPort.Send("{} {} {} E".format(numero_capt,capteur_type,MY_SERVER_ADDRESS))
   
 #print("Analyse_Trames END")
 

# A la réception d une trame
def OnReceiveSerialData(message):
 str_message = message.decode("utf-8")
 print(str_message) # Affiche la trame reçue
 Analyse_Trames(str_message)
 #print("OnReceiveSerialData END")


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
 #print("TIME CYCLE")

