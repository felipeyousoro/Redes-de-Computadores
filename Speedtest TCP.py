from select import select
import readchar
import struct
import sys
import time
import socket
import os
import numpy as np

def rec(numero):
    if len(numero) > 3:
        return formatar_milhar(numero[:-3]) + "." + numero[-3:]
    else:
        return numero

def formatar_milhar(numero):
    numero = numero.split('.')

    if len(numero) == 1:
        return rec(numero[0])
    else:
        return rec(numero[0]) + "," + numero[1][:3]



def interface_type():
    select = 0
    print("O que você gostaria de fazer com os arquivos?")
    while (True):
        if select == 0:
            sys.stdout.write("\r=> Enviar\t   Receber")
        else:
            sys.stdout.write("\r   Enviar\t=> Receber")
        inpt = (repr(readchar.readkey()))
        if inpt[2] == 'r':
            print("")
            return select
        if inpt[5] == 'K':
            select = 0
        elif inpt[5] == 'M':
            select = 1
        sys.stdout.flush()

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

class Server:
    def __init__(self, port):
        HOST = extract_ip()
        print("   IP: " + HOST)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, port))
        self.server.listen(1)
        self.server.setblocking(1)
        self.client, address = self.server.accept()

    def receive_file(self):
        
        start_time = time.time()
        packages_received = 0

        while True:
            ready = select([self.client], [], [], 5)

            if ready[0]:
                data = self.client.recv(500)

                if len(data) == 0:
                    break
                if len(data) == 500:
                    packages_received += 1
                if len(data) < 500:
                    data += self.client.recv(500 - len(data))
                    packages_received += 1

        total_time = time.time() - start_time

        print("Packages received: " + formatar_milhar(str(packages_received)))
        print("Packages by second: " + formatar_milhar(str(packages_received / total_time)))
        print("Total bytes received: " + formatar_milhar(str(packages_received * 500)))
        print("Total bits per second: " + formatar_milhar(str(packages_received * 500 * 8 / total_time)))
        print("Total kilobits per second: " + formatar_milhar(str(packages_received * 500 * 8 / (total_time * 1000))))
        print("Total megabits per second: " + formatar_milhar(str(packages_received * 500 * 8 / (total_time * 1000000))))
        print("Total gigabits per second: " + formatar_milhar(str(packages_received * 500 * 8 / (total_time * 1000000000))))

class Client:
    def __init__(self, HOST, PORT, SIZE):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.client.setblocking(1)
        self.file_name = None
        self.file_path = None
        self.pckg_size = SIZE

    def send_file(self):

        start = time.time()

        data = 'teste de rede *2022*'.zfill(500)

        cont = 0
        while time.time() - start < 20:
            cont += 1
            self.client.send(data.encode("utf-8"))
        end = time.time() - start 

        print("Packages sent: \t\t" + formatar_milhar(str(cont)))
        print("Total bytes sent: \t\t" + formatar_milhar( str(cont * 500)))
        print("Total gigabits per second: \t" + formatar_milhar(str(cont * 4000 / (end) / 1000000000)) + " Gbps")
        print("Total megabits per second: \t" + formatar_milhar( str(cont * 4000 / (end) / 1000000)) + " Mbps")
        print("Total kilobits per second: \t" + formatar_milhar( str(cont * 4000 / (end) / 1000)) + " Kbps")
        print("Packages by second: \t\t" + formatar_milhar(str(cont / (end))))
    
        self.client.send("".encode('utf-8'))

if __name__ == "__main__":

    file = open('test','wb')

    file.close()

    __select__ = interface_type()

    if __select__:
        __server = Server(3000)
        __server.receive_file()

    if not __select__:
        PORT = 3000
        # HOST = str(input("   Insira o IP: "))
        __client = Client('191.52.64.98', PORT, 0)
        __client.send_file()

    print("\n\n   Tranferencia concluida")
