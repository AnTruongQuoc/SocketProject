import socket, threading

HOST = socket.gethostname()
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
            if (data.decode("utf-8") == "1"):
                break
            else:
                print("From client ", self.caddress, " content:", data.decode("utf-8"))
            
        print("Client at ", self.caddress, " disconnected...")
#Class for multithread server socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cấu hình kết nối
s.bind((HOST, PORT)) #lắng nghe kết nối
s.listen(numOfConnet) #thiết lập số kết nối đồng thời


print("Server started at ", HOST, ":", PORT)
print("Waiting for client request")

while (True):
    clientsocket, address = s.accept() #chấp nhận kết nối
    newthread = ClientThread(address, clientsocket)
    newthread.start() #start() sử dụng để chạy thread
