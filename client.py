import sys
import socket
import errno
import os
import sign
import pickle #to send object
import re
import tkinter
from threading import Thread
from getpass import getpass
from appJar import gui


host = 'localhost'
port = 8080


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 8080)) #must change port from string to int
numByteReceive = 1024
user = {"username": "", "password": "", "fullname": "", "birth": "", "notelist": "", "status": "off"}



def login_quit():
    s.send(bytes("login_quit", "utf-8"))
    return

def log():
    rep = s.recv(1024).decode("utf-8")
    global user
    choice = sign.sign()
    if (choice == "1"):
        user = sign.login(user)
        s.send(bytes("login", "utf-8"))
        msg = pickle.dumps(user)
        s.send(msg)
    elif (choice == "2"):
        user = sign.regis(user)
        print("User info", user)
        s.send(bytes("regis", "utf-8"))
        msg = pickle.dumps(user)
        print("User info dump", msg)
        s.send(msg)
    elif (choice == "3"):
        user = sign.unlogin_changePassword(user)
        s.send(bytes("unlogin_cpass", "utf-8"))
        msg = pickle.dumps(user)
        s.send(msg)
    else:
        s.send(bytes("quit", "utf-8"))
    msg = s.recv(numByteReceive)
    
    if msg.decode("utf-8") == "success":
        print('Hello, ', user["username"], '!')
        return True
    elif msg.decode("utf-8") == "000":
        print('>> NOTICE: This account has been logged in from another client')
        return log()
    elif msg.decode("utf-8") == "regis_success":
        str = "regis_success"
        return str
    elif msg.decode("utf-8") == "regis_fail":
        print(">> ERROR:Username is already existed. Please use another username")
        return log()
    elif msg.decode("utf-8") == "login_fail":
        print(">> ERROR: Username or passsword incorrect !!!")
        return log()
    elif msg.decode("utf-8") == "exit":
        str = "exit"
        print(">> CLIENT: Disconnected")
        return str
    elif msg.decode("utf-8") == "cpass_200":
        newpass = getpass("New password >> ")
        user['password'] = newpass
        s.send(pickle.dumps(user))
        print(s.recv(numByteReceive).decode("utf-8"))
        return log()
    elif msg.decode("utf-8") == "cpass_404":
        print("Username or passsword incorrect !!!")
        return log()
    else:
        print("Something went wrong!!")
        tempInput = input("Press anykey to try again")
        return log()

def changePass():
    global user
    newPass = sign.changePassword(user)
    if newPass == False:
        return False
    s.send(bytes("newpass", "utf-8"))
    msg = pickle.dumps(user)
    s.send(msg)
    server_msg = s.recv(numByteReceive).decode("utf-8")
    print(server_msg)

    return

def checkUser(username, option):
    pack = {"option": option,"username": username}
    s.send(bytes("check_user", "utf-8"))
    msg = pickle.dumps(pack)
    s.send(msg)

    rep = s.recv(numByteReceive)
    if rep.decode("utf-8") == "user_404":
        print("404: USER NOT FOUND")

    if rep.decode("utf-8") == "user_obj":
        info = s.recv(numByteReceive)
        user_info = pickle.loads(info)
        print_user_info(user_info)
    elif rep.decode("utf-8") == "err_option":
        err = s.recv(numByteReceive)
        opt = err.decode("utf-8")
        print(">> ERROR: Option " + opt + " is invalid")
    else:
        print(rep.decode("utf-8"))

def setupInfo(option, content):
    pack = {
        "option": option,
        "content": content,
        "username": user["username"] 
    }
    s.send(bytes("set_info", "utf-8"))
    msg = pickle.dumps(pack)
    s.send(msg)

    rep = s.recv(numByteReceive)
    if rep.decode("utf-8") == "set_success":
        print(">> Change Info Successful")
    else:
        err = rep.decode("utf-8")
        print(">> ERROR: Option " + err + " is invalid")


def recive():
    while True:
        try:
            if stop_thread:
                break
            msg = s.recv(numByteReceive)
            m = msg.decode('utf-8')
            lists.append(m)
            recall = "cli_res"
            press(recall)
            #msg_list.insert(tkinter.END,msg)
        except OSError:
            break



def chat_with_user(username):
    s.send(bytes("chat", "utf-8"))
    s.send(bytes(username, "utf-8"))

    rep = s.recv(numByteReceive)
    r = rep.decode('utf-8')
    if r == "user_404":
        print(">> ERROR: User not found")
    else:
        #r = s.recv(numByteReceive).decode("utf-8")
        if r == "onl":
            #dosth
            recive_thread = Thread(target=recive)
            recive_thread.start()
            chatbox() 
        else:
            print(r)
    
