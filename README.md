# Prisma Access Traffic Replication
Scripts for Decoding Prisma Access Traffic Replication PCAP Files

Each PCAP file is inside a ZIP file with an encrypted JSON file. This JSON file can be decrypted using the RSA private
key. After decryption, the JSON file exposes the AES GCM tag, nonce and key. These parameters can be used to decrypt the
PCAP file.

usage: tm_decr_pt.py [-h] -k PRIVATE_KEY_PATH -j KEY_FILE_PATH -p DATA_FILE_PATH

options:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-h, --help  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;show this help message and exit  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-k, --private-key PRIVATE_KEY_PATH  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The RSA private key  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-j, --json-file KEY_FILE_PATH  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The encrypted JSON file  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-p, --pcap-file DATA_FILE_PATH  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The PCAP file to decrypt  
