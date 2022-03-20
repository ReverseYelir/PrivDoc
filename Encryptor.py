'''
Encrypts a file given a file name or absolute path

****IMPORTANT****
Public key is loaded from pubkey.txt. If file does not exist, a new rsa
keypair is generated and displayed to the user. This is the only time
to make note of
Encryption:
        1) Grab file stream
        2) encrypt file with AES
        3) encrpyt AES key with RSA using public key found in pubkey.txt
        4) output the encrypted file's content to "encrypted-{input file name}.txt"
        5) output encrypted aeskey to "aeskey.txt"
'''

import os
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Encryptor:
    message_file = None
    message_directory = None
    SALT_SIZE = 8


    def __init__(self, file_path):
        try:
            #  opens the file and changes the current directory to match the input file
            self.message_file = open(file_path, "rb")
            file_name = os.path.basename(self.message_file.name)
            path = self.message_file.name.replace(file_name, "")
            os.chdir(path)

        except FileNotFoundError:
            print("Input File not found.")
            exit(1)

    def create_key_file(self, pubkey):
        file = open("pubkey.txt", "w")
        file.write(f"{pubkey.n}, {pubkey.e}")
        file.close()

    def create_key(self):
        first_resp = ""
        second_resp = " "
        while first_resp != second_resp:
            first_resp = input("Enter Encryption Passphrase: ")
            second_resp = input("Confirm Passphrase: ")
        salt = os.urandom(self.SALT_SIZE)  # creates 64-bit salt
        key = PBKDF2(first_resp, salt).read(32)  # creates 256-bit key
        return key, salt

    def parse_file_name(self):
        name_list = self.message_file.name.split("\\")
        name = name_list[-1]
        return name

    def encrypt(self):
        # grab password and hash via PBKDF2
        aes_key, salt = self.create_key()
        aes_cipher_obj = AES.new(aes_key, AES.MODE_EAX, salt)

        #  Read in message and encrypt with AES
        msg_file = self.message_file
        msg = msg_file.read()
        msg_file.close()
        msg_ciphertext, tag = aes_cipher_obj.encrypt_and_digest(msg)

        #  write out encrypted file
        out_name = f"encrypted-{self.parse_file_name()}"
        file_out = open(out_name, "wb")
        file_out.write(msg_ciphertext+salt)
        file_out.close()

