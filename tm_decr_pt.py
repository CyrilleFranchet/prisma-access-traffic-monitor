#Created on Jan 18, 2023
#@author: zhanglin
import rsa 
import argparse
import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
import logging
import tm_common
def loadKeys():
    with open('keys/publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('keys/privateKey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey, publicKey
def aes_decrypt(cipher_text, key, iv, aes_mode=AES.MODE_CBC):
    try:
        iv = b64decode(iv)
        key = b64decode(key)
        cipher = AES.new(key, aes_mode, iv)
        plaintext = unpad(cipher.decrypt(cipher_text), AES.block_size)
        return plaintext
    except Exception as e:
        logging.error(f"aes_decrypt error: {e}")
        
        
def rsa_decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key)
    except Exception as e:
        print(f"decrypt error: {e}")
        return None
    
    
def tm_decrypt(data_file_path, key_file_path, private_key_path):
    # privateKey, publicKey = loadKeys()
    key = RSA.importKey(open(private_key_path).read())
    cipher = PKCS1_OAEP.new(key, hashAlgo = SHA256)
    
    key_file_content = tm_common.read_file_content(key_file_path) 
    decrypted_key_content = ""
    try:
        print("try loading random-key file as plaintext")
        _ = json.loads(key_file_content.decode('utf-8'))
        decrypted_key_content = key_file_content
    except Exception as e:
        print("try to decrypt random-key file")
        decrypted_key_content = cipher.decrypt(key_file_content).decode('utf-8')
    # decrypted_key_content = rsa_decrypt(key_file_content, privateKey).decode('utf-8')
    print(f"decrypted_key_content: {decrypted_key_content}")
    
    decrypted_result = json.loads(decrypted_key_content)
    data_content = tm_common.read_file_content(data_file_path)
    
    decrypted_data_content = aes_decrypt(data_content, decrypted_result['key'], decrypted_result['iv'])
    decrypted_data_file_path = data_file_path + '.dec'
    if data_file_path.endswith('.enc'):
        decrypted_data_file_path = data_file_path.rpartition('.')[0]
    tm_common.write_file(decrypted_data_file_path, decrypted_data_content)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("private_key_path", help="private_key_path")
    parser.add_argument("key_file_path", help="key_file_path")
    parser.add_argument("data_file_path", help="data_file_path")
    args = parser.parse_args()
    
    tm_decrypt(args.data_file_path, args.key_file_path, args.private_key_path)

if __name__ == '__main__':
    main()
