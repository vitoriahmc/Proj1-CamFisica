# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 13:47:12 2017

@author: sabri
"""


from construct import *

class packet(object):
    
    

    def __init__(self):
        self.headSTART = 0xFF
        self.headStruct = Struct("start" / Int8ub, 
                                 "size" / Int16ub, 
                                 "tipos" / Int8ub)
        self.eopConstant =  bytearray([0xAB, 0xBC, 0xCD, 0xDE, 0xEF, 0xFA])
        self.HeadLen = self.headStruct.sizeof() 

    def buildHead(self, dataLen, tipo):
        head = self.headStruct.build(dict(
                                    start = self.headSTART,
                                    size  = dataLen,
                                    tipos = tipo))
        return(head)

    
    def buildPacket(self, dataLen, data, tipo):
        
        packet = self.buildHead(dataLen, tipo)
        packet += data
        packet += self.eopConstant

        return packet

    def get_bin(self, x):

        return format(x, 'b').zfill(8)

    def unpack(self, pacote):
        if (len(pacote) != 0):
            payload = bytearray([])
            lenght = self.get_bin(pacote[1]) + self.get_bin(pacote[2]) 
            lenght = int(lenght, 2)
    
            tipo = 3
    
            if lenght > 0:
                lenght += self.HeadLen
                payload = pacote[self.HeadLen:lenght]
            else:
                tipo = pacote[3]
    
            if payload == bytearray([]):
                payload = None
            
            return payload, tipo
        else:
            data = None
            tipo = 4
            return data, tipo

            