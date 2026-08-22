import os
import io
import time
import pandas as pd
import shutil
from tqdm import tqdm
from pathlib import Path
from azure.storage.blob import BlobServiceClient, ContainerClient
import logging
from pprint import pprint


logger = logging.getLogger(__name__)

# def _prepare_files(dir_source_path:str, dir_process_path:str, keep:int = 1):
#     with os.scandir(dir_source_path) as entries:
#         sorted_entries = sorted(entries, key=lambda e: e.name)
#         entries_to_process = sorted_entries[:-keep] if keep else sorted_entries[:]
        
#         for entry in entries_to_process:
#             if not entry.is_file():
#                 continue
#             shutil.move(entry.path, os.path.join(dir_process_path, entry.name))
#             logger.debug(f"Moved {entry.name} to {dir_process_path}.")

# def _export_file(entry:os.DirEntry[str], container_client:ContainerClient, device_id:str) -> bool:
#     name = entry.name

#     if len(name) < 12:
#         return False
    
#     file_date = name[:10]
#     file_name = name[11:]

#     if file_date.count("-") != 2:
#         return False
    
#     year, month, day = file_date.split("-")

#     blob_path = f"archive/device={device_id}/year={year}/month={month}/day={day}/{file_name[:-4]}.parquet"

#     buffer = io.BytesIO()
#     df = pd.read_csv(entry)
#     df["timestamp"] = pd.to_datetime(df["timestamp"])
#     df = df.set_index("timestamp")
#     df.to_parquet(buffer, engine="pyarrow")
#     buffer.seek(0)
    
#     try:
#         # with open(entry.path, "rb") as data:
#         container_client.upload_blob(name=blob_path, data=buffer, overwrite=True)
#     except Exception as e:
#         logger.error(f"❌ Failed to upload blob: {e}")
#         return False
    
#     return True

# def _export_files(
#         directory_path:str, 
#         directory_archive:str,
#         connection_string:str,
#         container_name:str,
#         device_id:str 
#         ):

#     blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#     container_client = blob_service_client.get_container_client(container_name)

#     succeeded = 0
#     failed = 0

#     with os.scandir(directory_path) as entries:
#         for entry in entries:
#             file_suffix_list = (".csv",)
#             if entry.is_file and not entry.name.startswith(".") and entry.name.endswith(file_suffix_list):
#                 if not _export_file(
#                     entry=entry, 
#                     container_client=container_client,
#                     device_id=device_id
#                 ):
#                     # move file to discard folder?
#                     logger.error(f"Error in exporting file {entry.name}")
#                     failed += 1
#                 else:
#                     logger.info(f"successful upload of {entry.name}")
#                     shutil.move(entry.path, os.path.join(directory_archive, entry.name))
#                     logger.debug(f"Moved {entry.name} to {directory_archive}.")
#                     succeeded += 1
#     return succeeded, failed

def _export_file(blob_path:str, file_path: Path):
    pass

def upload_files(
        source_dir_path:str, 
        staging_dir_path:str,
        az_storage_connection_string:str,
        az_storage_container_name:str,
        keep:int=1
    ) -> None:
    logger.info("Starting upload_files process... <--- <----")
    dir_to_process = f"{staging_dir_path}/to_process"
    dir_archive = f"{staging_dir_path}/archive"

    # staging directories
    os.makedirs(dir_to_process, exist_ok=True)
    os.makedirs(dir_archive, exist_ok=True)

    # paths
    source_path = Path(source_dir_path)
    process_path = Path(dir_to_process)
    archive_path = Path(dir_archive)
    
    # locate files in source directory
    files = [f for f in source_path.rglob("*") if f.is_file()]
    files_num = len(files)
    logger.debug(f"Found {files_num} files in source directory {source_dir_path}.")

    GROUP_LEVEL = 2 # campaign, source | date, hour (?), file.sample

    files_grouped = {}

    for file in files:
        parts = file.relative_to(source_path).parts
        group_key = "/".join(parts[:GROUP_LEVEL])
        files_grouped.setdefault(group_key, []).append(file)

    groups_num = len(files_grouped)

    for files in files_grouped.values():
        files.sort(key=lambda f: f.relative_to(source_path))

    files_to_process = [file for group_key, files in files_grouped.items() for file in (files[:-keep] if keep else files)]
    files_to_process_num = len(files_to_process)
    
    logger.info(f"Total files to process after keeping {keep} latest files in each of {groups_num} groups: {files_to_process_num} ({files_num} - {files_num - files_to_process_num})")

    with tqdm(
        total=files_to_process_num,
        unit="files",
        unit_scale=True,
        desc="Moving files"
    ) as progress:
        for file in files_to_process:
            dest_path = os.path.join(process_path, file.relative_to(source_path))
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.move(str(file), dest_path)
            progress.update(1)
            logger.debug(f"({progress.n}/{progress.total}) Moved {file} to {dest_path} .")

    # locate files in processing directory
    files_to_export = [f for f in process_path.rglob("*") if f.is_file()]
    files_to_export_num = len(files_to_export)

    PLATFORM_NAME = "test-platform-001"

    with tqdm(
        total=files_to_export_num,
        unit="files",
        unit_scale=True,
        desc="Uploading files"
    ) as progress:
        for file in files_to_export:
            relative_path = file.relative_to(process_path)
            blob_path = f"platform={PLATFORM_NAME}/{relative_path}"
            progress.update(1)
            time.sleep(1) # Simulate upload time


    return

    _prepare_files(
        dir_source_path = source_dir_path,
        dir_process_path = dir_to_process,
        keep = keep
    )

    succeeded, failed = _export_files(
        directory_path = dir_to_process,
        directory_archive = dir_archive,
        source=source_path,
        connection_string=az_storage_connection_string,
        container_name=az_storage_container_name
    )
    logger.info(f"Successfuly uploaded {succeeded} file(s), failed to upload {failed} file(s)  <--- <----")
