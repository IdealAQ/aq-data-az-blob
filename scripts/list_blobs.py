import argparse
from aqblob import list_blobs, config, setup_logging
from pprint import pprint
from azure.storage.blob import BlobServiceClient


def parse_args():
    parser = argparse.ArgumentParser(
        description="Lists files in Azure Storage by prefix."
    )
    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        required=True,
        help="Prefix to filter files for listing.",
    )
    parser.add_argument(
        "-c",
        "--container",
        type=str,
        required=False,
        default=config.AZ_STORAGE_CONTAINER_NAME,
        help="Azure Storage container name (default: from config).",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    blobs = []

    with BlobServiceClient.from_connection_string(
        config.AZ_STORAGE_CONNECTION_STRING
    ) as blob_service_client:
        container_client = blob_service_client.get_container_client(args.container)
        blobs = list_blobs(
            container_client=container_client,
            prefix=args.prefix,
        )

    pprint(f"Blobs with prefix '{args.prefix}':")
    pprint(blobs)


if __name__ == "__main__":
    setup_logging(log_dir=config.LOG_DIRECTORY_PATH)
    main()
