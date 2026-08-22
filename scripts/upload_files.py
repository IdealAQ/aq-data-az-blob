import argparse
from aqblob import upload_files, config, setup_logging

def main():
    parser = argparse.ArgumentParser(description="Upload files to Azure Storage.")

    parser.add_argument(
        "-k", "--keep",
        type = int,             
        required = False,        
        help = "Number of latest files to ignore (default: -1 for the latest file - being written into).",
        default = 1
    )

    args = parser.parse_args()

    upload_files(
        source_dir_path = config.SOURCE_DIR_PATH,
        staging_dir_path = config.STAGING_DIR_PATH,
        az_storage_connection_string = config.AZ_STORAGE_CONNECTION_STRING,
        az_storage_container_name = config.AZ_STORAGE_CONTAINER_NAME,
        keep = args.keep
    )

if __name__ == "__main__":
    setup_logging(log_dir=config.LOG_DIRECTORY_PATH)
    main()
