
from construct import *
import binascii


class Package (object):
    
    # Define o tamanho do HEAD e do EOP
    def __init__(self, data, datatype):
        if datatype == "data":
            self.dataType = 0x00
        elif datatype == "sync":
            self.dataType = 0x01
        elif datatype == "ACK":
            self.dataType = 0x02
        elif datatype == "NACK":
            self.dataType = 0x03
        
        self.data = data
        if len(data) == None:
            self.dataLen = 0
        else:
            self.dataLen = len(data)
        
        self.headSTART  = 0xFF
        self.eopSTART = bytearray([0xFA,0xF8,0xF3,0xF5])
        self.headStruct = Struct("start" / Int8ub, "size"  / Int16ub, "type" / Int8ub )
                            
        
    # Constroi o HEAD de acordo com as informacoes setadas na funcao __init__ e retorna o HEAD
    def buildHead(self):
        head = self.headStruct.build(dict(start = self.headSTART,size  = self.dataLen, type = self.dataType))
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
    size = int(binascii.hexlify(package[1:3]), 16) 
    print("size",size)
    type_package = package[3:4]

    if type_package == b'\x00':
        type_package = "data"
    elif type_package == b'\x01':
        type_package = "sync"
    elif type_package == b'\x02':
        type_package = "ACK"
    elif type_package == b'\x03':
        type_package = "NACK"
    payload = package[4:] #A partir do 4
    # print("EOP", eop)
    #print("DATA", data)
    return (payload,size,type_package)

elements = [0, 200, 50, 25, 10, 255, 23]

# Create bytearray from list of integers.
# values = bytearray(elements)
# a = Package(values,"sync").buildPackage()
# print("PACKAGE",a)
# b = undoPackage(a)
# print(b)
