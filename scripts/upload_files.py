import argparse
from aqblob import upload_files, config, setup_logging
from pathlib import Path
from azure.storage.blob import BlobServiceClient


def main():
    parser = argparse.ArgumentParser(description="Upload files to Azure Storage.")

    parser.add_argument(
        "-k",
        "--keep",
        type=int,
        required=False,
        help="Number of latest files to ignore (default: -1 for the latest file - being written into).",
        default=1,
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        required=False,
        help="Limit the number of files per directory to upload (default: 1000).",
        default=1000,
    )
    parser.add_argument(
        "-b",
        "--batch_lvl",
        type=int,
        required=False,
        help="Path batch level.",
        default=3
    )

    args = parser.parse_args()

    with BlobServiceClient.from_connection_string(
        config.AZ_STORAGE_CONNECTION_STRING,
        connection_timeout=600,
        max_block_size=1024 * 1024,  # 1 MiB
        max_single_put_size=1024 * 1024,  # force block upload for >1 MiB
    ) as blob_service_client:
        container_client = blob_service_client.get_container_client(
            az_storage_container_name=config.AZ_STORAGE_CONTAINER_NAME
        )
        upload_files(
            container_client=container_client,
            source_dir_path=Path(config.SOURCE_DIR_PATH),
            staging_dir_path=Path(config.STAGING_DIR_PATH),
            suffixes=config.FILE_SUFFIXES,
            keep=args.keep,
            limit=args.limit,
            batch_lvl=args.batch_lvl
        )


if __name__ == "__main__":
    setup_logging(log_dir=config.LOG_DIRECTORY_PATH)
    main()
