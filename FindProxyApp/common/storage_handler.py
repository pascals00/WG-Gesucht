from azure.storage.blob import BlobServiceClient
from common.constants import *
import os
import logging


class StorageHandler:

    def __init__(self):
        self.connection_string = os.environ["AzureWebJobsStorage"]
        self.container_name = STORAGE_CONTAINER["CSV"]
        self.path_to_csv = PROXY_CSV_PATH

    def connect_to_storage_account(self):
        try:
            blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            return blob_service_client
        except Exception as e:
            logging.error(f"Failed to connect to storage account: {str(e)}")
            raise

    def store_csv_file(self, container_name, file_path, file_name):
        try:
            blob_service_client = self.connect_to_storage_account()
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
        except Exception as e:
            logging.error(f"Failed to store CSV file: {str(e)}")
            raise
    
    def get_csv_file(self, container_name, file_name):
        try:
            blob_service_client = self.connect_to_storage_account()
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
            blob =  blob_client.download_blob().readall()
        
            with open(self.path_to_csv, "wb") as data:
                data.write(blob)
        except Exception as e:
            logging.error(f"Failed to get CSV file: {str(e)}")
            raise