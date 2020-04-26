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
    encrypt(user)
    return user

def regis(user):
    user["username"] = input("Please enter your username: ")
    user["password"] = getpass("Please enter your password: ")
    user["fullname"] = input("Enter your full name: ")
    user["birth"] = input("Enter your birthday")
    encrypt(user)
    return user


def encrypt(user):
    encrypt = input("Do you want to encrypt your password? (Y/N)")
    if encrypt == "Y":
        print("Your information has been encrypted")
        #add code below this line
            #encrypt password
        #add code above this line
        return 1
    else:
        print("You choose not to encrypt your password.")
        return 0
