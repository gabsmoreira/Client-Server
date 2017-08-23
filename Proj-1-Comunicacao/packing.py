
from construct import *
import binascii


class Package (object):
    
    # Define o tamanho do HEAD e do EOP
    def __init__(self, data):
        self.data = data
        self.headSTART  = 0xFF
        self.eopSTART = 0xFAF8F3f5
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
    def buildPackage(self,data_len):
        package = self.buildHead(data_len)
        #print(len(self.data)) 
        package += self.data
        package += self.buildEOP()
        return package


# # Desempacota os dados
def undoPackage(package):
    head = package[0:2]
    eop = package[-2:]
    data = package[2:-2]
    print("HEAD", head)
    print("EOP", eop)
    print("DATA", data)
    return (head,eop,data)

elements = [0, 200, 50, 25, 10, 255, 0]

# Create bytearray from list of integers.
values = bytearray(elements)
a=Package(values).buildPackage(len(values))
print("PACKAGE",a)
print(hex(a[2]))
undoPackage(a)