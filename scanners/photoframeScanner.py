import requests,time
from cryptography.fernet import Fernet
import cv2
from tkinter import messagebox
cam = cv2.VideoCapture(0)
detect = cv2.QRCodeDetector()

host="192.168.29.186" #TODO:add way to choose host at runtime (future upgrade)
port = 5000
qrsFile = open("qrUids.txt","r")


def processData(line):
    status = ""
    keyEnd = line.find("=")
    key = line[:keyEnd+1]
    uid = line[keyEnd+1:]
    f = Fernet(bytes(key,"utf-8"))
    decrypted = str(f.decrypt(bytes(uid,"utf-8")),"utf-8")
    print(f"Querying {decrypted}\n")
    rn,name,mode = decrypted.split("+")
    response = requests.get("http://" + host + f":{port}/photoframe/" + decrypted)
    if response.text == "Valid":
        status = "Valid"
        print("New person")
    elif response.text == "Duplicate":
        status = "Duplicate"
        print("Oh shit, we got a fox")
    else:
        print(response.text)
    return rn,name,mode,status

while cv2.waitKey(1)!=ord('q'):
    ret,frm = cam.read()
    value,points,straight = detect.detectAndDecode(frm)
    cv2.imshow("img",frm)
    if value:
        try:
            rn,name,mode,status = processData(value)
            messagebox.showinfo("Info",f"Name : {name}\nRoll Number : {rn}\nStatus : {status}")
        except:
            print("An unknown error has occured reading the QR Code")
            print(f"Data = {value}")
            messagebox.showerror("QR Error", f"Erroneous QR scanned, press OK to try again\nData : {value}")

