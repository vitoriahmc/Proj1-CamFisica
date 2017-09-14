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
import crcmod
# Construct Struct
from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

import packet

import crcmod

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    max_pkt = 2048
    
    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False

        construtor = packet.packet()
        
        nada = bytearray([])
        self.SYN = construtor.buildPacket(0, nada, 0, nada, nada, nada, nada)
        self.ACK = construtor.buildPacket(0, nada, 1, nada, nada, nada, nada)
        self.nACK = construtor.buildPacket(0, nada, 2, nada, nada, nada, nada)

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
        
        max_pkt = self.max_pkt
        qtdpartes = math.ceil(len(data)/max_pkt)
        atual = 1
        x = 0
        y = max_pkt + 1
        while atual <= qtdpartes:
            data_cortada = data[x:y]
            pacote = construtor.buildPacket(len(data_cortada), data_cortada, 3, atual, qtdpartes, 0, 0) #constroi pacote falso
            crc_head = self.CRC(pacote[0:5]) #calcula crc pro pacote falso
            crc_payload = self.CRC(data_cortada)
            pacote_final = construtor.buildPacket(len(data_cortada), data_cortada, 3, atual, qtdpartes, crc_head, crc_payload)
            self.tx.sendBuffer(pacote_final) #envia pacote verdadeiro
            time.sleep(0.05)
            
            if self.getData(10)[2] == 1: #10 é valor do timeout
                print("Recebi o Ack, vou enviar o proximo pacote")
                atual += 1
                x += y
                y += max_pkt
                print("Checagem pacote: "+str(len(pacote_final)))
                
            if self.getData(10)[2] == 2:
                print("Recebi um nAck, vou reenviar o ultimo pacote")
                self.tx.sendBuffer(pacote_final)
            time.sleep(0.05)
        

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
        payload = bytearray([])
        while True:
            
            pacote = self.rx.getPacket(timeout)
            construtor = packet.packet()          
            
            data, tipo, atual, total, crc_head, crc_payload = construtor.unpack(pacote)
            
            if data != None:
               
                while atual <= total:
                    crc_payload_2 = self.CRC(data)
                    crc_head_2 = self.CRC(pacote[0:5])
                    if crc_payload_2 == crc_payload and crc_head_2 == crc_head:
                        #comparação de crcs, se der certo, envia Ack
                        payload += data
                        self.sendCmd(1)
                        print("Recebi o pacote, mandando o Ack")
                        time.sleep(0.05)
                        pacote = self.rx.getPacket(timeout)
                        data, tipo, atual, total, crc_head, crc_payload = construtor.unpack(pacote)
                    else:
                        self.sendCmd(2)
                        print("Recebi o pacote corrompido, mandando nAck")
                    
                return(payload, len(payload), 3)
                break
            else:
                return(None, 0, tipo)
                break
    
    def CRC(self,data):
        crc8 = crcmod.predefined.mkCrcFun("crc-8")

        CRC = (crc8(data))

        return CRC

#    def pegar_CRC(self,data):
#      head = data[0:9]
#      container = packet.headStruct.parse(head)
#      return (container["checksum_head"], container["checksum_payload"])
#      
#    def comparar_CRC(self,data):
#        crc8 = crcmod.predefined.mkCrcFun("crc-8")
#        checksum_head,checksum_payload = self.pegar_CRC(data)
#        semCRC = data[0:5] 
#
#        mydata = self.pacotinho(data)
#
#        if checksum_head == crc8(mydata) and checksum_payload == crc8(semCRC):
#            return True
#        else:
#            return False
#
#
#    def pacotinho(self,data):
#
#        head = data[0:9]
#        #resto =  data[9:-10]
#
#        return(head)

#    def sendData2(self, data):
#        """ Send data over the enlace interface
#        """
#        construtor = packet.packet()
#      
#        pacote = construtor.buildPacket(len(data), data, 3)
#        
#        print("Checagem pacote: "+str(len(pacote)))
#       
#        while self.getData2(11)[2] != 1:
#            print("Estou reenviando o pacote pois nao recebi o Ack")
#           # self.rx.clearBuffer()
#            self.tx.sendBuffer(pacote)
    
#    def getData2(self, timeout):
#        """ Get n data over the enlace interface
#        Return the byte array and the size of the buffer
#        """
#        tmp = False
#        while tmp == False:
#            pacote = self.rx.getPacket(timeout)
#            construtor = packet.packet()
#            
#            data, tipo = construtor.unpack(pacote)
#           
#            if data != None:
#                return(data, len(data), 3)
#                time.sleep(0.2)
#                self.sendCmd(1)
#                print("mandando Ack do pacote")
#                tmp = Trues
#            else:
#                time.sleep(0.2)
#                self.sendCmd(2)
#                print("mandando nAck do pacote")
#                return(None, 0, tipo)

 