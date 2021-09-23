import time
import string
import random
import socket
import server as srvr
import client as clnt
from os import system as cmd

currentSystemIPV4 = socket.gethostbyname(socket.gethostname())
listAllIndex = ["[CURRENT_SESSION_KEY]", "[CURRENT_CLIENT_LOG]", "[CURRENT_SERVER_LOG]", "[CURRENT_SYSTEM_STATUS]", "[SERVER_PORT]", "[SYSTEM_IPV4]"]
dataValues = "data_values.txt"

def checkIPV4(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False
    
def rewriteLine(file, lineKey, newLine):
    currentFile = open(file, "r")
    listAllLines = currentFile.readlines()

    listAllLines[listAllIndex.index(lineKey)] = lineKey + ' <-> ' + newLine + '\n'

    currentFile = open(file, "w")
    currentFile.writelines(listAllLines)
    currentFile.close()

def setUpCurrentSystemStatus():
    cmd('cls')

    try:
        currentFile = open(dataValues, "r")
    except:
        currentFile = open(dataValues, "a+")
        for keyName in listAllIndex:
            currentFile.write(keyName + ' <-> \n')
    currentFile.flush()

    listAllLines = currentFile.readlines()
    line = listAllLines[3].split(' <-> ')
    systemStatus = line[1].strip()
    setUpKey = True

    if systemStatus == 'admin' or systemStatus == 'client':
        pass
    else:
        while setUpKey:
            systemStatus = input("\nWelcome to LNCS!\n\nPlease set up your system...\nPrint 'admin' if your are admin, 'client' if your are a client, 'e' for exit: ")

            if systemStatus == 'admin' or systemStatus == 'client':
                while True:
                    confirmation = input(f"\nYour chose {systemStatus} system status. Please confirm your choice (y/n): ")

                    if confirmation == 'y':
                        setUpKey = False
                        break
                    elif confirmation == 'n':
                        cmd('cls')
                        break
                    else:
                        cmd('cls')
            elif systemStatus == 'e':
                exit()
            else:
                cmd('cls')

        rewriteLine(dataValues, listAllIndex[3], systemStatus)
        setUpKey = True
        
        while setUpKey:
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
                
                if int(PORT) >= 55000 aand int(PORT) <= 70000:
                    setUpKey = False
        
        rewriteLine(dataValues, listAllIndex[4], PORT)
        rewriteLine(dataValues, listAllIndex[5], IPV4)
        
        print(f"Your system is running on {IPV4}:{PORT}")
            
    return systemStatus

def systemStatusAdmin():
    server = srvr.newServer()
    server.start()

def systemStatusClient():
    client = clnt.newClient()
    client.start()
    client.connect()

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
