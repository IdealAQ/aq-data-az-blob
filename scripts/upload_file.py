import argparse
from aqblob import upload_file, config, setup_logging


def main():
    parser = argparse.ArgumentParser(description="Upload file to Azure Storage.")

    parser.add_argument(
        "-bp",
        "--blob-path",
        type=str,
        required=True,
        help="Path for the blob in Azure Storage.",
    )
    parser.add_argument(
        "-fp",
        "--file-path",
        type=str,
        required=True,
        help="Path to the file to upload.",
    )

    args = parser.parse_args()

    raise NotImplementedError

    upload_file(
        file_path=args.file_path,
        blob_path=args.blob_path,
        az_storage_connection_string=config.AZ_STORAGE_CONNECTION_STRING,
        az_storage_container_name=config.AZ_STORAGE_CONTAINER_NAME,
    )


if __name__ == "__main__":
    setup_logging(log_dir=config.LOG_DIRECTORY_PATH)
    main()
