import socket
import threading
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nick = "" # nick do cliente

def asciiCode(char):
    return ord(char)
    
def receive():
    global client 
    
    while True: 
        message = client.recv(1024).decode("utf-8") # recebe mensagem do servidor

        if not message: break

        print(message) # imprime mensagem do servidor

def send():
    global client 
    global nick 

    while True:
        message = input()
        client.send((nick + ": " + message).encode("utf-8")) # envia mensagem para o servidor


if __name__ == "__main__":
    HOST = str(input("Enter host: ")) # host do servidor
    PORT = int(input("Enter port: ")) # porta do servidor
    nick = str(input("Enter your nickname: ")) # nick do cliente

    client.connect((HOST, PORT)) # conecta ao servidor

    rcv = threading.Thread(target=receive) # cria thread para receber mensagens do servidor
    rcv.start() # inicia thread

    snd = threading.Thread(target=send) # cria thread para enviar mensagens para o servidor
    snd.start() # inicia thread

    while(True):
        time.sleep(1)

    client.close()

