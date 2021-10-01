import numpy as np
import socket
import pickle
import struct
import pyautogui
import threading
from PIL import Image

class __stream__:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.keyExit = False
    
    def __start__(self):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((self.IP, self.PORT))


        while not self.keyExit:
            try:
                image = pyautogui.screenshot()
                image = image.resize((1280, 720), Image.ANTIALIAS)
                image = np.array(image)
                img = Image.frombytes('RGB', (1280, 720), image)
                data = pickle.dumps(np.array(img))
                clientsocket.sendall(struct.pack("L", len(data)) + data)
            except:
                break

    def start(self):
        st = threading.Thread(target = self.__start__, args =())
        st.start()
    
    def close(self):
        self.keyExit = True