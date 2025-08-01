import socket
import threading
import queue
from datetime import datetime
from time import sleep

class NwTcpConnection:

    def __init__(self, isHost: bool, ip: str, port: int, readSize: int,debugMode:bool = False):
        self.debugMode = debugMode
        self.isHost = isHost
        self.isRunning = threading.Event()
        self.isRunning.set()
        self.readSize = readSize
        self.keepReceiving = threading.Event()
        if self.isHost:
            self.keepReceiving.set()
        self.serverSocket = None
        self.connection = None
        self.ip = ip
        self.port = port
        self.rxQueue = queue.Queue()
        self.txThread = None
        self.txQueue = None
        self.isDisconnected = threading.Event()
        self.waitReturnQueue = queue.Queue()
        self.isConnected = threading.Event()
        self.acceptThread = None
        self.setupConnection()

    def setupHostConnection(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.ip, self.port))
        self.serverSocket.listen()
        self.hostWaitForConnection()

    def setupClientConnection(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientConnect()
        self.keepReceiving.set()

    def clientConnect(self):
        try:
            self.connection.connect((self.ip, self.port))
            if self.debugMode:
                print("CLIENT CONNECTED")
        except Exception:
            if self.debugMode:
                print("ERROR: CLIENT CONNECTION FAILED")
            self.connection = None

    def hostWaitForConnection(self):
        if self.debugMode:
            print("HOST WAITING FOR CONNECTION")
        self.waitReturnQueue.put(self.serverSocket)
        self.acceptThread = threading.Thread(target=self.hostAcceptConnection,)
        self.acceptThread.start()

    def hostAcceptConnection(self):
        try:
            socket = self.waitReturnQueue.get()
            connection, clientAdress = socket.accept()
            self.keepReceiving.set()
            if self.isDisconnected.is_set():
                self.isDisconnected.clear()
            self.waitReturnQueue.put(connection)
            self.isConnected.set()
            if self.debugMode:
                print("HOST INCOMMING CONNECTION ACCEPTED")
        except OSError:
            pass

    def setupConnection(self):
        if self.isHost:
            if self.debugMode:
                print("CREATING CONNECTION AS HOST")
            self.setupHostConnection()
        else:
            if self.debugMode:
                print("CREATING CONNECTION AS CLIENT")
            self.setupClientConnection()
        self.receiveThread = threading.Thread(target=self.receiveData,)
        self.keepSending = threading.Event()
        self.receiveThread.start()

    def shutdown(self):
        if self.debugMode:
            print("CLOSING CONNECTION")
        if self.txQueue is not None: 
            while not self.txQueue.empty() and not self.isDisconnected.is_set():
                sleep(0.1)
        self.isRunning.clear()
        self.keepSending.clear()
        if self.txThread is not None and not self.txQueue.empty():
            self.txThread.join()
        self.keepReceiving.clear()
        if self.connection is not None:
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            self.connection.close()
        if self.serverSocket:
            self.serverSocket.close()
        self.receiveThread.join()
        self.isConnected.clear()

    def receiveData(self):
        while self.keepReceiving.is_set():
            try:
                data = self.connection.recv(self.readSize)
                if data:
                    self.rxQueue.put(data)
                else:
                    self.isDisconnected.set()
            except Exception:
                pass

    def send(self, data: bytes):
        if self.connection is not None and data is not None:
            try:
                self.connection.sendall(data)
                return True
            except Exception:
                pass
            return False

    def autoSend(self, tickRate: int):
        sendDelay = 1 / tickRate
        while self.keepSending.is_set():
            currentDateTime = datetime.now()
            currentTime = currentDateTime.timestamp()
            if not self.txQueue.empty() and self.connection is not None:
                toTransmit = self.txQueue.get()
                self.send(toTransmit)
            doneDateTime = datetime.now()
            doneTime = doneDateTime.timestamp()
            if doneTime < currentTime+ sendDelay:
                sleep(currentTime + sendDelay - doneTime)

    def setupAutoSender(self, tickRate: int):
        self.keepSending.set()
        self.txQueue = queue.Queue()
        self.txThread = threading.Thread(target=self.autoSend, args=(tickRate,))
        self.txThread.start()

    def update(self):
        if self.connection is not None and self.isDisconnected.is_set():
            self.connection = None
            if self.debugMode:
                print("MANAGING DISCONNECTION")
            if self.isHost:
                if self.debugMode:
                    print("REOPEN HOST CONNECTION")
                self.hostWaitForConnection()

            else:
                if self.debugMode:
                    print("CLIENT ATTEMPT RECONNECT")
                self.clientConnect()

        if not self.isHost and self.connection is None:
            if self.debugMode:
                print("CLIENT ATTEMPT TO CONNECT")
            self.setupClientConnection()

        if self.isHost:
            if self.isConnected.is_set():
                self.connection = self.waitReturnQueue.get()    
                self.isConnected.clear()
                self.acceptThread.join()


