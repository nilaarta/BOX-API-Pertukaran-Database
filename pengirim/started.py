from boxsdk import OAuth2, Client

auth = OAuth2(
    client_id='c0hjuh3tjr90sloycc4g0jcdvid1yjs2',
    client_secret='w5oJLroCuN4TQ8bEjmJycwFmOexZXB2g',
    access_token='GS3u5KorxW0jVURWMmBtNogkEhP2YwUu',
)
client = Client(auth)

# collections = client.collections()
# for collection in collections:
#     print('Collection "{0}" has ID {1}'.format(collection.name, collection.id))

# items = client.collection(collection_id='5731943133').get_items()
# for item in items:
#     print('{0} "{1}" is in the collection'.format(item.type.capitalize(), item.name))

user = client.user().get()
print('The current user ID is {0}'.format(user.id))
print('The current user name is {0}'.format(user.name))

items = client.folder(folder_id='0').get_items()
for item in items:
    print(item.id)
    if item.name == "7.json":
        print('{0} {1} is named "{2}"'.format(item.type.capitalize(), item.id, item.name))
        with open(item.name, 'wb') as open_file:
            client.file(item.id).download_to(open_file)
            open_file.close()



# file_name = 'abc.pdf'
# stream = open('abc.pdf', 'rb')

# folder_id = '0'
# new_file = client.folder(folder_id).upload_stream(stream, file_name)
# print('File "{0}" uploaded to Box with file ID {1}'.format(new_file.name, new_file.id))