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
    print("   Qual o tamanho máximo de paco que você deseja receber?")
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

    def receive_file(self):
        file_name = self.client.recv(1024).decode("utf-8")
        print("   File name: " + file_name)
        self.client.send(("File name received").encode("utf-8"))
        pckg_bytes = int(self.client.recv(1024).decode("utf-8"))
        pckg_size = int(self.client.recv(1024).decode("utf-8"))
        time.sleep(2)
        file = open(file_name, "wb")
        start = time.time()
        size = 0
        for i in range(pckg_size):
            pck = self.client.recv(pckg_bytes)
            size += len(pck)
            self.client.send(("Package received").encode("utf-8"))
            file.write(pck)
        Time = time.time() - start + 1e-10
        size = size * 8
        file.close()
        self.client.send(("File received").encode("utf-8"))
        print("File received")
        report_1 = self.client.recv(1024).decode('utf-8')
        report_2 = "   Download speed:\t" + str(size / Time) + " bit/s"
        report_2 += "\n   Download time:\t" + str(Time)
        report_2 += "\n   Received packages:\t" + str(pckg_size)
        report_2 += "\n   Packages lost:\t" + str(0)
        self.client.send((report_2).encode("utf-8"))
        print(report_1)
        print(report_2)

class Client:
    def __init__(self, HOST, PORT, SIZE):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.file_name = None
        self.file_path = None
        self.pckg_size = SIZE

    def select_file(self):
        self.file_path = input("Insert file directory")
        self.file_name = os.path.basename(self.file_path)

    def send_file(self):
        self.client.send(self.file_name.encode('utf-8'))
        feedback = self.client.recv(1024).decode("utf-8")
        self.client.send(str(self.pckg_size).encode('utf-8'))
        file_content = []
        if feedback == 'File name received':
            file = open(self.file_path, "rb")
            while True:
                byte = file.read(1)
                if not byte:
                    break
                file_content.append(byte)
            file.close()

        self.client.send(
            str(1 + int((len(file_content) / self.pckg_size))).encode('utf-8'))
        time.sleep(1)

        pkg = b''
        idx = 0
        start = time.time()
        for idx in range(len(file_content)):
            pkg += file_content[idx]
            if (len(pkg) == self.pckg_size or idx == len(file_content) - 1):
                self.client.send(pkg)
                pkg = b''
                feedback = self.client.recv(1024).decode("utf-8")
        Time = time.time() - start + 1e-10

        feedback = self.client.recv(1024).decode("utf-8")

        if feedback == 'File received':
            print("File uploaded successfully")
        
        # REPORT
        report_1 = "\n   File Size:\t\t" + str(len(file_content)) + " bytes" + "\n   Packages sent:\t" + str(
            1 + int((len(file_content) / self.pckg_size)))
        report_1 += "\n   Upload speed:\t" +  str((len(file_content) * 8) / Time) + " bit/s"
        report_1 += "\n   Upload time:\t\t" + str(Time)
        self.client.send(report_1.encode('utf-8'))
        report_2 = self.client.recv(1024).decode("utf-8")
        print(report_1)        
        print(report_2)        


if __name__ == "__main__":
    __select__ = interface_type()

    if __select__:
        PORT = int(input("   Enter port: "))
        __server = Server(PORT)
        __server.receive_file()

    if not __select__:
        PORT = int(input("   Enter port: "))
        HOST = str(input("   Enter host: "))
        SIZE = interface_size()
        __client = Client(HOST, PORT, SIZE)
        __client.select_file()
        __client.send_file()

    out = input("\n\n   Press ENTER to exit")