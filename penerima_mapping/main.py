import time
import json
import pymysql
from box_con import *
from decrypt_json import *

FILE_NAME = 'last_name.txt'


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

def connect_database(db_name, host_name, username, password):
    conection = pymysql.connect(host=host_name, user=username, passwd=password, db=db_name)
    return conection

def extrack_file_name(file_name):
    mpfile = file_name[:7]
    mapping= False
    if mpfile == "mapping":
        mapping = True

    if mapping:
        date = file_name[:-13][8:]
    else:
        date = file_name[:-13][1:]
    return mapping, date, file_name

def check_box_file(date_file):
    items = client.folder(folder_id='0').get_items()
    for item in items:
        file_name = extrack_file_name(item.name)
        if int(file_name[1]) > date_file:
            print("-------------------------------------------")
            print("--------------FILE DITEMUKAN---------------")
            print('~~~ Download file {0} dari box'.format(item.name))

            with open(item.name, 'wb') as open_file:
                client.file(item.id).download_to(open_file)
                open_file.close()
            return file_name
    print("tidak ada file baru")
    return False

def listToString(s):  
    # initialize an empty string 
    str1 = ""  
    s.pop(0)
    # traverse in the string   
    for ele in s:  
        str1 = str1 + """'"""+str(ele)+ """'"""+ ","
    # return string   
    return str1[:-1]  


if __name__ == '__main__':
    connection = False
    field_destination = ""
    table_destination = ""
    con=None
    while True:
        last_seen_id = retrieve_last_seen_id(FILE_NAME)
        box_file = check_box_file(last_seen_id)
        if box_file != False:
            
            decrypt_name = decyrpt_file_json(box_file[2])
            if box_file[0]:
                if connection:
                    curDb.close()
                    con.close()
                field_source=""
                with open(decrypt_name) as json_file:
                    json_data = json.load(json_file)
                for data in json_data:
                    db_name_source = data[0]
                    table_source = data[8]
                    host_destination = data[5]
                    username_destination = data[6]
                    password_destination = data[7]
                    db_name_destination = data[4]
                    table_destination = data[9]
                    field_source = field_source +data[10] + ","
                    field_destination = field_destination +data[11] + ","
                field_source = field_source[:-1]
                field_destination = field_destination[:-1]

                print("~~~ DETAIL MAPPING")
                print("~~~ from db %s to db %s"%(db_name_source, db_name_destination) )
                print("~~~ from table %s to table %s"%(table_source, table_destination))
                print("~~~ from field %s to field %s"%(field_source, field_destination))

                connection = True
                con = connect_database(db_name_destination, host_destination, username_destination, password_destination)                
                
                store_last_seen_id(box_file[1], FILE_NAME)
                print("~~~Menguhubungkan ke Database ")

            else:
                if connection == True:
                    with open(decrypt_name) as json_file:
                        json_data = json.load(json_file)
                    for data in json_data:
                        data_tabel = listToString(data)
                        sql = "INSERT INTO %s(%s) VALUES (%s)"%(table_destination, field_destination, data_tabel)
                        curDb = con.cursor()
                        curDb.execute(sql)
                        con.commit()
                        print(data_tabel)
                        print(sql)
                    store_last_seen_id(box_file[1], FILE_NAME)
                    print("Menyimpan Data ke database")

                else:
                    print("tidak ada koneksi database")
                




        # curDb = connDb.cursor()

        
        # engineID(last_seen_id)

        time.sleep(5)