import socket
import os
import sign
import pickle #to send object
from getpass import getpass

host = input("Input IP server: ")
port = input("Input port server: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, int(port))) #must change port from string to int
numByteReceive = 1024
user = {"username": "", "password": "", "fullname": "", "birth": "", "notelist": ""}

def log():
    global user
    choice = sign.sign()
    if (choice == "1"):
        user = sign.login(user)
        s.send(bytes("login", "utf-8"))
        msg = pickle.dumps(user)
        s.send(msg)
    else:
        user = sign.regis(user)
    
def main():
    log()

main()
s.close()
