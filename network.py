import pwn


class Connection():

    def __init__(self):
        self.data_buffer = []

    def listen(self, port_no):
        l = pwn.listen(port_no)
        self.conn = l.wait_for_connection()

    def connect(self, ip, port_no):
        self.conn = pwn.remote(ip, port_no)

    def recv(self):
        try:
            return self.conn.recvline().strip().decode('utf-8')
        except EOFError:
            return None

    def send(self, data):
        self.conn.send(str(data).replace('\n', '') + '\n')