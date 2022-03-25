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
        file_path = self.getAbsolutePath(file_path)
        try:
            self.message_file = open(file_path, "rb")
            file_name = os.path.basename(self.message_file.name)
            path = self.message_file.name.replace(file_name, "")
            os.chdir(path)
        except FileNotFoundError:
            print("Input File not found. Path Example: C:\\Users\\user\\example.txt")
            exit(1)

    '''
    Function is meant to return an absolute path based on the input.
    If the input is absolute, no changes are needed.
    If the path is relative, we convert it to an absolute path and return
    '''
    def getAbsolutePath(self, file_path):
        if os.path.isabs(file_path):
            return file_path
        else:
            return os.path.abspath(file_path)


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
            first_resp = input("Enter Encryption Password: ")
            second_resp = input("Confirm Password: ")
        key = PBKDF2(second_resp, self.salt).read(32)  # creates 256-bit key
        return key

    def decrypt(self):
        msg_ciphertext = self.load_message()
        aes_key = self.create_key()
        cipher = AES.new(aes_key, AES.MODE_EAX, self.salt)
        try:
            msg_plaintext = cipher.decrypt(msg_ciphertext).decode()
        except UnicodeDecodeError:
            print("Invalid Password or Input File is not Encrypted.")
            exit(1)

        print("="*10 + " Decrypted Message " + "="*10)
        print(msg_plaintext)

        #  write out decrypted file
        if input("Save to a file? (Y/N)?").lower().strip() == "y":
            out_name = input("Save file as: ").lower().strip()
            file_out = open(out_name, "w")
            file_out.write(msg_plaintext)
            file_out.close()
