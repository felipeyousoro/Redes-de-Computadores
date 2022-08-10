import socket
import threading
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nick = ""

def receive():
    global client 
    
    while True:
        message = client.recv(1024).decode("utf-8")

        if not message: break

        print(message)

def send():
    global client 
    global nick 

    while True:
        message = input()
        client.send((nick + ": " + message).encode("utf-8"))


if __name__ == "__main__":
    #HOST = str(input("Enter host: "))
    #PORT = int(input("Enter port: "))
    nick = str(input("Enter your nickname: "))

    #client.connect((HOST, PORT))    
    client.connect(("localhost", 55555))

    rcv = threading.Thread(target=receive)
    rcv.start()

    snd = threading.Thread(target=send)
    snd.start()

    while(True):
        time.sleep(1)

    client.close()

