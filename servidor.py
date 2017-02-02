import socket
import threading
import sys
import pickle

class Servidor:

    def __init__(self, host="localhost", port=5000):
        self.clientes = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host),int(port)))
        self.sock.listen(10) #maximo de conexiones que va a escuchar
        self.sock.setblocking(False)

        #hilos para aceptar y procesar las conexiones
  
        aceptar = threading.Thread(target=self.aceptarCon)
        procesar = threading.Thread(target=self.procesarCon)

        #decirle a los hilos que sean demonios e iniciarlos
        aceptar.daemon = True
        aceptar.start()

        procesar.daemon = True
        procesar.start()

        while True:
            msg = input("->")
            if msg == "salir":
                self.sock.close()
                sys.exit()
            else:
                pass


    def msg_to_all(self, msg, cliente):
        for c in self.clientes:
            try:
                if c != cliente:
                    c.send(msg) 
            except:
                self.clientes.remove(c)
        

    def aceptarCon(self):
        print("AceptarCon iniciado")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clientes.append(conn)
            except:
                pass

    def procesarCon(self):
        print("ProcesarCon iniciado")
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(1024)
                        if data:
                            self.msg_to_all(data,c)
                    except:
                        pass 
                            

s = Servidor()
