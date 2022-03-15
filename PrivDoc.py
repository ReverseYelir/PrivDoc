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
import traceback

from time import sleep
import Encryptor
import Decryptor

def run_encryption(args):
    # encryption
    print(f"enc args {args}")
    absolute_path = args[1]
    enc = Encryptor.Encryptor(absolute_path)
    enc.encrypt()

def run_decryption(args):

    absolute_path = args[1]
    try:
        key_list = [args[2], args[3], args[4], args[5], args[6]]
    except IndexError:
        print("Invalid key. Need n, e, d, p, q")
        exit(1)
    dec = Decryptor.Decryptor(absolute_path, key_list)
    dec.decrypt()

def parse_args():
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

'''
return [absolute_path]
return [absolute_path, privatekey_string]
    privatekey_string: "n, e, d, p, q"
'''
def fetch_input():
    print("Absolute Path Ex: C:\\Users\\user\\input.txt\n")
    file_path = input("Enter Absolute Path for file to Encrypt or Decrypt: ").lstrip().rstrip()
    if not os.path.exists(file_path):
        print("File Not Found. Ex: C:\\Users\\user\\input.txt\nNote the slash direction")
        exit(1)

    mode = input("Do you want to Encrypt or Decrypt? (E/D)?").lower()
    if mode == 'e':
        return [file_path]
    elif mode == 'd':
        print("Gathering PrivateKey information for Decryption...\n")
        try:
            n = int(input("Enter n: "))
            e = int(input("Enter e: "))
            d = int(input("Enter d: "))
            p = int(input("Enter p: "))
            q = int(input("Enter q: "))
        except ValueError:
            print("Please enter valid integers for your private key.")
            exit(1)
        key_list= [n, e, d, p, q]
        return [file_path, key_list]


def main():
    # user_args = fetch_input()
    # if len(user_args) == 1:
    #     run_encryption(user_args)
    # elif len(user_args) == 2:
    #     try:
    #         run_decryption(user_args)
    #     except:
    #         traceback.print_ecx()
    # input()
    parse_args()


if __name__ == "__main__":
    main()
