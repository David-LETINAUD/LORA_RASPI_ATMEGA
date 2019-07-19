# -*- coding: utf-8 -*
# https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
from math import *
from log_files import *

# Convertion de Celsius en Fahrenheit
def cCelToFah(celsius) :
 try:
  fahrenheit= 9./5.*celsius+32
 except:
  s=sys.exc_info()[0]
  print("Error converting Celsius to Fahrenheit : ", s )
  logger_warning.warning("Error converting Celsius to Fahrenheit : {}".format(s) )
 else: 
  return fahrenheit

# Convertion de Fahrenheit en Celsius
def cFahToCel(fahrenheit) :
 try:
  celsius= 5./9.*(fahrenheit-32)
 except:
  s=sys.exc_info()[0]
  print("Error converting Fahrenheit to Celsius : ", s)
  logger_warning.warning("Error converting Fahrenheit to Celsius : {}".format(s) )
 else: 
  return celsius

def heat_index(temperature, rh):
 try:
  T = cCelToFah(temperature)
    
  rh2 = rh * rh
  T2 = T * T

  # Calculation based on https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml and http://www.atmos.albany.edu/student/msmith/misc/vtemp.py
  # Calculate the Heat Index -- constants converted for RH in [0, 100]
  # Steadman equation
  hi = (-42.379
        + 2.04901523 *T
        + 10.14333127 * rh
        - 0.22475541 * T * rh
        - 6.83783e-3 * T2
        - 5.481717e-2 * rh2
        + 1.22874e-3 * T2 * rh
        + 8.5282e-4 * T * rh2
        - 1.99e-6 * T2 * rh2)

  if (rh < 13.00 and T >= 80.00 and T<=112.00):
   delta = ((13.-rh)/4.)*sqrt((17.-abs(T-95.))/17.)
   res = cFahToCel(hi-delta)

  elif (rh >= 85.00 and T >= 80.00 and T<=87.00):
   delta = ((rh-85.)/10.)*(87.-T)/5.
   res = cFahToCel(hi+delta)

  elif (rh >= 40.00 and T >= 80.00): # 80°F = 26.67°C voir aussi https://en.wikipedia.org/wiki/Heat_index
   res = cFahToCel(hi)

  else :
   res = cFahToCel(0.5 * (T + 61.0 + (T-68.0)*1.2 + rh*0.094))
  
 except:
  s=sys.exc_info()[0]
  print("Error converting temperature to heat index : ", s )
  logger_warning.warning("Error converting temperature to heat index : {}".format(s) )
 else:
  return round(res, 2)

