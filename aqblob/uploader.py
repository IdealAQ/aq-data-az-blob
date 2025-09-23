import os
import io
import pandas as pd
import shutil
from azure.storage.blob import BlobServiceClient, ContainerClient
import logging

logger = logging.getLogger(__name__)

def _prepare_files(source_path:str, dir_to_process:str):
    with os.scandir(source_path) as entries:
        keep = -1 #keep one most recent file
        sorted_entries = sorted(entries, key=lambda e: e.name)
        entries_to_process = sorted_entries[:keep]
        
        for entry in entries_to_process:
            if not entry.is_file():
                continue
            shutil.move(entry.path, os.path.join(dir_to_process, entry.name))
            logger.debug(f"Moved {entry.name} to {dir_to_process}.")

def _export_file(entry:os.DirEntry[str], container_client:ContainerClient, device_id:str) -> bool:
    name = entry.name

    if len(name) < 12:
        return False
    
    file_date = name[:10]
    file_name = name[11:]

    if file_date.count("-") != 2:
        return False
    
    year, month, day = file_date.split("-")

    blob_path = f"aq-data/device_id={device_id}/year={year}/month={month}/day={day}/{file_name[:-4]}.parquet"

    buffer = io.BytesIO()
    df = pd.read_csv(entry)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")
    df.to_parquet(buffer, engine="pyarrow")
    buffer.seek(0)
    
    try:
        # with open(entry.path, "rb") as data:
        container_client.upload_blob(name=blob_path, data=buffer, overwrite=True)
    except Exception as e:
        logger.error(f"❌ Failed to upload blob: {e}")
        return False
    
    return True

def _export_files(
        directory_path:str, 
        directory_archive:str,
        connection_string:str,
        container_name:str,
        device_id:str 
        ):

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    succeeded = 0
    failed = 0

    with os.scandir(directory_path) as entries:
        for entry in entries:
            if entry.is_file and not entry.name.startswith(".") and entry.name.endswith(".csv"):
                if not _export_file(
                    entry=entry, 
                    container_client=container_client,
                    device_id=device_id
                ):
                    # move file to discard folder?
                    logger.error(f"Error in exporting file {entry.name}")
                    failed += 1
                else:
                    logger.info(f"successful upload of {entry.name}")
                    shutil.move(entry.path, os.path.join(directory_archive, entry.name))
                    logger.debug(f"Moved {entry.name} to {directory_archive}.")
                    succeeded += 1
    return succeeded, failed

def upload_files(
        source_dir_path:str, 
        staging_dir_path:str,
        device_id:str,
        az_storage_connection_string:str,
        az_storage_container_name:str
    ) -> None:
    logger.info("Starting upload_files process... <--- <----")
    dir_to_process = f"{staging_dir_path}/to_process"
    dir_archive = f"{staging_dir_path}/archive"

    os.makedirs(dir_to_process, exist_ok=True)
    os.makedirs(dir_archive, exist_ok=True)

    _prepare_files(
        source_path = source_dir_path,
        dir_to_process = dir_to_process
    )

    succeeded, failed = _export_files(
        directory_path = dir_to_process,
        directory_archive = dir_archive,
        device_id=device_id,
        connection_string=az_storage_connection_string,
        container_name=az_storage_container_name
    )
    logger.info(f"Successfuly uploaded {succeeded} file(s), failed to upload {failed} file(s)  <--- <----")


    