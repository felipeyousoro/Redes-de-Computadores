import socket
import threading
import time

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nick = "" 
    
def receiveClient():
    global socket 
    
    while True: 
        message = socket.recv(1024).decode("utf-8")

        if not message: break

        print(message) 

def send():
    global socket 
    global nick 

    while True:
        message = input()
        socket.send((nick + ": " + message).encode("utf-8")) 

def receiveServer(client):
    while True:
        message = client.recv(1024).decode("utf-8") 

        if not message: break

        print(message)

def sendServer(client):
    while True:
        message = input()
        client.send((nick + ": " + message).encode("utf-8")) 

def serverManager():
    while(True):
        client, address = socket.accept() 

        rcv = threading.Thread(target=receiveServer, args=(client,)) 
        rcv.start() 

        snd = threading.Thread(target=sendServer, args=(client,)) 
        snd.start() 

if __name__ == "__main__":
    #HOST = str(input("Enter host: "))
    HOST = "191.52.64.217"
    PORT = int(input("Enter port: ")) 
    nick = str(input("Enter your nickname: ")) 
    role = int(input("Type 1 if you want to be a server, else you will be a socket "))

    if role != 1:
        socket.connect((HOST, PORT))
    else:
        socket.bind((HOST, PORT))
        socket.listen(1)
        serverManager()

    rcv = threading.Thread(target=receiveClient) # cria thread para receber mensagens do servidor
    rcv.start() 

    snd = threading.Thread(target=send) # cria thread para enviar mensagens para o servidor
    snd.start()

    while(True):
        time.sleep(1)

    socket.close()

