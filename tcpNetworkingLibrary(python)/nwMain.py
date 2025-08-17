import threading
from nwManager import NwManager

def host(): # example of a host setup (here running on a seperate thread)
    print("Host")
    host = NwManager(5,20,20,60) # debug mode is avaiable. to create multiple connections create multiple manager instances and choose a different port and/or ip
    host.createConnection(True,"127.0.0.1",65432) # creates a host connection with the given ip and port

    hostRx = host.createRxItem(1,10) # creates receiving and transmittion items with the item-id 1 and a buffer size of 10 (item ids have to be shared between client and host and represent one variable shared across the instances)
    hostTx = host.createTxItem(1,10)

    hostRx2 = host.createRxItem(2,10) # creates receiving and transmittion items with the item-id 2 and a buffer size of 10
    hostTx2 = host.createTxItem(2,10)

    for i in range(0,10): # adds example numbers to the transmittion items to be shared with the client connection
        hostTx.add(i)
        hostTx2.add(i)

    hostADone = False # waits untill all data is confirmed to be returned by the client
    hostBDone = False
    while not (hostADone and hostBDone):

        host.update() # sorts all incomming data by incomming id to the matching item and will send all buffered data by all items
        
        check = hostRx.getNewest() # getNewest returns the data last added to the buffer
        if(check is not None):
            if(check >= 9):
                hostADone = True
         
        check2 = hostRx2.getNewest()
        if(check2 is not None):
            if(check2 >= 9):
                hostBDone = True

    print(f"A{hostRx.buffer.items}") # shows the returned data
    print(f"B{hostRx2.buffer.items}")

    host.cleanup() # cleans up the conection
    print("host complete")

def client(): # example of a client setup (exept connection mode same as host)
    print("Client")
    client = NwManager(5,20,20,60) # debug mode is avaiable
    client.createConnection(False,"127.0.0.1",65432)
    clientRx = client.createRxItem(1,10)
    clientTx = client.createTxItem(1,10)

    clientRx2 = client.createRxItem(2,10)
    clientTx2 = client.createTxItem(2,10)

    clientAdone = False # waits untill all data is returned
    clientBdone = False
    while not (clientAdone and clientBdone):
        client.update()
        if clientRx.getNewest() == 9:
            while True:
                nextOne = clientRx.grabNext() # grabNext() will return the oldest item in the buffer and removes it to make space for new data (should the buffer overflow the oldest data will be removed first, should that be an issue increase buffer sizes. buffer overflows will be shown if debugmode is set to True)
                if nextOne is None:
                    clientAdone = True
                    break
                clientTx.add(nextOne) # adds the received data to be returned to sender
                print(f"received: A{nextOne} returning...")

        if clientRx2.getNewest() == 9:
            while True:
                nextOne2 = clientRx2.grabNext()
                if nextOne2 is None:
                    clientBdone = True
                    break
                clientTx2.add(nextOne2)
                print(f"received: B{nextOne2} returning...")

    client.cleanup() # closes the connection
    print("client complete")
    

def test(): # sets up a host-client example in different threads (client remains on the main thread)
    hostThread = threading.Thread(target=host)
    hostThread.start()
    client()
    hostThread.join()
  

if __name__ == "__main__":
    test()


