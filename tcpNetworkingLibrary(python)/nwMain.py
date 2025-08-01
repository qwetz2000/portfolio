import threading
from nwManager import NwManager

def host():
    print("Host")
    host = NwManager(5,20,20,60)
    host.createConnection(True,"127.0.0.1",65432)
    hostRx = host.createRxItem(1,10)
    hostTx = host.createTxItem(1,10)

    hostRx2 = host.createRxItem(2,10)
    hostTx2 = host.createTxItem(2,10)

    for i in range(0,10):
        hostTx.add(i)
        hostTx2.add(i)

    hostADone = False
    hostBDone = False
    while not (hostADone and hostBDone):

        host.update()
        
        check = hostRx.getNewest()
        if(check is not None):
            if(check >= 9):
                hostADone = True
         
        check2 = hostRx2.getNewest()
        if(check2 is not None):
            if(check2 >= 9):
                hostBDone = True

    print(f"A{hostRx.buffer.items}")
    print(f"B{hostRx2.buffer.items}")

    host.cleanup()
    print("host complete")

def client():
    print("Client")
    client = NwManager(5,20,20,60)
    client.createConnection(False,"127.0.0.1",65432)
    clientRx = client.createRxItem(1,10)
    clientTx = client.createTxItem(1,10)

    clientRx2 = client.createRxItem(2,10)
    clientTx2 = client.createTxItem(2,10)

    clientAdone = False
    clientBdone = False


    while not (clientAdone and clientBdone):
        client.update()
        if clientRx.getNewest() == 9:
            while True:
                nextOne = clientRx.grabNext()
                if nextOne is None:
                    clientAdone = True
                    break
                clientTx.add(nextOne)
                print(f"received: A{nextOne} returning...")

        if clientRx2.getNewest() == 9:
            while True:
                nextOne2 = clientRx2.grabNext()
                if nextOne2 is None:
                    clientBdone = True
                    break
                clientTx2.add(nextOne2)
                print(f"received: B{nextOne2} returning...")

    client.cleanup()
    print("client complete")
    

def test():
    hostThread = threading.Thread(target=host)
    hostThread.start()
    client()
    hostThread.join()
  

if __name__ == "__main__":
    test()


