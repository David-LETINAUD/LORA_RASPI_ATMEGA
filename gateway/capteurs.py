# -*- coding: utf-8 -*
from log_files import logger_info, logger_warning
from heat_index import heat_index
from config import param_mysql,temp_table

import MySQLdb as mysql


MY_SERVER_ADDRESS=0 # de 0 a 9

# Gestion base de donnees
temp_map_query = "INSERT INTO {} (TEMP_numero,TEMP_name, TEMP_temp, TEMP_hum, TEMP_tension,TEMP_T_ressentie ) VALUES(%s, %s, %s, %s, %s, %s)".format(temp_table)

db = mysql.connect(**param_mysql)        # name of the database
cur = db.cursor()


def insert_db(query,values):
 try:
  print("Execute")
  cur.execute(query,values)
  print("Commit")
  db.commit()
  print("Insert end")
  #print(cur.rowcount, "record inserted")
  # Gestion position des capteurs
 except:
  s=sys.exc_info()[0]
  print("Error database insertion : ",s)
  logger_warning.warning('insert_db : {}'.format(s))
 

class Temp_sensor_class:
  
  def __init__(self, num, nm):
    self.numero = num
    self.name = nm
    self.ack = 0
    self.time_cycle=0

            
capteurs = {1:Temp_sensor_class(1,"IT"),
            2:Temp_sensor_class(2,"quai expedition"),
            3:Temp_sensor_class(3,"zone dechets"),
            4:Temp_sensor_class(4,"quai reception"),
            5:Temp_sensor_class(5,"prepa expedition"),
            6:Temp_sensor_class(6,"SAV"),
            7:Temp_sensor_class(7,"zone magasin"),
            8:Temp_sensor_class(8,"retour SAV"),
            9:Temp_sensor_class(9,"Emballage"),            
            11:Temp_sensor_class(11,"Acceuil"),
            12:Temp_sensor_class(12,"RD"),
            13:Temp_sensor_class(13,"qualite"),
            14:Temp_sensor_class(14,"HR"),
            15:Temp_sensor_class(15,"ADV"),
            16:Temp_sensor_class(16,"salle bleue"),            
            18:Temp_sensor_class(18,"Achats"),
            19:Temp_sensor_class(19,"vestiaires")
            }
 
 
def Temp_sensor_packet(msg):
 tab = msg.split()
 numero = int(tab[0])
 temp = float(tab[1])
 hum = float(tab[2])
 vbat = float(tab[3])

 ressentie = heat_index(temp, hum)
 
 if numero in capteurs:
 
   values = ( numero,capteurs[numero].name, temp, hum, vbat,ressentie)
   print("numero : {} name : {} temp : {} hum : {} vbat : {} HI : {}".format(numero,capteurs[numero].name, temp, hum, vbat,ressentie))

   # Si valeur improbable : trame corrompu rendre code erreur
   if numero < 0 or numero > 255:
    print("num error")
    logger_info.info("Erreur numero (out of range) : {}".format(numero))
    return -1
   elif vbat < 0 or vbat > 10:
    print("vbat error")
    logger_info.info("Erreur tension batterie (out of range) : {}".format(vbat))
    return -2
   elif hum < 0 or hum > 100:
    print("hum error")
    logger_info.info("Erreur humidité (out of range) : {}".format(hum))
    return -3
   elif temp < -50 or vbat > 99:
    print("temp error")
    logger_info.info("Erreur température (out of range) : {}".format(temp))
    return -4

   # Commande SQL
   #print (capteurs[numero].ack )
   
   # Pas d erreur
   # Si recu et enregistrer dans la BDD alors
   if capteurs[numero].ack == 0:
    insert_db(temp_map_query,values)
    # Pas d erreur
    # Si recu et enregistrer dans la BDD alors
    capteurs[numero].ack = 1
   else:
    logger_info.info("Capteur temperature n°{} : envois multiples dans un cycle => Verifier periode d acquisition du capteur OU mauvaise reception de l aquitement (verifier antenne)".format(numero))
   #print (capteurs[numero].ack )
 else:
    logger_info.info("Capteur temperature n°{} non enregistre".format(numero))
 return numero
 
