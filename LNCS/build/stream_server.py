import cv2
import socket
import pickle
import struct
import threading

class __stream__:
    HOST = socket.gethostbyname(socket.gethostname())
    BUFFER = 2 ** 21
    
    def __init__(self, PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = PORT
    
    def __start__(self):
        while True:
            self.s.bind((self.HOST, self.PORT))
            self.s.listen()
            
            conn, addr = self.s.accept()

            data = b''
            payload_size = struct.calcsize("L")
            
            while True:
                while len(data) < payload_size:
                    data += conn.recv(self.BUFFER)
                packed_msg_size = data[:payload_size]
            
                data = data[payload_size:]
                msg_size = struct.unpack("L", packed_msg_size)[0]
            
                while len(data) < msg_size:
                    data += conn.recv(self.BUFFER)
                frame_data = data[:msg_size]
                data = data[msg_size:]
            
                frame = pickle.loads(frame_data)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                cv2.imshow(f'LNCS Live Stream {addr[0]}', frame)
                cv2.waitKey(10)

    def start(self):
        st = threading.Thread(target = self.__start__, args =())
        st.start()