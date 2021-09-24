import time
import string
import random
import socket
import threading
import server as srvr
import client as clnt
from os import system as cmd

currentSystemIPV4 = socket.gethostbyname(socket.gethostname())
listAllIndex = ["[CURRENT_SESSION_KEY]", "[CURRENT_CLIENT_LOG]", "[CURRENT_SERVER_LOG]", "[CURRENT_SYSTEM_STATUS]", "[SERVER_PORT]", "[SYSTEM_IPV4]", "[SYSTEM_NAME]"]
dataValues = "data_values.txt"
IPV4, PORT, SYSTEM_NAME = None, None, None
client, server = None, None
serverDataToSend = None

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

    listAllLines[listAllIndex.index(lineKey)] = lineKey + ' <-> ' + newLine + '\n'

    currentFile = open(file, "w")
    currentFile.writelines(listAllLines)
    currentFile.close()

def getServerData():
    global serverDataToSend
    while True:
        serverDataValues = server.returnClientDataList()

        serverDataToSend = ""

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
            c, addr = s.accept()
            c.send(serverDataToSend.encode('utf-8'))
            c.close()

def setUpCurrentSystemStatus():
    global IPV4, PORT, SYSTEM_NAME

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
            SYSTEM_NAME = returnValue(dataValues, listAllIndex[5])
    else:
        while setUpKey:
            try:
                systemStatus = input("\nWelcome to LNCS!\n\nPlease set up your system...\nPrint 'admin' if your are admin, 'client' if your are a client, 'e' for exit: ")

                if systemStatus == 'admin' or systemStatus == 'client':
                    while True:
                        confirmation = input(f"\nYour chose {systemStatus} system status. Please confirm your choice (y/n): ")

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
                cmd('clr')

        rewriteLine(dataValues, listAllIndex[3], systemStatus)
        setUpKey = True
        
        while setUpKey:
            try:
                cmd('cls')
                print("Set up your system...\n\n")
                print(f"Current system ipv4: {currentSystemIPV4}")
                if systemStatus == 'client':
                    IPV4, PORT = input("Print server addres IPV4, PORT(55000 ≈ 70000) in format (IPV4:PORT): ").split(':')
                    if checkIPV4(IPV4) and int(PORT) >= 55000 and int(PORT) <= 70000:
                        setUpKey = False
                elif systemStatus == 'admin':
                    PORT = input("Print PORT (55000 ≈ 70000): ")
                    IPV4 = currentSystemIPV4
                    
                    if int(PORT) >= 55000 and int(PORT) <= 70000:
                        setUpKey = False
            except:
                cmd('clr')

        rewriteLine(dataValues, listAllIndex[3], systemStatus)
        
        if systemStatus == 'client':
            setUpKey = True
            while setUpKey:
                try:
                    cmd('cls')
                    print("Set up your system...\n\n")
                    SYSTEM_NAME = input("Create current system name (will be displayed at server): ")
                    if SYSTEM_NAME[0] not in string.digits:
                        setUpKey = False
                except:
                    cmd('clr')
        
        rewriteLine(dataValues, listAllIndex[4], PORT)
        rewriteLine(dataValues, listAllIndex[5], IPV4)
        rewriteLine(dataValues, listAllIndex[6], SYSTEM_NAME)
        
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

    time.sleep(25)

def systemStatusClient():
    global client

    client = clnt.newClient()
    client.start(__SERVER__ = IPV4, __PORT__ = int(PORT), __SYSTEM_NAME__ = SYSTEM_NAME)
    client.connect()
    client.send('Hello!')
    time.sleep(2)

def main():
    systemStatus = setUpCurrentSystemStatus()

    currentSessionKey = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = 16))

    rewriteLine(dataValues, listAllIndex[0], currentSessionKey)

    if systemStatus == 'admin':
        systemStatusAdmin()
    else:
        systemStatusClient()



if __name__ == "__main__":
    main()