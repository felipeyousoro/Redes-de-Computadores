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

         
def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


if __name__ == "__main__":
    #HOST = socket.gethostbyname(socket.gethostname()) # host do servidor
    HOST = extract_ip()
    print(HOST)
    PORT = int(input("Enter port: ")) # porta do servidor

    server.bind((HOST, PORT)) # bind do servidor
    server.listen(1) # escuta conexões do servidor

    manager() # chamada de função para gerenciar conexões do servidor
