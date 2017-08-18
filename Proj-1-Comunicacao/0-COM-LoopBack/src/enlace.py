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
        self.eopConstant = 0xFF
        self.eopStruct = Struct("Constant" / Int8ub)                      
                        
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
        head = headStruct.build(dict(
                                    start = self.headSTART,
                                    size  = dataLen))
        return(head)
    
    def buildEop(self):
        eop = eopStruct.build(dict(constante = self.eopConstant))
        
        return(eop)
    
    def buildPacket(self, data):
        packet = self.buildHead(len(data))
        #print(packet)
        packet += data
        #print(packet)
        packet += buildEop()
        #print(packet)
        return (packet)

    def sendData(self, data):
       self.tx.sendBuffer(buildPacket(data))
       #print(self.buildPacket(data))
       
    def getData(self, size):
        data = self.rx.getNData(size)
        return(data, len(data))


