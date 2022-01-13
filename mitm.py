import threading
import sys
import network
from AliceBob import Person
from crypto import CryptoProtocol


def usage():
    print("Usage:")
    print("    " + sys.argv[0] + " server_ip server_port client_port")
    sys.exit()

if len(sys.argv) != 4:
    usage()


def get_line(conn):
    line = None
    while line is None:
        line = conn.recv()
    return line

server_ip = sys.argv[1]
server_port = int(sys.argv[2])
client_port = int(sys.argv[3])

conn_server = network.Connection()  # connection with server
conn_client = network.Connection()  # connection with client
p_server = None
p_client = None
crypto_protocol_server = None
crypto_protocol_client = None

try:
    conn_client.listen(client_port)
except:
    print("Unable to open port %d" % client_port)
    sys.exit()

try:
    conn_server.connect(server_ip, server_port)
except:
    print("Unable to connect to %s at port %d" % (server_ip, server_port))

# Key exchange: Later can be added some other variants too.#######

p_server = Person()
pubkey_server = p_server.generate_public_broadcast()

p_client = Person()
pubkey_client = p_client.generate_public_broadcast()

p_malice = Person()
pubkey_malice = p_malice.generate_public_broadcast()

conn_server.send("Bob's public key: (malice)" + pubkey_server.decode("utf-8"))
A_server = get_line(conn_server)
crypto_protocol_server = CryptoProtocol()

conn_client.send("Alice's public key: " + pubkey_malice.decode("utf-8"))
A_client = get_line(conn_client)
crypto_protocol_client = CryptoProtocol()



# KEY EXCHANGE ENDS
def send_message_server(text):
    conn_server.send(text)

class GUIThread (threading.Thread):

    def run(self):
        import gui
        gui.start(True)

GUIThread().start()


def session(conn_receive, cp_receive, conn_send, cp_send, name):
    while True:
        line = conn_receive.recv()
        if line is not None:
            import gui
            if line != '':
                gui.add_new_text("[" + name + "] " + line)
                conn_send.send(line)
        else:
            break

t = threading.Thread(target=session, args=(conn_server, crypto_protocol_server, conn_client, crypto_protocol_client, "server"))
t.daemon = True
t.start()

session(conn_client, crypto_protocol_client,
        conn_server, crypto_protocol_server, "client")