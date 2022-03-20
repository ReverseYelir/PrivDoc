'''
Class definition in charge of decrypting a given file provided
a private key.
Following Files Needed by Decryptor (same directory):
    input file
    nonce.txt
    pubkey.txt
    aeskey.txt
'''
import os

from Crypto.Cipher import AES
from pbkdf2 import PBKDF2

class Decryptor:
    message_file = None
    private_key = None
    salt = b''

    def __init__(self, file_path):
        try:
            self.message_file = open(file_path, "rb")
            file_name = os.path.basename(self.message_file.name)
            path = self.message_file.name.replace(file_name, "")
            os.chdir(path)
        except FileNotFoundError:
            print("Input File not found. Path Example: C:\\Users\\user\\example.txt")
            exit(1)


    def load_message(self):
        file = open(self.message_file.name, 'rb')
        contents = file.read()
        self.salt = contents[-8:]
        file.close()
        return contents[:-8]

    def create_key(self):
        first_resp = ""
        second_resp = " "
        while first_resp != second_resp:
            first_resp = input("Enter Encryption Passphrase: ")
            second_resp = input("Confirm Passphrase: ")
        key = PBKDF2(first_resp, self.salt).read(32)  # creates 256-bit key
        return key

    def decrypt(self):
        msg_ciphertext = self.load_message()
        aes_key = self.create_key()
        cipher = AES.new(aes_key, AES.MODE_EAX, self.salt)
        try:
            msg_plaintext = cipher.decrypt(msg_ciphertext).decode()
        except UnicodeDecodeError:
            print("Invalid Passphrase")
            exit(1)

        print(f"\nDecrypted Message {msg_plaintext}")

