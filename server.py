import socket, threading
import pandas as pd #convert csv to dictionary
import pickle

#HOST = socket.gethostname()
HOST = 'localhost'
PORT = 8080
numOfConnet = 5
numByteReceive = 1024

#Class for multithread server socket
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.caddress = clientAddress
        print("New connection added: ", clientAddress)
    def run(self):
        print("Connection from: ", self.caddress)
        while (True):
            data = self.csocket.recv(numByteReceive)
            
            #QUIT STATUS
            if (data.decode("utf-8") == "quit"):
                self.csocket.send(bytes("exit","utf8"))
                self.csocket.close()
                break
            elif (data.decode("utf-8") == "login_quit"):
                self.csocket.send(bytes("exit","utf8"))
                ur = self.csocket.recv(numByteReceive)
                txt = ur.decode("utf-8")
                user_data.loc[memory[txt], 'status'] = "off"
                self.csocket.close()
                break
            elif (data.decode("utf-8") == "log_out"):
                self.csocket.send(bytes("log_out_success","utf8"))
                ur = self.csocket.recv(numByteReceive)
                txt = ur.decode("utf-8")
                user_data.loc[memory[txt], 'status'] = "off"
                print(user_data)
            else:
                print("From client ", self.caddress, " content:", data.decode("utf-8"))
            #QUIT STATUS

            #HANDLE_LOGIN_REGIS
            if (data.decode("utf-8") == "regis"):
                msg = self.csocket.recv(4098)
                userdata = pickle.loads(msg)
                #print("Message: ", userdata)

                if check_user_regis(userdata):
                    self.csocket.send(bytes("regis_success", "utf-8"))
                else: 
                    self.csocket.send(bytes("regis_fail", "utf-8"))
            elif (data.decode("utf-8") == "login"):
                msg = self.csocket.recv(4098)
                userdata = pickle.loads(msg)

                if check_user_login(userdata) == True:
                    self.csocket.send(bytes("success", "utf-8"))
                elif check_user_login(userdata) == "000":
                    self.csocket.send(bytes("000", "utf-8"))
                else: 
                    self.csocket.send(bytes("login_fail", "utf-8"))
            #HANDLE_LOGIN_REGIS

            #CHANGE PASSWORD
            if (data.decode("utf-8") == "newpass"):
                msg = self.csocket.recv(4098)
                userdata = pickle.loads(msg)
                handle_changepass(userdata)
                self.csocket.send(bytes("Change password successfully", "utf-8"))
            elif (data.decode("utf-8") == "unlogin_cpass"):
                msg = self.csocket.recv(4098)
                userdata = pickle.loads(msg)

                if check_user_cpass(userdata):
                    self.csocket.send(bytes("cpass_200", "utf-8"))
                    obj = self.csocket.recv(4098)
                    newpass = pickle.loads(obj)
                    handle_unlogin_cpass(newpass)
                    self.csocket.send(bytes("Change password successfully", "utf-8"))
                else:
                    self.csocket.send(bytes("cpass_404", "utf-8"))
            #CHANGE PASSWORD

            #CHECK USER
            if (data.decode("utf-8") == "check_user"):
                msg = self.csocket.recv(4098)
                userdata = pickle.loads(msg)
                
                check = find_user(userdata)
                if check == "False":
                    self.csocket.send(bytes("user_404", "utf-8"))
                else:
                    rep = option_check(userdata, check)

                    if userdata["option"] == "-show_all":
                        self.csocket.send(bytes("user_obj", "utf-8"))
                        msg = pickle.dumps(rep)
                        self.csocket.send(msg)
                    else:
                        self.csocket.send(bytes(rep, "utf-8"))

            
        print("Client at ", self.caddress, " disconnected...")
    
