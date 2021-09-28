import time
import string
import random
import socket
import threading
import server as srvr
import client as clnt
from os import system as cmd
from datetime import datetime
from os import startfile, path

cmd('cls')

currentSystemIPV4 = socket.gethostbyname(socket.gethostname())
listAllIndex = ["[CURRENT_SESSION_KEY]", "[CURRENT_CLIENT_LOG]", "[CURRENT_SERVER_LOG]", "[CURRENT_SYSTEM_STATUS]", "[SERVER_PORT]", "[SYSTEM_IPV4]", "[SYSTEM_NAME]", "[SAVE_FILE_LOCATION]"]
currentPath = path.dirname(path.realpath(__file__))
IPV4, PORT, SYSTEM_NAME = None, None, None
dataValues = f"{currentPath}\data\data_values.txt"
print(currentPath)
SAVE_FILE_LOCATION = ""
client, server = None, None
serverDataToSend = None
serverDataValues = None

def checkIPV4(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def returnValue(file, lineKey):
    currentFile = open(file, "r")
    listAllLines = currentFile.readlines()

    line = listAllLines[listAllIndex.index(lineKey)].split(' <-> ')
    value = line[1].strip()
    
    return value

def rewriteLine(file, lineKey, newLine):
    currentFile = open(file, "r")
    listAllLines = currentFile.readlines()

    listAllLines[listAllIndex.index(lineKey)] = str(lineKey) + ' <-> ' + str(newLine) + '\n'

    currentFile = open(file, "w")
    currentFile.writelines(listAllLines)
    currentFile.close()

def getServerData():
    global serverDataToSend, serverDataValues
    while True:
        serverDataValues = server.returnClientDataList()

        serverDataToSend = ""

        if serverDataValues != None:
            for f in serverDataValues:
                for i in f:
                    serverDataToSend += str(i) + '<>'
                serverDataToSend = serverDataToSend[:-2]
                serverDataToSend += '<|>'
            serverDataToSend = serverDataToSend[:-3]

        time.sleep(1)

def sendServerData():
    global serverDataToSend

    while True:
        s = socket.socket()
        port = 55499
        s.bind((socket.gethostbyname(socket.gethostname()), port))         
        s.listen()

        while True:
            try:
                c, _ = s.accept()
                c.send(serverDataToSend.encode('utf-8'))
                c.close()
            except:
                pass

def setUpCurrentSystemStatus():
    global IPV4, PORT, SYSTEM_NAME, SAVE_FILE_LOCATION

    cmd('cls')

    try:
        currentFile = open(dataValues, "r")
    except:
        currentFile = open(dataValues, "a+")
        for keyName in listAllIndex:
            currentFile.write(keyName + ' <-> \n')
        currentFile = open(dataValues, "r")

    currentFile.flush()
    listAllLines = currentFile.readlines()
    line = listAllLines[3].split(' <-> ')
    systemStatus = line[1].strip()
    setUpKey = True

    if systemStatus == 'admin' or systemStatus == 'client':
        PORT = returnValue(dataValues, listAllIndex[4])
        IPV4 = returnValue(dataValues, listAllIndex[5])
        if systemStatus == 'client':
            SYSTEM_NAME = returnValue(dataValues, listAllIndex[6])
            SAVE_FILE_LOCATION = returnValue(dataValues, listAllIndex[7])
    else:
        while setUpKey:
            try:
                systemStatus = input("\nWelcome to LNCS!\n\nPlease set up your system...\nPrint 'admin' if your are admin, 'client' if your are a client, 'e' for exit: ")

                if systemStatus == 'admin' or systemStatus == 'client':
                    while True:
                        confirmation = input(f"\nYou chose {systemStatus} system status. Please confirm your choice (y/n): ")

                        if confirmation == 'y':
                            setUpKey = False
                            break

                        else:
                            cmd('cls')
                            break
                elif systemStatus == 'e':
                    exit()
                else:
                    cmd('cls')
            except:
                cmd('cls')

        rewriteLine(dataValues, listAllIndex[3], systemStatus)
        setUpKey = True
        
        while setUpKey:
            try:
                cmd('cls')
                print("Set up your system...\n\n")
                print(f"Current system ipv4: {currentSystemIPV4}")
                if systemStatus == 'client':
                    IPV4, PORT = input("Enter server addres IPV4, PORT(55000 ≈ 70000) in format (IPV4:PORT): ").split(':')
                    if checkIPV4(IPV4) and int(PORT) >= 55000 and int(PORT) <= 70000:
                        setUpKey = False
                elif systemStatus == 'admin':
                    PORT = input("Enter PORT (55000 ≈ 70000): ")
                    IPV4 = currentSystemIPV4
                    
                    if int(PORT) >= 55000 and int(PORT) <= 70000:
                        setUpKey = False
            except:
                cmd('cls')

        rewriteLine(dataValues, listAllIndex[3], systemStatus)
        
        if systemStatus == 'client':
            setUpKey = True
            while setUpKey:
                try:
                    cmd('cls')
                    print("Set up your system...\n\n")
                    SYSTEM_NAME = input("Enter current system name (will be displayed at server): ")
                    if SYSTEM_NAME[0] not in string.digits:
                        setUpKey = False
                except:
                    cmd('cls')

            setUpKey = True
            while setUpKey:
                try:
                    cmd('cls')
                    print("Set up your system...\n\n")
                    SAVE_FILE_LOCATION = input("Enter location of folder for saving files: ")
                    if path.isdir(SAVE_FILE_LOCATION):
                        setUpKey = False
                except:
                    cmd('cls')
        
        rewriteLine(dataValues, listAllIndex[4], PORT)
        rewriteLine(dataValues, listAllIndex[5], IPV4)
        rewriteLine(dataValues, listAllIndex[6], SYSTEM_NAME)
        rewriteLine(dataValues, listAllIndex[7], SAVE_FILE_LOCATION)
        
        print(f"Your system is running on {IPV4}:{PORT}")
            
    return systemStatus

def systemStatusAdmin():
    global server

    gsd = threading.Thread(target = getServerData, args = (), daemon = True)
    ssd = threading.Thread(target = sendServerData, args = (), daemon = True)
    server = srvr.newServer(__PORT__ = int(PORT))

    server.start()
    gsd.start()
    ssd.start()

    time.sleep(120)

def systemStatusClient():
    global client

    client = clnt.newClient()
    client.start(__SERVER__ = IPV4, __PORT__ = int(PORT), __SYSTEM_NAME__ = SYSTEM_NAME, __SAVE_FILE_LOCATION__ = SAVE_FILE_LOCATION)
    client.connect()
    client.send('Hello world!')
    time.sleep(5)
    client.send('Msg1 delay 5 sec')
    time.sleep(5)
    client.send('Msg2 delay 5 sec')
    time.sleep(10)
    client.send('Msg3 delay 10 sec')
    time.sleep(10)
    client.send('Msg4 delay 10 sec')   


def main(startConnectionStatus = False):
    cmd(f"mkdir {currentPath}\cashe")
    cmd(f"attrib +h {currentPath}\cashe")
    cmd(f"mkdir {currentPath}\data")
    cmd(f"attrib +h {currentPath}\data")

    systemStatus = setUpCurrentSystemStatus()

    currentSessionKey = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = 16))

    rewriteLine(dataValues, listAllIndex[0], currentSessionKey)

    if systemStatus == 'admin':
        systemAdmin = threading.Thread(target = systemStatusAdmin, args = (), daemon = True)
        systemAdmin.start()

        time.sleep(1)

        if startConnectionStatus:
            try:
                startfile(f'{currentPath}\connectionStatus.exe')
                print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [STARTING] ConnectionStatus.exe is starting.")
            except:
                print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [ERROR] ConnectionStatus.exe is missing.")
        
        time.sleep(75)

    else:
        systemClient = threading.Thread(target = systemStatusClient, args = (), daemon = True)
        systemClient.start()

        time.sleep(25)


if __name__ == "__main__":
    try:
        main(startConnectionStatus = True)
    except KeyboardInterrupt:
        print(f"[{datetime.now().strftime('''%H:%M:%S''')}] [ERROR] Forced termination by user.")
