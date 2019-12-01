#By Will Eatherly

import requests
import time
from datetime import datetime
import os
import pysftp


def commrequest(ip, password):

    r = requests.get("http://"+ip+":5000/")
    # loop checks for empty queue, sleeps when it finds one
    if(r.text) == 'empty':
        print("No command found. Sleeping...\n")
        time.sleep(15)
        commrequest(ip, password)

    # What happens when it gets out of the request loop
    print("Running the following command: "+ r.text)
    rsplit = r.text.split(" ")
    commname = rsplit[0]

    # creates a unique filename for each command so it can be tracked in the sftp server
    filebase = datetime.now().strftime("%H:%M:%S")+commname
    os.system(r.text + " -oA " + filebase)

    # connects to the sftp server with the provided information, transfers the file
    srv = pysftp.Connection(host=ip, username="root",password=password)
    if commname == "nmap":
        srv.put(filebase + ".xml")
        srv.put(filebase + ".gnmap")
        srv.put(filebase + ".nmap")
    else:
        srv.put(filebase)

    srv.close()
    
    os.system("rm -rf " + filebase + ".xml")
    os.system("rm -rf " + filebase + ".gnmap")
    os.system("rm -rf " + filebase + ".nmap")
    # rinse and repeat
    commrequest(ip, password)


if __name__ == "__main__":

    # inputs the data required for the program to function
    print("Input the server IP: ")
    ip = input()
    print("Input the SFTP user password: ")
    password = input()
    commrequest(ip, password)
