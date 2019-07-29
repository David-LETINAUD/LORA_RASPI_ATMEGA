# -*- coding: utf-8 -*
# Lecture fichier config.cfg

import configparser # Permet de parser le fichier de parametres
import os #Pour getcwd
# https://www.quennec.fr/trucs-astuces/langages/python/python-utiliser-un-fichier-de-param%C3%A8tres

pwd = os.getcwd()

config = configparser.RawConfigParser() # On cree un nouvel objet "config"

try:
 config.read(pwd+'/config.cfg') # On lit le fichier de parametres
except:
 s=sys.exc_info()[0]
 print("Error lecture config.cfg : ",s)
 logger_warning.warning('config.read : {}'.format(s))

try:
    # Recuperation CONFIG SERIAL
    port = config.get('SERIAL','port')
    baudrate = config.get('SERIAL','baudrate')
    bytesize = config.get('SERIAL','bytesize')
    parity = config.get('SERIAL','parity')
    stopbits = config.get('SERIAL','stopbits')
except:
    s=sys.exc_info()[0]
    print("Error lecture SERIAL config  : ",s)
    logger_warning.warning('config.get(SERIAL) : {}'.format(s))

try:
    # Recuperation CONFIG DATABASE
    param_mysql = {
        'host'   : config.get('MYSQL','host'),
        'user'   : config.get('MYSQL','user'),
        'passwd' : config.get('MYSQL','passwd'),
        'db'     : config.get('MYSQL','db')
    }
    temp_table = config.get('MYSQL','table')
except:
    s=sys.exc_info()[0]
    print("Error lecture MYSQL config  : ",s)
    logger_warning.warning('config.get(MYSQL) : {}'.format(s))
