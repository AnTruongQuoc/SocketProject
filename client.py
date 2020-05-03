import socket
import os
import sign
import pickle #to send object
import re
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
        s.send(bytes("regis", "utf-8"))
        msg = pickle.dumps(user)
        s.send(msg)
    msg = s.recv(numByteReceive)
    if msg.decode("utf-8") == "success":
        return True
    else:
        print("Something went wrong!!")
        tempInput = input("Press anykey to try again")
        return log()

def changePass():
    global user
    newPass = sign.changePass(user)
    if newPass == False:
        return False
    s.send(bytes("newpass", "utf-8"))
    msg = pickle.dumps(user)
    s.send(msg)

def checkUser(username, option):
    s.send(bytes("check"),"utf-8")
    s.send(bytes(username),"utf-8")
    s.send(bytes(option),"utf-8")
    msg = s.recv(numByteReceive)
    print(msg.decode("utf-8"))

def setupInfo(option):
    global user
    s.send(bytes("update"),"utf-8")
    s.send(bytes(user["username"]),"utf-8")
    s.send(bytes(option),"utf-8")
    msg = s.recv(numByteReceive)

def analyzeCommand(command):
    splitCmd = re.split("\s", command)
    if splitCmd[0] == "change_password":
        changePass()
    elif splitCmd[0] == "check_user":
        checkUser(splitCmd[2], splitCmd[1])
    elif splitCmd[0] == "setup_info":
        setupInfo(splitCmd[1])
    else:


        
        return 0

def main():
    if log() == True:
        print("You have successfully connected to the server!!!!")
    
    while(True):
        command = input()


main()
s.close()
