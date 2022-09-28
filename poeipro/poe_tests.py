import socket
import time as t
from _thread import *

class SimulateClient():
    host = "127.0.0.1"  
    port = 1234

    def __init__(self, clients : int, packets_per_client : int, time_between_packet : int, host="127.0.0.1", port=1234):
        self.host = host    # The server's hostname or IP address
        self.port = port    # The port used by the server

        for i in range(clients):
            start_new_thread(self.client, (i, packets_per_client, time_between_packet, host, port))

    def client(self, index, packets, time, host, port):
        data = b'\x01\xFF\x00\x01'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print("{}[LOG]:{} client {} started".format("\033[96m", "\033[0m", index))

        while packets != 0:
            packets -= 1
            print("{}[LOG]:{} client {} sent {}{}{}".format("\033[94m", "\033[0m", index, "\033[92m", data, "\033[0m"))
            s.send(data) #\xFF\xFF\x00\x01
            t.sleep(time)
        s.close()

    def kill(self):
        pass