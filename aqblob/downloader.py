from pathlib import Path
from tqdm import tqdm
from azure.storage.blob import ContainerClient
import logging

logger = logging.getLogger(__name__)


def list_local_files(
    directory_path: str,
    prefix: str,
    suffixes: tuple[str],
) -> list[str]:
    """
    Lists local files in a directory that match the given prefix and suffixes.

    Args:
        directory_path (str): The path to the local directory.
        prefix (str): The prefix to filter files.
        suffixes (tuple[str]): A tuple of allowed file suffixes.

    Returns:
        list[str]: A list of matching file paths.
    """
    source_path = Path(directory_path)
    source_path_prefix = source_path / prefix
    if not source_path_prefix.exists():
        logger.warning(f"Directory {source_path_prefix} does not exist.")
        return []
    files = [
        str(f.relative_to(source_path))
        for f in source_path_prefix.rglob("*")
        if f.is_file() and any(str(f).endswith(suffix) for suffix in suffixes)
    ]

    return files


def download_files(
    container_client: ContainerClient,
    downloaded_dir_path: str,
    prefix: str,
    suffixes: tuple[str],
    skip_existing: bool = True,
) -> None:
    allowed_suffixes = tuple(suffixes)
    logging.getLogger("azure").setLevel(logging.WARNING)
    logger.info("Starting download_files process...")
    logger.info(f"Downloading files with prefix: {prefix}")

    blobs_all = container_client.list_blobs(name_starts_with=prefix)
    blobs_all = [blob for blob in blobs_all if blob.name.endswith(allowed_suffixes)]
    blobs = blobs_all

    if skip_existing:
        existing_files = list_local_files(
            directory_path=downloaded_dir_path,
            prefix=prefix,
            suffixes=allowed_suffixes,
        )
        existing_files_set = set(existing_files)
        blobs = [blob for blob in blobs_all if blob.name not in existing_files_set]

    if not blobs:
        logger.info("No new blobs found to download.")
        return

    logger.info(
        f"Found {len(blobs)} blobs to download. Skipping {len(blobs_all) - len(blobs)} existing files."
    )

    for blob in tqdm(
        blobs,
        desc="Downloading files",
        unit="file",
    ):
        try:
            # Preserve the complete blob path.
            local_file_path = Path(downloaded_dir_path) / Path(blob.name)

            # Create parent directories.
            local_file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            blob_client = container_client.get_blob_client(blob.name)

            with local_file_path.open("wb") as file:
                file.write(blob_client.download_blob().readall())

            logger.debug(f"Downloaded blob: {blob.name}")

        except Exception:
            logger.exception(f"Failed to download blob: {blob.name}")
