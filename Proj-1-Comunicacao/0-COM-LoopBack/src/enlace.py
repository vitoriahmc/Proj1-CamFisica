#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Construct Struct
from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False
        self.headSTART   = 0xFF 
        self.headStruct = Struct("start" / Int8ub,
                        "size"  / Int16ub )
        self.eopConstant = 0xABCDEF12
        self.eopStruct = Struct("constant" / Int64ub)                      
                        
    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################

    
    def buildHead(self, dataLen):
        head = self.headStruct.build(dict(
                                    start = self.headSTART,
                                    size  = dataLen))
        return(head)
    
    def buildEop(self):
        eop = self.eopStruct.build(dict(constant = self.eopConstant))
        
        return(eop)
    
    def buildPacket(self, data):
        packet = self.buildHead(len(data))
        #print(packet)
        packet += data
        #print(packet)
        packet += self.buildEop()
        #print(packet)
        return (packet)
        
    def unpackage (self, packet):
    
        head = packet[0:3]
        print(len(head))

        payload = packet[len(head):]
        print(len(payload))

        return payload

    def sendData(self, data):
        """ Send data over the enlace interface
        """
        packet = self.buildPacket(data)

        self.tx.sendBuffer(packet)

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        package = self.rx.getPacket()
        data = self.unpackage(package)
        return(data, len(data))

#    def sendData(self, data):
#        #buildPacket()
#        self.tx.sendBuffer(self.buildPacket(data))
#       #print(self.buildPacket(data))
#       
#    def getData(self):
#        data = self.rx.getPacket()[0]
#        return(data)
#
#
#    def getSize(self):
#        t = self.rx.getPacket()[1]
#        return(t)