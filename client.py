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
import time
import tqdm

host = 'localhost'
port = 8080


def login_quit():
    s.send(bytes("login_quit", "utf-8"))
    return

def log():
    global user, newpass
    choice = sign.sign()
    if (choice == "1"):
        user = sign.login(user)
        s.send(bytes("login", "utf-8"))
        msg = pickle.dumps(user)
        s.send(msg)
    elif (choice == "2"):
        user = sign.regis(user)
        s.send(bytes("regis", "utf-8"))
        msg = pickle.dumps(user)
        s.send(msg)
    elif (choice == "3"):
        user = sign.unlogin_changePassword(user)
        newpass = getpass("New password >> ")
        s.send(bytes("unlogin_cpass", "utf-8"))
        msg = pickle.dumps(user)
        s.send(msg)
    else:
        s.send(bytes("quit", "utf-8"))

def changePass():
    global user
    newPass = sign.changePassword(user)
    if newPass == False:
        return False
    s.send(bytes("newpass", "utf-8"))
    msg = pickle.dumps(user)
    s.send(msg)
    
def checkUser(username, option):
    pack = {"option": option,"username": username}
    s.send(bytes("check_user", "utf-8"))
    msg = pickle.dumps(pack)
    s.send(msg)
    
def setupInfo(option, content):
    pack = {
        "option": option,
        "content": content,
        "username": user["username"] 
    }
    s.send(bytes("set_info", "utf-8"))
    msg = pickle.dumps(pack)
    s.send(msg)


def recive():
    global app, login, out, filename, wait
    print("Open Thread Recive")
    while True:
        #print("Thread is working")
          
        msg = s.recv(numByteReceive)
        #HANDLE QUIT
        if msg.decode("utf-8") == "in_exit":
            print(">> CLIENT: Disconnected")
        if msg.decode("utf-8") == "log_out_success":
            print("Logged out")
        #HANDLE QUIT

        #HANDLE LOGIN 
        if msg.decode("utf-8") == "success":
            login = True
            print('Hello, ', user["username"], '!')
        elif msg.decode("utf-8") == "000":
            print('>> NOTICE: This account has been logged in from another client')
        elif msg.decode("utf-8") == "regis_success":
            print("Registration successful you can login now")
        elif msg.decode("utf-8") == "regis_fail":
            print(">> ERROR:Username is already existed. Please use another username")
        elif msg.decode("utf-8") == "login_fail":
            print(">> ERROR: Username or passsword incorrect !!!")
        elif msg.decode("utf-8") == "exit":
            out = True
            print(">> CLIENT: Disconnected")
            break 
        #HANDLE LOGIN
        
        #HANDLE CHANGEPASS
        if msg.decode("utf-8") == "log_cp_200":
            print("[S]>> Change password successfully")
        elif msg.decode("utf-8") == "cpass_200":
            user['password'] = newpass
            s.send(pickle.dumps(user))
            print(s.recv(numByteReceive).decode("utf-8"))
        elif msg.decode("utf-8") == "cpass_404":
            print("[S]>> Username or passsword incorrect !!!")
        #HANDLE CHANGEPASS

        #HANDLE CHECK_USER
        if msg.decode("utf-8") == "accept_ch_us":
            rep = s.recv(numByteReceive)
            if rep.decode("utf-8") == "user_obj":
                info = s.recv(numByteReceive)
                user_info = pickle.loads(info)
                print_user_info(user_info)
            elif rep.decode("utf-8") == "err_option":
                err = s.recv(numByteReceive)
                opt = err.decode("utf-8")
                print(">> ERROR: Option " + opt + " is invalid")
            elif rep.decode("utf-8") == "user_404":
                print("404: USER NOT FOUND")
            else:
                print(rep.decode("utf-8"))
        #HANDLE CHECK_USER
        #SETUP INFO
        if msg.decode("utf-8") == "set_success":
            print(">> Change Info Successful")
        elif msg.decode("utf-8") == "set_fail":
            rep = s.recv(numByteReceive)
            err = rep.decode("utf-8")
            print(">> ERROR: Option " + err + " is invalid")
        #SETUP INFO
        # HANDLE CHAT
        if msg.decode("utf-8") == "chat_user_404":
            print(">> ERROR: User not found")
        elif msg.decode("utf-8") == "chat_user_onl":
            chatbox_thread = Thread(target=chatbox)
            chatbox_thread.setDaemon(True)
            chatbox_thread.start()
            handle_cli_chat()
            #chatbox_thread.join()
        elif msg.decode("utf-8") == "chat_user_off":
            re = s.recv(numByteReceive).decode("utf-8")
            print(re)
            
        if msg.decode("utf-8") == "chat_req":
            s.send(bytes("cli_accept", "utf-8"))
            #app = None
            chatbox_thread = Thread(target=chatbox)
            chatbox_thread.setDaemon(True)
            chatbox_thread.start()
            handle_cli_chat()
            #chatbox_thread.join()      
        # HANDLE CHAT   
        # HANDLE DOWNLODD
        if msg.decode("utf-8") == "down_acpt":
            data = s.recv(numByteReceive).decode("utf-8")
            print("Down client msg: ", data)
            if data[:6] == "Exists":
                filesize = int(data[6:])
                print(data)
                s.send(bytes("ready", "utf-8"))
                #progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(path + filename, "wb") as f:
                    data = s.recv(1024)
                    totalRecv = len(data)
                    f.write(data)
                    while totalRecv < filesize:
                        data = s.recv(1024)
                        totalRecv += len(data)
                        f.write(data)
                        print("{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done")
                    print("Download Complete")
                wait = True
            else:
                print("File does not exists!")
                wait = True
        # HANDLE DOWNLOAD
        # HANDLE UPLOAD
        if msg.decode("utf-8") == "upload_acpt":
            data = s.recv(numByteReceive).decode("utf-8")
            print("Up client msg: ", data)
            link = path + filename
            if data == "up_file_exist":
                print(">> ERROR: Server already have this file")
                wait = True
            elif data == "ready":
                filesize = os.path.getsize(link)
                size = str(filesize)
                print("Filesize: " + size)
                s.send(bytes("Size " + size,"utf-8"))
                progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(link, "rb") as f:
                    for _ in progress:
                        bytes_read = f.read(1024)
                        if not bytes_read:   
                            break
                        s.sendall(bytes_read)
                        progress.update(len(bytes_read))
                wait = True

        # HANDLE UPLOAD


