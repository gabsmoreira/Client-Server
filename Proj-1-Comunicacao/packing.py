
from construct import *
import binascii


class Package (object):
    
    # Define o tamanho do HEAD e do EOP
    def __init__(self, data):
        self.data = data
        self.dataLen = len(data)
        self.headSTART  = 0xFF
        self.eopSTART = bytearray([0xFA,0xF8,0xF3,0xF5])
        self.headStruct = Struct("start" / Int8ub,
                            "size"  / Int16ub )
        

    # Constroi o HEAD de acordo com as informacoes setadas na funcao __init__ e retorna o HEAD
    def buildHead(self):
        head = self.headStruct.build(dict(start = self.headSTART,size  = self.dataLen))
        print("HEAD",head)                 
        return(head)

    # Constroi o PACKAGE ultilizando as funcoes buildHead e buildEOP, retorna o PACKAGE
    def buildPackage(self):
        package = self.buildHead()
        #print(len(self.data)) 
        package += self.data
        package += self.eopSTART
        print(package)
        return package


# # Desempacota os dados
def undoPackage(package):
    print(package)
    size = int(binascii.hexlify(package[2:4]), 16) 
    print("size",size)
    payload = package[4:] #A partir do 4
    # print("EOP", eop)
    #print("DATA", data)
    return (payload,size)

# elements = [0, 200, 50, 25, 10, 255, 0]

# Create bytearray from list of integers.
# values = bytearray(elements)
# a=Package(values).buildPackage(len(values))
# print("PACKAGE",a)
# print(hex(a[2]))
# undoPackage(a)