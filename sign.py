from getpass import getpass

def sign():
    print("What do you want to do:")
    print("1. Sign In")
    print('2. Sign Up')
    result = input("Input (1/2):")
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
    user["birth"] = input("Enter your birthday")
    user = encrypt(user)
    return user


def encrypt(user):
    encrypt = input("Do you want to encrypt your password? (Y/N)")
    if encrypt == "Y":
        print("Your information has been encrypted")
        #add code below this line
            #encrypt password
        #add code above this line
        return user
    else:
        print("You choose not to encrypt your password.")
        return user

def changePassword(user):
    oldPass = getpass("password: ")
    if oldPass == user["password"]:
        newPass = getpass("new password: ")
        user["password"] = newPass
        user = encrypt(user)
        return user["password"]
    else:
        return False