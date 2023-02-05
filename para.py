import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

user_group = "testgr"
user_name = "test42"
user_passwd = "azerty"
public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBqkYueUWYqTifdX4bD9JhZxHnYlV7SAzX1n4pQEAd5M x@x.fr"

HOST = "192.168.163.135"
USERNAME = "ssh-admin"
PASSWORD = "AZERTY"

# Connect to the remote server using the specified username and password

# Run a command on the remote server

if __name__ == "__main__":
	ssh.connect(hostname=HOST, username=USERNAME, password=PASSWORD)
	
	stdin, stdout, stderr = ssh.exec_command(f'sudo -S -i')
	stdin.write('AZERTY\n')
	stdin.write(f'useradd -m -g {user_group} -p $(openssl passwd -1 {user_passwd}) -s /bin/bash {user_name}')
	stdin.write(f'mkdir /home/{user_name}/.ssh\n')
	stdin.write(f'touch /home/{user_name}/.ssh/authorized_keys\n')
	stdin.write(f'echo {public_key} >> /home/{user_name}/.ssh/authorized_keys\n')
	stdin.close()
	
	# stdin.write('AZERTY\n')
	# stdin.close()
	# print(stdout.read().decode('utf-8'))
	# print(stderr.read().decode('utf-8'))
 
 
 
	# add the public key to the authorized_keys file
	# stdin, stdout, stderr = ssh.exec_command(f'echo {public_key} >> /home/{user_name}/.ssh/authorized_keys')
	# stdin.write('AZERTY\n')
	# stdin.close()
	print(stdout.read().decode('utf-8'))
	print(stderr.read().decode('utf-8'))
	print('fin')
 	# print(stdout.read().decode('utf-8'))

 
	# Close the SSH connection
	ssh.close()