def handle_cli_chat():
    global leave
    #print("Go to Handle Chat")
    while True:
        try:
            
            #s = "has left the chat"
            mes = s.recv(numByteReceive)
            m = mes.decode('utf-8')
            if m == "leave_chat":
                break
            else:
                lists.append(m)
                recall = "cli_res"
                press(recall)
            
        except OSError:
            print("Errorrrrr")
            break
    
    return

def chat_with_user(username):
    global stop_msg
    global app
    #app = None
    s.send(bytes("chat", "utf-8"))
    s.send(bytes(username, "utf-8"))
def upload_option_file(option, content):
    global filename, wait
    
    file_list = content

    if option == "-change_name":
        if len(file_list) > 2:
            print(" >> ERROR: Only need 2 filenames")
        elif len(file_list) < 2:
            print(" >> ERROR: Need 2 filenames")
        else:
            if any("." in x for x in file_list):
                if os.path.isfile(path + file_list[1]) == False:
                    print(">> ERROR: File does not exist in Client!")
                    return
                else:
                    filename = file_list[1]
                    s.send(bytes("upload", "utf-8"))
                    s.send(bytes(file_list[0], "utf-8"))
                    #waiting upload process
                    while True:
                        if wait:
                            break
        
                    wait = False
            else:
                print(">> ERROR: Missing type of file")
    elif option == "-multi_files":
        if len(file_list) < 2:
            print(">> ERROR: You must type at least 2 filenames")
        else:
            if any("." in x for x in file_list):
                for x in file_list:
                    if os.path.isfile(path + x) == False:
                        print(">> ERROR: File " + x + " does not exist in Client!!")
                    else:   
                        filename = x
                        s.send(bytes("upload", "utf-8"))
                        s.send(bytes(filename, "utf-8"))
                        #waiting download process finished
                        while True:
                            if wait:
                                break
        
                        wait = False
            else:
                 print(">> ERROR: Missing type of file!!!")
    else:
        print(">> ERROR: " + option + " is invalid")
        return
def upload_file(file_name):
    global filename, wait
    filename = file_name
    if os.path.isfile(path + filename) == False:
        print(">> ERROR: File does not exist!")
        return
    if '.' in filename:
        s.send(bytes("upload", "utf-8"))
        s.send(bytes(filename, "utf-8"))
        #wait here
        while True:
            if wait:
                break
        
        wait = False
    else:
        print(">> ERROR: Missing type of file!!!")
    return   
def download_option_file(option, content):
    global filename, wait
    
    file_list = content

    if option == "-change_name":
        if len(file_list) > 2:
            print(" >> ERROR: Only need 2 filenames")
        elif len(file_list) < 2:
            print(" >> ERROR: Need 2 filenames")
        else:
            
            if any("." in x for x in file_list):
                if os.path.isfile(path + file_list[0]):
                    print(">> ERROR: Already have this file in Client!")
                    return
                else:
                    filename = file_list[0]
                    s.send(bytes("download", "utf-8"))
                    s.send(bytes(file_list[1], "utf-8"))
                    #waiting download process
                    while True:
                        if wait:
                            break
        
                    wait = False
            else:
                print(">> ERROR: Missing type of file")
    elif option == "-multi_files":
        if len(file_list) < 2:
            print(">> ERROR: You must type at least 2 filenames")
        else:
            if any("." in x for x in file_list):
                for x in file_list:
                    if os.path.isfile(path + x):
                        print(">> ERROR: File " + x + " alreay exist in Client!!")
                    else:   
                        filename = x
                        s.send(bytes("download", "utf-8"))
                        s.send(bytes(filename, "utf-8"))
                        #waiting download process finished
                        while True:
                            if wait:
                                break
        
                        wait = False
            else:
                 print(">> ERROR: Missing type of file!!!")
    else:
        print(">> ERROR: " + option + " is invalid")
        return
