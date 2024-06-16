# QR Ticketing system
---
## Parts of the system 
- The central Data server
- The QR Generator
- The Scanners

## Additional debugging code
- Test Sender
- More coming soon...
---
## Explanation
### How do I get it running?
* Modify the line `app.run(host="192.168.29.186", port=5000, debug=True)` to suit your IP address and port number for the Flask webserver in `data_server.py` file.
* Modify `host` and `port` variables in all the scanner programs to match the ones set in the webserver. That is, `host="192.168.29.186" port = 5000`
* Run the dataserver and wait for it to start up
* Run the scanners and you are not good to go
### Central Data Server
The central data server is located in the `data_server.py` file.  
It is a simple Flask WebApp, the data is received from the clients via **HTTP GET** requests and the response is sent back. `sqlite3` is used to connect to a local SQL database to maintain records.

### QR Generator
The QR generator is located in the `qr_generator.py` file, it takes in the **Roll Number**, **Name** and **Mode** of registration, converts it into a UID for that specific user and generates a **Fernet** Key before encrypting all the UIDs with that **Fernet** object and the key is combined with the output to make it easier to decrypt at the scanner, even though this is a security risk.  
Secret Keys and generated encrypted UIDs are stored in text files, the UIDs are then taken and converted to QR Images which will be sent out to the attendees.

### Scanners
The scanners can be found in the `scanners` folder. Each scanner scans the QR, decrypts it, and queries the Flask webserver with the UID at their respective URL paths. The response from the webserver is then used to decide whether the scanned QR is unique or has been scanned before.

---
## Future Work
* Adding a debug program to "peep" into the database
* Adding programs to conduct onspot registrations
* Adding program for manual entry into database incase of technical failures
