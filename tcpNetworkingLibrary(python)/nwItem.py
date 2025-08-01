from nwBuffer import NwBuffer
from nwPackage import NwPackage

class NwItem:

    def __init__(self, itemId: int, bufferSize: int):
        self.itemId = itemId
        self.buffer = NwBuffer(bufferSize)

    def add(self, var: any):
        package = NwPackage()
        package.create(self.itemId, var)
        if self.buffer.add(package):
            return True
        return False

    def grabNext(self):
        return self.buffer.grabNext()

    def getNewest(self):
        return self.buffer.getNewest()

    def updateVar(self, var: any):
        newVar = self.buffer.grabNext()
        if newVar is not None:
            var = newVar
            return True
        return False

    def getNitems(self):
        return self.buffer.getNitems()


class NwItemManager:
    def __init__(self, rxBuffer: NwBuffer, txBuffer: NwBuffer):
        self.rxBuffer = rxBuffer
        self.txBuffer = txBuffer
        self.rxItems = []
        self.txItems = []

    def bindRxItem(self, item: NwItem):
        self.rxItems.append(item)

    def bindTxItem(self, item: NwItem):
        self.txItems.append(item)

    def update(self):
        checkNotOverflowing = True
        while not self.rxBuffer.isEmpty():
            nextRxItem = self.rxBuffer.grabNext()
            sortId, payload = nextRxItem.deserialize()
            for thisItem in self.rxItems:
                if sortId is thisItem.itemId:
                    thisItem.buffer.add(payload)
        for eachItem in self.txItems:
            while not eachItem.buffer.isEmpty():
                nextItem = eachItem.buffer.grabNext()
                if nextItem is not None:
                    if not self.txBuffer.add(nextItem):
                        checkNotOverflowing = False
        return checkNotOverflowing

                    


