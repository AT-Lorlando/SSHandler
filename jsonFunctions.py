import json
from settings import *

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

def ReadFromFile(id, field):
    """
        Read in the JSON file a given field for a given id.
        Args: 
            id: (int) The id of the user you want to read
            field: (string) The field you want to read
        Returns:
            The value in the field for the given id
    """
    with open(DATAFILE, 'r') as f:
        json_object = json.load(f)
        
        if id in json_object:
            return json_object[id][field]
        else:
            return ""
        
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
    with open(POOLSFILE, 'r') as f:
        json_object = json.load(f)
        machines = []
        for machine in json_object[pool]['machines']:
            machines.append(machine)
        return machines