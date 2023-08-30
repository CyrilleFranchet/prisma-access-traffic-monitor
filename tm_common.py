#Created on Dec 22, 2022
#@author: zhanglin

import logging 
from google.cloud import storage
from google.oauth2 import service_account
import os 


def read_file_content(file_path):
    try:
        f = open(file_path, 'rb')
        file_content = f.read()
        f.close()
        return file_content
    except Exception as e:
        logging.error(f"read_file_content error: {file_path} {e}")
    
    
def write_file(file_path, file_content):
    try:
        f = open(file_path, 'wb')
        f.write(file_content)
        f.close()
    except Exception as e:
        logging.error(f"write_file error: {file_path} {e}")
    
    
def upload_file_to_gcs(bucket_name, file_path, local_file_path, key_path):
    try:
        credentials = service_account.Credentials.from_service_account_file(key_path)
        storage_client = storage.Client(credentials = credentials)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        f = open(local_file_path, 'rb')
        file_content = f.read()
        f.close()
        blob.upload_from_string(file_content)
        return True
    except Exception as e:
        logging.error(f"upload_file_to_gcs error: {e}", exc_info=True)
        return False


def download_file_from_gcs(bucket_name, file_path, local_file_path, key_path):
    try:
        credentials = service_account.Credentials.from_service_account_file(key_path)
        storage_client = storage.Client(credentials = credentials)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        with open(local_file_path, 'wb') as f:
            storage_client.download_blob_to_file(blob, f)
        return True
    except Exception as e:
        logging.error(f"download_file_from_gcs error: {e}", exc_info=True)
        return False


def sync_gcs_folder_to_local(bucket_name, folder_path, local_folder_path, key_path):
    try:
        logging.info(f"sync {bucket_name}:{folder_path} to {local_folder_path}")
        if not os.path.exists(local_folder_path):
            os.makedirs(local_folder_path)
        #only support one level
        local_files = os.listdir(local_folder_path)
        
        credentials = service_account.Credentials.from_service_account_file(key_path)
        storage_client = storage.Client(credentials = credentials)
        bucket = storage_client.bucket(bucket_name)
        folder_path = folder_path.rstrip("/")
        blobs = bucket.list_blobs(prefix=folder_path)
        remote_files = [os.path.relpath(blob.name, folder_path) for blob in blobs if len(blob.name) > len(folder_path) + 1]
        
        files_to_delete = [file_name for file_name in local_files if file_name not in remote_files]
        logging.info(f"remove local files: {files_to_delete}")
        for file_name in files_to_delete:
            file_path = os.path.join(local_folder_path, file_name)
            os.remove(file_path)
        
        files_to_download = [file_name for file_name in remote_files if file_name not in local_files]
        logging.info(f"download remote files: {files_to_download}")
        for file_name in files_to_download:
            local_file_path = os.path.join(local_folder_path, file_name)
            remote_file_path = os.path.join(folder_path, file_name)
            download_file_from_gcs(bucket_name, remote_file_path, local_file_path, key_path)
        return True
    except Exception as e:
        logging.error(f"sync_gcs_folder_to_local error: {e}", exc_info=True)
        return False


def main():
    logging.basicConfig(filename="traffic-mirroring-common.log", level=logging.DEBUG, format='%(asctime)s %(process)d.%(thread)d %(levelname)s:%(message)s')
    # upload_file_to_gcs("zhe-test-sharing-bucket", "test_1229.pcap", "raw_data/tls.pcap", "bucket.json")
    sync_gcs_folder_to_local("zhe-test-private-bucket", "ssl_keys", "ssl_keys", "bucket.json")
    sync_gcs_folder_to_local("zhe-test-private-bucket", "ipsec_keys", "ipsec_keys", "bucket.json")

if __name__ == '__main__':
    main()