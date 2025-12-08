import logging
import os
from azure.storage.blob import BlobServiceClient

logger = logging.getLogger(__name__)


def download_files(
        downloaded_dir_path:str, 
        prefix:str,
        az_storage_connection_string:str,
        az_storage_container_name:str
    ) -> None:
    logger.info("Starting download_files process... <--- <----")
    logger.info(f"Downloading files with prefix: {prefix}")
    blob_service_client = BlobServiceClient.from_connection_string(az_storage_connection_string)
    container_client = blob_service_client.get_container_client(az_storage_container_name)

    for blob in container_client.list_blobs(name_starts_with=prefix):
        blob_client = container_client.get_blob_client(blob.name)
        local_file_path = os.path.join(downloaded_dir_path, blob.name.replace("/", "_"))
        with open(local_file_path, "wb") as file:
            file.write(blob_client.download_blob().readall())
        logging.info(f"Downloaded blob: {blob.name}")