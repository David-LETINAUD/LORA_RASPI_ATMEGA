# Lecture fichier config.cfg

import configparser # Permet de parser le fichier de parametres

# https://www.quennec.fr/trucs-astuces/langages/python/python-utiliser-un-fichier-de-param%C3%A8tres

config = configparser.RawConfigParser() # On cree un nouvel objet "config"
config.read('config.cfg') # On lit le fichier de parametres

# Recuperation CONFIG SERIAL
port = config.get('SERIAL','port')
baudrate = config.get('SERIAL','baudrate')
bytesize = config.get('SERIAL','bytesize')
parity = config.get('SERIAL','parity')
stopbits = config.get('SERIAL','stopbits')

# Recuperation CONFIG DATABASE
param_mysql = {
    'host'   : config.get('MYSQL','host'),
    'user'   : config.get('MYSQL','user'),
    'passwd' : config.get('MYSQL','passwd'),
    'db'     : config.get('MYSQL','db')
}
temp_table = config.get('MYSQL','table')


# Recuperation CONFIG MSSQL
param_mssql = {
    'host'   : config.get('MSSQL','host'),
    'user'   : config.get('MSSQL','user'),
    'password' : config.get('MSSQL','passwd'),
    'database'     : config.get('MSSQL','db')
}
mssql_table = config.get('MSSQL','table')
