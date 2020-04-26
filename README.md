# SocketProject

Note:
+ Trước khi gửi user về sẽ gửi thông báo là login/signup
+ Sau em sẽ gửi một object user (bao gồm username và pass) cho anh.
(https://www.youtube.com/watch?v=WM1z8soch0Q&t=285s) !Nhận và gửi object em kham thảo link này, dùng pickle dumps và loads
+ Khi đăng ký, em sẽ gửi object user gồm đầy đủ thông tin (trừ listNote)
+ Anh chỉ cần gửi cho em thông báo thành công hay thất bại là được


#################
Đoạn code em test thử để nhận object đã hoạt động được
if (data.decode("utf-8") == "login"):
    msg = self.csocket.recv(numByteReceive)
    print(msg)
    user = pickle.loads(msg)
    print(user)
