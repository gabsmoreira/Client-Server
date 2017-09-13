
from construct import *
import binascii


class Package (object):
    
    # Define o tamanho do HEAD e do EOP
    def __init__(self, data, datatype, number_packets,index):
        if datatype == "data":
            self.dataType = 0x00
        elif datatype == "sync":
            self.dataType = 0x10
        elif datatype == "ACK":
            self.dataType = 0x11
        elif datatype == "NACK":
            self.dataType = 0x12
        
        self.data = data
        if self.data == None:
            self.dataLen = 0
            self.data = bytearray([])
        else:
            self.dataLen = len(data)
        
        self.headSTART  = 0xFF
        self.index = '0x{0:04X}'.format(index)
        self.number_packets = '0x{0:04X}'.format(number_packets)
        self.eopSTART = bytearray([0xFA,0xF8,0xF3,0xF5])
        self.headStruct = Struct("start" / Int8ub, "size"  / Int32ub, "type" / Int8ub, "number_packets" / Int16ub, "index" / Int16ub)
                            
        
    # Constroi o HEAD de acordo com as informacoes setadas na funcao __init__ e retorna o HEAD
    def buildHead(self):
        head = self.headStruct.build(dict(start = self.headSTART,size  = self.dataLen, type = self.dataType, number_packets = self.number_packets))
        # print("HEAD",head)                 
        return(head)

    # Constroi o PACKAGE ultilizando as funcoes buildHead e buildEOP, retorna o PACKAGE
    def buildPackage(self):
        package = self.buildHead()
        #print(len(self.data)) 
        package += self.data
        package += self.eopSTART
        #print(package)
        return package


# # Desempacota os dados
def undoPackage(package):
    size = int(binascii.hexlify(package[1:5]), 32) 
    # print("size",size)
    type_package = package[5:6]
    number_packets = int(binascii.hexlify(package[6:8]), 16) 
    index = int(binascii.hexlify(package[8:10]), 16) 
    if type_package == b'\x00':
        type_package = "data"
    elif type_package == b'\x10':
        type_package = "sync"
    elif type_package == b'\x11':
        type_package = "ACK"
    elif type_package == b'\x11':
        type_package = "NACK"
    payload = package[10:] #A partir do 4
    # print("EOP", eop)
    #print("DATA", data)
    return (payload,size,type_package,number_packets,index)