#Class for multithread server socket
def option_check(user, count):
    option = user["option"]
    
    if option == "-find":
        msg = user["username"] + " is in database"
        return msg
    if option == "-online":
        msg = user["username"] + " is offline"
        if user_data.at[count, 'status'] == "online":
            msg = user["username"] + " is online"
            return msg
        return msg
    if option == "-show_date":
        msg = ">> Birthday of " + user["username"] +": "+  user_data.at[count, 'birth']
        
        return msg
    if option == "-show_fullname":
        msg =  ">> Fullname of " +user["username"] +": "+ user_data.at[count, 'fullname']
        
        return msg
    if option == "-show_note":
        msg =  ">> Notes of " + user["username"] +": "+ user_data.at[count, 'notelist']
        
        return msg
    if option == "-show_all":
        info = dict()
        info.update({
            "Username": user["username"],
            "Status": user_data.at[count, 'status'],
            "Fullname": user_data.at[count, 'fullname'],
            "Birthday": user_data.at[count, 'birth'],
            "Note": user_data.at[count, 'notelist'],
        })
        print("debug note: ", user_data.at[count, 'notelist'])
        return info
        
def find_user(user):
    count = 0
    for x in user_data["username"]:
        if user["username"] == x:
            return count
        count+=1
  
    return "False" #count = 0 <=> False so returning str
def handle_unlogin_cpass(user): #Change password when user not log in
    count = 0
    for x in user_data["username"]:
        if user["username"] == x:
            print(x)
            print(user_data.at[count, 'password'])
            user_data.loc[count, 'password'] = user["password"]
            print("newpassword: ",user_data.at[count, 'password'])
            #save to database
            user_data.to_csv("userdata.csv", index=False)
            break
        count +=1
    return
def check_user_cpass(user):
    count = 0
    for x in user_data["username"]:
        if user["username"] == x:
            if user["password"] == user_data.at[count, 'password']:
                return True
        count +=1

    return False
def handle_changepass(user): #handle changpassword when user already log in
    count = 0
    for x in user_data["username"]:
        if user["username"] == x:
            print(x)
            print(user_data.at[count, 'password'])
            user_data.loc[count, 'password'] = user["password"]
            user_data.loc[count, 'status'] = "off"
            print("newpassword: ",user_data.at[count, 'password'])
            #save to database
            user_data.to_csv("userdata.csv", index=False)
            user_data.loc[count, 'status'] = "online"
            break
        count += 1
    return
def check_user_login(user):
    
    count = 0
    for x in user_data["username"]:
        if user["username"] == x:
            print(x)
            print(user_data.at[count, 'password'])
            if user["password"] == user_data.at[count, 'password']:
                print(user_data.at[count, 'status'] == "online")
                if user_data.at[count, 'status'] == "online":
                    return "000"
                user_data.loc[count, 'status'] = "online"
                memory.update({user["username"]: count})
                print(user_data)
                print(memory)
                return True
        count += 1
    
    return False       
    
def check_user_regis(user):
    for x in user_data["username"]:
        if user["username"] == x:
            return False
    
    #new = pd.DataFrame([user])
    
    #print(new.dtypes)
    #user_data.update(user_data.append(new, ignore_index=True))
    total_row = user_data.shape[0]
    user_data.loc[total_row] = [user["username"], user["password"], user["fullname"], user["birth"], user["notelist"], user["status"]]
    #print("So dong: ", total_row)
    print(user_data)
    
    user_data.to_csv("userdata.csv", index=False)
    return True

def incoming_connection():
    while True:
        clientsocket, address = s.accept() #chấp nhận kết nối
        newthread = ClientThread(address, clientsocket)
        newthread.start() #start() sử dụng để chạy thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cấu hình kết nối
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT)) #lắng nghe kết nối

if __name__ == "__main__":
    s.listen(numOfConnet) #thiết lập số kết nối đồng thời

    memory = dict()
    user_data = pd.read_csv("userdata.csv")
    print(user_data)
    print("Server started at ", HOST, ":", PORT)
    print("Waiting for client request")

    NEW_THREAD = threading.Thread(target=incoming_connection)
    NEW_THREAD.start()
    NEW_THREAD.join()
    s.close()
