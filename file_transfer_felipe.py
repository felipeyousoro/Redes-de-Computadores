from select import select
import readchar
import sys
import time
import socket
import os

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
    print("   Qual o tamanho máximo de pacote que você deseja receber?")
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
        print("   IP:" + HOST)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, port))
        self.server.listen(1)
        self.client, address = self.server.accept()

    def send_confirmation(self):
        self.client.send(("OK").encode("utf-8"))

    def receive_file(self):
        file_name = self.client.recv(1024).decode("utf-8")
        elapsed_time = time.time()
        print("   Nome do arquivo: " + file_name)
        self.send_confirmation()

        file_size = int(self.client.recv(1024).decode("utf-8"))
        print("   Tamanho do arquivo: " + str(file_size))
        self.send_confirmation()

        packet_num = int(self.client.recv(1024).decode("utf-8"))
        print("   Número de pacotes: " + str(packet_num))
        self.send_confirmation()
        
        file = open(file_name, "wb")
        for i in range(packet_num):
            package = self.client.recv(file_size)
            
            header = package[0:100]
            header = header.decode("utf-8")
            header = header.split("0")[1]

            file.write(package[100:])

            self.send_confirmation()

        file.close()

        print('   Estatisticas:')
        elapsed_time = time.time() - elapsed_time
        print('   Tempo de envio: ' + str(elapsed_time))
    
class Client:
    def __init__(self, HOST, PORT, SIZE):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.file_name = None
        self.file_path = None
        self.pckg_size = SIZE

    def select_file(self):
        self.file_path = input("   Insira o caminho do arquivo: ")
        self.file_name = os.path.basename(self.file_path)

    def check_confirmation(self):
        confirmation = self.client.recv(1024).decode("utf-8")
        if confirmation == "OK":
            return True
        else:
            return False

    def send_file(self):
        self.client.send(self.file_name.encode('utf-8'))
        elapsed_time = time.time()
        while(not self.check_confirmation()):
            pass

        print(self.pckg_size)
        self.client.send(str(self.pckg_size).encode('utf-8'))
        while(not self.check_confirmation()):
            pass

        packet_num = os.stat(self.file_path).st_size / (self.pckg_size - 100) #Tamanho do header = 100
        packet_num = int(packet_num) + 1
        print("   Pacotes a serem enviados: " + str(packet_num))
        self.client.send(str(packet_num).encode('utf-8'))
        while(not self.check_confirmation()):
            pass

        file = open(self.file_path, "rb")
        for i in range(packet_num):
            header = str("pck_num:" + str(i))
            header = header + ' '
            header = header.zfill(100)

            package = file.read(self.pckg_size - 100)

            self.client.send(header.encode('utf-8') + package)
            
            while(not self.check_confirmation()):
                pass

        file.close()
        
        print('   Estatisticas:')
        elapsed_time = time.time() - elapsed_time
        print('   Tempo de envio: ' + str(elapsed_time))

    
if __name__ == "__main__":
    __select__ = interface_type()

    if __select__:
        PORT = int(input("   Insira a porta: "))
        __server = Server(PORT)
        __server.receive_file()

    if not __select__:
        PORT = int(input("   Insira a porta: "))
        HOST = str(input("   Insira o ip:"))
        SIZE = interface_size()
        __client = Client(HOST, PORT, SIZE)
        __client.select_file()
        __client.send_file()

    out = input("\n\n   Pressione ENTER para sair")