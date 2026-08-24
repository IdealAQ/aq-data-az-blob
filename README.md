# AQ blob upload and download scripts
> These scripts use UTC time for all input, output, logs, and internal calculations.

> **This README file is out of date and neets to be updated!**

## Installation
### ENV variables overview
The following Environmental variables must be set. Setting them in .env file located in the project root directory is possible.

| ENV variable | description | exmple |
| -------------|-------------|--------|
|`AQ_AZ_BLOB_LOG_DIRECTORY_PATH`| log path | `/Users/rohal/projects/aq/local/aq-data-az-blob/logs` |
|`AQ_AZ_SOURCE_FILE_DIRECTORY_PATH`|path to the directory with csv files|`/Users/rohal/projects/aq/local/aq-gateway/measurements`|
|`AQ_AZ_DOWNLOADED_DIR_PATH`|path to the directory where files are downloaded from azure|`/Users/rohal/projects/aq/local/aq-data-az-blob/downloaded`|
|`AQ_AZ_STAGING_DIRECTORY_PATH`|path to the directory used by the script for file manipulation and local archiving|`/Users/rohal/projects/aq/local/aq-data-az-blob/staging`|
|`AQ_AZ_STORAGE_CONNECTION_STRING`|connection string from azure storage account|_never ever share this_|
|`AQ_AZ_STORAGE_CONTAINER_NAME`|azure storage container name|`measures-archive`|
|`AQ_AZ_PLATFORM_NAME`|name/id of mounting point|`platform-001`|
|`AQ_AZ_FILE_SUFFIXES`|comma-separated list of file suffixes|`.flac,.wav`|


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

## Files
TODO:

## scripts
Scripts are located in the [scripts](./scripts/) directory.

### [upload_files.py](./scripts/upload_files.py)

#### Required ENV variables
`AQ_BLOB_LOG_DIRECTORY_PATH`,
`AQ_AZ_SOURCE_FILE_DIRECTORY_PATH`,`AQ_AZ_STAGING_DIRECTORY_PATH`,
`AQ_AZ_STORAGE_CONNECTION_STRING`,
`AQ_AZ_STORAGE_CONTAINER_NAME`,
`AQ_AZ_PLATFORM_NAME`,
`AQ_AZ_FILE_SUFFIXES`

#### Arguments

| Argument | Type | Default | Description|
|----------|------|---------|------------|
|`--keep` `-k`|int|`1`|Number of the newest files to ingnore in each directory|
|`--limit` `-l`|int|`1000`|Max. number of oldest files to upload in each directory|


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
> Outdated!!!

Downloads files from Azure storage service.

#### Required ENV variables
`AQ_AZ_DOWNLOADED_DIR_PATH`, `AQ_AZ_STORAGE_CONNECTION_STRING`, `AQ_AZ_STORAGE_CONTAINER_NAME`, `AQ_AZ_FILE_SUFFIXES`

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

### [parquet_to_csv.py](./scripts/upload_files.py)
#### Description
Convert Parquet file to CSV.

#### Required ENV variables
`AQ_AZ_DOWNLOADED_DIR_PATH`

#### Arguments

| Argument | Type | Default | Description|
|----------|------|---------|------------|
|`--file_name`, `-f`|str|_required_|Name of parquet file in `DOWNLOADED_DIR_PATH` directory.|
|`--output`, `-o`|str|_required_|Path of new csv file to be created.|

#### Use
> **NOTE:** run as a module (use `-m` flag)

To convert `2026_month=02_day=19_hour=12_1771506660.parquet` file into `./output.csv`, run
```
uv run python -m scripts.parquet_to_csv -f="archive_device=gateway-002_year=2026_month=02_day=19_hour=12_1771506660.parquet" -o="./output.csv"
```