#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Sabrina e Vitoria
#  Abril/2017
#  Client
####################################################

from enlace import *
#import time

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM8"                  # Windows(variacao de)

def main():
    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # Endereco da imagem a ser transmitida
    imageR = "./imgs/imageC.png"

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega imagem
    print ("Carregando imagem para transmissão :")
    print (" - {}".format(imageR))
    print("-------------------------")
    txBuffer = open(imageR, 'rb').read()
    txLen    = len(txBuffer)
    print(txLen)
    ######r = '\x0f'.encode()

#    waitingHandshake = True
#    while waitingHandshake:
#        print('waiting Handshake')
#        com.sendSyn()
#        time.sleep(0.1)
#        print(com.getCmd())
#        if com.getCmd() == b'\xaa': #tem que receber o AA e o 0F
#            time.sleep(0.15)
#            if com.getCmd() == b'\x0f':
#                waitingHandshake = False
#                com.sendAck()
#            else:
#                com.sendnAck()
#        else:
#             com.sendnAck()
             
    waitingHandshake = True
    while waitingHandshake:
        print('waiting Handshake')
        com.sendSyn()
        time.sleep(0.1)
        print(com.getCmd())


    inicial = time.time()
    # Transmite imagem
    print("Transmitindo .... {} bytes".format(txLen))
    com.sendData(txBuffer)

    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
        pass
    
    final = time.time()
    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()
    print ("Transmitido       {} bytes ".format(txSize))


    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    print("Tempo de transmissão")
    print(final-inicial)
    com.disable()

if __name__ == "__main__":
    main()
