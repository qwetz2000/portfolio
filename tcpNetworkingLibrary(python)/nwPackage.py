import pickle

class NwPackage:

    def __init__(self):
        self.payload = None

    def create(self, packageId: int, data: any):
        serializedData = pickle.dumps(data)
        byteLength = 8+len(serializedData)
        binData = bytearray(byteLength)
        binData[0:4] = byteLength.to_bytes(4,byteorder='big')
        binData[4:8] = packageId.to_bytes(4,byteorder='big')
        binData[8:byteLength] = serializedData
        self.payload = binData

    def insert(self,payload: any):
        self.payload = payload

    def deserialize(self):
        if self.payload != None:
            packageLength = len(self.payload)
            binLength = self.payload[0:4]
            length = int.from_bytes(binLength, byteorder='big')
            if  packageLength == length:
                packageId = int.from_bytes(self.payload[4:8], byteorder='big')
                deserializedData = pickle.loads(self.payload[8:packageLength])
                return packageId, deserializedData
            else:
                return None, None
        else:
            return None, None

    def getLength(self):
        if self.payload is not None:
            return len(self.payload)
        return 0

