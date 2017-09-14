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
serialName = "COM4"                  # Windows(variacao de)


def main():
    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # Endereco da imagem a ser salva
    imageW = "./imgs/recebida.png"

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    #txLen  = 96776 #len(txBuffer)- tamanho da imagem

    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
        pass

    # # Recebe 1o byte
    # print ("Recebendo dados .... ")
    # rxBuffer1, nRx1 = com.getData()

    # inicio = time.time()
    com.waitingHandshake()
    print("Comunicação COMPLETA")
    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    rxBuffer, nRx, trash = com.getData(10)
    print("nosso pacote retornou: "+str(trash))
    

    # tempo = time.time() - inicio

    # log
#    print ("Lido              {} bytes ".format(nRx))
    # print("Tempo de Recebimento: " + str(tempo) + " s")

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
    com.disable()

if __name__ == "__main__":
    main()