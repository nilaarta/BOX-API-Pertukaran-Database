from cryptography.fernet import Fernet

def encrypt_json_file(name_file, name_encryp_file):

# key = Fernet.generate_key()
# file = open('key.key', 'wb')
# file.write(key)
# file.close
    file = open('key.key','rb')
    key= file.read()
    file.close()

    with open(name_file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open (name_encryp_file, 'wb')as file:
        file.write(encrypted)