import socket
import threading
import time

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
file_size = 500

def serverManager():
    while(True):
        client, address = socket.accept() 

        #filename = client.recv(file_size).decode("utf-8")
        
        file = open("recebido.mkv", "wb")

        while(True):
            data = client.recv(file_size)

            if not data:
                print("END")
                file.close()
                client.close()
                exit()

            file.write(data)

if __name__ == "__main__":
    #HOST = str(input("Enter host: "))
    HOST = "191.52.64.217"
    PORT = int(input("Enter port: ")) 
    role = int(input("Type 1 if you want to be a server, else you will be a socket "))

    if role != 1:
        socket.connect((HOST, PORT))
        with open("anime.mkv", "rb") as f:
            while True:
                line = f.read(file_size)
                if not line:
                    f.close()
                    break
                socket.send(line)
        socket.close()
        exit()
    else:
        socket.bind((HOST, PORT))
        socket.listen(1)
        serverManager()



