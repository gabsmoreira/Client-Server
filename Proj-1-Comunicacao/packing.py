
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
        self.eopStruct = Struct("start" / Int32ub)

    # Constroi o HEAD de acordo com as informacoes setadas na funcao __init__ e retorna o HEAD
    def buildHead(self):
        head = self.headStruct.build(dict(start = self.headSTART,size  = self.dataLen))
        print("HEAD",head)                 
        return(head)

    # Constroi o EOP de acordo com as informacoes setadas na funcao __init__ e retorna o EOP
    def buildEOP (self):
        eop = self.eopStruct.build(dict(start = self.eopSTART))
        print("EOP",eop)
        return eop


    # Constroi o PACKAGE ultilizando as funcoes buildHead e buildEOP, retorna o PACKAGE
    def buildPackage(self):
        package = self.buildHead()
        #print(len(self.data)) 
        package += self.data
        package += self.buildEOP()
        return package


# # Desempacota os dados
def undoPackage(package):
    head = package[0:3]
    # eop = package[-4:]
    data = package[3:-4]
    print("HEAD", head)
    # print("EOP", eop)
    #print("DATA", data)
    return (head,data)

elements = [0, 200, 50, 25, 10, 255, 0]

# Create bytearray from list of integers.
# values = bytearray(elements)
# a=Package(values).buildPackage(len(values))
# print("PACKAGE",a)
# print(hex(a[2]))
# undoPackage(a)