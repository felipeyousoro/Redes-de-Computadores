import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clients = []    # lista de clientes conectados

def broadcastMessage(message):
    for client in clients:  # envia mensagem para todos os clientes conectados
        client.send(message.encode("utf-8")) 

def receive(client):
    while True:
        message = client.recv(1024).decode("utf-8") # recebe mensagem do cliente

        if not message: break

        broadcastMessage(message) # chamada de função para envia mensagem para todos os clientes conectados

def manager():
    while(True):
        client, address = server.accept() # aceita conexão do cliente
        clients.append(client) # adiciona cliente a lista de clientes conectados

        rcv = threading.Thread(target=receive, args=(client,)) # cria thread para receber mensagens do cliente
        rcv.start() # inicia thread

         



if __name__ == "__main__":
    HOST = str(input("Enter host: ")) # host do servidor
    PORT = int(input("Enter port: ")) # porta do servidor

    server.bind((HOST, PORT)) # bind do servidor
    server.listen(1) # escuta conexões do servidor

    manager() # chamada de função para gerenciar conexões do servidor