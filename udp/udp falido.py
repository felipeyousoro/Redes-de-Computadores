from select import select
import socket
import numpy as np
import os
import readchar
import sys
import time 

buffer_size = 1000
window_size = 2

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
        file = open(file_name, "rb")
        self.send_file_header(file_name, ip, port)
        print("Header sent")    
    
        self.socket.settimeout(0.05)

        global buffer_size
        pckg_num = int(np.ceil(os.path.getsize(file_name) / (buffer_size - 10)))

        start_time = time.time()

        self.send_file_content(file, pckg_num, ip, port)
        file.close()
   
        end_time = time.time()

        print("File %s sent to %s:%d" % (file_name, ip, port))
        print("File size: %s bytes" % (str("{:,}".format(os.path.getsize(file_name)).replace(',','.'))))
        print("Total packages sent %d/%d" % (pckg_num, pckg_num))
        print("Time spent: %.6f seconds" % (float(end_time) - start_time))

        total_per_s = float(int(os.path.getsize(file_name)) / (end_time - start_time))
        print("Total %s bits/s" % (str("{:,}".format(total_per_s).replace('.','#').replace(',','.').replace('#',","))))


    def send_file_header(self, file_name, ip, port):
        file_size = os.path.getsize(file_name)

        header = file_name + ";" + str(file_size)
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
            except socket.timeout:
                continue

    def send_file_content(self, file, pckg_num, ip, port):
        global buffer_size

        for i in range(1, int((pckg_num + 1)/window_size)):
            if i % 5000 == 0:
                print("Sending package %d of %d" % (i, pckg_num))
            while True:
                try:
                    for i in range(window_size):
                        data = file.read(buffer_size - 10)
                        data = (str(i) + ";").encode('utf-8') + data
                        data = data.zfill(buffer_size)

                        self.socket.sendto(data, (ip, port))

                    ack_msg = self.socket.recv(buffer_size)
                    ack_msg = ack_msg.decode('utf-8').lstrip('0')
                    if ack_msg == "ACK":
                        break
                    
                except socket.timeout:
                    continue



#################################################################################
    def receive_file(self):
        header, addr = self.receive_header()
        file_name, file_size = header.split(";")

        self.socket.settimeout(0.1)

        global buffer_size
        pckg_num = int(np.ceil(int(file_size) / (buffer_size - 10)))

        start_time = time.time()

        lost_packages = self.receive_file_content(file_name, pckg_num, addr)

        end_time = time.time()

        print("File %s received from %s:%d" % (file_name, addr[0], addr[1]))
        print("File size: %s bytes" % (str("{:,}".format(int(file_size)).replace(',','.'))))
        print("Total packages received %d/%d" % (pckg_num, pckg_num))
        print("Total lost packages %d" % (lost_packages))
        print("Time spent: %.6f seconds" % (float(end_time) - start_time))

        total_per_s = float(int(file_size) / (end_time - start_time))
        print("Total %s bits/s" % (str("{:,}".format(total_per_s).replace('.','#').replace(',','.').replace('#',","))))

    def receive_header(self):
        while True:
            try:
                header, addr = self.socket.recvfrom(buffer_size)
                self.socket.sendto("ACK".encode('utf-8'), addr)
                header = header.decode('utf-8').lstrip('0')
                break
            except socket.timeout:
                continue


        print("Header has been received")
        return header, addr

    def receive_file_content(self, file_name, pckg_num, addr):
        global buffer_size
        file = open("chegou-" + file_name, "wb")

        lost_packages = 0
        for i in range(1, int((pckg_num + 1)/window_size)):
            if i % 5000 == 0:
                print("Receiving package %d of %d" % (i, pckg_num))
            while True:
                data_list = []
                try:
                    for i in range(window_size):
                        data, addr = self.socket.recvfrom(buffer_size)
                        if len(data) != buffer_size:
                            lost_packages += 1
                            continue

                        header = data[:data.find(b';')]
                        header = header.decode('utf-8').lstrip('0')
                        data = data[data.find(b';') + 1:]

                        data_list.append(data)
                    
                    self.socket.sendto("ACK".encode('utf-8'), addr)
                    
                except socket.timeout:
                    lost_packages += 1
                    continue

                for i in range(window_size):
                        file.write(data_list[i])

        file.close()
        return lost_packages

if __name__ == "__main__":
    __select__ = choose_peer_type()

    choose_package_size()
    choose_window_size()

    if(__select__ == 1):
        peer = Peer("191.52.64.209", 3000)
        peer.socket.bind((peer.ip, peer.port))
        peer.receive_file()
    else:
        peer = Peer("191.52.64.63", 3000)
        peer.send_file("musica.flac", "191.52.64.209", 3000)