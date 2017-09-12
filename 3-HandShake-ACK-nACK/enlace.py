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
    def sendData(self, data):
        """ Send data over the enlace interface
        """
        package = Package(data,"data").buildPackage()
        self.tx.sendBuffer(package)


    def sendACK(self):
        package = Package(None,"ACK").buildPackage()
        self.tx.sendBuffer(package)
    
    def sendNACK(self):
        package = Package(None,"NACK").buildPackage()
        self.tx.sendBuffer(package)
    
    def sendSync(self):
        package = Package(None,"sync").buildPackage()
        self.tx.sendBuffer(package)

    def getData(self):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        
        package = self.rx.getHeadPayload()
        print(package)
        data = undoPackage(package)
        #print(data)
        return(data[0], data[1],(len(data[0])),data[2],data[3],data[4])
        

    def waitConnection(self):
        while self.connected ==  False:
            response = self.getData()
            print("Waiting sync...")
            if response[3] == "sync":
                print("Sync received")
                self.sendSync()
                time.sleep(0.5)
                self.sendACK()
                print("ACK SENT")
                response = self.getData()
                if response[3] == "ACK":
                    print("Ready to receive package")
                    return True
            else:
                return False

    def howmanyPackets(self, size):
        list_size=[0]
        res = size//self.maxbytes
        for i in range (res):
            list_size.append(self.maxbytes)
        list_size.append(size%self.maxbytes)
        return list_size


                    
                
    def establishConnection(self,size):    
        while self.connected ==  False:
            self.sendSync()
            response = self.getData()
            print("Waiting sync...")
            if response[3] == "ACK" or "sync":
                print("Sync received")
                response = self.getData()
                if response[3] == "sync" or "ACK":
                    print("ACK received")
                    time.sleep(0.5)
                    self.sendACK()
                    return True
            else:
                return False   