def download_file(file_name):
    global filename, wait
    filename = file_name
    if os.path.isfile(path + filename):
        print(">> ERROR: Already have this file!")
        return
    if '.' in filename:
        s.send(bytes("download", "utf-8"))
        s.send(bytes(filename, "utf-8"))
        #wait here
        while True:
            if wait:
                break
        
        wait = False
    else:
        print(">> ERROR: Missing type of file!!!")
    return   
def analyzeCommand(command):
    splitCmd = re.split("\s", command)
    #print(splitCmd) #use for debugging
    if splitCmd[0] == "change_password":
        changePass()
    elif splitCmd[0] == "check_user" and len(splitCmd) == 3:
        checkUser(splitCmd[2], splitCmd[1])
    elif splitCmd[0] == "setup_info" and len(splitCmd) >= 3:
        content = ""
        for i in range(2, len(splitCmd)):
            content += splitCmd[i]
            content += " "
        setupInfo(splitCmd[1], content)
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
    elif splitCmd[0] == "/help" and splitCmd[1] == "upload":
        help_details(4)
    elif splitCmd[0] == "/help" and splitCmd[1] == "download":
        help_details(5)
    elif splitCmd[0] == "quit":
        login_quit()
        #s.send(bytes(user["username"], "utf-8"))
        return "exit"
    elif splitCmd[0] == "log_out":
        s.send(bytes("log_out", "utf-8"))
        return "log_out"
    elif splitCmd[0] == "download":
        if len(splitCmd) == 2:
            download_file(splitCmd[1])
        elif len(splitCmd) > 2:
            content = []
            for i in range(2, len(splitCmd)):
                content.append(splitCmd[i])
            download_option_file(splitCmd[1], content)
    elif splitCmd[0] == "upload":
        if len(splitCmd) == 2:
            upload_file(splitCmd[1])
        elif len(splitCmd) > 2:
            content = []
            for i in range(2, len(splitCmd)):
                content.append(splitCmd[i])
            upload_option_file(splitCmd[1], content)
    else:
        s.send(bytes("cmd_invalid", "utf-8"))
        print(">> ERROR: Invalid Command. Try again !\n")
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
        print('\t -note [note]      : Update note of user')
        print('\n')
    elif command == 4:
        print('upload [-option] [filename]     : Upload file to server, you can dont use option')
        print('\t Without [-option]            : Upload file with [filename]')
        print('\t -change_name [new] [current] : Change file name when upload to server')
        print('\t -multi_files [list_file]     : Upload multiple files')
        print('\t Ps: all file must be in "client" folder')
    elif command == 5:
        print('download [-option] [filename]     : Download file to client, you can dont use option')
        print('\t Without [-option]            : Download file with [filename]')
        print('\t -change_name [new] [current] : Change file name when download to client')
        print('\t -multi_files [list_file]     : Download multiple files')
        print('\t Ps: all file will be in "client" folder')
    return
    
def help():
    print('change_password [username]      : Change your password')
    print('check_user [-option] [username] : Check user infomation')
    print('setup_info [-option]            : Setup your infomation')
    print('chat [username]                 : Chat with another user')  
    print('upload [-option] [filename]     : Upload file to server, you can dont use option')
    print('download [-option] [filename]     : Download file to client, you can dont use option')
    print('--> For more details: Type "/help command" - Ex: /help check_user')
    
    return

def press(btn):
    global app, leave
    if btn == "Send":
        note = app.getEntry("e1")
        s.send(bytes(note, "utf-8"))
        #lists.append(note)
        #app.updateListBox("list", lists, False, False)
    elif btn == "Leave":
        s.send(bytes("chat_quit", "utf-8"))
        
        #tmp = s.recv(numByteReceive)
        #print(tmp.decode('utf-8'))
        app.stop()
    elif btn == "cli_res":
        app.updateListBox("list", lists, False, False)
        pass

def chatbox():
    global app
    app = gui(user["username"], "300x300")
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
    global stop_msg
    global app
    global login, out

    recive_thread = Thread(target=recive)
    recive_thread.start()

    while True:
        log()
        time.sleep(1)
        if login == True:
            print("You have successfully connected to the server!!!!")
            break
        if out == True:
            break
    if out:
        return
    
    print('Type "/help" to know more about commands')

    while True:      
        command = input(">> ")
        #print("DEBUG: command -> ", command)
        a = analyzeCommand(command)
        if a == "exit":
            break
        if a == "log_out":
            login = False
            break
        time.sleep(1)

    recive_thread.join()         

stop_msg = True
lists = []
app = None
newpass = None
login = False
out = False
leave = False
wait = False
path = 'client/'
filename = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 8080)) #must change port from string to int
numByteReceive = 1024
user = {"username": "", "password": "", "fullname": "", "birth": "", "notelist": "", "status": "off"}

if __name__ == "__main__":
    main()

    s.close()
