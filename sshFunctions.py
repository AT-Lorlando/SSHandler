import paramiko


# For testing purposes :
#######################
# user_group = "testgr"
# user_name = "test42"
# user_passwd = "azerty"
# public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBqkYueUWYqTifdX4bD9JhZxHnYlV7SAzX1n4pQEAd5M x@x.fr"

# machine = "192.168.163.135"

#######################

def AddNewUser(username, password, public_key, machine, group = ""):
	"""
		Add a new user on a machine.
		Args:
			username: (string) The username of the new user
			password: (string) The password of the new user
			public_key: (string) The public key of the new user
			machine: (string) The machine where you want to add the new user
			group: (string) The group of the new user
	"""
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print('SSH creation on ' + machine + ' for user ' + username + ' started')
	ssh.connect(hostname=machine, username=SSH_ADMIN_USERNAME, key_filename=ADMIN_KEY)
	
	# Launch a superuser shell
	stdin, stdout, stderr = ssh.exec_command(f'sudo -S -i')
	stdin.write('AZERTY\n')
	# Create a new user and add his public key
	stdin.write(f'useradd -m -g {group} -p $(openssl passwd -1 {password}) -s /bin/bash {username}')
	stdin.write(f'mkdir /home/{username}/.ssh\n')
	stdin.write(f'touch /home/{username}/.ssh/authorized_keys\n')
	stdin.write(f'echo {public_key} >> /home/{username}/.ssh/authorized_keys\n')
	stdin.close()

	print(stdout.read().decode('utf-8'))
	print(stderr.read().decode('utf-8'))
	print('SSH creation on' + machine + ' for user ' + username + ' ended')

 
	# Close the SSH connection
	ssh.close()
	print('SSH connection closed')
 
def DeleteUser(username, machine):
	"""
		Delete a user on a machine.
		Args:
			username: (string) The username of the user to delete
			machine: (string) The machine where you want to delete the user
	"""
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print('SSH deletion on ' + machine + ' for user ' + username + ' started')
	ssh.connect(hostname=machine, username=SSH_ADMIN_USERNAME, password=SSH_ADMIN_PASSWORD)
	
	# Launch a superuser shell
	stdin, stdout, stderr = ssh.exec_command(f'sudo -S -i')
	stdin.write('AZERTY\n')
	# Delete the user
	stdin.write(f'userdel -r {username}')
	stdin.close()

	print(stdout.read().decode('utf-8'))
	print(stderr.read().decode('utf-8'))
	print('SSH deletion on' + machine + ' for user ' + username + ' ended')

 
	# Close the SSH connection
	ssh.close()
	print('SSH connection closed')