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
import timeit

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/cu.usbmodem1451" # Mac    (variacao de)
#serialName = "COM3"                  # Windows(variacao de)
#serialName = "COM3"

def main(serialName):
    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # Endereco da imagem a ser transmitida
    imageR = "./imgs/imageB.png"

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")
    txBuffer = open(imageR, 'rb').read()
    txLen = (len(txBuffer))
    list_size = com.howmanyPackets(txLen)
    for i in range (1,len(list_size)):
        begin += list_size[i-1]
        final += list_size[i]  
        if com.establishConnection():
            # Carrega imagem
            print ("Carregando imagem para transmissão :")
            print (" - {}".format(imageR))
            print("-------------------------")
            txBuffer = open(imageR, 'rb').read()
            txLen = (len(txBuffer))
            print(txBuffer)
            print("Transmitindo .... {} bytes".format(txLen))
            start = time.time()
            com.sendData(txBuffer[begin:final])
        


        # espera o fim da transmissão
        while(com.tx.getIsBussy()):
            pass

        # Encerra comunicação
        stop = time.time()
        print("Tempo de transmissão:  {} ms ".format((stop-start)*1000))
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com.disable()
        






    

