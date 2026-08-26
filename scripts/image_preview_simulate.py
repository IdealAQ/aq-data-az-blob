import argparse
from aqblob import config, setup_logging
import logging
from azure.storage.blob import BlobServiceClient, ContainerClient
from pathlib import Path
import time


def main():
    parser = argparse.ArgumentParser(
        description="Upload camera preview to Azure Storage."
    )
    parser.add_argument(
        "--directory",
        type=str,
        required=True,
        help="Directory containing images to upload",
    )
    parser.add_argument(
        "--interval",
        type=int,
        required=False,
        help="Interval in seconds used to rotate uploaded image.",
        default=10,
    )

    args = parser.parse_args()

    logging.info(args.directory)
    logging.info(args.interval)

    directory = Path(args.directory)

    if not directory.is_dir():
        logging.error(f"Directory {args.directory} does not exist!")

    CAMERA_IMG_SUFFIXES = {".jpg"}
    images = [f for f in directory.iterdir() if f.suffix in CAMERA_IMG_SUFFIXES]
    logging.info(f"loaded {len(images)} images in {args.directory}")

    az_storage_connection_string = config.AZ_STORAGE_CONNECTION_STRING
    az_storage_container_name = "camera"  # kept hardcoded for now

    blob_service_client = BlobServiceClient.from_connection_string(
        az_storage_connection_string
    )
    container_client = blob_service_client.get_container_client(
        az_storage_container_name
    )

    CAM1_PREVIEW_PATH = "preview/cam1.jpg"

    try:
        while True:
            for image in images:
                with open(image.resolve(), "rb") as data:
                    blob_client = container_client.get_blob_client(CAM1_PREVIEW_PATH)
                    blob_client.upload_blob(data, overwrite=True)
                print(f"uploaded {image.name} to {CAM1_PREVIEW_PATH} blob")
                print(f"sleeping {args.interval} seconds")
                time.sleep(args.interval)

    except KeyboardInterrupt:
        logging.info("Shutting down gracefully (Ctrl+C)")


if __name__ == "__main__":
    setup_logging(log_dir=config.LOG_DIRECTORY_PATH)
    main()
