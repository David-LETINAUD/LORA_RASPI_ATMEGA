#
from heat_index import *
from config import *
import MySQLdb as mysql# Database
from collections import namedtuple

MY_SERVER_ADDRESS=0 # de 0 à 9

# Gestion base de données
temp_query = "INSERT INTO {} (capteur, temp, hum, tension) VALUES(%s, %s, %s, %s)".format(temp_table)
temp_map_query = "INSERT INTO {} (capteur, temp, hum, tension,T_ressentie,latitude, longitude ) VALUES(%s, %s, %s, %s, %s, %s, %s)".format(temp_table)
db = mysql.connect(**param_db)        # name of the data base

cur = db.cursor()

def insert_db(query,values):
 cur.execute(query,values)
 db.commit()
 #print(cur.rowcount, "record inserted")


# Gestion position des capteurs
Capt_pos = namedtuple("Capt_pos", "latitude longitude")
IT_capt = Capt_pos(45.965039,2.195339)
Exp_capt = Capt_pos(45.964338,2.196025)
capteurs = {1:IT_capt, 2:Exp_capt}

# Fonctions traitement de trames
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
 
 
def Temp_map(msg):
 tab = msg.split()
 capteur = int(tab[0])
 temp = float(tab[1])
 hum = float(tab[2])
 vbat = float(tab[3])

 ressentie = heat_index(temp, hum)
 
 values = ( capteur, temp, hum, vbat,ressentie,capteurs[capteur].latitude,capteurs[capteur].longitude)
 print("capteur : {} temp : {} hum : {} vbat : {} HI : {} lat : {} long : {}".format(capteur, temp, hum, vbat,ressentie,capteurs[capteur].latitude,capteurs[capteur].longitude ))

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
 insert_db(temp_map_query,values)
 # Pas d'erreur
 return 0
