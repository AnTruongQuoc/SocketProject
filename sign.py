from getpass import getpass
import crypt as cr

def sign():
    print("What do you want to do:")
    print("1. Sign In")
    print('2. Sign Up')
    print('3. Change Password')
    print("4. Quit")
    result = input("Input (1/2/3/4):")
    print(result)
    if(result != "1" and result != "2" and result != "3" and result != "4"):
        print("Wrong choice! Please choose again")
        return sign()
    
    return result

def login(user):
    user["username"] = input("Please enter your username: ")
    user["password"] = getpass("Please enter your password: ")
    user = encrypt(user)
    return user

def regis(user):
    user["username"] = input("Please enter your username: ")
    user["password"] = getpass("Please enter your password: ")
    user["fullname"] = input("Enter your full name: ")
    user["birth"] = input("Enter your birthday: ")
    user = encrypt(user)
    return user


def encrypt(user):
    encrypt = input("Do you want to encrypt your password? (Y/N)")
    if encrypt == "Y":
        print("Your information has been encrypted")
        #add code below this line
            #encrypt password
        affine = cr.Affine()
        affine.encrypt(user["password"])
        #add code above this line
        return user
    else:
        print("You choose not to encrypt your password.")
        return user
def unlogin_changePassword(user):
    user["username"] = input("Username >> ")
    user["password"] = getpass("Current password >> ")
    return user
def changePassword(user):
    oldPass = getpass("Current password >> ")
    if oldPass == user["password"]:
        newPass = getpass("New password    >> ")
        user["password"] = newPass
        user = encrypt(user)
        return user["password"]
    else:
        print("Wrong old password")
        return False