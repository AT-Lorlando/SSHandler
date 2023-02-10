# File to create the admin command
import json
from jsonFunctions import *
from sshFunctions import *

def CreateEmployee():
    print("Enter the employee details")
    email = input("Email: ")
    password = input("Password: ") # TODO: Hash the password
    print("Pools disponibles: ")
    POOLS = getPools()
    # Parse the pools and put them in a list
    poolTab = []
    for i,pool in enumerate(POOLS):
        poolTab.append(pool)
        print(f'{i}: {pool}')
    poolID = input("Pool (id): ")
    pool = poolTab[int(poolID)]
    print(f'Are the following details correct? (y/n)')
    print(f'Email: {email}')
    print(f'Password: {password}')
    print(f'Pool: {pool}')
    if input() == 'y':
        print("Creating the employee...")
        # Create the employee
        with open(DATAFILE, 'r') as f:
            json_object = json.load(f)
            id = str(len(json_object)+1)
            json_object[id] = {}
            json_object[id]['email'] = email
            json_object[id]['password'] = password
            json_object[id]['pool'] = pool
            json_object[id]['public_key'] = ''
        with open(DATAFILE, 'w') as f:
            json.dump(json_object, f, indent=4)
        print("Employee created!")
    else:
        print("Employee creation cancelled")
        
def DeleteEmployee():
    print("Employees list:")
    with open(DATAFILE, 'r') as f:
        json_object = json.load(f)
        for id in json_object:
            print(f'{id}: {json_object[id]["email"]}')
    ID = input("Employee ID: ")
    if ID not in json_object:
        print("Error: Employee ID doesn't exist")
        return
    print(f'Are you sure you want to delete the employee {json_object[ID]["email"]}? (y/n)')
    if input() == 'y':
        print("Deleting the employee...")
        username = json_object[ID]['email'].split('@')[0]
        machines = getMachinesFromPool(json_object[ID]['pool'])
        for machine in machines:
            DeleteUser(username, machine)
        # Delete the employee
        with open(DATAFILE, 'r') as f:
            json_object = json.load(f)
            del json_object[ID]
        with open(DATAFILE, 'w') as f:
            json.dump(json_object, f, indent=4)
        print("Employee deleted!")
        # TODO : Revoking the employee's public key
    else:
        print("Employee deletion cancelled")
        
def AddPool():
    print("Enter the pool details")
    pool = input("Pool: ")
    name = input("Name: ")
    print(f'Are the following details correct? (y/n)')
    print(f'Pool: {pool}')
    print(f'Name: {name}')
    if input() == 'y':
        print("Adding the pool...")
        # Add the pool
        with open(POOLSFILE, 'r') as f:
            json_object = json.load(f)
            json_object[pool] = {}
            json_object[pool]['name'] = name
            json_object[pool]['machines'] = []
        with open(POOLSFILE, 'w') as f:
            json.dump(json_object, f, indent=4)
        print("Pool added!")
    else:
        print("Pool addition cancelled")
    
def DeletePool():
    print("Pools list:")
    with open(POOLSFILE, 'r') as f:
        json_object = json.load(f)
        for pool in json_object:
            print(f'{pool}')
    pool = input("Pool: ")
    print(f'Are you sure you want to delete the pool {pool}? (y/n)')
    if input() == 'y':
        print("Deleting the pool...")
        # Delete the pool
        with open(POOLSFILE, 'r') as f:
            json_object = json.load(f)
            del json_object[pool]
        with open(POOLSFILE, 'w') as f:
            json.dump(json_object, f, indent=4)
        print("Pool deleted!")
        # TODO : Revoking the employees' public keys
    else:
        print("Pool deletion cancelled")
        
def addMachine():
    print("Enter the machine details")
    machine = input("Machine: ")
    POOLS = getPools()
    # Parse the pools and put them in a list
    poolTab = []
    for i,pool in enumerate(POOLS):
        poolTab.append(pool)
        print(f'{i}: {pool}')
    poolID = input("Pool (id): ")
    pool = poolTab[int(poolID)]
    print(f'Are the following details correct? (y/n)')
    print(f'Machine: {machine}')
    print(f'Pool: {pool}')
    if input() == 'y':
        print("Adding the machine...")
        # Add the machine
        with open(POOLSFILE, 'r') as f:
            json_object = json.load(f)
            json_object[pool]['machines'].append(machine)
        with open(POOLSFILE, 'w') as f:
            json.dump(json_object, f, indent=4)
        print("Machine added!")
    else:
        print("Machine addition cancelled")
        
def deleteMachine():
    print("Machines list:")
    with open(POOLSFILE, 'r') as f:
        json_object = json.load(f)
        for pool in json_object:
            print(f'    {pool}:')
            for machine in json_object[pool]['machines']:
                print(f'        {machine}')
    machine = input("Machine: ")
    print(f'Are you sure you want to delete the machine {machine}? (y/n)')
    if input() == 'y':
        print("Deleting the machine...")
        # Delete the machine
        with open(POOLSFILE, 'r') as f:
            json_object = json.load(f)
            for pool in json_object:
                if machine in json_object[pool]['machines']:
                    json_object[pool]['machines'].remove(machine)
        with open(POOLSFILE, 'w') as f:
            json.dump(json_object, f, indent=4)
        print("Machine deleted!")
        
def RevokeEmployee():
    print("Employees list:")
    with open(DATAFILE, 'r') as f:
        json_object = json.load(f)
        for id in json_object:
            print(f'{id}: {json_object[id]["email"]}')
    ID = input("Employee ID: ")
    print(f'Are you sure you want to revoke the employee {json_object[ID]["email"]}? (y/n)')
    if input() == 'y':
        pass
        # TODO : Revoking the employee's public key
    else:
        print("Employee revocation cancelled")
        
def main():
    while True:
        print("Welcome to the admin panel")
        print("1: Create an employee")
        print("2: Delete an employee")
        print("3: Add a pool")
        print("4: Delete a pool")
        print("5: Add a machine")
        print("6: Delete a machine")
        print("7: Revoke an employee")
        print("8: Exit")
        choice = input("Choice: ")
        if choice == '1':
            CreateEmployee()
        elif choice == '2':
            DeleteEmployee()
        elif choice == '3':
            AddPool()
        elif choice == '4':
            DeletePool()
        elif choice == '5':
            addMachine()
        elif choice == '6':
            deleteMachine()
        elif choice == '7':
            RevokeEmployee()
        elif choice == '8':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()