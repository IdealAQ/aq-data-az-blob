from azure.storage.blob import BlobServiceClient, ContainerClient
from dotenv import load_dotenv
import os
import shutil
import io
import pandas as pd

ENV_SOURCE_PATH="AQ_AZ_SOURCE_FILE_DIRECTORY_PATH"
ENV_STAGING_PATH="AQ_AZ_STAGING_DIRECTORY_PATH"
ENV_AZ_STORAGE_CONNECTION_STRING="AQ_AZ_STORAGE_CONNECTION_STRING"
ENV_AZ_STORAGE_CONTAINER_NAME="AQ_AZ_STORAGE_CONTAINER_NAME"
ENV_DEVICE_ID="AQ_DEVICE_ID"
ENV_AES_KEY="AQ_AES_KEY"

def prepare_files(source_path:str, dir_to_process:str):
    with os.scandir(source_path) as entries:
        keep = -1 #keep one most recent file
        sorted_entries = sorted(entries, key=lambda e: e.name)
        entries_to_process = sorted_entries[:keep]
        
        for entry in entries_to_process:
            if not entry.is_file():
                continue
            shutil.move(entry.path, os.path.join(dir_to_process, entry.name))
            print(f"Moved {entry.name} to {dir_to_process}.")

def _explort_file(entry:os.DirEntry[str], container_client:ContainerClient) -> bool:
    device_id = os.getenv(ENV_DEVICE_ID)
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
        with open(entry.path, "rb") as data:
            container_client.upload_blob(name=blob_path, data=buffer, overwrite=True)
    except Exception as e:
        print(f"❌ Failed to upload blob: {e}")
        return False
    
    return True

    
def export_files(directory_path:str, directory_archive:str, directory_discard_path:str):
    connection_string= os.getenv(ENV_AZ_STORAGE_CONNECTION_STRING)
    container_name = os.getenv(ENV_AZ_STORAGE_CONTAINER_NAME)

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    with os.scandir(directory_path) as entries:
        for entry in entries:
            if entry.is_file and not entry.name.startswith(".") and entry.name.endswith(".csv"):
                if not _explort_file(entry, container_client):
                    # move file to discard folder?
                    print("some error")
                else:
                    print(f"successful upload of {entry.name}")
                    shutil.move(entry.path, os.path.join(directory_archive, entry.name))
                    print(f"Moved {entry.name} to {directory_archive}.")

def main():
    load_dotenv()
    source_path = os.getenv(ENV_SOURCE_PATH)
    staging_path = os.getenv(ENV_STAGING_PATH)
    dir_to_process = f"{staging_path}/to_process"
    dir_archive = f"{staging_path}/archive"
    dir_discarded = f"{staging_path}/discarded"

    os.makedirs(dir_to_process, exist_ok=True)
    os.makedirs(dir_archive, exist_ok=True)
    os.makedirs(dir_discarded, exist_ok=True)

    prepare_files(
        source_path = source_path,
        dir_to_process = dir_to_process
    )

    export_files(
        directory_path = dir_to_process,
        directory_archive = dir_archive,
        directory_discard_path = dir_discarded
    )

if __name__ == "__main__":
    main()
