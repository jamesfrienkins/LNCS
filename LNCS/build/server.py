import time
import socket
import os.path
import threading
from os import walk
from os import system as cmd
from datetime import datetime

class newServer:
    HEADER = 64
    PORT = 55000
    CHUNKSIZE = 1000000
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "[DISCONNECT]"
    GET_PORT_MESSAGE = "[GET_PORT_MESSAGE]"
    CHECK_CONNECTION_MESSAGE  = "[CHECK_CONNECTION]"
    GET_CLIENT_NAME = "[GET_CLIENT_NAME]"
    TEXT_MESSAGE = "[TEXT]"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listAllIndex = ["[CURRENT_SESSION_KEY]", "[CURRENT_CLIENT_LOG]", "[CURRENT_SERVER_LOG]", "[CURRENT_SYSTEM_STATUS]", "[SERVER_PORT]", "[SYSTEM_IPV4], [SYSTEM_NAME]"]
    clientPortNameForFiles = {}
    pathToTarget = {}
    clientIpPort = {}
    
    log = ""

    currentPath = os.path.dirname(os.path.realpath(__file__))
    dataValues = f"{currentPath}\data\data_values.txt"
    clientConnections = {}

    listFilesToSend = []
    entryLog = []
    clientList = []
    clientId = {}

    serverIsRunning = False
    activeClients = 0
    maxActiveClients = 0

    def output(self, value):
        self.log.write(value + "\n")
        self.log.flush()
        self.entryLog.append(value)
        print(value)

    def checkIPV4(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def sendFolder(self, pathToFolders, client):        
        k = True

        if not self.checkIPV4(client):
            k = False
            for data in self.clientDataList:
                name = data[1]
                if name == client:
                    k = True
                    client = data[0]

        if k:
            v = self.pathToTarget.get(self.clientIpPort.get(client))
            if v != None:
                for p in pathToFolders:
                    v.append(p)
            else:
                valueOutput = (f'''[{datetime.now().strftime("%H:%M:%S")}] [ERROR] File sending failed. Client "{client}" isn't connected.\n''')
                self.output(valueOutput)
        else:
            if self.checkIPV4(client):
                valueOutput = (f'''[{datetime.now().strftime("%H:%M:%S")}] [ERROR] File sending failed. Incorrect ip "{client}" or client isn't connected.''')
                self.output(valueOutput)
            else:
                valueOutput = (f'''[{datetime.now().strftime("%H:%M:%S")}] [ERROR] File sending failed. Incorrect name "{client}" or client isn't connected.''')
                self.output(valueOutput)

    def __sendFolder__(self, addr):
        key = addr[0]
        sock = socket.socket()
        clntAddr = (socket.gethostbyname(socket.gethostname()), int(self.clientPortNameForFiles.get(addr)))
        sock.bind(clntAddr)
        sock.listen()

        sock.settimeout(0.5)

        print(clntAddr)

        self.pathToTarget[addr] = []
        k = f"{addr[0]}.{str(addr[1])}"

        while self.clientId.get(k):
            values = self.pathToTarget.get(addr)

            if values != []:
                value = values.pop(0)
                self.pathToTarget[addr[0]] = values
                client, _ = sock.accept()
                sd = value

                if not os.path.isdir(value):
                    cmd(f"mkdir {self.currentPath}\cashe\{key}")
                    cmd(f'''copy "{value}" "{self.currentPath}\cashe\{key}"''')
                    value = f"{self.currentPath}\cashe\{key}"
                with client:
                    try:
                        for path, _, files in walk(value):
                            valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [FILE] Sending {sd}")
                            self.output(valueOutput)

                            for file in files:
                                filename = os.path.join(path, file)
                                relpath = os.path.relpath(filename, value)
                                filesize = os.path.getsize(filename)


                                with open(filename, 'rb') as f:
                                    client.sendall(relpath.encode() + b'\n')
                                    client.sendall(str(filesize).encode() + b'\n')

                                    while True:
                                        data = f.read(self.CHUNKSIZE)
                                        if not data:
                                            break
                                        client.sendall(data)
                        valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [FILE] Sending {sd} finished.")
                        self.output(valueOutput)
                    except:
                        valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [FILE] Sending {sd} failed.")
                        self.output(valueOutput)

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
        self.clientIpPort[addr[0]] = addr
        clientInfo = [None, None, None, None]
        self.clientId[f"{addr[0]}.{addr[1]}"] = True
        self.clientPortNameForFiles[addr] = (self.PORT + self.maxActiveClients + 1)
        connected = True

        timeStart = time.time()

        clnt_addr = addr[0]
        clientInfo[0] = clnt_addr

        threadAdditional = threading.Thread(target = self.__sendFolder__, args = (addr,), daemon = True)
        threadAdditional.start()

        try:
            while connected and self.clientId.get(f"{addr[0]}.{addr[1]}"):
                clientInfo[3] = round(time.time() - timeStart + 0.02, 2)
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
                    elif msgKey == self.GET_PORT_MESSAGE:
                        conn.send(str(self.clientPortNameForFiles.get(addr)).encode(self.FORMAT))
                    elif msgKey == self.CHECK_CONNECTION_MESSAGE:
                        conn.send(str(self.CHECK_CONNECTION_MESSAGE).encode(self.FORMAT))
                    elif msgKey == self.GET_CLIENT_NAME:
                        clientInfo[1] = msgValue
                    elif msgKey == self.TEXT_MESSAGE:
                        valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgValue}\n")
                        self.output(valueOutput)
                        conn.send("NONE".encode(self.FORMAT))
                    else:
                        valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [MESSAGE] {addr} {msgKey} {msgValue}\n")
                        self.output(valueOutput)
                        conn.send("NONE".encode(self.FORMAT))
        except:
            connected = False
            clientInfo[2] = self.__updateClientStatus__(connected)
            valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Client don't respond. Active connections = {self.activeClients - 1}\n")
            self.output(valueOutput)

        try:
            conn.close()
        except:
            pass

        if self.clientId.get(f"{addr[0]}.{addr[1]}"):
            self.clientId[f"{addr[0]}.{addr[1]}"] = False
            self.clientList.remove(addr)
            self.activeClients -= 1
            clientInfo[2] = self.__updateClientStatus__(connected)

            if connected:
                connected = False
                
                valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {addr} Disconnected by client. Active connections = {self.activeClients}\n")
                self.output(valueOutput)

    def __start__(self):
        try:
            valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [STARTING...] Server is starting...\n")
            self.output(valueOutput)

            self.server.listen()

            valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [LISTENING] Server is listening on {self.SERVER}:{self.PORT}\n")
            self.output(valueOutput)

            while self.serverIsRunning:
                conn, addr = self.server.accept()
                self.clientList.append(addr)

                threadMain = threading.Thread(target = self.handle_client, args = (conn, addr), daemon = True)

                threadMain.start()

                self.activeClients += 1
                self.maxActiveClients += 1
                valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING] {addr} Active connections = {self.activeClients}\n")
                self.output(valueOutput)
        except:
            pass

    def start(self):
        self.server.bind(self.ADDR)
        self.serverIsRunning = True

        self.log = open(f"{self.currentPath}\data\log-server-{self.SERVER}.{self.PORT}.txt", 'a+')

        self.__rewriteLine__(self.dataValues, self.listAllIndex[2], f"{self.currentPath}\log-server-{self.SERVER}.{self.PORT}.txt")

        self.entryLog = self.log.readlines()

        startServer = threading.Thread(target = self.__start__, args = (), daemon = True)
        startServer.start()
    
    def returnClientDataList(self):
        self.clientDataList = list(self.clientConnections.values())

        return self.clientDataList

    def close(self):
        for clientIP in self.clientList:
            if self.clientId.get(clientIP) == True:
                self.clientId[clientIP] = False
                self.activeClients -= 1
                valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {clientIP} Disconnected by server. Active connections = {self.activeClients}\n")
                self.output(valueOutput)

                time.sleep(1)

        self.clientList = []

        self.server.close()
        valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [CLOSING...]\n")
        self.output(valueOutput)
