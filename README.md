# CSV to Blob export
This script scans specified directory for *.csv files and exports them as *.parquet files to Azure Storage.

## Prerequisites
Files must be saved in a single directory named accordingly: `<datetime>_<fixed_digit_increment>.csv`.

`<datetime>` is in `YYYY-MM-DD` (ISO 8601) format.

Example: `2025-11-25_00321.csv`. 
Leading zeroes in `<fixed_digit_increment>` part ensure the files sorted by name are ordered from the oldest to the newest ones. The `<fixed_digit_increment>` part can be the second of the day the file is created, ranging from `00000` to `86400` (**recommended**).

## Installation
### ENV variables
The following Environmental variables must be set. Setting them in .env file located in the [/src](./src/) directory is possible.

| ENV variable | description | exmple |
| -------------|-------------|--------|
|AQ_AZ_SOURCE_FILE_DIRECTORY_PATH|path to the directory with csv files|/Users/rohal/projects/aq/local/aq-gateway/measurements|
|AQ_AZ_STAGING_DIRECTORY_PATH|path to the directory used by the script for file manipulation and local archiving|/Users/rohal/projects/aq/local/aq-data-az-blob/staging|
|AQ_AZ_STORAGE_CONNECTION_STRING|connection string from azure storage account|never_ever_share_this|
|AQ_AZ_STORAGE_CONTAINER_NAME|azure storage container name||
|AQ_DEVICE_ID|device id|test|
|AQ_AES_KEY|||

### Virtual environment
Use [uv](https://docs.astral.sh/uv/) to create virtual environment, install necessary packages and run the script.

install UV
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

download and install dependencies
```bash
uv sync
```

run the script
> **NOTE:** run as a module (use `-m` flag)
```bash
uv run python -m scripts.upload_files
```

### CRON
It is recommended to trigger the script regularily with [cron](https://en.wikipedia.org/wiki/Cron).
