import socket
import threading
import rsa 

host = '10.0.0.100' 
port = 9999 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((host, port)) 
server.listen() 

clients = [] 
names = [] 

def broadcast_message(message):
    for client in clients: 
        client.send(message) 


def handle_clients(client): 
    while True:
        try:
            message = client.recv(1024) 
            broadcast_message(message)
        except:
            index = clients.index(client) 
            clients.remove(client) 
            client.close() 
            name = names[index] 
            broadcast_message('{} has disconnected'.format(name).encode('ascii')) 
            names.remove(name)
            break 


def server_receive():
    while True:
        client, address = server.accept()
        print('Connected with {}'.format(str(address))) 
        client.send('NAME'.encode('ascii'))
        name = client.recv(1024).decode('ascii') 
        names.append(name) 
        clients.append(client)
        
        print('User {} has connected'.format(name)) 
        broadcast_message('{} has joined'.format(name).encode('ascii'))
        client.send('Connection successful!'.encode('ascii'))

        thread = threading.Thread(target=handle_clients, args=(client,)) 
        thread.start()


if __name__ == '__main__':
    server_receive()
    print('[*] Server is active') 

