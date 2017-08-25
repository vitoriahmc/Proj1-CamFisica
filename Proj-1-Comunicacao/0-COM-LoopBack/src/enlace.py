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
        self.Syn         = 0xAA
        self.Ack         = 0x0F
        self.nAck        = 0xF0
        self.Data        = 0x24
        self.sizeCmd     = 0x00 + 0x00
        self.headStruct = Struct("start" / Int8ub,
                        "size"  / Int16ub, 
                        "tipo" / Int8ub)
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
        packet += data
        packet += self.buildEop()
        return (packet)
        
    def unpack (self, packet):
    
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
        data = self.unpack(package)
        return(data, len(data))

#    def sendData(self, data):
#        #buildPacket()
#        self.tx.sendBuffer(self.buildPacket(data))
#       #print(self.buildPacket(data))
#       
#    def getData(self):
#        data = self.rx.getPacket()[0]
#        return(data)

     def buildHeadData(self, dataLen):
        head = self.headStruct.build(dict(
                                    start = self.headSTART,
                                    tipo = self.Data,
                                    size  = dataLen))
        return(head)
        
    def buildHeadCmd(self, subtype):
        head = self.headStruct.build(dict(
                                    start = self.headSTART,
                                    size = self.sizeCmd,
                                    tipo = self.Syn if subtype == 0 else (self.Ack if subtype == 1 else self.nAck) 
                                    ))
        return(head+self.buildEop())
    
       
    def sendSyn(self):
        #buildPacket()
        self.tx.sendBuffer(self.buildSynPacket())
        
    def sendAck(self):
        #buildPacket()
        self.tx.sendBuffer(self.buildAckPacket())
        
    def sendnAck(self):
        #buildPacket()
        self.tx.sendBuffer(self.buildnAckPacket())
        
        
    def buildSynPacket(self):
        return(self.buildHeadCmd(0))
        
    def buildAckPacket(self):
        return(self.buildHeadCmd(1))
    
    def buildnAckPacket(self):
        return(self.buildHeadCmd(2))