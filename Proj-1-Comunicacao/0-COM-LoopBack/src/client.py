#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Aplicação
####################################################

from enlace import *
import time

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM7"                  # Windows(variacao de)

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
    #print (" - {}".format(imageR))
    print("-------------------------")
    txBuffer = open(imageR, 'rb').read()
    txLen    = len(txBuffer)
    print(txLen)
    
    # Transmite imagem
    print("Transmitindo .... {} bytes".format(txLen))
    inicio = time.time()
    #com.Handshake()
    time.sleep(0.1)
    com.sendData(txBuffer)

    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
        pass
    tempo = time.time()-inicio

    # Atualiza dados da transmissão
    print ("Transmitido       {} bytes ".format(txLen))
    print ("Tempo de envio: ", tempo," s")

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

if __name__ == "__main__":
    main()