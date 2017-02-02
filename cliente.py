import socket
import threading
import sys
import pickle

class Cliente():
    """Abstraccion de un cliente que se conectara a un servidor"""

    def __init__(self, host="localhost",port=5000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((str(host),int(port)))

        msg_rcv = threading.Thread(target=self.msg_rcv)
        msg_rcv.daemon = True
        msg_rcv.start()
  
        while True:
            msg = input('->')
            if msg != 'salir':
                self.send_msg(msg)
            else:
                self.sock.close()
                sys.exit()

    def msg_rcv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    print(pickle.loads(data))
            except:
                pass


    def send_msg(self,msg):
        self.sock.send(pickle.dumps(msg))


c = Cliente()
