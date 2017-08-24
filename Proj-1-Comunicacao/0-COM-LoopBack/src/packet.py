# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 07:58:26 2017

@author: Vitoria
"""

from construct import *

class Pacote (object):
    
    def __init__(self, data):
        self.data = data
        self.dataLen = len(data)
        self.headSTART  = 0xFF
        self.eopSTART = 0xABCDEF12
        self.headStruct = Struct("start" / Int8ub,
                            "size"  / Int16ub )
        self.eopStruct = Struct("start" / Int64ub)

    def buildHead(self, dataLen):
        head = self.headStruct.build(dict(start = self.headSTART,size  = dataLen))
        return(head)

    def buildEOP (self):
        eop = self.eopStruct.build(dict(start = self.eopSTART))
        return eop

    def buildPacket(self):
        packet = self.buildHead(self.dataLen)
        packet += self.data
        packet += self.buildEOP()
        return packet


def unbuildPacket(package):
    head = package[0:3]
    data = package[3:-2]
    return (head,data)

def OverHead(self):
    overhead = len(self.buildPacket())/len(self.data)
    return (overhead/100, "%")
    