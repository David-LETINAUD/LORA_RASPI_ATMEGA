import logging
from logging.handlers import RotatingFileHandler


# Gestion log file
formatter_warning = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
formatter_info = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

logger_warning = logging.getLogger("warning_log")
handler_warning= logging.handlers.RotatingFileHandler("/home/pi/Desktop/gateway/log/warning.log", mode="a", maxBytes= 1000000, backupCount= 1 , encoding="utf-8")
handler_warning.setFormatter(formatter_warning)
logger_warning.setLevel(logging.WARNING)
logger_warning.addHandler(handler_warning)

logger_info = logging.getLogger("info_log")
handler_info = logging.handlers.RotatingFileHandler("/home/pi/Desktop/gateway/log/info.log", mode="a", maxBytes= 1000000, backupCount= 1,encoding="utf-8")
handler_info.setFormatter(formatter_info)
logger_info.setLevel(logging.INFO)
logger_info.addHandler(handler_info)
