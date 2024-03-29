#
# Serial COM Port receive message event handler
# 8/17/2017, Dale Gambill
# When a line of text arrives from the COM port terminated by a \n character, this module will pass the message to
# the function specified by the instantiator of this class.
#
import serial
import sys
# Pour compatibilité python 2 et 3
try:
 import thread as _thread
except:
 import _thread 
    
import threading

from log_files import logger_info, logger_warning

class SerialPort:
    def __init__(self):
        self.comportName = ""
        self.baud = 0
        self.timeout = None
        self.ReceiveCallback = None
        self.isopen = False
        self.receivedMessage = None
        self.serialport = serial.Serial()

    def __del__(self):
        try:
            if self.serialport.is_open():
                self.serialport.close()
        except:
            s=sys.exc_info()[0] 
            print("Destructor error closing COM port: ", s)
            logger_warning.warning('Destructor : {}'.format(s))

    def RegisterReceiveCallback(self,aReceiveCallback):
        self.ReceiveCallback = aReceiveCallback
        try:
            _thread.start_new_thread(self.SerialReadlineThread, ())
        except:
            s=sys.exc_info()[0] 
            print("Error starting Read thread: ", sys.exc_info()[0])
            logger_warning.warning('RegisterReceiveCallback : {}'.format(s))

    def SerialReadlineThread(self):
        while 1:
            try:
                if self.isopen:
                    self.receivedMessage = self.serialport.readline()
                    if self.receivedMessage != "":
                        self.ReceiveCallback(self.receivedMessage)
            except:
                s=sys.exc_info()[0]
                print("Error reading COM port: ",s)
                logger_warning.warning('SerialReadlineThread : {}'.format(s))
                sys.exit(0) # evite une écriture infini dans le fichier log
                

    def IsOpen(self):
        return self.isopen

    def Open(self,portname,baudrate,bytesize,parity,stopbits):
        if not self.isopen:
            # serialPort = 'portname', baudrate, bytesize = 8, parity = 'N', stopbits = 1, timeout = None, xonxoff = 0, rtscts = 0)
            self.serialport.port = portname
            self.serialport.baudrate = baudrate
            self.serialport.bytesize = int(bytesize)
            self.serialport.parity = parity
            self.serialport.stopbits = int(stopbits)
            
            try:
                self.serialport.open()
                self.isopen = True
            except:
                s=sys.exc_info()[0] 
                print("Error opening COM port: ", s)
                logger_warning.warning('Open : {}'.format(s))
                


    def Close(self):
        if self.isopen:
            try:
                self.serialport.close()
                self.isopen = False
            except:
                s=sys.exc_info()[0] 
                print("Close error closing COM port: ", s)
                logger_warning.warning('Close : {}'.format(s))

    def Send(self,message):
        if self.isopen:
            try:
                # Ensure that the end of the message has both \r and \n, not just one or the other
                newmessage = message.strip()
                newmessage += '\r\n'
                self.serialport.write(newmessage.encode('utf-8'))
            except:
                s=sys.exc_info()[0] 
                print("Error sending message: ", s )
                logger_warning.warning('Send : {}'.format(s))
            else:
                return True
        else:
            return False




