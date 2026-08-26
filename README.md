# AQ blob upload and download scripts
> These scripts use UTC time for all inputs, outputs, and internal calculations.

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
|`AQ_AZ_STORAGE_CONTAINER_NAME`|azure storage container name - must match existing container name|`raw-sound`|
|`AQ_AZ_FILE_SUFFIXES`|comma-separated list of file suffixes|`.flac,.wav`|


### Virtual environment
Use [uv](https://docs.astral.sh/uv/) to create virtual environment, install necessary packages and run the scripts.

install UV (mac/linux)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

download and install dependencies
```bash
uv sync
```

## Files
The suggested local file structure is shown below. In this example, `raw-sound` is the root directory specified by `AQ_AZ_SOURCE_FILE_DIRECTORY_PATH`. On Linux, you can run `pwd` from the `raw-sound` directory to get the path to use for `AQ_AZ_SOURCE_FILE_DIRECTORY_PATH`.

```text
raw-sound/                                       # Local root directory
└── campaign=helsinki-spring-2026/               # <campaign-name>
    └── platform=scooter-001/                    # <platform-name>
        └── source=microphone-001/               # <source-name>
            └── date=2026-03-18/
                ├── 16-22-56.wav
                ├── 16-30-00.wav
                └── 16-40-00.wav
```
The local file:<br>
`raw-sound/campaign=helsinki-spring-2026/platform=scooter-001/source=microphone-001/date=2026-03-18/16-22-56.wav`<br>
corresponds to the following Azure Blob Storage blob path:<br>
`campaign=helsinki-spring-2026/platform=scooter-001/source=microphone-001/date=2026-03-18/16-22-56.wav`.

It is reccomended to name the root directory the same as the container name. In this case, `raw-sound` would be the name of the Azure Blob container specified in env variable `AQ_AZ_STORAGE_CONTAINER_NAME`.

The file name should be the UTC timestamp of the start of the contained data, in `hh-mm-ss` format, unless otherwise required.

## scripts
Scripts are located in the [scripts](./scripts/) directory.
> An alternative way to run sripts is `uv run python -m scripts.<script_name>` (i.e. `uv run python -m scripts.upload_files` instead of `uv run upload`).

### [upload_files.py](./scripts/upload_files.py)
#### Description
Uploads files in subfolders of specified root. The paths of the uploaded blobs match the relative paths of the uploaded files from the root directory.

#### Required ENV variables
`AQ_BLOB_LOG_DIRECTORY_PATH`,
`AQ_AZ_SOURCE_FILE_DIRECTORY_PATH`,`AQ_AZ_STAGING_DIRECTORY_PATH`,
`AQ_AZ_STORAGE_CONNECTION_STRING`,
`AQ_AZ_STORAGE_CONTAINER_NAME`,
`AQ_AZ_FILE_SUFFIXES`

#### Arguments

| Argument | Type | Default | Description|
|----------|------|---------|------------|
|`--keep` `-k`|int|`1`|Number of the newest files to ingnore in each directory|
|`--limit` `-l`|int|`1000`|Max. number of oldest files to include in each directory|

\* **Note:** `--keep` relies on the filename/path following naming pattern which keeps newst files to be last when file paths are sorted. Example: `.../date=yyyy-mm-dd/hh-mm-ss.suffix`.

**sequence:**
1. **Step 1:** move files from `AQ_AZ_SOURCE_FILE_DIRECTORY_PATH` to `AQ_AZ_STAGING_DIRECTORY_PATH`
2. **Step 2:** upload files from `AQ_AZ_STAGING_DIRECTORY_PATH` to Azure Storage

\* `--keep` and `--limit` affect only step 1


#### Use
To upload all files **except the newest one** (max 1000 or `-l`) in each terminal subdirectory of root specified in `AQ_AZ_SOURCE_FILE_DIRECTORY_PATH` ENV variable:
```bash
uv run upload
```
The script above prevents the file that is being writen into to be uploaded _(if file naming convention is followed)_.

To upload **all** files in directory specified in `AQ_AZ_SOURCE_FILE_DIRECTORY_PATH` ENV variable:
```bash
uv run upload -k 0 # be careful to not run it when a file is being written into!
```

### [list_blobs.py](./scripts/list_blobs.py)
#### Description
Lists files from Azure storage service.

#### Required ENV variables
`AQ_BLOB_LOG_DIRECTORY_PATH`,
`AQ_AZ_STORAGE_CONNECTION_STRING`,
`AQ_AZ_STORAGE_CONTAINER_NAME`,
`AQ_AZ_FILE_SUFFIXES`

#### Arguments

| Argument | Type | Default | Description|
|----------|------|---------|------------|
|`-p`, `--prefix`|string|_required_|Prefix of the blobs to download.|
|`-c`, `--container`|string|env `AQ_AZ_STORAGE_CONTAINER_NAME`|Azure Storage container name (default: from config).|

#### Use
To download files from campaign none-001 and platform scooter-001, run:
```bash
uv run list -p="campaign=none-001/platform=scooter-001/" -c="raw-sound"
```

### [download_blobs.py](./scripts/download_blobs.py)
#### Description
Downloads files from Azure storage service into directory structure matching the file's prefixes.

#### Required ENV variables
`AQ_BLOB_LOG_DIRECTORY_PATH`,
`AQ_AZ_STORAGE_CONNECTION_STRING`,
`AQ_AZ_STORAGE_CONTAINER_NAME`,
`AQ_AZ_DOWNLOADED_DIR_PATH`,
`AQ_AZ_FILE_SUFFIXES`

#### Arguments

| Argument | Type | Default | Description|
|----------|------|---------|------------|
|`-p`, `--prefix`|string|_required_|Prefix of the blobs to download.|
|`-c`, `--container`|string|env `AQ_AZ_STORAGE_CONTAINER_NAME`|Azure Storage container name (default: from config).|
|`-f`, `--force`|flag||Overwrite existing files locally.|


#### Use
> **NOTE:** run as a module (use `-m` flag)

To download files from campaign none-001 and platform scooter-001, run:
```bash
uv run download -p="campaign=none-001/platform=scooter-001/" -c="raw-sound"
```

To redownload existing files, run:
```bash
uv run download -p="campaign=none-001/platform=scooter-001/" -c="raw-sound" -f
```

### [parquet_to_csv.py](./scripts/upload_files.py)
> **Outdated**

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
