import random
import string

def generate_password(length = 10):
    alpabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(alpabet) for i in range(length))
    return password

password = generate_password()
print("Generated password:", password)