import string

def ceaser_encrypt(message, key):
    shift = key % 26
    cipher = str.maketrans(string.ascii_lowercase, string.ascii_lowercase[shift:] + string.ascii_lowercase[:shift])

    encrypted_message = message.lower().translate(cipher)

    return encrypted_message

def ceaser_decrypt(encypted_message, key):

    shift = 26 - (key % 26)
    cipher = str.maketrans(string.ascii_lowercase, string.ascii_lowercase[shift:] + string.ascii_lowercase[:shift]) 

    message = encypted_message.translate(cipher)
    return message

message = input("Enter the message: ")
key = 3

encrypted_message = ceaser_encrypt(message, key)
print(f"Encrypted message: {encrypted_message}")

decrypted_message = ceaser_decrypt(encrypted_message, key)
print(f"Decrypted message: {decrypted_message}")