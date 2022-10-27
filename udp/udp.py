import json
from select import select
import socket
import numpy as np
import os
import readchar
import sys
import time 

buffer_size = 1000
window_size = 2

# verifica se a lista de numeros naturais não possui lacunas
def ehContinuo(List = []):
    for i in range(len(List) - 1):
        if List[i] + 1 != List[i + 1]:
            return False
    return True

def choose_peer_type():
    select = 0
    print("What would you like to do?")
    while (True):
        if select == 0:
            sys.stdout.write("\r=> Send\t   Receive")
        else:
            sys.stdout.write("\r   Send\t=> Receive")
        inpt = (repr(readchar.readkey()))
        if inpt[2] == 'r':
            print("")
            return select
        if inpt[5] == 'K':
            select = 0
        elif inpt[5] == 'M':
            select = 1
        sys.stdout.flush()

def choose_package_size():
    select = 0
    print("Which package size would you like to use?")
    while (True):
        if select == 0:
            sys.stdout.write("\r=> 1000\t   1500")
        elif select == 1:
            sys.stdout.write("\r   1000\t=> 1500")
        inpt = (repr(readchar.readkey()))
        if inpt[2] == 'r':
            print("")
            global buffer_size
            buffer_size = 1000 + 500 * select
            return select
        if inpt[5] == 'K':
            select = 0
        elif inpt[5] == 'M':
            select = 1

        sys.stdout.flush()

def choose_window_size():
    select = 0
    print("Which window size would you like to use?")
    while (True):
        if select == 0:
            sys.stdout.write("\r=> 2\t   4")
        elif select == 1:
            sys.stdout.write("\r   2\t=> 4")
        inpt = (repr(readchar.readkey()))
        if inpt[2] == 'r':
            print("")
            global window_size
            window_size = 2 + 2 * select
            return select
        if inpt[5] == 'K':
            select = 0
        elif inpt[5] == 'M':
            select = 1

class Peer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#################################################################################
    def send_file(self, file_name, ip, port):
            self.socket.settimeout(0.02)
            file = open(file_name, "rb")
            self.send_file_header(file_name, ip, port)
          
            start_time = time.time()

            self.send_file_content(file, 0, ip, port)
            file.close()
    
            end_time = time.time()

            print("File %s sent to %s:%d" % (file_name, ip, port))
            print("File size: %s bytes" % (str("{:,}".format(os.path.getsize(file_name)).replace(',','.'))))
            print("Time spent: %.6f seconds" % (float(end_time) - start_time))
            total_per_s = float(int(os.path.getsize(file_name)) / (end_time - start_time))
            print("Total %s bits/s" % (str("{:,}".format(8 * total_per_s).replace('.','#').replace(',','.').replace('#',","))))


    def send_file_header(self, file_name, ip, port):
        header = file_name
        header = header.zfill(buffer_size)
        header = header.encode('utf-8')
        ack_msg = ""
        while True:
            try:
                self.socket.sendto(header, (ip, port))
                ack_msg = self.socket.recv(buffer_size)
                ack_msg = ack_msg.decode('utf-8').lstrip('0')
                if ack_msg == "ACK":
                    break
            except:
                continue
        print("Header sent")  
        
    def send_file_content(self, file, pckg_num, ip, port):
        global buffer_size
        

        cont = 1
        check = True
        while check:
            janela = []
            for n in range(window_size):
                data = file.read(buffer_size - 10)
                if not data:
                    check = False
                data = (str(cont) + ";").encode('utf-8') + data
                cont = cont + 1
                data = data.zfill(buffer_size)
                janela.append(data)

            for n in range(100):
                try:
                    for n in range(len(janela)):
                        self.socket.sendto(janela[n], (ip, port))
                    feedback = json.loads(self.socket.recv(buffer_size).decode('utf-8').lstrip('0'))
                    if feedback["status"]:
                        break
                except:
                    continue
        self.socket.sendto("END".encode('utf-8'), (ip, port))
    
#################################################################################
    def receive_file(self):
        file_name, addr = self.receive_header()
        print(file_name)
        global buffer_size
        start_time = time.time()
        lost_packages = self.receive_file_content(file_name, 0, addr)
        end_time = time.time()
        print("File %s received from %s:%d" % (file_name, addr[0], addr[1]))

    def receive_header(self):
        while True:
            try:
                header, addr = self.socket.recvfrom(buffer_size)
                header = header.decode('utf-8').lstrip('0')
                self.socket.sendto("ACK".encode('utf-8'), addr)
                break 
            except:
                continue
        print("Header has been received")
        return header, addr

    def receive_file_content(self, file_name, pckg_num, addr):
        global buffer_size
        file = open("chegou-" + file_name, "wb")
        check = True
        cont = 1
        while check:
            while True:
                try:
                    data_list_bruto = []
                    cont_bkp = cont
                    for n in range(window_size):
                        data, addr = self.socket.recvfrom(buffer_size)
                        if data == b'END':
                            check = False
                            break
                        data_list_bruto.append(data)
                    if not check:
                        break
                    data_list = []
                    headers = []

                    print("Esperando :", end = "")
                    print("[%d, %d]" % (cont, cont + 1), end = "")
                    print(" Recebendo :", end = "")
                    
                    pkg_check = True
                    for n in range(len(data_list_bruto)):
                        headers.append(int(data_list_bruto[n][:data_list_bruto[n].find(b';')]))
                        data_list.append(data_list_bruto[n][data_list_bruto[n].find(b';') + 1:])
                        
                    if [cont, cont + 1] == headers:                        
                        cont = cont + 2
                    elif [cont + 1, cont] == headers:
                        data_list[0], data_list[1] = data_list[1], data_list[0]
                        cont = cont + 2
                    else:
                        pkg_check = False

                    print(headers)

                    if pkg_check:
                        for n in range(len(data_list_bruto)):
                            file.write(data_list[n])
                        self.socket.sendto(str("{\"status\":true}").encode('utf-8'), addr)
                    else:
                        self.socket.sendto(str("{\"status\":false}").encode('utf-8'), addr)
                        cont = cont_bkp
                except:
                    continue
        file.close()
        return 0

if __name__ == "__main__":
    __select__ = choose_peer_type()

    choose_package_size()
    choose_window_size()

    if(__select__ == 1):
        peer = Peer("191.52.64.155", 3000)
        peer.socket.bind((peer.ip, peer.port))
        peer.receive_file()
    else:
        peer = Peer("191.52.64.155", 3000)
        peer.send_file("s0ukmn.flac", "191.52.64.155", 3000)