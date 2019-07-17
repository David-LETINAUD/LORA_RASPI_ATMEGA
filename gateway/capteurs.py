#
# -*- coding: utf-8 -*
from heat_index import *
from config import *
#import pymssql
import MySQLdb as mysql# Database
from collections import namedtuple


MY_SERVER_ADDRESS=0 # de 0 a 9

# Gestion base de donnees
temp_map_query = "INSERT INTO {} (TEMP_numero,TEMP_name, TEMP_temp, TEMP_hum, TEMP_tension,TEMP_T_ressentie ) VALUES(%s, %s, %s, %s, %s, %s)".format(temp_table)

db = mysql.connect(**param_mysql)        # name of the database
cur = db.cursor()

#cpt=0

def insert_db(query,values):
 cur.execute(query,values)
 db.commit()
 #print(cur.rowcount, "record inserted")
# Gestion position des capteurs

class Temp_sensor_class:
  numero = 0
  name = ""
  ack = 0
  time_cycle = 0
  
  def __init__(self, num, nm):
    self.numero = num
    self.name = nm


#Temp_sensor_type = namedtuple("Temp_sensor_type", "name ack")
# Capt_pos = namedtuple("Capt_pos", "name latitude longitude")
# 3:Temp_sensor_type("Reception", 45.964281,2.194614)
# Associations numeros <-> capteurs 
#capteurs = {1:Temp_sensor_type("IT", 0),
            #2:Temp_sensor_type("Expedition", 0),
            #3:Temp_sensor_type("Reception", 0)
            #}
            
capteurs = {1:Temp_sensor_class(1,"IT"),
            2:Temp_sensor_class(2,"quai expedition"),
            3:Temp_sensor_class(3,"aspiration"),
            4:Temp_sensor_class(4,"quai reception"),
            5:Temp_sensor_class(5,"prepa expedition"),
            6:Temp_sensor_class(6,"SAV"),
            7:Temp_sensor_class(7,"zone magasin"),
            8:Temp_sensor_class(8,"retour SAV"),
            9:Temp_sensor_class(9,"Emballage"),
            10:Temp_sensor_class(10,"Achats"),
            11:Temp_sensor_class(11,"Acceuil"),
            12:Temp_sensor_class(12,"RD"),
            13:Temp_sensor_class(13,"qualite"),
            14:Temp_sensor_class(14,"HR"),
            15:Temp_sensor_class(15,"ADV"),
            16:Temp_sensor_class(16,"magasin proto"),
            17:Temp_sensor_class(17,"vestiaires")
            }
 
 
def Temp_sensor_packet(msg):
 tab = msg.split()
 numero = int(tab[0])
 temp = float(tab[1])
 hum = float(tab[2])
 vbat = float(tab[3])
 
 #global cpt
 
 #if cpt==1:
  #numero=2
  #cpt=2
 #elif cpt==2:
  #numero=3
  #cpt=0
 #else :
  #cpt=1

 ressentie = heat_index(temp, hum)
 
 values = ( numero,capteurs[numero].name, temp, hum, vbat,ressentie)
 print("numero : {} name : {} temp : {} hum : {} vbat : {} HI : {}".format(numero,capteurs[numero].name, temp, hum, vbat,ressentie))

 # Si valeur improbable : trame corrompu rendre code erreur
 if numero < 0 or numero > 255:
  return -1
 elif vbat < 0 or vbat > 10:
  return -2
 elif hum < 0 or hum > 100:
  return -3
 elif temp < -50 or vbat > 99:
  return -4

 # Commande SQL
 print (capteurs[numero].ack )
 
 
 # Pas d erreur
 # Si recu et enregistrer dans la BDD alors
 if capteurs[numero].ack == 0:
  insert_db(temp_map_query,values)
  # Pas d erreur
  # Si recu et enregistrer dans la BDD alors
 capteurs[numero].ack = 1
 
 #print (capteurs[numero].ack )
 return numero
 
