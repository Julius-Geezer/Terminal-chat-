import socket
import threading
import rsa 
import os 

ip_address = input('Enter IP address: ') 

# Initializing server
host = ip_address 
port = 9999 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((host, port)) 
server.listen() 
print('[*] Server is online') 


# Storing clients and their names 
clients = [] 
names = [] 


# Sending messages to all clients connected to the server 
def broadcast_message(message):
    for client in clients: 
        client.send(message) 


# Saving messages from clients then sending them to other clients using previous function 
# Handling clients leaving the server
# Sends all messages to an encrypted .txt file for logging purposes 
def handle_clients(client): 
    while True:
        try:
            message = client.recv(1024) 
            broadcast_message(message)
            with open('encrypted_chatlogs.txt', 'a') as f:
                f.write(message.decode('ascii') + '\n')
        except:
            index = clients.index(client) 
            clients.remove(client) 
            client.close() 
            name = names[index] 
            broadcast_message('{} has disconnected'.format(name).encode('ascii')) 
            names.remove(name)
            break 


# Handling server side information
# Sending connection details to clients 
# Initializing thread 
def server_receive():
    while True:
        client, address = server.accept()
        print('[*] Connected with {}'.format(str(address))) 
        client.send('NAME'.encode('ascii'))
        name = client.recv(1024).decode('ascii') 
        names.append(name) 
        clients.append(client)
        
        print('[*] User {} has connected'.format(name)) 
        broadcast_message('{} has joined'.format(name).encode('ascii'))
        client.send('Connection successful'.encode('ascii'))

        thread = threading.Thread(target=handle_clients, args=(client,)) 
        thread.start()


if __name__ == '__main__':
    server_receive()
