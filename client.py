import socket

host = socket.gethostname()
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), port))

numByteReceive = 1024

while (True):
    #receivemessage from server
    #msg = s.recv(numByteReceive)
    #print(msg.decode("utf-8"))
    sendData = input()
    s.send(bytes(sendData, "utf-8"))
    if (sendData == "1"):
        break
    
s.close()