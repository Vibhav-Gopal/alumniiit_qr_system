from flask import Flask
import sqlite3
from threading import Semaphore

# Connect to SQL db
sqliteConnection = sqlite3.connect('sql.db', check_same_thread=False)
cursor = sqliteConnection.cursor()

pftableCmd = """ CREATE TABLE PHOTOFRAME (
NAME VARCHAR(255) NOT NULL,
ROLLNO VARCHAR(30) NOT NULL,
UID VARCHAR(255) NOT NULL
);"""
ybtableCmd = """ CREATE TABLE YEARBOOK (
NAME VARCHAR(255) NOT NULL,
ROLLNO VARCHAR(30) NOT NULL,
UID VARCHAR(255) NOT NULL
);"""
idtableCmd = """ CREATE TABLE IDCARD (
NAME VARCHAR(255) NOT NULL,
ROLLNO VARCHAR(30) NOT NULL,
UID VARCHAR(255) NOT NULL
);"""

# Create tables if not there
try:
    cursor.execute(pftableCmd)
    print("PHOTOFRAME table created")
except sqlite3.OperationalError as e:
    print(e)
try:
    cursor.execute(ybtableCmd)
    print("YEARBOOK table created")
except sqlite3.OperationalError as e:
    print(e)
try:
    cursor.execute(idtableCmd)
    print("IDCARD table created")
except sqlite3.OperationalError as e:
    print(e)

dbKey = Semaphore()


app = Flask(__name__)

@app.route('/')
def base():
    return "Not permitted, Illegal Access"

@app.route('/photoframe/<uid>')
def validate_pf(uid):
    allowed_modes = ["pre","onspot"] #For onspot and pre registration differentiation
    dbKey.acquire()
    cursor.execute(f"SELECT UID FROM PHOTOFRAME WHERE UID = '{uid}'")
    results = cursor.fetchall()
    rn,name,mode = uid.split("+")
    if len(results) == 0:
        if mode not in  allowed_modes:
            dbKey.release()
            return f"Mode {mode} not in allowed modes"
        print("New entry")
        cursor.execute(f"INSERT INTO PHOTOFRAME VALUES ('{name}' ,'{rn}','{uid}')")
        sqliteConnection.commit()
        dbKey.release()
        return "Valid"
    if len(results) == 1:
        dbKey.release()
        return "Duplicate"


@app.route('/yearbook/<uid>')
def validate_yb(uid):
    allowed_modes = ["pre","onspot"]
    dbKey.acquire()
    cursor.execute(f"SELECT UID FROM YEARBOOK WHERE UID = '{uid}'")
    results = cursor.fetchall()
    rn,name,mode = uid.split("+")
    if len(results) == 0:
        if mode not in  allowed_modes:
            dbKey.release()
            return f"Mode {mode} not in allowed modes"
        print("New entry")
        cursor.execute(f"INSERT INTO YEARBOOK VALUES ('{name}' ,'{rn}','{uid}')")
        sqliteConnection.commit()
        dbKey.release()
        return "Valid"
    if len(results) == 1:
        dbKey.release()
        return "Duplicate"


@app.route('/idcard/<uid>')
def validate_id(uid):
    allowed_modes = ["pre","onspot"]
    dbKey.acquire()
    cursor.execute(f"SELECT UID FROM IDCARD WHERE UID = '{uid}'")
    results = cursor.fetchall()
    rn,name,mode = uid.split("+") 
    if len(results) == 0:
        if mode not in  allowed_modes:
            dbKey.release()
            return f"Mode {mode} not in allowed modes"
        print("New entry")
        cursor.execute(f"INSERT INTO IDCARD VALUES ('{name}' ,'{rn}','{uid}')")
        sqliteConnection.commit()
        dbKey.release()
        return "Valid"
    if len(results) == 1:
        dbKey.release()
        return "Duplicate"


if __name__ == "__main__":
    app.run(host="192.168.29.186", port=5000, debug=True)