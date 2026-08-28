import argparse
from aqblob import download_files, config, setup_logging
from azure.storage.blob import BlobServiceClient
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Downloads files from Azure Storage by prefix."
    )

    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        required=True,
        help="Prefix to filter files for download.",
    )

    parser.add_argument(
        "-c",
        "--container",
        type=str,
        required=False,
        default=config.AZ_STORAGE_CONTAINER_NAME,
        help="Azure Storage container name (default: from config).",
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite existing files locally.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    with BlobServiceClient.from_connection_string(
        config.AZ_STORAGE_CONNECTION_STRING
    ) as blob_service_client:
        container_client = blob_service_client.get_container_client(args.container)
        download_files(
            container_client=container_client,
            downloaded_dir_path=Path(config.DOWNLOADED_DIR_PATH),
            prefix=args.prefix,
            suffixes=config.FILE_SUFFIXES,
            skip_existing=not args.force,
        )


if __name__ == "__main__":
    setup_logging(log_dir=config.LOG_DIRECTORY_PATH)
    main()
