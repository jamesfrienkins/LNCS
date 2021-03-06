import os
import time
import socket
import threading
import stream_client
from os import system as cmd
from datetime import datetime

class newClient:
    HEADER = 64
    FORMAT = 'utf-8'
    SYSTEM_NAME = ""
    DISCONNECT_MESSAGE = "[DISCONNECT]"
    CHECK_CONNECTION_MESSAGE  = "[CHECK_CONNECTION]"
    GET_PORT_MESSAGE = "[GET_PORT_MESSAGE]"
    GET_CLIENT_NAME = "[GET_CLIENT_NAME]"
    CMD_MESSAGE = "[CMD]"
    TEXT_MESSAGE = "[TEXT]"
    START_STREAM = "[START_STREAM]"
    GET_STREAM_PORT = "[GET_STREAM_PORT]"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER = socket.gethostbyname(socket.gethostname())
    listAllIndex = ["[CURRENT_SESSION_KEY]", "[CURRENT_CLIENT_LOG]", "[CURRENT_SERVER_LOG]", "[CURRENT_SYSTEM_STATUS]", "[SERVER_PORT]", "[SYSTEM_IPV4], [SYSTEM_NAME]"]
    currentPath = os.path.dirname(os.path.realpath(__file__))
    dataValues = f"{currentPath}\data\data_values.txt"
    sendMessageList = []
    CHUNKSIZE = 1000000
    PORT_FOR_FILES = ""
    folderToSave = ""
    STREAM_PORT = ""
    PORT = 55000
    ADDR = (SERVER, PORT)
    log = ""

    entryLog = []

    client.settimeout(0.25)

    clientIsConnected = False

    def __init__(self):
        cmd('cls')

    def output(self, value):
        self.log.write(value + "\n")
        self.log.flush()
        self.entryLog.append(value)
        print(value)

    def __rewriteLine__(self, file, lineKey, newLine):
        currentFile = open(file, "r")
        listAllLines = currentFile.readlines()

        listAllLines[self.listAllIndex.index(lineKey)] = lineKey + ' <-> ' + newLine + '\n'

        currentFile = open(file, "w")
        currentFile.writelines(listAllLines)
        currentFile.close()

    def start(self, __SERVER__ = socket.gethostbyname(socket.gethostname()), __PORT__ = 55000, __SYSTEM_NAME__ = "", __SAVE_FILE_LOCATION__ = f"{currentPath}\saved_files"):
        self.PORT = __PORT__
        self.SERVER = __SERVER__
        self.SYSTEM_NAME = __SYSTEM_NAME__
        self.folderToSave = __SAVE_FILE_LOCATION__

        self.ADDR = (self.SERVER, self.PORT)

        self.log = open(f"{self.currentPath}\data\log-client-{__SERVER__}.{__PORT__}.txt", 'a+')

        self.__rewriteLine__(self.dataValues, self.listAllIndex[1], f"log-client-{__SERVER__}.{__PORT__}.txt")
        
        self.entryLog = self.log.readlines()
        valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [STARING...] Client starting on {self.SERVER}:{self.PORT}")
        self.output(valueOutput)

    def connect(self):
        try:
            self.client.connect(self.ADDR)
            
            valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Connected to {self.SERVER}:{self.PORT}...")
            self.output(valueOutput)

            sendThread = threading.Thread(target = self.__sendThread__, args = (), daemon = True)
            sendThread.start()

            self.clientIsConnected = True

            try:
                self.PORT_FOR_FILES = self.send__(msgKey = self.GET_PORT_MESSAGE, msgValue = self.GET_PORT_MESSAGE)
            except:
                pass

            try:
                self.STREAM_PORT = self.send__(msgKey = self.GET_STREAM_PORT, msgValue = self.GET_STREAM_PORT)
            except:
                pass

            self.stream = stream_client.__stream__(self.ADDR[0], int(self.STREAM_PORT))

            recieveFolderThread = threading.Thread(target = self.__recieveFolder__, args = (self.ADDR[0], self.PORT_FOR_FILES, self.folderToSave), daemon = True)
            recieveFolderThread.start()

            checkConnection = threading.Thread(target = self.__checkConnection__, args = (), daemon = True)

            try:
                self.send__(msgKey = self.GET_CLIENT_NAME, msgValue = self.SYSTEM_NAME)
            except:
                pass

            checkConnection.start()
        except:
            valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Can't connect to {self.SERVER}:{self.PORT}...")
            self.output(valueOutput)

    def disconnect(self):
        self.send__(self.DISCONNECT_MESSAGE, msgKey=self.DISCONNECT_MESSAGE)
        valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {self.ADDR} Disconnected by client.")
        self.output(valueOutput)
    
    def close(self):
        self.client.close()
        valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [CLOSING...]")
        self.output(valueOutput)

    def send(self, msgValue, msgKey = "[TEXT]"):
        self.sendMessageList.append([msgValue, msgKey])

    def __sendThread__(self):
        while True:
            if self.sendMessageList != [] and self.clientIsConnected:
                msgValue, msgKey = self.sendMessageList.pop(0)

                self.send__(msgValue, msgKey)

    def __recieveFolder__(self, ip, port, pathToSave):
        key = False
        while self.clientIsConnected:
            if key == False:
                sock = socket.socket()
                key = not key
            try:
                srvAddr = (ip, int(port))
                sock.connect(srvAddr)
                with sock,sock.makefile('rb') as clientfile:
                    while True:
                        raw = clientfile.readline()
                        if not raw: break

                        filename = raw.strip().decode()
                        length = int(clientfile.readline())

                        path = os.path.join(pathToSave,filename)
                        os.makedirs(os.path.dirname(path),exist_ok=True)

                        with open(path,'wb') as f:
                            while length:
                                chunk = min(length, self.CHUNKSIZE)
                                data = clientfile.read(chunk)
                                if not data: break
                                f.write(data)
                                length -= len(data)
                            else:
                                valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [FILE] File {filename} received successfully.")
                                self.output(valueOutput)
                                key = not key
                                continue

                        valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [FILE] {filename} Error occurred while file receiving.")
                        self.output(valueOutput)
                        break
            except:
                pass

    def send__(self, msgValue, msgKey = "[TEXT]"):
        if self.clientIsConnected:
            msg = msgKey + " --> " + msgValue

            if msgKey not in (self.CHECK_CONNECTION_MESSAGE, self.GET_CLIENT_NAME, self.CHECK_CONNECTION_MESSAGE, self.GET_PORT_MESSAGE, self.GET_STREAM_PORT):
                valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] {msg}")
                self.output(valueOutput)

            message = msg.encode(self.FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(self.FORMAT)
            send_length += b' ' * (self.HEADER - len(send_length))
            self.client.send(send_length)
            self.client.send(message)

            serverAnsw = "NONE"
            serverAnsw = str(self.client.recv(1024).decode(self.FORMAT))

            if serverAnsw != "NONE" and serverAnsw != self.CHECK_CONNECTION_MESSAGE and serverAnsw != self.START_STREAM and msgKey != self.CHECK_CONNECTION_MESSAGE and msgKey != self.GET_PORT_MESSAGE and msgKey != self.GET_STREAM_PORT:
                valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [SERVER ANSWER] {serverAnsw}")
                self.output(valueOutput)
        
            return serverAnsw
    
    def __checkConnection__(self):
        while True:
            if self.clientIsConnected:
                try:
                    answ = self.send__(msgValue = self.CHECK_CONNECTION_MESSAGE, msgKey = self.CHECK_CONNECTION_MESSAGE)

                    if answ != self.CHECK_CONNECTION_MESSAGE:
                        self.stream.start()
                except:
                    self.clientIsConnected = False
                    valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [DISCONNECTED] {self.ADDR} Server don't respond.")
                    self.output(valueOutput)
            else:
                try:
                    self.stream.close()
                except:
                    pass

                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    self.client.connect(self.ADDR)
                    self.clientIsConnected = True
                    valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Connected to {self.SERVER}:{self.PORT}...")
                    self.output(valueOutput)
                    self.PORT_FOR_FILES = self.send__(msgKey = self.GET_PORT_MESSAGE, msgValue = self.GET_PORT_MESSAGE)
                    recieveFolderThread = threading.Thread(target = self.__recieveFolder__, args = (self.ADDR[0], self.PORT_FOR_FILES, self.folderToSave), daemon = True)
                    recieveFolderThread.start()

                    try:
                        self.send__(msgKey = self.GET_CLIENT_NAME, msgValue = self.SYSTEM_NAME)
                    except:
                        pass

                except:
                    valueOutput = (f"[{datetime.now().strftime('''%H:%M:%S''')}] [CONNECTING...] Can't connect to {self.SERVER}:{self.PORT}...")
                    self.output(valueOutput)

            time.sleep(0.1)