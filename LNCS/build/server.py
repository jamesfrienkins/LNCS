import time
import socket
import threading
from os import system as cmd
from datetime import datetime

class newServer:
    HEADER = 64
    PORT = 55000
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "[DISCONNECT]"
    CHECK_CONNECTION_MESSAGE  = "[CHECK_CONNECTION]"
    GET_CLIENT_NAME = "[GET_CLIENT_NAME]"
    TEXT_MESSAGE = "[TEXT]"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listAllIndex = ["[CURRENT_SESSION_KEY]", "[CURRENT_CLIENT_LOG]", "[CURRENT_SERVER_LOG]", "[CURRENT_SYSTEM_STATUS]", "[SERVER_PORT]", "[SYSTEM_IPV4], [SYSTEM_NAME]"]
    dataValues = "data_values.txt"
    log = ""

    clientConnections = {}

    entryLog = []
    clientList = []
    clientId = {}

    serverIsRunning = False
    activeClients = 0

    def __updateClientStatus__(self, connected):
        if connected:
            return "Connected"
        else:
            return "Disconnected"

    def __init__(self, __PORT__ = 55000):
        self.PORT = __PORT__
        self.ADDR = (self.SERVER, __PORT__)
        cmd('cls')

    def __rewriteLine__(self, file, lineKey, newLine):
        currentFile = open(file, "r")
        listAllLines = currentFile.readlines()

        listAllLines[self.listAllIndex.index(lineKey)] = lineKey + ' <-> ' + newLine + '\n'

        currentFile = open(file, "w")
        currentFile.writelines(listAllLines)
        currentFile.close()
        
    def handle_client(self, conn, addr):
        clientInfo = [None, None, None, None]
        self.clientId[addr] = True
        connected = True

        timeStart = time.time()

        clnt_addr = addr[0]
        clientInfo[0] = clnt_addr

        try:
            while connected and self.clientId.get(addr):
                clientInfo[3] = round(time.time() - timeStart + 0.01, 2)
                clientInfo[2] = self.__updateClientStatus__(connected)
                self.clientConnections[addr[0]] = clientInfo
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)

                if msg_length:
                    msg_length = int(msg_length)
                    msgKey, msgValue = str(conn.recv(msg_length).decode(self.FORMAT)).split(" --> ")


                    if msgKey == self.DISCONNECT_MESSAGE:
                        connected = False
                        clientInfo[2] = self.__updateClientStatus__(connected)
                        conn.send("NONE".encode(self.FORMAT))
                    elif msgKey == self.CHECK_CONNECTION_MESSAGE:
                        conn.send(str(self.CHECK_CONNECTION_MESSAGE).encode(self.FORMAT))
                    elif msgKey == self.GET_CLIENT_NAME:
                        clientInfo[1] = msgValue
                    elif msgKey == self.TEXT_MESSAGE:
                        self.log.write(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgValue}\n")
                        self.log.flush()
                        self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgValue}")
                        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgValue}")

                        conn.send("NONE".encode(self.FORMAT))
                    else:
                        self.log.write(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgKey} {msgValue}\n")
                        self.log.flush()
                        self.entryLog(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgKey} {msgValue}")
                        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgKey} {msgValue}")

                        conn.send("NONE".encode(self.FORMAT))
        except:
            connected = False
            clientInfo[2] = self.__updateClientStatus__(connected)
            self.log.write(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Client don't respond.\n")
            self.log.flush()
            self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Client don't respond.")
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Client don't respond.")
        try:
            conn.close()
        except:
            pass

        if self.clientId.get(addr):
            self.clientId[addr] = False
            self.clientList.remove(addr)
            self.activeClients -= 1

            connected = False
            clientInfo[2] = self.__updateClientStatus__(connected)
            
            self.log.write(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Disconnected by client. Active connections = {self.activeClients}\n")
            self.log.flush()
            self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Disconnected by client. Active connections = {self.activeClients}")
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Disconnected by client. Active connections = {self.activeClients}")
            
    def __start__(self):
        try:
            self.log.write(f"[{datetime.now().strftime('''%H:%M:%S''')}] [STARTING...] Server is starting...\n")
            self.log.flush()
            self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [STARTING...] Server is starting...")
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [STARTING...] Server is starting...")

            self.server.listen()

            self.log.write(f"[{datetime.now().strftime('''%H:%M:%S''')}] [LISTENING] Server is listening on {self.SERVER}:{self.PORT}\n")
            self.log.flush()
            self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [LISTENING] Server is listening on {self.SERVER}:{self.PORT}")
            print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [LISTENING] Server is listening on {self.SERVER}:{self.PORT}")

            while self.serverIsRunning:
                conn, addr = self.server.accept()
                self.clientList.append(addr)
                thread = threading.Thread(target = self.handle_client, args = (conn, addr), daemon = True)

                thread.start()

                self.activeClients += 1
                self.log.write(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING] {addr} Active connections = {self.activeClients}\n")
                self.log.flush()
                self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING] {addr} Active connections = {self.activeClients}")
                print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING] {addr} Active connections = {self.activeClients}")
        except:
            pass

    def start(self):
        self.server.bind(self.ADDR)
        self.serverIsRunning = True

        self.log = open(f"log-server-{self.SERVER}.{self.PORT}.txt", 'a+')

        self.__rewriteLine__(self.dataValues, self.listAllIndex[2], f"log-server-{self.SERVER}.{self.PORT}.txt")

        self.entryLog = self.log.readlines()

        startServer = threading.Thread(target = self.__start__, args = (), daemon = True)
        startServer.start()
    
    def returnClientDataList(self):
        return list(self.clientConnections.values())

    def close(self):
        for clientIP in self.clientList:
            if self.clientId.get(clientIP) == True:
                self.clientId[clientIP] = False
                self.activeClients -= 1
                self.log.write(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {clientIP} Disconnected by server. Active connections = {self.activeClients}\n")
                self.log.flush()
                self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {clientIP} Disconnected by server. Active connections = {self.activeClients}")
                print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {clientIP} Disconnected by server. Active connections = {self.activeClients}")
                time.sleep(1)

        self.clientList = []

        self.server.close()
        self.log.write(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CLOSING...]\n")
        self.log.flush()
        self.entryLog.append(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CLOSING...]")
        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [CLOSING...]")