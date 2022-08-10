import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clients = []

def broadcastMessage(message):
    for client in clients:
        client.send(message.encode("utf-8"))

def receive(client):
    while True:
        message = client.recv(1024).decode("utf-8")

        if not message: break

        broadcastMessage(message)

def manager():
    while(True):
        client, address = server.accept()
        clients.append(client)

        print("Connected with {}".format(str(address)))
        print("Greta Thunberg impregnator has joined the chat")
        rcv = threading.Thread(target=receive, args=(client,))
        rcv.start()

         



if __name__ == "__main__":
    #HOST = str(input("Enter host: "))
    #PORT = int(input("Enter port: "))

    #server.bind((HOST, PORT))
    server.bind(("localhost", 55555))
    server.listen(1)

    manager()
    