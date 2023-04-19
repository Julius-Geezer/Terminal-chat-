import socket 
import threading 

name = input('Choose your name: ') 


# Initializing client and connecting to the server 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect(('10.0.0.100', 7976)) 


# Receiving messages and error handling for unsuccessful connections 
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NAME':
                client.send(name.encode('ascii'))
            else:
                print(message) 
        except:
            print('[*] An error has occured, connection unsuccessful.') 
            client.close()
            break


# Writing messages and sending them 
def write():
    while True:
        message = '{}: {}'.format(name, input(''))
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)

receive_thread.start()
write_thread = threading.Thread(target=write)

write_thread.start()
