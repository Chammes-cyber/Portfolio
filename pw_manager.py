import hashlib
import getpass

password_manager = {}

def create_account():
    usnername = input("Enter a username: ")
    password = getpass.getpass("Enter a password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    password_manager[usnername] = hashed_password
    print("Account created successfully!")

def login():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username in password_manager and password_manager[username] == hashed_password:
        print("Login successful!")
    else:
        print("Invalid username or password.")

def main():
    while True:
        choice = input("Enter 1 to create an account, 2 to login, or 3 to exit:")
        if choice == '1':
            create_account()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
# This code is a simple password manager that allows users to create accounts and log in securely using hashed passwords.