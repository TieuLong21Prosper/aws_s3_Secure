
import euclid
import mail
from configparser import ConfigParser
import secrets
from Cryptodome.Cipher import AES
from Cryptodome import Random
import stego

def mainMenu():
    print("\n |-----------------------------[COLLOSUS PROGRAME]----------------------------------| *")    
    print(" |--------------------------------> welcome <---------------------------------------| *")

    print("[*] Starting encrypt and decrypt a message using AES and RSA algorithm")
    print("[*] Processing generated keys ...")

    #configur = ConfigParser()
    #configur.read('configurations.ini')
    #location = configur.get('SMTPlogin', 'file_location')

    # Obtains public key.
    print("[*] ------------------------------------------------------------- [*]")
    print("[*] RSA public and Privite keys ....")
    pub,pri=euclid.KeyGeneration()

    # Generates a fresh symmetric key for the data encapsulation scheme.
    print("[*] Genering AES symmetric key ....")
    key = secrets.token_hex(16)
    KeyAES=key.encode('utf-8')

    # Encrypts the message under the data encapsulation scheme, using the symmetric key just generated.
    plainText = input("\n-> Enter the message: ")
    cipherAESe = AES.new(KeyAES,AES.MODE_GCM)
    nonce = cipherAESe.nonce

    print("[*] Encrypting the message with AES......")
    cipherText=euclid.encryptAES(cipherAESe,plainText)
    print("\n")
    src = input(r"-> Enter image source: ")
    stego.Encode(src, cipherText, src)
    print("[*] -------------------------------------------------------------- [*] ")
    print("[*] Successfully encrypted and hidden the text in picture......")
    print("[*] Encrypted key chars:")
    # Encrypt the symmetric key under the key encapsulation scheme, using Alice’s public key.
    cipherKey=euclid.encrypt(pub,key)
    print("[*] Encrypting the AES symmetric key with RSA......")

    # sending mail
    mail.mail(pri, cipherKey, nonce, src)
