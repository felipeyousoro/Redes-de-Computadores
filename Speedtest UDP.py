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

        print("Packages sent: " + formatar_milhar(str(packages_sent)))
        print("Packages by second: " + formatar_milhar(str(packages_sent / _time)))
        print("Total bytes sent: " + formatar_milhar(str(packages_sent * buffer_size * 8)))
        print("Total bits per second: " + formatar_milhar(str(packages_sent * buffer_size * 8 / _time)))
        print("Total kilobits per second: " + formatar_milhar(str(packages_sent * buffer_size * 8 / (_time * 1000))))
        print("Total megabits per second: " + formatar_milhar(str(packages_sent * buffer_size * 8 / (_time * 1000000))))
        print("Total gigabits per second: " + formatar_milhar(str(packages_sent * buffer_size * 8 / (_time * 1000000000))))
        
#################################################################################
    def receive_packages(self, _time):
        packages_received = 0

        start_time = time.time()
        while True:
            ready = select([self.socket], [], [], 5)
            if ready[0]:
                data, addr = self.socket.recvfrom(buffer_size)
                packages_received += 1
            else:
                break

        total_time = time.time() - start_time - 5

        print("Packages received: " + formatar_milhar(str(packages_received)))
        print("Packages by second: " + formatar_milhar(str(packages_received / total_time)))
        print("Total bytes received: " + formatar_milhar(str(packages_received * buffer_size * 8)))
        print("Total bits per second: " + formatar_milhar(str(packages_received * buffer_size * 8 / total_time)))
        print("Total kilobits per second: " + formatar_milhar(str(packages_received * buffer_size * 8 / (total_time * 1000))))
        print("Total megabits per second: " + formatar_milhar(str(packages_received * buffer_size * 8 / (total_time * 1000000))))
        print("Total gigabits per second: " + formatar_milhar(str(packages_received * buffer_size * 8 / (total_time * 1000000000))))

    

if __name__ == "__main__":
    __select__ = choose_peer_type()

    # choose_package_size()
    # choose_window_size()

    if(__select__ == 1):
        peer = Peer("191.52.64.138", 3000)
        peer.socket.bind((peer.ip, peer.port))
        peer.receive_packages(20)
    else:
        peer = Peer("191.52.64.138", 3000)
        peer.send_packages("191.52.64.98", 3000, 20)