# -*- coding: utf-8 -*
import logging
from logging.handlers import RotatingFileHandler
from config import pwd

# Gestion log file
formatter_warning = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
formatter_info = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")


try:
	logger_warning = logging.getLogger("warning_log")
	handler_warning= logging.handlers.RotatingFileHandler(pwd+"/log/warning.log", mode="a", maxBytes= 1000000, backupCount= 1 , encoding="utf-8")
	handler_warning.setFormatter(formatter_warning)
	logger_warning.setLevel(logging.WARNING)
	logger_warning.addHandler(handler_warning)
except:
	s=sys.exc_info()[0]
	print("Error logger_warning : ",s)

try:
	logger_info = logging.getLogger("info_log")
	handler_info = logging.handlers.RotatingFileHandler(pwd+"/log/info.log", mode="a", maxBytes= 1000000, backupCount= 1,encoding="utf-8")
	handler_info.setFormatter(formatter_info)
	logger_info.setLevel(logging.INFO)
	logger_info.addHandler(handler_info)
except:
	s=sys.exc_info()[0]
	print("Error logger_info : ",s)
