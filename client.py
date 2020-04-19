import socket

host = input("Input IP server: ")
port = input("Input port server: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, int(port))) #must change port from string to int

numByteReceive = 1024

while (True):
    #receive message from server
    #msg = s.recv(numByteReceive)
    #print(msg.decode("utf-8"))
    sendData = input()
    s.send(bytes(sendData, "utf-8"))
    if (sendData == "1"):
        break
    
s.close()