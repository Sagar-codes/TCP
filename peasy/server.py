import threading
import socket

# post addr and port for server

host = '127.0.0.1' #localhost
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()
print("The Server is Running...")

clients = []
names = []


def brodcast(message):
    for client in clients:
        client.send(message)


def handel(client):
    while True:
        try:
            message = client.recv(1024)
            brodcast(message)
        except Exception as e:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            brodcast(f"{name} Left the Chat!".encode('ascii'))
            names.remove(name)
            break
    

def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected With {str(address)} ")

        client.send("NAME".encode('ascii'))

        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)

        print(f"name of client is {name}")
        brodcast(f"{name} joined the Chat".encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handel, args=(client,)) 
        thread.start()

recieve()