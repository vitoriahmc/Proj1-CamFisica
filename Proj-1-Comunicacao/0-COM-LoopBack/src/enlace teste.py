# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 14:43:49 2017

@author: sabri
"""
from enlace import *
imageR = "./imgs/imageD.png"
print ("Carregando imagem para transmissão :")
print (" - {}".format(imageR))
print("-------------------------")
txBuffer = open(imageR, 'rb').read()
txLen    = len(txBuffer)
print(txBuffer)
en = enlace('ggg')

en.sendData(txBuffer)