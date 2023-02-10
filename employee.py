import socket
import os
from settings import *
import random

def receiveFromServer():
    """
        Receive a message from the client.
        Args:
            connection: (socket) The connection with the client
        Returns:
            The message received from the client
    """
    data = ClientMultiSocket.recv(2048)
    if not data:
        # raise Exception('No data received')
        ClientMultiSocket.close()
        return ""
    else:
        return data.decode('utf-8')

def sendToServer(message):
    """
        Send a message to the client.
        Args:
            connection: (socket) The connection with the client
        Returns:
            The message to send to the client.
    """
    ClientMultiSocket.send(str.encode(message))

def generateKey(email = 'x@x.fr'):
    """
        Generate a key with ssh-keygen.
        Return:
            (pubkey: (string) The public key generated
    """
    x = random.randint(0, 10000)
    os.system(f'ssh-keygen -t ed25519 -f key{x} -N "" -C ' + email)
    with open(f'key{x}.pub', 'r') as f:
        pubkey = f.read()
    with open(f'key{x}', 'r') as f:
        privkey = f.read()
    return privkey, pubkey

if __name__ == '__main__':
    ClientMultiSocket = socket.socket()
    running = True

    print('Waiting for connection response')

    try:
        ClientMultiSocket.connect((HANDLER_IP, HANDLER_PORT
        ))
    except socket.error as e:
        print(str(e))
        
    # Step 0: connect to the server #
    res = receiveFromServer()
    if res.startswith('#00'):
        print('Connection successful')
    else:
        print('Connection failed')
        exit(1)

    while running:
        res = receiveFromServer()
        code = res[:3] 
        
        # If res start with #01, it's a message from the server, just print it
        if code == '#01':
            print(res)
        # If res start with #02, it's a message from the server, asking for an input, ask for an input and send it
        elif code == '#02':
            input_asked = res.split(': ')[1]
            i = input('Please enter ' + input_asked + ': ')
            sendToServer(i)
        # If res start with #03, it's a message from the server, asking for generate the key, generate it and send it.
        elif code == '#03':
            privateKey, publicKey = generateKey()
            sendToServer(publicKey)
        # if res start with #08, we can now end the connection
        elif code == '#08':
            print('Connection ended')
            ClientMultiSocket.close()
            running = False
        # if res start with #09, it's an error code, print it and exit
        elif code == '#09':
            print(res)
            exit(1)