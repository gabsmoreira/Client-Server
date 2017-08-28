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
serialName = "/dev/cu.usbmodem1461" # Mac    (variacao de)
#serialName = "COM3"                  # Windows(variacao de)
#serialName = "COM3"

def main():
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

    # Carrega imagem
    print ("Carregando imagem para transmissão :")
    print (" - {}".format(imageR))
    print("-------------------------")
    txBuffer = open(imageR, 'rb').read()
    txLen = (len(txBuffer))
    print(txLen)

    # Send sync
    com.sendSync()
    print("Sent sync")

    print ("Esperando sync")
    rxBuffer, nRx, real_nRx, package_type = com.getData()
    
    if package_type == "sync":
        rxBuffer, nRx, real_nRx, package_type = com.getData()
        com.sendACK()
    
    if package_type == "ACK":
        # Transmite imagem
        print("Transmitindo .... {} bytes".format(txLen))
        start = time.time()
        com.sendData(txBuffer)
        


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
        






    

