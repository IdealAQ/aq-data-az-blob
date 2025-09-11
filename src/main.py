from dotenv import load_dotenv
import os
import shutil

ENV_SOURCE_PATH="AQ_AZ_SOURCE_FILE_DIRECTORY_PATH"
ENV_STAGING_PATH="AQ_AZ_STAGING_DIRECTORY_PATH"

def prepare_files(source_path:str, dir_to_process:str, dir_archive:str):
    os.makedirs(dir_to_process, exist_ok=True)
    os.makedirs(dir_archive, exist_ok=True)

    with os.scandir(source_path) as entries:
        keep = -1 #keep one most recent file
        sorted_entries = sorted(entries, key=lambda e: e.name)
        entries_to_process = sorted_entries[:keep]
        
        for entry in entries_to_process:
            if not entry.is_file():
                continue
            shutil.move(entry.path, os.path.join(dir_to_process), entry.name)

def explort_file(file_path:str):
    pass

def main():
    load_dotenv()
    source_path = os.getenv(ENV_SOURCE_PATH)
    staging_path = os.getenv(ENV_STAGING_PATH)
    dir_to_process = f"{staging_path}/to_process"
    dir_archive = f"{staging_path}/archive"

    prepare_files(
        source_path=source_path,
        dir_to_process=dir_to_process,
        dir_archive=dir_archive
    )

if __name__ == "__main__":
    main()
