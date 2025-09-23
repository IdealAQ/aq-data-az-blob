from aqblob import upload_files, config, setup_logging

def main():
    upload_files(
        source_dir_path = config.SOURCE_DIR_PATH,
        staging_dir_path = config.STAGING_DIR_PATH,
        device_id = config.DEVICE_ID,
        az_storage_connection_string = config.AZ_STORAGE_CONNECTION_STRING,
        az_storage_container_name = config.AZ_STORAGE_CONTAINER_NAME
    )

if __name__ == "__main__":
    setup_logging(log_dir=config.LOG_DIRECTORY_PATH)
    main()
