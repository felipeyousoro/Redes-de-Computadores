from select import select
import socket
import numpy as np
import os
import time 

package_size = 1000


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

        global package_size
        pckg_num = int(np.ceil(os.path.getsize(file_name) / (package_size - 10)))

        self.send_file_content(file, pckg_num, ip, port)
   
        print("File %s sent to %s:%d" % (file_name, ip, port))
        file.close()

    def send_file_header(self, file_name, ip, port):
        file_size = os.path.getsize(file_name)

        header = file_name + ";" + str(file_size)
        header = header.zfill(package_size)
        header = header.encode('utf-8')
        
        ack_msg = ""
        while True:
            try:
                self.socket.sendto(header, (ip, port))
                ack_msg = self.socket.recv(package_size)
                ack_msg = ack_msg.decode('utf-8').lstrip('0')
                if ack_msg == "ACK":
                    break
            except socket.timeout:
                continue

    def send_file_content(self, file, pckg_num, ip, port):
        global package_size

        for i in range(1, pckg_num + 1):
            if i % 5000 == 0:
                print("Sending package %d of %d" % (i, pckg_num))
            while True:
                try:
                    data = file.read(package_size - 10)
                    data = (str(i) + ";").encode('utf-8') + data
                    data = data.zfill(package_size)

                    self.socket.sendto(data, (ip, port))
                    ack_msg = self.socket.recv(package_size)
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

        global package_size
        pckg_num = int(np.ceil(int(file_size) / (package_size - 10)))
        self.receive_file_content(file_name, pckg_num, addr)

        print("File %s received from %s:%d" % (file_name, addr[0], addr[1]))
        # print("\tReceived file %s" % file_name)
        # print("Time spent: %s seconds" % (time.time() - start_time))
        # print("Download speed: %s bps" % ( float(file_size * 8) / (time.time() - start_time) ))


    def receive_header(self):
        while True:
            try:
                header, addr = self.socket.recvfrom(package_size)
                self.socket.sendto("ACK".encode('utf-8'), addr)
                header = header.decode('utf-8').lstrip('0')
                break
            except socket.timeout:
                continue


        print("Header has been received")
        return header, addr

    def receive_file_content(self, file_name, pckg_num, addr):
        global package_size
        file = open("chegou-" + file_name, "wb")

        for i in range(1, pckg_num + 1):
            if i % 5000 == 0:
                print("Receiving package %d of %d" % (i, pckg_num))
            while True:
                try:
                    data, addr = self.socket.recvfrom(package_size)
                    self.socket.sendto("ACK".encode('utf-8'), addr)
                    header = data[:data.find(b';')]
                    header = header.decode('utf-8').lstrip('0')
                    data = data[data.find(b';') + 1:]

                    file.write(data)
                    break
                except socket.timeout:
                    continue

        file.close()

if __name__ == "__main__":
    rcv_snd = int(input("Send or receive file? (0/1): "))

    if(rcv_snd == 1):
        peer = Peer("192.168.1.6", 3000)
        peer.socket.bind((peer.ip, peer.port))
        peer.receive_file()
    else:
        peer = Peer("192.168.1.6", 3000)
        peer.send_file("musica.flac", "192.168.1.6", 3000)
    
