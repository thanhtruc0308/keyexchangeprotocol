import threading
import time
import sys
import network
from AliceBob import Person
from crypto import CryptoProtocol


def usage():
    print("Usage:")
    print("    Server: " + sys.argv[0] + " port_number")
    print("    Client: " + sys.argv[0] + " ip_address port_number")
    sys.exit()

if not (len(sys.argv) == 2 or len(sys.argv) == 3):
    usage()

conn = network.Connection()
ab = None


def get_line():
    line = None
    while line is None:
        line = conn.recv()
    return line

if len(sys.argv) == 2:  # server
    try:
        conn.listen(int(sys.argv[1]))
    except:
        print("Unable to open port %d" % int(sys.argv[1]))
        sys.exit()
    
    alice = Person()
    pubkey_A = alice.generate_public_broadcast()    
    conn.send("Alice's public key: " + pubkey_A.decode("utf-8"))
    B = get_line()
    print(B)
    
    
elif len(sys.argv) == 3:  # client
    try:
        conn.connect(sys.argv[1], int(sys.argv[2]))
    except:
        print("Unable to connect to %s at port %d" % (sys.argv[1], int(sys.argv[2])))
        sys.exit()
    A = get_line()
    print(A)
    bob = Person()
    pubkey_B = bob.generate_public_broadcast()
    conn.send("Bob's public key: " + pubkey_B.decode("utf-8"))
    

else:
    print("Unreachable code reached!!!")
    sys.exit()


def send_message(text):
    msg = CryptoProtocol().encrypt(text)
    conn.send(text)

class GUIThread (threading.Thread):

    def run(self):
        import gui
        gui.set_send_message_callback(send_message)
        gui.start()

GUIThread().start()

while True:
    line = conn.recv()
    if line is not None:
        import gui
        if line != '':
            gui.add_new_text("[Other] " + line)
    else:
        break

