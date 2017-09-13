#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Prof. Rafael Corsi
#  Abril/2017
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Construct Struct
from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX
from packing import *
from packing import Package

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False
        self.maxbytes    = 2048

    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################
    def howmanyPackets(self, size):
        list_size=[0]
        res = size//self.maxbytes
        for i in range (res):
            list_size.append(self.maxbytes)
        list_size.append(size%self.maxbytes)
        return list_size

    def sendData(self, data):
        """ Send data over the enlace interface
        """
        howmanyPackets = self.howmanyPackets((len(data)))
        for i in range (1,len(howmanyPackets)):
            begin = howmanyPackets[i-1] + 1
            end = howmanyPackets[i]
            actual_data = data[begin:end]
            package = Package(actual_data,"data",howmanyPackets[i],i).buildPackage()
            self.tx.sendBuffer(package)

    def sendACK(self):
        package = Package(None,"ACK",1,1).buildPackage()
        self.tx.sendBuffer(package)
    
    def sendNACK(self):
        package = Package(None,"NACK",1,1).buildPackage()
        self.tx.sendBuffer(package)
    
    def sendSync(self):
        package = Package(None,"sync",1,1).buildPackage()
        self.tx.sendBuffer(package)

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        index = 0
        number_packets = 1
        data = bytes(bytearray())
        while index != number_packets:
            package = self.rx.getHeadPayload()
            if package != None:
                package = self.rx.getHeadPayload()
                print(binascii.hexlify(package))
                payload, size, type_package, number_packets, index = undoPackage(package)
                real_size = (len(payload))
            while real_size != size:
                if package != None:
                    self.sendNACK()
                    time.sleep(0.2)
                    package = self.rx.getHeadPayload()
                    print(binascii.hexlify(package))
                    payload, size, type_package, number_packets, index = undoPackage(package)
                    real_size = (len(payload))
            data +=payload
        return(data, size, real_size, type_package)  

    def waitConnection(self):
        print("SERVER")
        time.sleep(2)
        response = self.getData()
        print(response)
        while response[3] != "sync":
            #self.sendNACK()
            time.sleep(0.15)
            response = self.getData()
        print("SYNC RECEIVED")
        self.sendSync()
        time.sleep(0.5)
        self.sendACK()
        time.sleep(0.15)
        response = self.getData()
        while response[3] != "ACK":
            self.sendNACK()
            time.sleep(0.15)
            self.sendSync()
            time.sleep(0.5)
            self.sendACK()
            time.sleep(0.15)
            response = self.getData()
        print("ACK RECEIVED")
        response = self.getData()
        while response[3] != "data":
            self.sendNACK()
            time.sleep(0.15)
            response = self.getData()
        print("DATA RECEIVED")
        return response
                    
    def establishConnection(self,data):
        print("CLIENT")
        self.sendSync()
        time.sleep(0.5)
        response = self.getData()
        while response[3] != "ACK" or "sync":
            self.sendSync()
            time.sleep(0.5)
            response = self.getData()
        print("ACK RECEIVED")
        response = self.getData()
        while response[3] != "ACK" or "sync":
            response = self.getData()
        print("SYNC RECEIVED")
        self.sendACK()
        time.sleep(0.15)
        self.sendData(data)
        while response[3] != "ACK":
            self.sendACK()
            time.sleep(0.15)
            self.sendData(data)
        print("DATA SENT")
        return True   