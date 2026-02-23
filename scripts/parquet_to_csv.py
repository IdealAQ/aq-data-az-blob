import argparse
import pandas as pd
from aqblob import config, setup_logging
import logging


def main():
    parser = argparse.ArgumentParser(description="Convert Parquet file to CSV.")

    parser.add_argument(
        "-f", "--file_name",
        type = str,             
        required = True,        
        help = "Name of parquet file in DOWNLOADED_DIR_PATH directory.",
    )

    parser.add_argument(
        "-o", "--output",
        type = str,             
        required = True,        
        help = "Path to the output CSV file.",
    )

    args = parser.parse_args()

    input_path = f"{config.DOWNLOADED_DIR_PATH}/{args.file_name}"


    # Read parquet file
    df = pd.read_parquet(input_path, engine="pyarrow")

    # Write to CSV
    df.to_csv(args.output, index=True)

    logging.info("Conversion complete!")

if __name__ == "__main__":
    setup_logging(log_dir=config.LOG_DIRECTORY_PATH)
    main()