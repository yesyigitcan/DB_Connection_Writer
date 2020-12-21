from tkinter import *
from cryptography.fernet import Fernet
import os
import json
import cx_Oracle
import logging

def Encrypt(input, key):
    f = Fernet(key)
    return f.encrypt(input.encode())

def Decrypt(input, key):
    f = Fernet(key)
    return f.decrypt(input.encode()).decode()

def PopUp(message, state):
    win = Toplevel()
    win.resizable(False, False)
    win.wm_title("Error")

    if state == 0:
        l = Label(win, text="Error Occured\n" + message)
    else:
        l = Label(win, text=message)
    l.grid(row=0, column=0)

    b = Button(win, text="Okay", command=win.destroy)
    b.grid(row=1, column=0)

if __name__ == '__main__':
    # Logging Settings
    logging.basicConfig(filename='Main.log',
        filemode='a',
        format='%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt = '%m/{}/%Y %H:%M:%S',
        level=logging.INFO)

    # Configuration file read
    try:
        with open('Config.json', 'r') as inputfile:
            conf = json.load(inputfile)
            key_name = conf["KEY_NAME"]
            if conf["KEY_PATH"] == "CURRENT":
                key_path = os.getcwd()
            else:
                key_path = conf["KEY_PATH"]
            target_normal = conf["TARGET_TABLE"]
            target_detail = conf["TARGET_TABLE_DETAIL"]
            columns = conf["COLUMNS"]
            db_columns = conf["DB_COLUMNS"]
            db_columns_detail = conf["DB_COLUMNS_DETAIL"]
            en_columns = conf["ENCRYPTED_COLUMNS"]
            
        filename = os.path.join(key_path, key_name)
        with open(filename, 'rb') as inputfile:
            key = inputfile.read()
    except Exception as e:
        logging.info("Error: CONFIG READ: " + str(e))

    # User credentials read
    try:
        with open('User.json', 'r') as inputfile:
            user_conf = json.load(inputfile)
            pre_username = user_conf["username"]
            pre_password = Decrypt(user_conf["password"], key)
    except Exception as e:
        logging.info("Predefined user credentials cannot be found")
        pre_username = None
        pre_password = None

    # DB Connection
    conn = None
    window = Tk()
    window.title("")
    window.resizable(False, False)
    window.geometry('300x150')

    lbl = Label(window, text="Connect to DB")
    lbl.grid(column=1, row=0)

    lbl = Label(window, text="Username")
    lbl.grid(column=0, row=1)
    txt1 = Entry(window,width=20)
    txt1.grid(column=1, row=1)

    lbl = Label(window, text="Password")
    lbl.grid(column=0, row=2)
    txt2 = Entry(window,width=20)
    txt2.grid(column=1, row=2)

    if pre_username and pre_password:
        txt1.insert(INSERT, pre_username)
        txt2.insert(INSERT, "".join("*" for i in range(len(pre_password))))

    cb_stat = IntVar()
    cb = Checkbutton(window, text="Save My Credentials", variable = cb_stat)
    cb.grid(column=0, row=3)

    try:
        with open('DB.json', 'r') as inputfile:
            db_conf = json.load(inputfile)
            ip = db_conf["ip"]
            port = db_conf["port"]
            service_name = db_conf["service_name"]
    except Exception as e:
        logging.info("Error: DB CONFIG READ: " + str(e))
    
    def Connected(pre_password):
        global conn
        try:
            username = txt1.get()
            if txt2.get() == "".join("*" for i in range(len(pre_password))):
                password = pre_password
            else:
                password = txt2.get()
            if cb_stat.get() == 1 or pre_username == None:
                if username != pre_username and password != pre_password:
                    json_content = { "username" : username, "password" : Encrypt(password, key).decode()}
                    json.dump(json_content, open('User.json', 'w'))
                    logging.info("New user credentials for user " + username)
            
            connect_ = username + "/" + password + "@" + ip + ":" + port + "/" + service_name
            conn = cx_Oracle.connect(connect_)
            window.destroy()
        except Exception as e:
            logging.info("Error: DB CONNECTION: " + str(e))
            PopUp(str(e), 0)
        

    btn = Button(window, text="Connect", command=lambda: Connected(pre_password))
    btn.grid(column=1, row=4)
    window.mainloop()

    # GUI
    print(conn)
    if not conn:
        logging.info("Error: Connection cannot be seen by the program")
        logging.info("Program terminated with error")
        import sys
        sys.exit(1)
    window = Tk()
    window.resizable(False, False)
    window.title("Py Connection Agent")
    window.geometry('350x270')
    

    lbl = Label(window, text="Target Table")
    lbl.grid(column=0, row=0)
    lbl = Label(window, text=target_normal)
    lbl.grid(column=1, row=0)
    
    lbl = Label(window, text="Target Table Detail")
    lbl.grid(column=0, row=1)
    lbl = Label(window, text=target_detail)
    lbl.grid(column=1, row=1)

    lbl = Label(window, text=columns[0])
    lbl.grid(column=0, row=2)
    txt1 = Entry(window,width=20)
    txt1.grid(column=1, row=2)

    lbl = Label(window, text=columns[1])
    lbl.grid(column=0, row=3)
    txt2 = Entry(window,width=20)
    txt2.grid(column=1, row=3)

    lbl = Label(window, text=columns[2])
    lbl.grid(column=0, row=4)
    txt3 = Entry(window,width=20)
    txt3.grid(column=1, row=4)

    lbl = Label(window, text=columns[3])
    lbl.grid(column=0, row=5)
    txt4 = Entry(window,width=20)
    txt4.grid(column=1, row=5)

    lbl = Label(window, text=columns[4])
    lbl.grid(column=0, row=6)
    txt5 = Entry(window,width=20)
    txt5.grid(column=1, row=6)

    lbl = Label(window, text=columns[5])
    lbl.grid(column=0, row=7)
    txt6 = Entry(window,width=20)
    txt6.grid(column=1, row=7)

    lbl = Label(window, text=columns[6])
    lbl.grid(column=0, row=8)
    txt7 = Entry(window,width=20)
    txt7.grid(column=1, row=8)
    
    lbl = Label(window, text=columns[7])
    lbl.grid(column=0, row=9)
    txt8 = Entry(window,width=20)
    txt8.grid(column=1, row=9)

    lbl = Label(window, text=columns[8])
    lbl.grid(column=0, row=10)
    txt9 = Entry(window,width=20)
    txt9.grid(column=1, row=10)

    def Submitted():
        if not txt7.get().isnumeric() or len(txt7.get()) != 8:
            PopUp("Create time is not in correct format", 0)
            return
        elif not txt8.get().isnumeric() or len(txt7.get()) != 8:
            PopUp("Update time is not in correct format", 0)
            return
        elif txt9.get().upper() not in ('Y', 'N'):
            PopUp("Valid must have Y or N", 0)
            return
        c_values = [
        txt1.get(),
        txt2.get(),
        txt3.get(),
        txt4.get(),
        txt5.get(),
        txt6.get(),
        txt7.get(),
        txt8.get(),
        txt9.get().upper()
        ]
        for i in en_columns:
            c_values[i] = Encrypt(c_values[i], key).decode()
        sql = "insert into {} ({}, {}) values ('{}', '{}')".format(target_normal, db_columns[0], db_columns[1], c_values[0], c_values[2])
        sql_detail = "insert into {} ({}, {}, {}, {} ,{} ,{} ,{} ,{} ,{}) values('{}','{}','{}','{}','{}','{}',to_date({}, 'mmddyyyy'),to_date({}, 'mmddyyyy'),'{}')".format(target_detail,
                        db_columns_detail[0], db_columns_detail[1], db_columns_detail[2], db_columns_detail[3], db_columns_detail[4], db_columns_detail[5], db_columns_detail[6], db_columns_detail[7], db_columns_detail[8],
                        c_values[0], c_values[1], c_values[2], c_values[3], c_values[4], c_values[5], c_values[6], c_values[7], c_values[8])
 
        try:
            cur = conn.cursor()
            cur.execute(sql)
            cur.execute(sql_detail)
            conn.commit()    
            cur.close() 
            logging.info("SUCCESS | Rows executed and committed")
            logging.info("SQL statemens are written below")
            logging.info(sql)
            logging.info(sql_detail)
            PopUp('Rows are executed successfully', 1)
        except Exception as e:
            conn.rollback()
            logging.info("Error: DB WRITE: " + str(e))
            logging.info("FAIL | Rollback Occured")
            logging.info("SQL statemens are written below")
            logging.info(sql)
            logging.info(sql_detail)
            PopUp(str(e), 0)
        


    btn = Button(window, text="Submit", command=Submitted)
    btn.grid(column=1, row=11)
    def on_closing():
        global conn
        try:
            conn.close()
            logging.info("DB Connection terminated..")
        except Exception as e:
            logging.info("Error: Closing program: " + str(e))
        window.destroy()
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()
    logging.info("Program terminated..")
    sys.exit(0)

    