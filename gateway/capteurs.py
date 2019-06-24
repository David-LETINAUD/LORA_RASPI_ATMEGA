#
# -*- coding: utf-8 -*
from heat_index import *
from config import *
import pymssql
import MySQLdb as mysql# Database
from collections import namedtuple


MY_SERVER_ADDRESS=0 # de 0 a 9

# Gestion base de donnees
temp_map_query = "INSERT INTO {} (numero,name, temp, hum, tension,T_ressentie,latitude, longitude ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)".format(temp_table)
temp_sql_server_query = "INSERT INTO {} (TEMP_numero,TEMP_name, TEMP_temp, TEMP_hum, TEMP_tension,TEMP_T_ressentie ) VALUES".format(mssql_table)

db = mysql.connect(**param_mysql)        # name of the database
cur = db.cursor()

conn = pymssql.connect(**param_mssql)
curs = conn.cursor()

cpt=0

def insert_db(query,values):
 cur.execute(query,values)
 db.commit()
 #print(cur.rowcount, "record inserted")

def insert_mssql(query,values):
 print("insert_mssql")
 query = query + ' ('+",".join(map(str,values))+')'
 
 # print("QUERY : " + query)
 curs.execute(query)
 conn.commit()

# Gestion position des capteurs
Capt_pos = namedtuple("Capt_pos", "name latitude longitude")
# Associations numeros <-> capteurs 
capteurs = {1:Capt_pos("IT", 45.965073,2.195131),
            2:Capt_pos("Expedition", 45.964338,2.196025),
            3:Capt_pos("Reception", 45.964281,2.194614)
            }
 
 
def Temp_map(msg):
 tab = msg.split()
 numero = int(tab[0])
 temp = float(tab[1])
 hum = float(tab[2])
 vbat = float(tab[3])
 
 global cpt
 
 if cpt==1:
  numero=2
  cpt=2
 elif cpt==2:
  numero=3
  cpt=0
 else :
  cpt=1

 ressentie = heat_index(temp, hum)
 
 values = ( numero,capteurs[numero].name, temp, hum, vbat,ressentie,capteurs[numero].latitude,capteurs[numero].longitude)
 print("numero : {} name : {} temp : {} hum : {} vbat : {} HI : {} lat : {} long : {}".format(numero,capteurs[numero].name, temp, hum, vbat,ressentie,capteurs[numero].latitude,capteurs[numero].longitude ))

 # Si valeur improbable : trame corrompu rendre code erreur
 if numero < 0 or numero > 255:
  return 1
 elif vbat < 0 or vbat > 10:
  return 2
 elif hum < 0 or hum > 100:
  return 3
 elif temp < -50 or vbat > 99:
  return 4

 # Commande SQL
 insert_db(temp_map_query,values)
 # Pas d erreur
 return 0
 
 
def Temp_mssql(msg):
 tab = msg.split()
 numero = int(tab[0])
 temp = float(tab[1])
 hum = float(tab[2])
 vbat = float(tab[3])
 
 global cpt
 
 if cpt==1:
  numero=2
  cpt=2
 elif cpt==2:
  numero=3
  cpt=0
 else :
  cpt=1

 ressentie = heat_index(temp, hum)
 
 values = (numero,"'{}'".format(capteurs[numero].name), temp, hum, vbat,ressentie)

 print("numero : {} name : {} temp : {} hum : {} vbat : {} HI : {}".format(numero,capteurs[numero].name, temp, hum, vbat,ressentie))

 # Si valeur improbable : trame corrompu rendre code erreur
 if numero < 0 or numero > 255:
  return 1
 elif vbat < 0 or vbat > 10:
  return 2
 elif hum < 0 or hum > 100:
  return 3
 elif temp < -50 or vbat > 99:
  return 4

 # Commande SQL
 insert_mssql(temp_sql_server_query,values)
 # Pas d erreur
 return 0

