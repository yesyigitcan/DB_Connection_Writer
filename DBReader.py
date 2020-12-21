import cx_Oracle
import json
import os
from cryptography.fernet import Fernet 

def Decrypt(input, key):
    f = Fernet(key)
    return f.decrypt(input.encode()).decode()

if __name__ == '__main__':

    if not os.path.isfile('User.json'):
        raise Exception('The file User.json has to be created first to use this script')

    rowLimiter = 5
    with open('Config.json', 'r') as inputfile:
        conf = json.load(inputfile)
        target_table = conf["TARGET_TABLE"]
        target_table_detail = conf["TARGET_TABLE_DETAIL"]
        db_columns = conf["DB_COLUMNS"]
        db_columns_detail = conf["DB_COLUMNS_DETAIL"]
        en_columns = conf["ENCRYPTED_COLUMNS"]
        key_path = conf["KEY_PATH"]
        if key_path == "CURRENT":
            key_path = os.getcwd()
        key_name = conf["KEY_NAME"]
        key_filename = os.path.join(key_path, key_name)
    with open(key_filename, 'r') as inputfile:
        key = inputfile.read()
    with open('User.json', 'r') as inputfile:
        conf_user = json.load(inputfile)
        username = conf_user["username"]
        password = Decrypt(conf_user["password"], key)
    with open('DB.json', 'r') as inputfile:
        db_conf = json.load(inputfile)
        ip = db_conf["ip"]
        port = db_conf["port"]
        service_name = db_conf["service_name"]
    connect_ = username + "/" + password + "@" + ip + ":" + port + "/" + service_name
    conn = cx_Oracle.connect(connect_)
    cur = conn.cursor()
    sql = "select {}, {} from {} where rownum < {}".format(db_columns[0], db_columns[1], target_table, rowLimiter+1)
    cur.execute(sql)
    print("TABLE: ", target_table)
    for row in cur.fetchall():
        for i in range(len(db_columns)):
            print(db_columns[i], ":", row[i], end=" \t ")
        print()

    print("\n")

    sql_detail = "select {}, {}, {}, {}, {}, {}, {}, {} ,{} from {} where rownum < {}".format(
        db_columns_detail[0], db_columns_detail[1], db_columns_detail[2], db_columns_detail[3], db_columns_detail[4], db_columns_detail[5], db_columns_detail[6], db_columns_detail[7], db_columns_detail[8],
        target_table_detail, rowLimiter+1) 
    cur.execute(sql_detail)
    print("TABLE: ", target_table_detail)
    for row in cur.fetchall():
        row = list(row)
        for i in en_columns:
            row[i] = Decrypt(row[i], key)
        for i in range(len(db_columns_detail)):
            print(db_columns_detail[i], ":", row[i], end=" \t ")
        print()
    cur.close()
    conn.close()

    