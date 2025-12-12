# CSV to Blob export and download
> These scripts use UTC time for all input, output, logs, and internal calculations.

## Installation
### ENV variables overview
The following Environmental variables must be set. Setting them in .env file located in the [/src](./src/) directory is possible.

| ENV variable | description | exmple |
| -------------|-------------|--------|
|`AQ_AZ_SOURCE_FILE_DIRECTORY_PATH`|path to the directory with csv files|`/Users/rohal/projects/aq/local/aq-gateway/measurements`|
|`AQ_AZ_STAGING_DIRECTORY_PATH`|path to the directory used by the script for file manipulation and local archiving|`/Users/rohal/projects/aq/local/aq-data-az-blob/staging`|
|`AQ_AZ_STORAGE_CONNECTION_STRING`|connection string from azure storage account|_never ever share this_|
|`AQ_AZ_STORAGE_CONTAINER_NAME`|azure storage container name|`measures-archive`|
|`AQ_DEVICE_ID`|device id|`test`|
|`AQ_BLOB_LOG_DIRECTORY_PATH`| log path | `/Users/rohal/projects/aq/local/aq-data-az-blob/logs` |
|`DOWNLOADED_DIR_PATH`|path to the directory where files are downloaded from azure|`/Users/rohal/projects/aq/local/aq-data-az-blob/downloaded`|

### Virtual environment
Use [uv](https://docs.astral.sh/uv/) to create virtual environment, install necessary packages and run the scripts.

install UV
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

download and install dependencies
```bash
uv sync
```

## CSV files
### Naming
Files must be saved in a single directory and they must be named accordingly: `<datetime>_<fixed_digit_increment>.csv`.

- `<datetime>` must be a date in `YYYY-MM-DD` (ISO 8601) format.
- `<fixed_digit_increment>` is recommended to be `%H-%M-%S` - hours, minutes and seconds, each 2 digit
- `<datetime>_<fixed_digit_increment>` should indicate exact date and time when the file was created and started beig written to
- Example: `2025-11-25_10-59-05.csv`.

_These conventions ensure that if the files are sorted by name, they are also sorted from the oldest to the newest ones_

### Structure
A file must contain a header. The number of columns is not fixed and may vary from file to file. Examples of files with dummy data are in [sample_files](./sample_files/) directory.

## scripts
Scripts are located in the [scripts](./scripts/) directory.

### [upload_files.py](./scripts/upload_files.py)
#### Description
Converts \*.csv files into \*.parquet format and uploads them into Azure storage service.

#### Required ENV variables
 `AQ_AZ_SOURCE_FILE_DIRECTORY_PATH`, `AQ_AZ_STAGING_DIRECTORY_PATH`, `AQ_DEVICE_ID`, `AQ_AZ_STORAGE_CONNECTION_STRING`, `AQ_AZ_STORAGE_CONTAINER_NAME`

#### Arguments

| Argument | Type | Default | Description|
|----------|------|---------|------------|
|`--keep` `-k`|int|`1`|Number of the newest files to ingnore|

#### Use
> **NOTE:** run as a module (use `-m` flag)

To upload all files **except the newest one** in directory specified in `AQ_AZ_SOURCE_FILE_DIRECTORY_PATH` ENV variable:
```bash
uv run python -m scripts.upload_files
```
The script above prevents the file that is being writen into to be uploaded _(if file naming convention is followed)_.

To upload **all** files in directory specified in `AQ_AZ_SOURCE_FILE_DIRECTORY_PATH` ENV variable:
```bash
uv run python -m scripts.upload_files -k 0 # be careful to not run it when a file is being written into!
```

### [download_files.py](./scripts/download_files.py)
#### Description
Downloads files from Azure storage service.

#### Required ENV variables
`AQ_AZ_DOWNLOADED_DIR_PATH`, `AQ_AZ_STORAGE_CONNECTION_STRING`, `AQ_AZ_STORAGE_CONTAINER_NAME`

#### Arguments

| Argument | Type | Default | Description|
|----------|------|---------|------------|
|`--id`|string|_required_|Device identifier to filter files for download.|
|`--year`|int|_required_|Year to filter files for download.|
|`--month`|int|_required_|Month to filter files for download.|
|`--day`|int|_required_|Day to filter files for download.|

#### Use
> **NOTE:** run as a module (use `-m` flag)

To download files from device test-001 produced on 2025-12-08, run:
```bash
uv run python -m scripts.download_files --id="test-001" --year=2025 --month=12 --day=8
```



