import socket
from _thread import *
import os
import json
import re
from settings import *

connections = []
ThreadCount = 0
ServerSideSocket = socket.socket()

# OS FUNCTIONS #

def WriteInFile(id, field, value):
    """
        Write in the JSON file a given value in a given field for a given id.
        Args: 
            id: (int) The id of the user you want to modify
            field: (string) The field you want to write
            value: (string) The value you want to write
    """
    value = value.replace('\n', '')
    
    with open(DATAFILE, 'r') as f:
        json_object = json.load(f)
        
        if id in json_object:
            json_object[id][field] = value
        else:
            json_object[id] = {field: value}
        
    with open(DATAFILE, 'w') as f:
        f.write(json.dumps(json_object, indent=4))

def getIdByEmail(email):
    """
        Get the id of a user with his email.
        Args: 
            email: (string) The email of the user you want to get the id
        Returns:
            The id of the user
    """
    with open(DATAFILE, 'r') as f:
        json_object = json.load(f)
        
        for id in json_object:
            if email == json_object[id]['email']:
                return id
    return -1

# SOCKET FUNCTIONS #    
    
def sendToClient(connection, message):
    """
        Send a message to the client.
        Args:
            connection: (socket) The connection with the client
        Returns:
            The message to send to the client.
    """
    connection.send(str.encode(message))

def receiveFromClient(connection):
    """
        Receive a message from the client.
        Args:
            connection: (socket) The connection with the client
        Returns:
            The message received from the client
    """
    data = connection.recv(2048)
    if not data:
        sendToClient(connection, 'No data, please try again')
        raise Exception('No data received')
        return ""
    else:
        return data.decode('utf-8')

def askForInput(connection, asked_input = '', message_code= '#02'):
    """
        Ask the client to send a message to the server.
        Args: 
            connection: (socket) The connection with the client
        Returns:
            The message received from the client
    """
    sendToClient(connection, message_code + ' afi: ' + asked_input)
    return receiveFromClient(connection)

# VALIDATOR FUNCTIONS #

def ValidateEmail(email):
    """
        Validate an email.
        Args: 
            email: (string) The email you want to validate
        Returns:
            True if the email is valid, False otherwise
    """
    if '@' in email and '.' in email:
        print('Email is valid.')
        return True
    else:
        print('Error: Email isn\'t valid.')
        return False

def EmailValidator(connection, email):
    """
        Validate an email and send the response to the client.
        Args: 
            connection: (socket) The connection with the client
            email: (string) The email you want to validate
    """
    sendToClient(connection, 'Validating email...')
    if not ValidateEmail(email):
        sendToClient(connection, '#09 Email is invalid, please check your email or contact the administrator.')
        print('Email validation failed.')
        return False
    else:
        print('Email validation success.')
        return True

def ValidatePassword(password):
    """
        Validate the password. (must contains only a-z, A-Z, 0-9, #,$,!,&)
        Args:
            password: (string) The password you want to validate
        Returns:
            True if the password is valid, False otherwise
    """
    if re.match('^[a-zA-Z0-9#,$,!,&]+$', password):
        print('Password is valid')
        return True
    else:
        print('Error: Password isn\'t valid.')
        return False

def CheckEmailInJSON(email):
    """
        Check if an email is in the JSON file.
        Args: 
            email: (string) The email you want to check
        Returns:
            True if the email is in the JSON file, False otherwise
    """
    with open(DATAFILE, 'r') as f:
        json_object = json.load(f)
        
        for id in json_object:
            if email == json_object[id]['email']:
                print('Email is in json')
                return True
    print('Error: Email isn\'t in json')
    return False

def CheckPasswordForID(id, password):
    """
        Check if a password is the good one for a given id.
        Args: 
            id: (int) The id of the user you want to check
            password: (string) The password you want to check
        Returns:
            True if the password is the good one, False otherwise
    """
    with open(DATAFILE, 'r') as f:
        json_object = json.load(f)
        
        if id in json_object:
            if password == json_object[id]['password']:
                print('Password is correct')
                return True
    print('Error: Password is incorrect for' + email)
    return False

def CheckPasswordForEmail(email, password):
    """
        Check if a password is the good one for a given email.
        Args: 
            email: (string) The email you want to check
            password: (string) The password you want to check
        Returns:
            True if the password is the good one, False otherwise
    """
    with open(DATAFILE, 'r') as f:
        json_object = json.load(f)
        
        for id in json_object:
            if email == json_object[id]['email'] and password == json_object[id]['password']:
                print('Password is correct')
                return True
    print('Error: Password is incorrect for' + email)
    return False

def PasswordValidator(connection, email, password):
    """
        Validate the password step and send the response to the client.
            Checks are ValidatePassword, CheckEmailInJSON, CheckPasswordForID
        Args: 
            connection: (socket) The connection with the client
            email: (string) The email you want to validate
            password: (string) The password you want to validate
    """
    sendToClient(connection, 'Validating password...')
    if not ValidatePassword(password):
        sendToClient(connection, '#09 Password is invalid, please check your password or contact the administrator')
        return False
    elif not CheckEmailInJSON(email):
        sendToClient(connection, '#09 An error occured, please check your credentials or contact the administrator')
        return False
    elif not CheckPasswordForEmail(email, password):
        sendToClient(connection, '#09 An error occured, please check your credentials or contact the administrator')
        return False
    else:
        sendToClient(connection, '#01 Credentials are valid, you can now send your public key')
        return True

