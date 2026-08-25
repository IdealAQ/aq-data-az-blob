import argparse
from aqblob import download_files, config, setup_logging

def main():
    parser = argparse.ArgumentParser(description="Downloads files from Azure Storage by prefix.")

    parser.add_argument(
        "-p", "--prefix",
        type = str,             
        required = True,        
        help = "Prefix to filter files for download.",
    )

    parser.add_argument(
        "-c", "--container",
        type = str,
        required = False,
        default = config.AZ_STORAGE_CONTAINER_NAME,
        help = "Azure Storage container name (default: from config).",
    )

    args = parser.parse_args()

    prefix = args.prefix
    download_files(
        downloaded_dir_path = config.DOWNLOADED_DIR_PATH,
        prefix=prefix,
        suffixes=config.FILE_SUFFIXES,
        az_storage_connection_string = config.AZ_STORAGE_CONNECTION_STRING,
        az_storage_container_name = args.container
    )


if __name__ == "__main__":
    setup_logging(log_dir=config.LOG_DIRECTORY_PATH)
    main()