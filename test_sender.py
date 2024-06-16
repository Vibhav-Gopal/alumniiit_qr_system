import requests,time
from cryptography.fernet import Fernet

host="192.168.29.186" #TODO:add way to choose host at runtime (future upgrade)
port = 5000
qrsFile = open("qrUids.txt","r")


for line in qrsFile:
    if line == "\n": continue
    keyEnd = line.find("=")
    key = line[:keyEnd+1]
    uid = line[keyEnd+1:]
    f = Fernet(bytes(key,"utf-8"))
    decrypted = str(f.decrypt(bytes(uid,"utf-8")),"utf-8")
    input(f"press enter to query {decrypted}\n")
    response = requests.get("http://" + host + f":{port}/photoframe/" + decrypted)
    if response.text == "Valid":
        print("New person")
    elif response.text == "Duplicate":
        print("Oh shit, we got a fox")
    else:
        print(response.text)

