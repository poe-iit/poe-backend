import poeipro as poe

import os
import time
import socket
from _thread import *

__location__    = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
#db_path         = os.path.join(__location__, "database.db")
db_path         = os.path.join(__location__, "../Software-Frontend-Backend-master/IPRO_SOTERIA/db.sqlite3")
poe_main        = None
port            = 1234
max_connections = 1024
    
def help(opt):
    s = """
    h: help
    q: quit
    l: list connections
    t: test by launching fake client
        -c <int>: number of clients
        -p <int>: number of packets per client; -1 = inf
        -t <float>: time (seconds) between sending packet
    """
    print(s)

def verbose(opt):
    poe_main.set_verbose(not poe_main.verbose)

def close_app(opt):
    # close server and threads
    # not sure if python's low level threads require manual cleanup, i.e. orphaned processes 
    # poe_main.close()
    # quit()
    exit()

def test_client(opts):
    clients     = 1
    packets     = 5
    time        = 0

    try:
        for i in range(0, len(opts), 2): 
            if opts[i] == "-c": # match case not working
                clients = int(opts[i+1])
            elif opts[i] == "-p":
                packets = int(opts[i+1])
            elif opts[i] == "-t":
                time = int(opts[i+1])

        poe.SimulateClient(clients, packets, time)
    except:
        print("error reading command")
        help(0)

def terminal_proc():
    opts = {"h" : help,
            "q" : close_app,
            "l" : poe_main.list_connections,
            "t" : test_client,
            "v" : verbose,
            }

    while True:
        args = input('POE-TERM: ')

        if len(args) == 0:
            continue

        args = args.split(" ")

        if args[0] not in opts:
            #print("NONE")
            help(0)
            continue
        opts[args[0]](args[1:])
        pass

if __name__ == "__main__":
    # Scale horizontally with multiple Poe objects, if bottleneck appears
    # Fault loop, auto recovery.  Remove fault loop later, potential issues rebind socket
    #ip = auto_resolve_ip()
    while True:
        try:
            ip = '0.0.0.0'
            poe_db = poe.DB(db_path)
            poe_main = poe.Sys(ip, port, max_connections, poe_db)
            terminal_proc()
        except Exception as e:
            print("[ERR]: " + str(e))
            print("[ERR]: Restarting program")
            try:
                poe_main.stop()
            except:
                pass
            time.sleep(1)


    