def CheckEmailPK(email):
    """
        Check if an email already has a public key.
        Args: 
            email: (string) The email you want to check
        Returns:
            True if the email hasn't a public key, False otherwise
    """
    with open(DATAFILE, 'r') as f:
        json_object = json.load(f)
        
        for id in json_object:
            if email == json_object[id]['email'] and not json_object[id]['public_key']:
                return True
    return False
    
# THREAD FUNCTIONS #

def multi_threaded_client(connection, thread):
    print('Connected to: ' + address[0] + ':' + str(address[1]) + ' with thread ' + str(thread))
    
    # Start the discussion with the client #
    connection.send(str.encode('#00 Server is working:'))
    
    # Step 1: Receive the email #
    print(str(thread) + ': Waiting for email...')
    try:
        email = askForInput(connection, 'Email')
    except Exception as e:
        print(str(thread) + ':', e)
        connection.close()
        return
            
    # Step 2: Validate the email #
    print(str(thread) + ': Validating the email (' + email + ')')
    if not EmailValidator(connection, email):
        print(str(thread) + ": Email is invalid, closing the connection...")
        connection.close()
        return
    print(str(thread) + ': Email is valid.')
        
    
    # Step 3: Receive the password #
    print(str(thread) + ': Waiting for password...')
    try:
        password = askForInput(connection, 'Password')
    except Exception as e:
        print(e)
        connection.close()
        print(str(thread) + ': ' + e)
        return
    
    # Step 4: Validate the password #
    print(str(thread) + ': Validating the password (' + password + ')')
    if not PasswordValidator(connection, email, password):
        print(str(thread) + ": Password is invalid, closing the connection...")
        connection.close()
        return
    print(str(thread) + ': Password is valid.')
        
    # Step 5: Receive the public key #
    print(str(thread) + ': Waiting for public key...')
    try:
        publicKey = askForInput(connection, 'public key', '#03')
    except Exception as e:
        print(str(thread) + ':', e)
        connection.close()
        return
    print(str(thread) + ': Public key received.')
    
    # Step 6: Check if the email already has a public key #
    # TODO #
    
    # Step 7: Save the public key #
    userID = getIdByEmail(email)
    if userID:
        print(str(thread) + ': Saving the public key...')
        WriteInFile(userID, 'public_key', publicKey)
        print(str(thread) + ': Public key saved for ' + email + '!') 
    
    # Step 8: Inform the client that the public key is saved #
    sendToClient(connection, '#08 Public key saved!')
    
    # Close the connection now ? #
    
    #Step 9: Close the connection #
    connection.close()
    
    # End of the discussion with the client #
    
    # Populate the public key to the pools #
    
    return    

# ADMIN FUNCTIONS #

def admin_thread():
    """ 
        The admin thread is used to manage the server. It's a GUI with tkinter, where 
        you can view and edit the pools, the users, the logs, etc...
    """
    # TODO #
    
# POOLS FUNCTIONS #

def getPools():
    """
        Get the pools from the pools.json file.
        Returns:
            The pools.json file as a dict
    """
    with open(POOLSFILE, 'r') as f:
        json_object = json.load(f)
        return json_object

def getMachinesFromPool(pool):
    """
        Get the machines from a pool.
        Args:
            pool: (string) The pool you want to get the machines from.
        Returns:
            A list of machines from the pool.
    """
    # Read in json file the machines from the pool #
    with open(POOLFILE, 'r') as f:
        json_object = json.load(f)
        machines = []
        for id in json_object:
            if json_object[id]['pool'] == pool:
                machines.append(json_object[id]['machine'])
        return machines

def Populate(public_key, pool):
    """
        Populate a pool with a public key.
        Connect on every machine of the pool and send the public key.
        Args:
            public_key: (string) The public key you want to add to the pool
            pool: (string) The pool you want to populate.
    """
    for machine in getMachinesFromPool(pool):
        # Connect to machine on port 4242 and send the public key #
        print('Connecting to ' + machine + '...')
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((machine, 4242))
            s.send(str.encode(public_key))
            s.close()
        except Exception as e:
            print(e)
            return False
    return True


if __name__ == '__main__':   
    try:
        ServerSideSocket.bind((HANDLER_IP, HANDLER_PORT))
    except socket.error as e:
        print(str(e))
        
    print('Socket is listening..')

    ServerSideSocket.listen(5)

    while True:
        Client, address = ServerSideSocket.accept()
        ThreadCount += 1
        connections.append({'connection': Client, 'address': address, 'thread': ThreadCount})
        start_new_thread(multi_threaded_client, (Client, ThreadCount,))
        print('Thread Number: ' + str(ThreadCount))
        
        # Make a thread waiting for an input from the admin on stdin #
        start_new_thread(admin_thread, ())
    
    ServerSideSocket.close()