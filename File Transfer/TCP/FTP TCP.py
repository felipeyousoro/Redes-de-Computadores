from select import select
import readchar
import struct
import sys
import time
import socket
import os
import numpy as np

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

def interface_size():
    select = 0
    print("   Qual o tamanho máximo de pacote que você deseja enviar?")
    while (True):
        if select == 0:
            sys.stdout.write("\r=> 500\t   1000\t   1500")
        elif select == 1:
            sys.stdout.write("\r   500\t=> 1000\t   1500")
        elif select == 2:
            sys.stdout.write("\r   500\t   1000\t=> 1500")
        inpt = (repr(readchar.readkey()))
        if inpt[2] == 'r':
            print("")
            return (select + 1) * 500
        if inpt[5] == 'K':
            if select == 2:
                select = 1
            else:
                select = 0
        elif inpt[5] == 'M':
            if select == 1 or select == 2:
                select = 2
            else:
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
        file_name = self.client.recv(1024).decode("utf-8")
        print("   Nome do arquivo: " + file_name)
        self.client.send(("File name received").encode("utf-8"))
        pckg_bytes = struct.unpack('i', self.client.recv(1024))[0]
        file = open(file_name, "wb")
        start_t = time.time()
        size = 0
        while True:
            pck = self.client.recv(pckg_bytes)
            if len(pck) == 0:
                break
            while len(pck) < pckg_bytes:
                pck_2 = self.client.recv(pckg_bytes - len(pck))
                if len(pck_2) == 0:
                    break
                pck += pck_2
            size += len(pck) - 4
            file.write(pck[4:])
        fim_t = time.time() - start_t
        print('   Tempo total gasto: ' + str(fim_t) + ' segundos')
        print('   Tamanho do arquivo: ' + str("{:,}".format(size)).replace(',','.') + ' bytes' )
        print('   Velocidade de download: ' +  "{:,}".format(((size * 8) / fim_t)).replace('.','#').replace(',','.').replace('#',",") + ' bits/s')
        file.close()

class Client:
    def __init__(self, HOST, PORT, SIZE):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.client.setblocking(1)
        self.file_name = None
        self.file_path = None
        self.pckg_size = SIZE

    def select_file(self):
        self.file_path = input("   Insira o caminho do arquivo: ")
        self.file_name = os.path.basename(self.file_path)

    def send_file(self):
        self.client.send(self.file_name.encode('utf-8'))
        feedback = self.client.recv(1024).decode("utf-8")
        self.client.send(struct.pack('i',self.pckg_size))
    
        start = time.time()
        if feedback == 'File name received':
            file = open(self.file_path, "rb")
            cont = 0
            while True:
                byte_1 = struct.pack('i', cont)
                
                cont += 1

                byte_2 = file.read(self.pckg_size - len(byte_1))

                if not byte_2:
                    break

                self.client.send(byte_1 + byte_2)

            file.close()
        Time = time.time() - start + 1e-10

        self.client.send("".encode('utf-8'))

if __name__ == "__main__":

    file = open('test','wb')

    file.close()

    __select__ = interface_type()

    if __select__:
        PORT = int(input("   Insira a porta: "))
        __server = Server(PORT)
        __server.receive_file()

    if not __select__:
        PORT = int(input("   Insira a porta: "))
        HOST = str(input("   Insira o IP: "))
        SIZE = interface_size()
        __client = Client(HOST, PORT, SIZE)
        __client.select_file()
        __client.send_file()

    print("\n\n   Tranferencia concluida")
