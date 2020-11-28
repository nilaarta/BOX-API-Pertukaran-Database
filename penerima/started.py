import pandas as pd
import json
from db_con import *


curDb = connDb.cursor()

with open("1.json") as json_file:
    json_data = json.load(json_file)
for data in json_data:
    nama = data[1]
    deskripsi = data[2]
    jumlah = data[3]

    print ("%s %s %s", nama, deskripsi, jumlah)
    curDb.execute("INSERT INTO tb_produk_penerima(nama, deskripsi, jumlah) VALUES (%s, %s, %s)", (nama, deskripsi, jumlah))
connDb.commit()