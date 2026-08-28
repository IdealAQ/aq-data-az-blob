from aqblob.uploader import (
    batch_files_by_path,
    sort_file_batches_by_path_asc,
    extract_batches,
    upload_files,
)
from pathlib import Path


def test_sort_file_batches_by_path_asc(file_batches):
    batches_sorted = sort_file_batches_by_path_asc(file_batches)

    assert list(batches_sorted.keys()) == sorted(batches_sorted.keys())

    assert batches_sorted["aaa"] == sorted(batches_sorted["aaa"])
    assert batches_sorted["bbb"] == sorted(batches_sorted["bbb"])
    assert batches_sorted["ccc"] == sorted(batches_sorted["ccc"])


def test_batch_files_by_path_level_0(file_paths):
    batches = batch_files_by_path(
        files=file_paths,
        source_path=Path("/data"),
        level=0,
    )

    assert list(batches.keys()) == [""]


def test_batch_files_by_path_level_1(file_paths):
    batches = batch_files_by_path(
        files=file_paths,
        source_path=Path("/data"),
        level=1,
    )

    assert sorted(batches.keys()) == ["aaa", "bbb"]


def test_batch_files_by_path_level_2(file_paths):
    batches = batch_files_by_path(
        files=file_paths,
        source_path=Path("/data"),
        level=2,
    )

    assert sorted(batches.keys()) == [
        "aaa/aaa",
        "aaa/bbb",
        "bbb/aaa",
    ]


def test_batch_files_by_path_level_larger_than_path(file_paths):
    batches = batch_files_by_path(
        files=file_paths,
        source_path=Path("/data"),
        level=100,
    )

    assert len(batches) == len(file_paths)


def test_extract_batches_keep1_limit1(file_batches):
    extracted = extract_batches(file_batches, keep=1, limit=1)

    sorted_batches = sort_file_batches_by_path_asc(file_batches)

    assert extracted == [values[0] for values in sorted_batches.values()]


def test_extact_batches_keep1_limit_larger_than_files(file_batches):
    extracted = extract_batches(file_batches, keep=1, limit=1000)

    sorted_batches = sort_file_batches_by_path_asc(file_batches)
    kept = [batch[-1] for batch in sorted_batches.values()]

    assert len(extracted) == 6
    assert set(extracted).isdisjoint(kept)


def test_extract_batches_keep0_limit_1(file_batches):
    extracted = extract_batches(file_batches, keep=1, limit=1)
    sorted_batches = sort_file_batches_by_path_asc(file_batches)

    expected = [batch[0] for batch in sorted_batches.values()]

    assert extracted == expected


def test_extract_batches_keep_larger_than_files(file_batches):
    extracted = extract_batches(file_batches, keep=1000, limit=1000)

    assert extracted == []


def test_extract_batches_limit0(file_batches):
    extracted = extract_batches(file_batches, keep=0, limit=0)

    assert extracted == []


def test_upload_files(container_client, upload_dirs, source_files):
    source_dir_path = upload_dirs["source"]
    staging_dir_path = upload_dirs["staging"]
    archive_dir_path = upload_dirs["archive"]

    upload_files(
        container_client=container_client,
        source_dir_path=source_dir_path,
        staging_dir_path=staging_dir_path,
        suffixes=[".txt"],
        keep=1,
        limit=1000,
        batch_lvl=1,
    )

    source_dir_files = [path for path in source_dir_path.rglob("*") if path.is_file()]
    archive_dir_files = [path for path in archive_dir_path.rglob("*") if path.is_file()]

    archive_dir_files_json = [
        path for path in archive_dir_path.rglob("*.json") if path.is_file()
    ]
    source_dir_files_json = [
        path for path in source_dir_path.rglob("*.json") if path.is_file()
    ]
    archive_dir_files_txt = [
        path for path in archive_dir_path.rglob("*.txt") if path.is_file()
    ]

    assert len(source_files) == len(source_dir_files) + len(archive_dir_files)
    assert len(archive_dir_files_json) == 0
    assert len(source_dir_files_json) == 1
    assert len(archive_dir_files_txt) == 3


def test_upload_files_keep_0(container_client, upload_dirs, source_files):
    source_dir_path = upload_dirs["source"]
    staging_dir_path = upload_dirs["staging"]
    archive_dir_path = upload_dirs["archive"]
    process_dir_path = upload_dirs["process"]

    upload_files(
        container_client=container_client,
        source_dir_path=source_dir_path,
        staging_dir_path=staging_dir_path,
        suffixes=[".txt", ".json"],
        keep=0,
        limit=1000,
        batch_lvl=2,
    )

    source_dir_files = [path for path in source_dir_path.rglob("*") if path.is_file()]
    process_dir_files = [path for path in process_dir_path.rglob("*") if path.is_file()]
    archive_dir_files = [path for path in archive_dir_path.rglob("*") if path.is_file()]

    assert len(source_files) == len(source_dir_files) + len(archive_dir_files)
    assert len(source_dir_files) == 1
    assert source_dir_files[0].suffix == ".wav"
    assert len(process_dir_files) == 0
