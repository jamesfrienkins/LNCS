import time
import server as srvr
import client as clnt
import string
import random
from os import system as cmd

listAllIndex = ["[CURRENT_SESSION_KEY]", "[CURRENT_CLIENT_LOG]", "[CURRENT_SERVER_LOG]", "[CURRENT_SYSTEM_STATUS]"]
dataValues = "data_values.txt"

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

    return systemStatus

def systemStatusAdmin():
    server = srvr.newServer()

    server.start()
    time.sleep(30)

def systemStatusClient():
    client = clnt.newClient()

    client.start()
    client.connect()

    client.send('Hello world!')
    time.sleep(5)

    client.send('Hello Volodya!')
    time.sleep(5)

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
