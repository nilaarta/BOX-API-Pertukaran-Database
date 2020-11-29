from cryptography.fernet import Fernet

def decyrpt_file_json(file_name, file_decrypt_name):
    file=open('key.key','rb')
    key= file.read()
    file.close

    with open(file_name, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open (file_decrypt_name, 'wb')as file:
        file.write(decrypted)