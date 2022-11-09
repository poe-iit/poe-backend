from .poe_data import *

import socket
from _thread import *
from collections import deque

# socket.SOCK_STREAM = TCP
# socket.SOCK_DGRAM = UDP (Switch To UDP if performance bottleneck appears via network limitations)
# Leave Connection Open For Arduino Communication (do not close for performance reasons)

class Sys:
    def __init__(self, ip, port, max_connections, poe_db):
        # global poe_main
        # poe_main = self

        # Not sure if 100% db needs a lock, just assumed so
        self.db             = poe_db

        self.connections    = {}
        self.c_lock         = allocate_lock()
        self.server         = None
        self.verbose        = False
        self.blocking       = False

        self.start_server(ip, port, max_connections)

    def auto_resolve_ip(self): # Unused for now
        local_ip = "127.0.0.1" # Listen Local Host (Within PC)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0] # Listen default lan IP
        except:
            local_ip = "0.0.0.0" # Listen All
        print("listening on: " + local_ip)
        return local_ip
        
    def set_verbose(self, status : bool):
        self.verbose = status

    def stop(self):
        #for thd in self.connections:
        #    self.connections[thd][-1] = True
        self.server.shutdown()
        self.server.close()

    def post_update_db(self, data):
        unpack_data = data.to_tupple()
        if self.verbose:
            print(unpack_data)
        self.db.upload(unpack_data)

    def list_connections(self, opt):
        # self.c_lock.acquire()
        for thd in self.connections:
            print("{}: {}".format(thd, self.connections[thd]))
        # self.c_lock.release()
        
    def add_connection(self, thd, connection):
        self.c_lock.acquire()
        self.connections[thd] = connection
        self.c_lock.release()

    def remove_connection(self, index):
        self.c_lock.acquire()
        del self.connections[index]
        self.c_lock.release()

    def start_client(self, client, address):
        # How to secure the system:
        # Use symmetric enc with timestamps for secure line of coms
        while True:
            try:
                # 4 (larger maybe better for efficeny, not verified, just hearsay)
                data = client.recv(1024) # Blocking Operation

                # Does not trigger on some disconnects
                if not data: # Check conn status
                    self.remove_connection(get_ident())
                    print("[LOG]: connection closed on thread {}".format(get_ident()))
                    exit()
                    continue
                
                if self.verbose:
                    print("[LOG]: poe_sys received {}".format(data))

                if len(data) % 4 != 0:
                    print("[ERROR]: Incompatible byte array received data from " + str(address[0]) + ":" + str(address[1]))
                    continue

                for i in range(0, len(data), 4):
                    opt     = int.from_bytes([data[i]],   "big")
                    id      = int.from_bytes([data[i+1]], "big")
                    type    = int.from_bytes([data[i+2]], "big")
                    reading = int.from_bytes([data[i+3]], "big")

                    self.post_update_db(sensor(address[0], address[1], str(id), type, reading))

            except Exception as e:
                # Occassional "disk I/O error" needs to be resolved
                print(e)
                print("[ERROR]: Error reading received data from " + str(address[0]) + ":" + str(address[1]))
        client.close()
    
    def server_loop(self):
        while True:
            # Using Sockets
            client, address = self.server.accept()
            if self.blocking:
                client.close()
                continue

            print("{}Connection Estabilished - {} : {}{}".format("\033[92m", address[0], address[1], "\033[0m"))
            thd = start_new_thread(self.start_client, (client, address))
            self.add_connection(thd, [False, client, address]) # Validity, thread, client, address
            

    def start_server(self, ip, port, max_connections):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, port))
        self.server.listen(max_connections)

        start_new_thread(self.server_loop, ())


