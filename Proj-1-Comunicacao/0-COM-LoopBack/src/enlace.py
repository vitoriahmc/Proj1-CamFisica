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

import packet

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

        construtor = packet.packet()
        
        nada = bytearray([])
        self.SYN = construtor.buildPacket(0, nada, 0)
        self.ACK = construtor.buildPacket(0, nada, 1)
        self.nACK = construtor.buildPacket(0, nada, 2)

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

    def Handshake(self):#client
        
        print("Estabelecendo conexao...")
        timeout=2.0

        while self.connected == False:
          time.sleep(0.1)
          self.sendCmd(0)
          
          
          tempacote= self.getData(timeout)[2]
          if tempacote == 4:
              print("Nao recebi o Syn ainda")
              #time.sleep(0.01)
              #self.sendCmd(2)
              #manda o nAck quando chegou algo que nao é um Syn ou quando nao chegou nada
          if tempacote == 0:
              print("Recebi o Syn!")
              tempacote= self.getData(timeout)[2]
              if tempacote == 4:
                  print("Recebi o Syn e ainda não recebi o Ack")
                  time.sleep(0.1)
                  self.sendCmd(2) #manda o nAck enquanto o Ack nao chega
              if tempacote == 1:
                  print("Recebi o Ack")
                  self.sendCmd(1)
                  print("Mandei o ultimo Ack")
                  self.connected = True
          
        print("Conectado com sucesso!")

    def waitingHandshake(self): #SERVER
        timeout= 2.0
        while True:    
    
            print("Esperando o Syn...")
            while(self.getData(timeout)[2] != 0):
                print("...")
                continue
            print("Recebi o Syn")
            time.sleep(0.1)
            self.sendCmd(0)
            print("enviei o Syn")
            time.sleep(0.1)
            self.sendCmd(1)
            print("enviei o Ack")
            
            print("Aguardando o Ack")
            tempacote= self.getData(timeout)[2]
            print("tempacote: "+str(tempacote))
            if tempacote == 4:
                print("Não recebi nada (timeout)")
            if tempacote == 2:
                print("Recebi nAck")
            if tempacote == 1:
                print("Recebi o ultimo Ack")
                print("Handshake ENCERRADO")
                break
        print("----")
        
    def sendData(self, data):
        """ Send data over the enlace interface
        """
        construtor = packet.packet()
        pacote = construtor.buildPacket(len(data), data, 3)
        
        print("Checagem pacote: "+str(len(pacote)))
        while self.getData(10)[2] != 1:
            print("Estou reenviando o pacote pois nao recebi o Ack")
            self.tx.sendBuffer(pacote)
        break
    
    def sendCmd(self, tipo):
        if tipo == 0:
            self.tx.sendBuffer(self.SYN)
        if tipo == 1:
            self.tx.sendBuffer(self.ACK)
        if tipo == 2:
            self.tx.sendBuffer(self.nACK)
    
    #

    def getData(self, timeout):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """

        pacote = self.rx.getPacket(timeout)
        construtor = packet.packet()
        
        data, tipo = construtor.unpack(pacote)
       
        if data != None:
            return(data, len(data), 3)
            self.sendCmd(1)
            print("mandando Ack do pacote")
        else:
            self.sendCmd(2)
            print("mandando nAck do pacote")
            return(None, 0, tipo)


