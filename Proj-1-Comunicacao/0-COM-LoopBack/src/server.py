# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 07:52:22 2017

@author: Vitoria
"""

from enlace import *
from enlaceRx import RX
#import time

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM9"                  # Windows(variacao de)

def main():
    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # Endereco da imagem a ser salva
    imageW = "./imgs/recebida.png" and "./imgs/recebida2.png"

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")
    
    while(com.tx.getIsBussy()):
        pass

    waitingHandshake = True
    while waitingHandshake:
         print('waiting Handshake')
         time.sleep(0.1)
         print(com.getCmd())
         if com.getCmd() == b'\xaa':
             com.sendSyn()
             time.sleep(0.1)
             com.sendAck()
             time.sleep(0.1)
             if com.getCmd() == b'\x0f':
                 waitingHandshake = False
             else:
                 com.sendnAck()
         else:
             com.sendnAck()

    inicial = time.time()
    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    rxBuffer, nRx = com.getData()
    final = time.time()

    # Salva imagem recebida em arquivo
    print("-------------------------")
    print ("Salvando dados no arquivo :")
    print (" - {}".format(imageW))
    f = open(imageW, 'wb')
    f.write(rxBuffer)

    # Fecha arquivo de imagem
    f.close()

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    print("Tempo de Recebimento")
    print(final-inicial)
    print("-------------------------")
    com.disable()

if __name__ == "__main__":
    main()
