from cryptography.fernet import Fernet

file=open('key.key','rb')
key= file.read()
print(key)

with open('newfile.json', 'rb') as f:
    data = f.read()

fernet = Fernet(key)
decrypted = fernet.decrypt(data)

with open ('data.json', 'wb')as file:
    file.write(decrypted)