import time
import json
from db_con import *
from box_con import *


FILE_ID = 'last_id.txt'
FILE_NAME = 'last_name.txt'

def engineID(last_seen_id):
    sql = "select * from tb_produk where id > %d;"%(last_seen_id)
    curDb.execute(sql)
    connDb.commit()
    dataProduk = curDb.fetchall()
    if curDb.rowcount == 0:
        print("Tidak Ada Data Baru")
        return
    print("---------------------------------------------")
    print("-------------DATA BARU DITEMUKAN-------------")
    print("* Total data yang ditemukan: %d"%curDb.rowcount)
    save_to_json(dataProduk)

    for data in dataProduk:
        idProduk = data[0]
        store_last_seen_id(idProduk, FILE_ID)

def save_to_json(dataName):
    json_data= json.dumps(dataName)
    number_file = 1 + retrieve_last_seen_id(FILE_NAME)
    nama_file ="%d.json"%number_file
    print("** Penyimpanan data pada file %s" %nama_file)
    with open(nama_file, 'w') as fh:
        fh.write(json_data)
    upload_to_box(nama_file)
    store_last_seen_id(number_file, FILE_NAME)

    
    return

def upload_to_box(file_name):
    stream = open(file_name, 'rb')

    folder_id = '0'
    new_file = client.folder(folder_id).upload_stream(stream, file_name)
    print('*** Upload file "{0}" ke Box'.format(new_file.name))
    print('**** ID file :"{0}" '.format(new_file.id))
    print("------------------SELESAI--------------------")
    print("---------------------------------------------")


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

        last_seen_id = retrieve_last_seen_id(FILE_ID)
        engineID(last_seen_id)

        time.sleep(5)