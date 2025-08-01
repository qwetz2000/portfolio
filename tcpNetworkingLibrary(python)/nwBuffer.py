class NwBuffer:

    def __init__(self, size: int):
        if size < 1:
            self.size = 1
        else:
            self.size = size
        self.items = []

    def getNewest(self):
        if self.items:
            return self.items[-1]
        else:
            return None

    def add(self, item: any):
        notOverflowing = True
        if item is not None:
            if len(self.items) >= self.size:
                self.items.pop(0)
                notOverflowing = False
            self.items.append(item)
        return notOverflowing

    def grabNext(self):
        if self.items:
            return self.items.pop(0)
        else:
            return None

    def isEmpty(self):
        if len(self.items) <= 0:
            return True
        return False

    def getNitems(self):
        return len(self.items)

