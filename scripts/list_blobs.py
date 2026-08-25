import argparse
from aqblob import list_blobs, config, setup_logging
from pprint import pprint

def parse_args():
    parser = argparse.ArgumentParser(description="Lists files in Azure Storage by prefix.")
    parser.add_argument(
        "-p", "--prefix",
        type=str,
        required=True,
        help="Prefix to filter files for listing."
    )
    parser.add_argument(
        "-c", "--container",
        type=str,
        required=False,
        default=config.AZ_STORAGE_CONTAINER_NAME,
        help="Azure Storage container name (default: from config)."
    )
    
    return parser.parse_args()

def main():
    args = parse_args()

    blobs = list_blobs(
        prefix=args.prefix,
        az_storage_connection_string=config.AZ_STORAGE_CONNECTION_STRING,
        az_storage_container_name=args.container
    )

    pprint(f"Blobs with prefix '{args.prefix}':")
    pprint(blobs)


if __name__ == "__main__":
    setup_logging(log_dir=config.LOG_DIRECTORY_PATH)
    main()