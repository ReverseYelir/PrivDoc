'''
Program encrypts/decrypts files. This is a command line tool.

Encryption requires a file name and pubkey.txt:
    If pubkey.txt does not exist, a new keypair is generated and
    the new privatekey is displayed to the user. Key in the file
    in the form: n, e

Decryption requires these files to exist:
    (created by the end of encryption)
    nonce.txt
    aeskey.txt
    pubkey.txt
    (provided by user)
    file name to decrypt

Usage:
    Encryption: python main.py -enc file_path
    Decryption: python main.py -dec file_path privkey_string
        privkey_string form: "n, e, d, p, q"

-mode:
    -enc: Flag notifying you want to ENCRYPT the file
    -dec: Flag notifying you want to DECRYPT the file
'''
import sys, os

import Encryptor
import Decryptor

def run_encryption(args):
    print(args)
    # encryption
    absolute_path = args[1]
    enc = Encryptor.Encryptor(absolute_path)
    enc.encrypt()

def run_decryption(args):
    absolute_path = args[1]
    dec = Decryptor.Decryptor(absolute_path)
    dec.decrypt()

'''
return [absolute_path]
return [absolute_path, privatekey_string]
    privatekey_string: "n, e, d, p, q"
'''



def main():
    args = sys.argv
    print(args)
    cmd_str = args[1].rstrip(" ").lstrip(" ")
    args = cmd_str.split(" ")
    if "-enc".lower() in cmd_str:
        run_encryption(args)
    elif "-dec".lower() in cmd_str:
        run_decryption(args)
    else:
        print("User error or need to ask for input directly")
        exit(1)


if __name__ == "__main__":
    main()
