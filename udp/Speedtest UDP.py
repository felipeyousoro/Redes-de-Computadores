from select import select
import socket
import numpy as np
import os
import readchar
import sys
import time 

buffer_size = 500
window_size = 2
package_content = "teste de rede *2022*".zfill(buffer_size)


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

# def choose_package_size():
#     select = 0
#     print("Which package size would you like to use?")
#     while (True):
#         if select == 0:
#             sys.stdout.write("\r=> 1000\t   1500")
#         elif select == 1:
#             sys.stdout.write("\r   1000\t=> 1500")
#         inpt = (repr(readchar.readkey()))
#         if inpt[2] == 'r':
#             print("")
#             global buffer_size
#             buffer_size = 1000 + 500 * select
#             return select
#         if inpt[5] == 'K':
#             select = 0
#         elif inpt[5] == 'M':
#             select = 1

#         sys.stdout.flush()

# def choose_window_size():
#     select = 0
#     print("Which window size would you like to use?")
#     while (True):
#         if select == 0:
#             sys.stdout.write("\r=> 2\t   4")
#         elif select == 1:
#             sys.stdout.write("\r   2\t=> 4")
#         inpt = (repr(readchar.readkey()))
#         if inpt[2] == 'r':
#             print("")
#             global window_size
#             window_size = 2 + 2 * select
#             return select
#         if inpt[5] == 'K':
#             select = 0
#         elif inpt[5] == 'M':
#             select = 1

class Peer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


#################################################################################
    def send_packages(self, ip, port, _time):
        packages_sent = 0

        start_time = time.time()
        while time.time() - start_time < _time:
            self.socket.sendto(package_content.encode(), (ip, port))
            packages_sent += 1

        print("Packages sent: " + str(packages_sent))
        print("Packages by second: " + str(packages_sent / _time))
        print("Total bytes sent: " + str(packages_sent * buffer_size * 8))
        print("Total bits per second: " + str(packages_sent * buffer_size * 8 / _time))
        print("Total kilobits per second: " + str(packages_sent * buffer_size * 8 / (_time * 1000)))
        print("Total megabits per second: " + str(packages_sent * buffer_size * 8 / (_time * 1000000)))
        print("Total gigabits per second: " + str(packages_sent * buffer_size * 8 / (_time * 1000000000)))
        
#################################################################################
    def receive_packages(self, _time):
        packages_received = 0

        while True:
            try:
                self.socket.recvfrom(buffer_size)
                packages_received += 1
                break
            except:
                pass

        start_time = time.time()
        while time.time() - start_time < _time:
            try:
                self.socket.recvfrom(buffer_size)
                packages_received += 1
            except:
                pass

        print("Packages sent: " + str(packages_received))
        print("Packages by second: " + str(packages_received / _time))
        print("Total bytes sent: " + str(packages_received * buffer_size * 8))
        print("Total bits per second: " + str(packages_received * buffer_size * 8 / _time))
        print("Total kilobits per second: " + str(packages_received * buffer_size * 8 / (_time * 1000)))
        print("Total megabits per second: " + str(packages_received * buffer_size * 8 / (_time * 1000000)))
        print("Total gigabits per second: " + str(packages_received * buffer_size * 8 / (_time * 1000000000)))

    

if __name__ == "__main__":
    __select__ = choose_peer_type()

    # choose_package_size()
    # choose_window_size()

    if(__select__ == 1):
        peer = Peer("192.168.1.6", 3000)
        peer.socket.bind((peer.ip, peer.port))
        peer.receive_packages(20)
    else:
        peer = Peer("192.168.1.6", 3000)
        peer.send_packages("192.168.1.6", 3000, 20)