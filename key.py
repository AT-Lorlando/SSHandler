import os

# Call ssh-key to generate a key

def generateKey():
    """
        Generate a key with ssh-keygen.
        Return:
            pubkey: (string) The public key generated
    """
    os.system('ssh-keygen -t ed25519 -f key -N "" -C "x@x.fr"')
    with open('key.pub', 'r') as f:
        pubkey = f.read()
    with open('key', 'r') as f:
        privkey = f.read()
    return privkey, pubkey

generateKey()