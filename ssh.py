import paramiko


# For testing purposes :
#######################
user_group = "testgr"
user_name = "test42"
user_passwd = "azerty"
public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBqkYueUWYqTifdX4bD9JhZxHnYlV7SAzX1n4pQEAd5M x@x.fr"

machine = "192.168.163.135"

#######################

if __name__ == "__main__":   
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print('SSH creation on ' + machine + ' for user ' + user_name + ' started')
	ssh.connect(hostname=machine, username=SSH_ADMIN_USERNAME, password=SSH_ADMIN_PASSWORD)
	
	# Launch a superuser shell
	stdin, stdout, stderr = ssh.exec_command(f'sudo -S -i')
	stdin.write('AZERTY\n')
	# Create a new user and add his public key
	stdin.write(f'useradd -m -g {user_group} -p $(openssl passwd -1 {user_passwd}) -s /bin/bash {user_name}')
	stdin.write(f'mkdir /home/{user_name}/.ssh\n')
	stdin.write(f'touch /home/{user_name}/.ssh/authorized_keys\n')
	stdin.write(f'echo {public_key} >> /home/{user_name}/.ssh/authorized_keys\n')
	stdin.close()

	print(stdout.read().decode('utf-8'))
	print(stderr.read().decode('utf-8'))
	print('SSH creation on' + machine + ' for user ' + user_name + ' ended')

 
	# Close the SSH connection
	ssh.close()
	print('SSH connection closed')