import os
from pathlib import Path
from tqdm import tqdm
from azure.storage.blob import BlobServiceClient
import logging

logger = logging.getLogger(__name__)

def download_files(
    downloaded_dir_path: str,
    prefix: str,
    suffixes: tuple[str],
    az_storage_connection_string: str,
    az_storage_container_name: str,
) -> None:
    allowed_suffixes = tuple(suffixes)
    logging.getLogger("azure").setLevel(logging.WARNING)
    logger.info("Starting download_files process...")
    logger.info(f"Downloading files with prefix: {prefix}")

    with BlobServiceClient.from_connection_string(
        az_storage_connection_string
    ) as blob_service_client:

        container_client = blob_service_client.get_container_client(
            az_storage_container_name
        )

        blobs = container_client.list_blobs(name_starts_with=prefix)
        blobs = [blob for blob in blobs if blob.name.endswith(allowed_suffixes)]

        for blob in tqdm(
            blobs,
            desc="Downloading files",
            unit="file",
        ):
            try:
                # Preserve the complete blob path.
                local_file_path = (
                    Path(downloaded_dir_path)
                    / Path(blob.name)
                )

                # Create parent directories.
                local_file_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                blob_client = container_client.get_blob_client(blob.name)

                with local_file_path.open("wb") as file:
                    file.write(
                        blob_client.download_blob().readall()
                    )

                logger.debug(f"Downloaded blob: {blob.name}")

            except Exception:
                logger.exception(
                    f"Failed to download blob: {blob.name}"
                )
