import time
import socket
import threading
from os import system as cmd

class connections:
    updateInfo = True

    def fill(self, string, n, symbol = " "):
        n = max(len(string), n)

        string += str(symbol) * (n - len(string))

        return string

    def printCurrentConnections(self, spacing = 25):
        lastConnectionList = ""
        while True:
            if self.updateInfo == True:
                connectionList = self.getConnectionList()
                if connectionList != None:
                    connectionList = connectionList.decode('utf-8')

                    if lastConnectionList != connectionList:
                        lastConnectionList = connectionList

                        cmd('cls')
                        self.updateInfo = False
                        print(self.fill('Address', spacing + 2) + self.fill('Name', spacing) + self.fill('Status', spacing - 2) + self.fill('Connection time', spacing + 5) + '\n')

                        listA = connectionList.split('<|>')

                        for a in listA:
                            a = a.split('<>')
                            clnt_addr, clnt_name, clnt_status, clnt_connection_time = a

                            print(self.fill(clnt_addr, spacing + 2) + self.fill(clnt_name, spacing) + self.fill(clnt_status, spacing - 2) + self.fill(clnt_connection_time, spacing + 5))

    def start(self):
        startOutput = threading.Thread(target = self.printCurrentConnections, args = (), daemon = True)
        startOutput.start()

        while True:
            time.sleep(1)
            self.update()
    
    def getConnectionList(self):
        try:
            s = socket.socket()
            port = 55499
            s.connect((socket.gethostbyname(socket.gethostname()), port))
            dataList = s.recv(2028)
            s.close()
            return dataList
        except:
            return None
    
    def update(self):
        self.updateInfo = True

c = connections()

c.start()