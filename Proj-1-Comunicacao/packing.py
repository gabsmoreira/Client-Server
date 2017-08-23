
from construct import *
import binascii


class Package (object):
    
    # Define o tamanho do HEAD e do EOP
    def __init__(self, data):
        self.data = data
        self.dataLen = len(data)
        self.headSTART  = 0xFF
        self.eopSTART = 0xFAF8F3F5
        self.headStruct = Struct("start" / Int8ub,
                            "size"  / Int16ub )
        self.eopStruct = Struct("start" / Int64ub)

    # Constroi o HEAD de acordo com as informacoes setadas na funcao __init__ e retorna o HEAD
    def buildHead(self, dataLen):
        head = self.headStruct.build(dict(start = self.headSTART,size  = dataLen))
        print("HEAD",head)                 
        return(head)

    # Constroi o EOP de acordo com as informacoes setadas na funcao __init__ e retorna o EOP
    def buildEOP (self):
        eop = self.eopStruct.build(dict(start = self.eopSTART))
        print("EOP",eop)
        return eop


    # Constroi o PACKAGE ultilizando as funcoes buildHead e buildEOP, retorna o PACKAGE
    def buildPackage(self):
        package = self.buildHead(self.dataLen)
        #print(len(self.data)) 
        package += self.data
        package += self.buildEOP()
        return package


# # Desempacota os dados
def undoPackage(package):
    head = package[0:3]
    #eop = package[-6:]
    data = package[3:-4]
    print("HEAD", head)
    return (head,data)