def analyzeCommand(command):
    splitCmd = re.split("\s", command)
    print(splitCmd) #use for debugging
    if splitCmd[0] == "change_password":
        changePass()
    elif splitCmd[0] == "check_user" and len(splitCmd) == 3:
        checkUser(splitCmd[2], splitCmd[1])
    elif splitCmd[0] == "setup_info" and len(splitCmd) == 3:
        setupInfo(splitCmd[1], splitCmd[2])
    elif splitCmd[0] == "chat" and len(splitCmd) == 2:
        chat_with_user(splitCmd[1])
    elif splitCmd[0] == "/help" and len(splitCmd) < 2:
        help()
    elif splitCmd[0] == "/help" and splitCmd[1] == "change_password":
        help_details(1)
    elif splitCmd[0] == "/help" and splitCmd[1] == "check_user":
        help_details(2)
    elif splitCmd[0] == "/help" and splitCmd[1] == "setup_info":
        help_details(3)
    elif splitCmd[0] == "quit":
        login_quit()
        msg = s.recv(numByteReceive)
        s.send(bytes(user["username"], "utf-8"))
        if msg.decode("utf-8") == "exit":
            str = "exit"
            print("Disconnected")
            return str
    elif splitCmd[0] == "log_out":
        s.send(bytes("log_out", "utf-8"))
        msg = s.recv(numByteReceive)
        s.send(bytes(user["username"], "utf-8"))
        if msg.decode("utf-8") == "log_out_success":
            print("Logged out")
            return "log_out"
    else:
        s.send(bytes("cmd_invalid", "utf-8"))
        print("Invalid Command. Try again !")
    return 0
def print_user_info(info):
    for x in info:
        print(x + ": " + str(info[x]))
def help_details(command):
    if command == 1:
        print('change_password [username]      : Change your password')
        print('\n')
    elif command == 2:
        print('check_user [-option] [username] : Check user infomation')
        print('\t -find         : check user account exist in database')
        print('\t -online       : check online status of user')
        print('\t -show_date    : show date of birth of user')
        print('\t -show_fullname: show name of user')
        print('\t -show_note    : show note of user')
        print('\t -show_all     : show all infomations of user')
        print('\n')
    elif command == 3:
        print('setup_info [-option] : Setup infomation of user')
        print('\t -fullname [name]  : Update name of user')
        print('\t -date [birthday]  : Update date of birth of user')
        print('\t -note [note]  : Update note of user')
        print('\n')
    s.send(bytes("help_detail", "utf-8"))
    return
def help():
    print('change_password [username]      : Change your password')
    print('check_user [-option] [username] : Check user infomation')
    print('setup_info [-option]            : Setup your infomation')
    print('char [username]                 : Chat with another user')
    print('--> For more details: Type "/help command" - Ex: /help check_user')
    s.send(bytes("help", "utf-8"))
    return



def press(btn):
    if btn == "Send":
        note = app.getEntry("e1")
        s.send(bytes(note, "utf-8"))
        #lists.append(note)
        #app.updateListBox("list", lists, False, False)
    elif btn == "Leave":
        global stop_thread
        s.send(bytes("quit", "utf-8"))
        stop_thread = True
        app.stop()
    if btn == "cli_res":
        app.updateListBox("list", lists, False, False)

def chatbox():
    app.setFont(20)
    app.addLabel("title", " Welcome to Chatroom ") 
    app.startScrollPane("PANE")
    app.addListBox("list", lists)
    app.stopScrollPane()
    app.setFont(13)
    app.addEntry("e1")
    app.setEntryDefault("e1", "Type message here")
    app.addButtons(["Send", "Leave"], press) 
    app.go()


def main():
    log_state = log()
    if log_state == True:
        #handlethread = Thread(target=handle_thread)
        #handlethread.start()
        print("You have successfully connected to the server!!!!")
    elif log_state == "regis_success":
        print("Registration successful you can login now")
        main()
    elif log_state == "exit":
        return
    
    print('Type "/help" to know more about commands')
    
    
    while(True):
        data = s.recv(1024).decode("utf-8")
        splitData = re.split("\s", data)
        if (splitData[0] == "chat"):
            s.send(bytes("cli_accept", "utf-8"))
            name = splitData[1]
            print(">> SERVER: User " + name + " want to chat with you.")
            recive_thread = Thread(target=recive)
            recive_thread.start()
            chatbox()
        print(data)
        command = input(">> ")
        a = analyzeCommand(command)
        if a == "exit":
            return
        if a == "log_out":
            break
        
        
    main()

stop_thread = False
lists = []
app = gui("Chatter", "300x300")

main()
s.close()
