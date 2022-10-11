from select import select
import socket
import numpy as np
import os
import time 

class Peer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#################################################################################
    def send_file(self, file_name, ip, port):
        file = open(file_name, "rb")
        self.send_file_header(file_name, ip, port)
        
        pckg_num = int(np.ceil(os.path.getsize(file_name) / 990))
        self.send_file_content(file, pckg_num, ip, port)
   
        print("\tFile %s sent to %s:%d" % (file_name, ip, port))
        file.close()

    def send_file_header(self, file_name, ip, port):
        file_size = os.path.getsize(file_name)

        header = file_name + ";" + str(file_size)
        header = header.zfill(1000)
        header = header.encode('utf-8')
        
        ack_msg = ""
        while ack_msg != "ACK":
            self.socket.sendto(header, (ip, port))
            ack_msg = self.socket.recv(1000)
            ack_msg = ack_msg.decode('utf-8')

        print("\tHeader has been sent")

    def send_file_content(self, file, pckg_num, ip, port):
        for i in range(1, pckg_num + 1):
            data = file.read(990)
            data = (str(i) + ";").encode('utf-8') + data
            data = data.zfill(1000)

            self.socket.sendto(data, (ip, port))



#################################################################################
    def receive_file(self):
        header, addr = self.receive_header()
        file_name, file_size = header.split(";")
        
        self.socket.settimeout(0.05)
        start_time = time.time()

        pckg_num = int(np.ceil(os.path.getsize(file_name) / 990))
        self.receive_file_content(file_name, pckg_num, addr)

        # print("\tReceived file %s" % file_name)
        # print("Time spent: %s seconds" % (time.time() - start_time))
        # print("Download speed: %s bps" % ( float(file_size * 8) / (time.time() - start_time) ))


    def receive_header(self):
        header, addr = self.socket.recvfrom(1000)
        while not header:
            header, addr = self.socket.recvfrom(1000)
        self.socket.sendto("ACK".encode('utf-8'), addr)

        header = header.decode('utf-8').lstrip('0')

        print("\tHeader has been received")
        return header, addr

    def receive_file_content(self, file_name, pckg_num, addr):
        file = open("recebido.png", "wb")

        for i in range(1, pckg_num + 1):
            data, addr = self.socket.recvfrom(1000)
            
            header = data[:data.find(b';')]
            header = header.decode('utf-8').lstrip('0')
            data = data[data.find(b';') + 1:]

            file.write(data)
            
        file.close()

if __name__ == "__main__":
    rcv_snd = int(input("Send or receive file? (0/1): "))

    if(rcv_snd == 1):
        peer = Peer("191.52.64.211", 3000)
        peer.socket.bind((peer.ip, peer.port))
        peer.receive_file()
    else:
        peer = Peer("191.52.64.211", 3000)
        peer.send_file("bg.png", "191.52.64.211", 3000)
    
