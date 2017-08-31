# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 13:47:12 2017

@author: sabri
"""


from construct import *

class Packet(object):
    
    

    def __init__(self):
        self.headSTART = 0xFF
        self.headStruct = Struct("start" / Int8ub, "size" / Int16ub, "type" / Int8ub)

        ## TYPES
        # 0x00 SYN
        # 0x01 ACK
        # 0x02 nACK
        # 0x03 DATA

        self.eop =  bytearray([0x13, 0x12, 0x15, 0x14, 0x08, 0x01])
        self.lenhead = 4## O LEN DO HEAD, ATUALIZAR SE PRECISO


    def buildHead(self, dataLen, tipo):
        head = self.headStruct.build(dict(start = self.headSTART, size = dataLen, type = tipo))
        return head

    
    def empacota(self, dataLen, dados, tipo):
        
        packet = self.buildHead(dataLen, tipo)
        packet += dados
        packet += self.eop

        return packet

    def get_bin(self, x):

        return format(x, 'b').zfill(8)

    def desempacota(self, pacote):
        payload = bytearray([])
        len = self.get_bin(pacote[1]) + self.get_bin(pacote[2]) 
        len = int(len, 2)

        tipo = 3

        if len > 0:
            len += self.lenhead
            payload = pacote[self.lenhead:len]
        else:
            tipo = pacote[3]

        if payload == bytearray([]):
            payload = None
        
        return payload, tipo

            
