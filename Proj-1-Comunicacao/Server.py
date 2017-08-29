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

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem1431" # Mac    (variacao de)
#serialName = "COM3"                  # Windows(variacao de)

def main():
    # Inicializa enlace
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    # Endereco da imagem a ser transmitida

    # Endereco da imagem a ser salva
    imageW = "./imgs/recebida.png"

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    
    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
        pass
    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()

    # Faz a recepção dos dados

    print ("Recebendo dados .... ")
    if com.waitConnection():
        rxBuffer, nRx, real_nRx, package_type = com.getData()


        start = time.time()
        print(nRx)

        
        
        lost_bytes = nRx-real_nRx
        # log
        print ("Lido              {} bytes ".format(real_nRx))
        print ("Perdas            {} bytes ".format(lost_bytes))
        stop = time.time()

        # Salva imagem recebida em arquivo
        print("-------------------------")
        print ("Salvando dados no arquivo :")
        print (" - {}".format(imageW))
        f = open(imageW, 'wb')
        f.write(rxBuffer)

        # Fecha arquivo de imagem
        f.close()

        # Encerra comunicação
        print("Tempo de transmissão:  {} ms ".format((stop-start)*1000))

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com.disable()


