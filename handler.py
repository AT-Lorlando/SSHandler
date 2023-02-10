import socket
from _thread import *
import os
import json
import re
from settings import *
from jsonFunctions import *
from sshFunctions import *

connections = []
ThreadCount = 0
ServerSideSocket = socket.socket()

# OS FUNCTIONS #

# def WriteInFile(id, field, value):
        
# def ReadFromFile(id, field):

# def getIdByEmail(email):

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

# def CheckEmailInJSON(email):

# def CheckPasswordForID(id, password):

# def CheckPasswordForEmail(email, password):

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

# def CheckEmailPK(email)

    
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
    sendToClient(connection, '#01 Public key saved!')

    # Close the connection now ? #

    # End of the discussion with the client #

    # Population of the pools #

    # Get the pool of the user #

    # TODO: More than one pool #
    userPool = ReadFromFile(userID, 'pool')

    # Populate the public key to the pools #
    
    username = email.split("@")[0]

    Populate(username, password, userID, userPool)

    userMachines = getMachinesFromPool(userPool)
    # to string
    strMachines = ""
    for machine in userMachines:
        strMachines += machine + "\n"

    sendToClient(connection, '#08 Your instance is now ready to use! You can now connect to it with SSH.\n   ssh -i your_key ' + username + '@server_ip\n  You have acces to the following machines:\n' + strMachines)

    # sendToClient(connection, '#08 Public key populated to the pools!')

    #Step 9: Close the connection #
    connection.close()

    return

# ADMIN FUNCTIONS #

def admin_thread():
    """ 
        The admin thread is used to manage the server. It's a GUI with tkinter, where 
        you can view and edit the pools, the users, the logs, etc...
    """
    # TODO #
    
# POOLS FUNCTIONS #

# def getPools():

# def getMachinesFromPool(pool):

def Populate(username, password, userID, pool):
    """
        Populate a pool with a public key.
        Connect on every machine of the pool and send the public key.
        Args:
            userID: (string) The ID of the user
            pool: (string) The name of the pool
    """
    # Get the public key #
    publicKey = ReadFromFile(userID, 'public_key')
    
    # Get the machines of the pool #
    machines = getMachinesFromPool(pool)
    
    # Connect to every machine and send the public key #
    for machine in machines:
        print('Handler: connecting to ' + machine + '...')
        AddNewUser(username=username, password=password, public_key=publicKey, machine=machine)


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