rollNum = "ec21b1027"
rollNum = rollNum.lower()
name = "mudigonda vibhavgopal lakshmi narasimha"
name = name.lower()
name = name.replace(" ","_")
uid = rollNum + "+"+ name + "+" + "pre"
uids = [uid,uid]
# TODO: Read data from csv

from cryptography.fernet import Fernet
import qrcode

# if input("WARNING : Regenerating new QR codes will render the old ones invalid. This step is irreversible. Are you Sure? Type \"YES\" to continue\n") != "YES" : exit(0)

#Generate and write key to file
key = Fernet.generate_key()
with open("secretKey.txt",'a') as fil:
    fil.write("\n"+str(key,"utf-8"))

f = Fernet(key)
open("qrUids.txt","w").close() #Clear file

#Encrypt uids and save tokens in file and make qr
with open("qrUids.txt",'a+') as fil:
    for uid in uids:
        token = f.encrypt(bytes(uid,"utf-8"))
        img = qrcode.make(bytes(str(key,"utf-8") + str(token,"utf-8") , "utf-8"))
        img.save("qrCodes/"+uid+".png")
        fil.write("\n" + str(key,"utf-8") + str(token,"utf-8") )

