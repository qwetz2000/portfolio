from nwBuffer import NwBuffer
import pickle
from nwPackage import NwPackage

class NwBatch:

    batchStartSequence = 0
    bufferForNext = None

    def __init__(self, size, debugMode: bool = False):
        self.debugMode = debugMode
        if size < 8:
            self.size = 8
        else:
            self.size = size
        self.avaiableSpace = self.size - 8
        self.payload = None
        self.nextPosition = 0
        self.flushBuffer()


    def flushBuffer(self):
        if NwBatch.bufferForNext is not None:
            self.add(NwBatch.bufferForNext)
            NwBatch.bufferForNext = None

    def initializeBatch(self):
        if self.payload is None:
            self.payload = bytearray(self.size)
            self.payload[0:4] = NwBatch.batchStartSequence.to_bytes(4,byteorder='big')
            self.payload[4:8] = self.size.to_bytes(4,byteorder='big')
            self.nextPosition = 8

    def fromBuffer(self, buffer: NwBuffer):
        while not buffer.isEmpty():
            toAdd = buffer.grabNext()
            if not self.add(toAdd):
                break

    def add(self, toAdd: NwPackage):
        if toAdd is not None:
            self.initializeBatch()
            addLength = len(toAdd.payload)
            if self.avaiableSpace - addLength >= 0:
                self.payload[self.nextPosition:self.nextPosition + addLength] = toAdd.payload
                self.nextPosition += addLength
                self.avaiableSpace -= addLength
                return True
            else:
                for i in range(self.nextPosition, self.size):
                    self.payload[i] = 0
                if addLength <= self.size - 8:
                    NwBatch.bufferForNext = NwPackage()
                    NwBatch.bufferForNext.insert(toAdd.payload)
                else:
                    NwBatch.bufferForNext = None
                    if self.debugMode:
                        print("BATCH SIZE TO SMALL FOR PAYLOAD")
                return False
            
    def insert(self, payload: bytes):
        if payload is not None:
            self.payload = payload 

    def toBuffer(self, buffer: NwBuffer):
        checkOverflow = False
        if self.payload is not None:
            if int.from_bytes(self.payload[0:4], byteorder='big') == NwBatch.batchStartSequence and int.from_bytes(self.payload[4:8], byteorder='big') == self.size:
                self.nextPosition = 8
                while self.nextPosition < self.size:
                    nextLength = int.from_bytes(self.payload[self.nextPosition:self.nextPosition + 4], byteorder='big')
                    if nextLength > 0:
                        outPackage = NwPackage()
                        outPackage.insert(self.payload[self.nextPosition:self.nextPosition + nextLength])
                        checkOverflow = buffer.add(outPackage)
                        self.nextPosition += nextLength
                    else:
                        self.nextPosition = self.size
        return checkOverflow

    def toQueue(self, queue):
        if self.payload is not None:
            queue.put(self.payload)

    def fromQueue(self, queue):
        if not queue.empty():
            self.insert(queue.get())
