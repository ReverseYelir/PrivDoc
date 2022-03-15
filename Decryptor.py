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

import rsa
from Crypto.Cipher import AES
from rsa import DecryptionError


class Decryptor:
    message_file = None
    private_key = None

    def __init__(self, file_path, key_list):
        try:
            self.message_file = open(file_path, "rb")
            file_name = os.path.basename(self.message_file.name)
            path = self.message_file.name.replace(file_name, "")
            os.chdir(path)
        except FileNotFoundError:
            print("Input File not found. Path Example: C:\\Users\\user\\example.txt")
            exit(1)
        self.private_key = rsa.PrivateKey(int(key_list[0]), int(key_list[1]), int(key_list[2]), int(key_list[3]), int(key_list[4]))

    def load_privkey(self):
        key_list = input("Enter Private Key in the form: n, e, d, p, q\n").split(",")
        return rsa.PrivateKey(int(key_list[0]), int(key_list[1]), int(key_list[2]), int(key_list[3]), int(key_list[4]))

    def load_nonce(self):
        file = open("nonce.txt", "rb")
        contents = file.read()
        file.close()
        return contents

    def load_message(self):
        file = open(self.message_file.name, 'rb')
        contents = file.read()
        file.close()
        return contents

    def decrypt(self):
        #  decrypt aes key
        privkey = self.private_key
        aes_file = open('aeskey.txt', 'rb')
        aes_key_ct = aes_file.read()
        aes_file.close()
        try:
            aes_key_pt = rsa.decrypt(aes_key_ct, privkey)
        except ValueError:
            print("Invalid Private key paramaters")
            exit(1)
        except DecryptionError:
            print("Decryption error. Likely issue with aeskey's ciphertext")
            exit(1)

        #  load decryption necessities
        nonce = self.load_nonce()
        msg_ciphertext = self.load_message()

        #  decrypt message
        cipher = AES.new(aes_key_pt, AES.MODE_EAX)
        pt = cipher.decrypt(msg_ciphertext)
        print(f"Decrypted message {pt}\n")