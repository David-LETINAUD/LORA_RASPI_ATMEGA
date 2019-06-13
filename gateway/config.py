# Lecture fichier config.cfg

import configparser # Permet de parser le fichier de parametres

# https://www.quennec.fr/trucs-astuces/langages/python/python-utiliser-un-fichier-de-param%C3%A8tres

config = configparser.RawConfigParser() # On créé un nouvel objet "config"
config.read('config.cfg') # On lit le fichier de paramètres

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
