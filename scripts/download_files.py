import argparse
from aqblob import download_files, config, setup_logging

def main():
    parser = argparse.ArgumentParser(description="Downloads files from Azure Storage.")

    parser.add_argument(
        "--id",
        type = str,             
        required = True,        
        help = "Device identifier to filter files for download.",
    )

    parser.add_argument(
        "--year",
        type = int,             
        required = True,        
        help = "Year to filter files for download.",
    )

    parser.add_argument(
        "--month",
        type = int,             
        required = True,        
        help = "Month to filter files for download.",
    )

    parser.add_argument(
        "--day",
        type = int,             
        required = True,        
        help = "Day to filter files for downloading.",
    )

    # aq-data/device_id=test-001/year=2025/month=12/day=08/51778.parquet


    args = parser.parse_args()

    prefix = f"aq-data/device_id={args.id}/year={args.year}/month={args.month:02}/day={args.day:02}/"
    download_files(
        downloaded_dir_path = config.DOWNLOADED_DIR_PATH,
        prefix=prefix,
        az_storage_connection_string = config.AZ_STORAGE_CONNECTION_STRING,
        az_storage_container_name = config.AZ_STORAGE_CONTAINER_NAME
    )


if __name__ == "__main__":
    setup_logging(log_dir=config.LOG_DIRECTORY_PATH)
    main()