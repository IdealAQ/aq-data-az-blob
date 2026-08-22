import os
import io
import time
import pandas as pd
import shutil
from tqdm import tqdm
from pathlib import Path
from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.core.exceptions import AzureError
import logging

logger = logging.getLogger(__name__)


def _export_file(
    blob_path: str,
    file_path: Path,
    container_client: ContainerClient,
) -> bool:
    try:
        with file_path.open("rb") as data:
            container_client.upload_blob(
                name=blob_path,
                data=data,
                overwrite=True,
            )
    except (AzureError, OSError) as e:
        logger.error("Failed to upload %s: %s", file_path, e)
        return False
    return True

def upload_file() -> None:
    # TODO: Implement the upload_file function to handle single file uploads if needed.
    pass

def upload_files(
    source_dir_path: str,
    staging_dir_path: str,
    platform_name: str,
    az_storage_connection_string: str,
    az_storage_container_name: str,
    keep: int = 1,
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

    GROUP_LEVEL = 2  # campaign, source | date, hour (?), file.sample

    files_grouped = {}

    for file in files:
        parts = file.relative_to(source_path).parts
        group_key = "/".join(parts[:GROUP_LEVEL])
        files_grouped.setdefault(group_key, []).append(file)

    groups_num = len(files_grouped)

    for files in files_grouped.values():
        files.sort(key=lambda f: f.relative_to(source_path))

    files_to_process = [
        file
        for group_key, files in files_grouped.items()
        for file in (files[:-keep] if keep else files)
    ]
    files_to_process_num = len(files_to_process)

    logger.info(
        f"Total files to process after keeping {keep} latest files in each of {groups_num} groups: {files_to_process_num} ({files_num} - {files_num - files_to_process_num})"
    )

    with tqdm(
        total=files_to_process_num, unit="files", unit_scale=False, desc="Moving files"
    ) as progress:
        for file in files_to_process:
            dest_path = os.path.join(process_path, file.relative_to(source_path))
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.move(str(file), dest_path)
            progress.update(1)
            logger.debug(
                f"({progress.n}/{progress.total}) Moved {file} to {dest_path} ."
            )

    # locate files in processing directory
    files_to_export = [f for f in process_path.rglob("*") if f.is_file()]
    files_to_export_num = len(files_to_export)

    success_count = 0
    failure_count = 0

    with (
        BlobServiceClient.from_connection_string(
            az_storage_connection_string
        ) as blob_service_client,
        tqdm(
            total=files_to_export_num,
            unit="files",
            unit_scale=False,
            desc="Uploading files",
        ) as progress,
    ):
        container_client = blob_service_client.get_container_client(
            az_storage_container_name
        )
        for file in files_to_export:
            relative_path = file.relative_to(process_path)
            blob_path = f"platform={platform_name}/{relative_path}"

            if _export_file(
                blob_path=blob_path, file_path=file, container_client=container_client
            ):  
                dest_path = os.path.join(archive_path, relative_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.move(str(file), dest_path)
                success_count += 1
            else:
                failure_count += 1

            progress.update(1)

    logger.info(
        f"Successfuly uploaded {success_count} file(s), failed to upload {failure_count} file(s)"
    )