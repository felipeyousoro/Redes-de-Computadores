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
        
        start = time.time()
        cont = 0
        while time.time() - start < 20:
            pck = self.client.recv(500)
            cont += 1
            if len(pck) == 0:
                break
        end = time.time() - start 

        message = ''

        message += ("   Pacotes recebidos: \t\t" + formatar_milhar(str(cont))) + '\n'
        message += ("   Bytes recebidos: \t\t" +formatar_milhar( str(cont * 500))) + '\n'
        message += ("   Velocidade Gigabit: \t\t" + formatar_milhar(str(cont * 500 / (end) / 1000000000)) + " Gbps") + '\n'
        message += ("   Velocidade Megabit: \t\t" +formatar_milhar( str(cont * 500 / (end) / 1000000)) + " Mbps") + '\n'
        message += ("   Velocidade Kilobit: \t\t" +formatar_milhar( str(cont * 500 / (end) / 1000)) + " Kbps") + '\n'
        message += ("   Pacotes por segundo: \t" + formatar_milhar(str(cont / (end)))) + '\n'
        message += ("   Tempo total gasto: \t\t" + str(end).split('.')[0] + " segundos") + '\n'
    
        print(message)

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

        message = ''

        message += ("   Pacotes enviados: \t\t" + formatar_milhar(str(cont))) + '\n'
        message += ("   Bytes enviados: \t\t" +formatar_milhar( str(cont * 500))) + '\n'
        message += ("   Velocidade Gigabit: \t\t" + formatar_milhar(str(cont * 500 / (end) / 1000000000)) + " Gbps") + '\n'
        message += ("   Velocidade Megabit: \t\t" +formatar_milhar( str(cont * 500 / (end) / 1000000)) + " Mbps") + '\n'
        message += ("   Velocidade Kilobit: \t\t" +formatar_milhar( str(cont * 500 / (end) / 1000)) + " Kbps") + '\n'
        message += ("   Pacotes por segundo: \t" + formatar_milhar(str(cont / (end)))) + '\n'
        message += ("   Tempo total gasto: \t\t" + str(end).split('.')[0] + " segundos") + '\n'
    
        self.client.send("".encode('utf-8'))

        print(message)


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
        __client = Client('10.0.0.100', PORT, 0)
        __client.send_file()

    print("\n\n   Tranferencia concluida")
