from nwItem import NwItem, NwItemManager
from nwBuffer import NwBuffer
from nwTcp import NwTcpConnection
from nwBatch import NwBatch

class NwManager:

    def __init__(self, tickRate: int, rxBufferSize: int, txBufferSize: int, batchSize: int ,debugMode: bool = False):
        self.batchSize = batchSize + 8
        self.debugMode = debugMode
        self.tickRate = tickRate
        self.rxBuffer = NwBuffer(rxBufferSize)
        self.txBuffer = NwBuffer(txBufferSize)
        self.itemManager = NwItemManager(self.rxBuffer, self.txBuffer)
        self.connection = None
        if self.debugMode:
            print("MANAGER CREATED")

    def createConnection(self, isHost: bool, ip: str, port: int):
        if self.connection is None:
            self.connection = NwTcpConnection(isHost, ip, port, self.batchSize,self.debugMode)
            self.connection.setupAutoSender(self.tickRate)
            return True
        if self.debugMode:
            print("MANAGER ALREADY HAS CONNECTION")
        return False

    def createRxItem(self, itemId: int, bufferSize: int):
        rxItem = NwItem(itemId,bufferSize)
        self.itemManager.bindRxItem(rxItem)
        if self.debugMode:
            print("CREATED RX ITEM")
        return rxItem

    def createTxItem(self, itemId: int, bufferSize: int):
        txItem = NwItem(itemId,bufferSize)
        self.itemManager.bindTxItem(txItem)
        if self.debugMode:
            print("CREATED TX ITEM")
        return txItem

    def cleanup(self):
        self.update()
        if self.connection is not None:
            self.connection.shutdown()
            self.connection = None
            if self.debugMode:
                print("MANAGER CLEANED UP")
            return True
        if self.debugMode:
            print("NO CONNECTION TO CLEAN UP")
        return False

    def update(self):
        if self.connection is not None:
            while not self.connection.rxQueue.empty():
                rxBatch = NwBatch(self.batchSize,self.debugMode)
                rxBatch.fromQueue(self.connection.rxQueue)
                if not rxBatch.toBuffer(self.rxBuffer):
                    if self.debugMode:
                        print("RX BUFFER OVERFLOW")
            if not self.itemManager.update():
                if self.debugMode:
                    print("TX BUFFER OVERFLOW")
            while not self.txBuffer.isEmpty():
                txBatch = NwBatch(self.batchSize,self.debugMode)
                txBatch.fromBuffer(self.txBuffer)
                txBatch.toQueue(self.connection.txQueue)
            if NwBatch.bufferForNext is not None:
                flushBatch = NwBatch(self.batchSize,self.debugMode)
                flushBatch.toQueue(self.connection.txQueue)
        self.connection.update()

    def isConnectedAsClient(self):
        if self.connection is None:
            if self.debugMode:
                print("NO CONNECTION ESTABLISHED")
            return False
        else:
            if self.connection.isHost:
                if self.debugMode:
                    print("ERROR: CONNECTION TYPE IS HOST")
                return False
            else:
                if self.connection.connection is not None:
                    return True
            return False




