# Global
HANDLER_IP = '192.168.1.93'
HANDLER_PORT = 4242

# Handler
DATAFILE = 'data.json'
POOLFILE = 'pools.json'

## SSH

SSH_ADMIN_USERNAME = 'ssh-admin'
SSH_ADMIN_PASSWORD = 'AZERTY'

# Employee

# Machine


# JSON file hierarchy
# User
# {
#     "id": {
#         "email": "email",
#         "password": "pw",
#         "public_key": "pk"
#         "pools": [
#             "WebServer", "ProxmoxServer", "..."
#         ]
#     }
# }
#
# Pools
# {
#     "WebServer": {
#         "name": "Web Server",
#         "machines": [
#             "192.168.163.135"
#         ]
#     },
#     "ProxmoxServer": {
#         "name": "Proxmox Server",
#         "machines": [
#             "192.168.163.13X",
#             "192.168.163.13Y"
#         ]
#     }
# }
