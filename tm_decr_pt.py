#Created on October 18, 2024
#@author: zhanglin

import argparse
import json
from base64 import b64decode

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def tr_decrypt(data_file_path, key_file_path, private_key_path):
    with open(private_key_path, 'rb') as private_key_file:
        private_key = serialization.load_pem_private_key(private_key_file.read(),
                                                         password=None,
                                                         backend=default_backend()
        )

    with open(key_file_path, 'rb') as json_file:
        json_file_content = json_file.read()

    try:
        print("Try loading JSON file as plaintext")
        _ = json.loads(json_file_content.decode('utf-8'))
        decrypted_key_content = json_file_content
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Try to decrypt JSON file")
        decrypted_key_content = private_key.decrypt(json_file_content,
                                                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                 algorithm=hashes.SHA256(),
                                                                 label=None
                                                                 )
                                                    )

    print(f"decrypted_key_content: {decrypted_key_content}")
    
    aes_parameters = json.loads(decrypted_key_content)
    key = b64decode(aes_parameters['key'])
    tag = b64decode(aes_parameters['tag'])
    nonce = b64decode(aes_parameters['nonce'])
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    chunk_size = 4096
    pcap_file_path = data_file_path.removesuffix('.enc')
    with open(data_file_path, 'rb') as f_in:
        with open(pcap_file_path, 'wb') as f_out:
            while True:
                chunk = f_in.read(chunk_size)
                if len(chunk) == 0:
                    break
                decrypted_chunk = decryptor.update(chunk)
                f_out.write(decrypted_chunk)
            f_out.write(decryptor.finalize())
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--private-key', required=True, dest='private_key_path', help="The RSA private key")
    parser.add_argument('-j', '--json-file', required=True, dest='key_file_path', help="The encrypted JSON file")
    parser.add_argument('-p', '--pcap-file', required=True, dest='data_file_path', help="The PCAP file to decrypt")
    args = parser.parse_args()
    
    tr_decrypt(args.data_file_path, args.key_file_path, args.private_key_path)

if __name__ == '__main__':
    main()
