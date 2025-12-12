# CSV to Blob export
This script scans specified directory for *.csv files and exports them as *.parquet files to Azure Storage.

## CSV file naming
Files must be saved in a single directory and they must be named accordingly: `<datetime>_<fixed_digit_increment>.csv`.

- `<datetime>` must be a date in `YYYY-MM-DD` (ISO 8601) format.
- `<fixed_digit_increment>` is recommended to be `%H-%M-%S` - hours, minutes and seconds, each 2 digit
- `<datetime>_<fixed_digit_increment>` should indicate exact date and time when the file was created and started beig written to
- Example: `2025-11-25_10-59-05.csv`.

_These conventions ensure that if the files are sorted by name, they are also sorted from the oldest to the newest ones_

## Installation
### ENV variables overview
The following Environmental variables must be set. Setting them in .env file located in the [/src](./src/) directory is possible.

| ENV variable | description | exmple |
| -------------|-------------|--------|
|AQ_AZ_SOURCE_FILE_DIRECTORY_PATH|path to the directory with csv files|/Users/rohal/projects/aq/local/aq-gateway/measurements|
|DOWNLOADED_DIR_PATH|path to the directory with where files are downloaded from azure||
|AQ_AZ_STAGING_DIRECTORY_PATH|path to the directory used by the script for file manipulation and local archiving|/Users/rohal/projects/aq/local/aq-data-az-blob/staging|
|AQ_AZ_STORAGE_CONNECTION_STRING|connection string from azure storage account|never_ever_share_this|
|AQ_AZ_STORAGE_CONTAINER_NAME|azure storage container name||
|AQ_DEVICE_ID|device id|test|
|AQ_DEVICE_ID|device id|test|
|AQ_BLOB_LOG_DIRECTORY_PATH| log path | /Users/rohal/projects/aq/local/aq-data-az-blob/logs |

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


## scripts


run the script
> **NOTE:** run as a module (use `-m` flag)
```bash
uv run python -m scripts.upload_files
```

```bash
uv run python -m scripts.download_files --id="test-001" --year=2025 --month=12 --day=8
```

### CRON
It is recommended to trigger the script regularily with [cron](https://en.wikipedia.org/wiki/Cron).
