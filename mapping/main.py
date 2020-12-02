import time
import json
import pymysql
from encryp_json import *
from box_con import *

FILE_ID = 'last_id.txt'
FILE_NAME = 'last_name.txt'

db_mapping_name = 'db_source'
host_name_mapping = 'localhost'
username_mapping = 'root'
password_mapping = ''


def get_mapping_database(conection):
    sql ="SELECT `tb_mapping_db`.`nama_db_source`, `tb_mapping_db`.`ip_db_source`, `tb_mapping_db`.`user_name_source`, `tb_mapping_db`.`password_source`, `tb_mapping_db`.`nama_db_destination`, `tb_mapping_db`.`ip_db_destination`, `tb_mapping_db`.`user_name_destination`, `tb_mapping_db`.`password_destination`, `tb_mapping_table`.`nama_table_source`, `tb_mapping_table`.`nama_tabel_destination`, `tb_mapping_field`.`field_source`, `tb_mapping_field`.`field_destination` FROM `db_source`.`tb_mapping_table` INNER JOIN `db_source`.`tb_mapping_db` ON (`tb_mapping_table`.`id_mapping_db` = `tb_mapping_db`.`id_mapping_db`)    INNER JOIN `db_source`.`tb_mapping_field` ON (`tb_mapping_field`.`id_mapping_table` = `tb_mapping_table`.`id_mapping_table`) WHERE `tb_mapping_field`.`id_mapping_table` = (SELECT `tb_mapping_field`.`id_mapping_table` FROM `tb_mapping_field` WHERE `tb_mapping_field`.`id_mapping_field` = (SELECT(MAX(`tb_mapping_field`.`id_mapping_field`))FROM `tb_mapping_field`))"
    curDB_mapping = conection.cursor()
    curDB_mapping.execute(sql)
    data_mapping = curDB_mapping.fetchall()
    
    field_source=''
    field_destination=''
    for data in data_mapping:
        db_name_source = data[0]
        host_source = data[1]
        username_source = data[2]
        password_source = data[3]
        table_source = data[8]
        table_destination = data[9]
        db_name_destination = data[4]
        field_source = field_source +data[10] + ","
        field_destination = field_destination +data[11] + ","


    field_source = field_source[:-1]
    field_destination = field_destination[:-1]

    conection.close()
    curDB_mapping.close()
    return db_name_source, host_source, username_source, password_source,db_name_destination, table_source,table_destination, field_source, field_destination, data_mapping

def connect_database(db_name, host_name, username, password):
    conection = pymysql.connect(host=host_name, user=username, passwd=password, db=db_name)
    return conection

def engineID(last_seen_id, name_field, name_table):
    curDB_source = con.cursor()
    sql = "select id, %s from %s where id > %d;"%(name_field, name_table,last_seen_id)
    curDB_source.execute(sql)
    con.commit()
    dataProduk = curDB_source.fetchall()
    if curDB_source.rowcount == 0:
        print("Tidak Ada Data Baru")
        return
    print("-------------------------------------------------")
    print("---------------DATA BARU DITEMUKAN---------------")
    print("---- Total data yang ditemukan: %d"%curDB_source.rowcount)

    save_to_json(dataProduk, False)

    for data in dataProduk:
        idProduk = data[0]
        store_last_seen_id(idProduk, FILE_ID)

def save_to_json(dataName, mapping):
    json_data= json.dumps(dataName)
    timestr = time.strftime("%Y%m%d%H%M%S")
    if mapping:
        nama_file = "mapping-%s.json"%timestr
        nama_file_encryp ="mapping-%s-encrypt.json"%timestr
    else:
        nama_file ="z%s.json"%timestr
        nama_file_encryp ="z%s-encrypt.json"%timestr
    
    with open(nama_file, 'w') as fh:
        fh.write(json_data)
    encrypt_json_file(nama_file, nama_file_encryp)
    print("---- Enkripsi file: %s" %nama_file_encryp)
    upload_to_box(nama_file_encryp)
    # store_last_seen_id(number_file, FILE_NAME)  
    return

def upload_to_box(file_name):
    stream = open(file_name, 'rb')
    folder_id = '0'
    new_file = client.folder(folder_id).upload_stream(stream, file_name)
    print("---- Mengapload file ke BOX")
    print("-------------------------------------------------")
    print("-------------------------------------------------")


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
    print("-------------------------------------------------")
    print("---------------------START-----------------------")
    print("---- menghubungkan ke database mapping")
    con = connect_database(db_mapping_name, host_name_mapping, username_mapping, password_mapping)
    print("---- mengambil data pertukaran database")
    db_source = get_mapping_database(con)
    print("---- database : %s =====>>> %s"%(db_source[0], db_source[4]))
    print("---- tabel : %s =====>>> %s"%(db_source[5], db_source[6]))
    print("---- ___________________field____________________")
    print("----  %s"%(db_source[7]))
    print("----     ||     ||     ||    ||     ||   ")
    print("----     \/     \/     \/    \/     \/ ")
    print("----  %s"%(db_source[8]))
    print("---- ````````````````````````````````````````````")
    print("---- membuat file json data mapping")
    save_to_json(db_source[9], True)
    print("")
    print("")
    print("-------------------------------------------------")
    print("------------PENGECEKAN DATABASE ASAL-------------")
    con = connect_database(db_source[0], db_source[1], db_source[2], db_source[3])

    while True:
        last_seen_id = retrieve_last_seen_id(FILE_ID)
        engineID(last_seen_id, db_source[7], db_source[5])


        # sql = ("select %s from %s"%(db_source[7],db_source[5]))
        
        # curDB_source.execute(sql)
        # data_source = curDB_source.fetchall()
        # print(data_source)
        # curDb = connDb.cursor()

        

        time.sleep(5)







    # print(db_source)
    

    
