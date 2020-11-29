import time
import json
from db_con import *
from box_con import *
from decrypt_json import *

FILE_NAME = 'last_name.txt'

def download_file(name_file):
    items = client.folder(folder_id='0').get_items()
    for item in items:
        if item.name == name_file:
            print("-------------------------------------------")
            print("--------------FILE DITEMUKAN---------------")
            print('* Download file {0} dari box'.format(item.name))
            with open(item.name, 'wb') as open_file:
                client.file(item.id).download_to(open_file)
                open_file.close()
            return
    return False

def engineID(last_seen_id):
    number_file = 1 + last_seen_id
    name_file ="%d.json"%number_file
    nama_file_encryp ="%d-encrypt.json"%number_file
    if download_file(nama_file_encryp) == False:
        print("tidak ada file baru")
        return
    print('** Dekripsi file %s'%nama_file_encryp)
    decyrpt_file_json(nama_file_encryp, name_file)
    print('*** Hasil Dekripsi file %s'%name_file)

    json_to_mysql(name_file)
    store_last_seen_id(number_file, FILE_NAME)
    print("-----------------SELESAI-------------------")
    print("-------------------------------------------")

def json_to_mysql(file):
    print("**** Extrack data dari %s ke Database"%file )
    with open(file) as json_file:
        json_data = json.load(json_file)
    for data in json_data:
        nama = data[1]
        deskripsi = data[2]
        jumlah = data[3]
        
        curDb.execute("INSERT INTO tb_produk_penerima(nama, deskripsi, jumlah) VALUES (%s, %s, %s)", (nama, deskripsi, jumlah))
    connDb.commit()
    curDb.close()
    print("***** Menambahkan Data Ke Database ")

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

if __name__ == '__main__':
    while True:
        curDb = connDb.cursor()

        last_seen_id = retrieve_last_seen_id(FILE_NAME)
        engineID(last_seen_id)

        time.sleep(5)