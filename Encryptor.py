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

import rsa, os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Encryptor:
    message_file = None
    message_directory = None
    pubkey = None
    BIT = 2048

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

    def load_pubkey(self):
        if os.path.exists("pubkey.txt"):
            file = open("pubkey.txt")
        else:
            print(f"pubkey.txt not found. Generating {self.BIT} RSA keys...\n")
            (pubkey, privkey) = rsa.newkeys(self.BIT)
            print(f"n: {privkey.n}\n\ne: {privkey.e}\n\nd: {privkey.d}\n\np: {privkey.p}\n\nq: {privkey.q}\n\n")
            self.pubkey = pubkey
            self.create_key_file(pubkey)
            file = open('pubkey.txt', "r")
        key_list = file.read().split(",")
        file.close()
        self.pubkey = rsa.PublicKey(int(key_list[0]), int(key_list[1]))

    def load_privkey(self):
        key_list = input("Enter Private Key in the form: n, e, d, p, q\n").split(",")
        return rsa.PrivateKey(int(key_list[0]), int(key_list[1]), int(key_list[2]), int(key_list[3]), int(key_list[4]))

    def load_nonce(self):
        file = open("nonce.txt", "rb")
        return file.read()

    def parse_file_name(self):
        name_list = self.message_file.name.split("\\")
        name = name_list[-1]
        return name

    def encrypt(self):
        #  Generate AES key and cipher obj

        aes_key_pt = get_random_bytes(32)
        aes_cipher_obj = AES.new(aes_key_pt, AES.MODE_EAX)

        #  Stores nonce for decryption later
        nonce = aes_cipher_obj.nonce
        nonce_file = open("nonce.txt", "wb")
        nonce_file.write(nonce)
        nonce_file.close()

        #  Read in message and encrypt with AES
        msg_file = self.message_file
        msg = msg_file.read()
        msg_file.close()
        msg_ciphertext, tag = aes_cipher_obj.encrypt_and_digest(msg)

        #  write out encrypted file
        out_name = f"encrypted-{self.parse_file_name()}"
        file_out = open(out_name, "wb")
        file_out.write(msg_ciphertext)
        file_out.close()

        # encrypt aes key with rsa
        self.load_pubkey()
        print(self.pubkey)
        aes_key_ct = rsa.encrypt(aes_key_pt, self.pubkey)

        # write aeskey ciphertext
        file_out = open('aeskey.txt', 'wb')
        file_out.write(aes_key_ct)
        file_out.close()

        print(f"Encryption Successful. See '{out_name}'")
