from cryptography.fernet import Fernet

def decyrpt_file_json(file_name):
    print("~~~ dekripsi %s"%file_name)
    file=open('key.key','rb')
    key= file.read()
    file.close

    with open(file_name, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    output_name = file_name[:-13]+".json"

    with open (output_name, 'wb')as file:
        file.write(decrypted)
    return output_name