from pprint import pprint

from aqblob.uploader import batch_files_by_path, sort_file_batches_by_path_asc
from pathlib import Path


def test_sort_file_batches_by_path_asc(file_batches):
    batches_sorted = sort_file_batches_by_path_asc(file_batches)

    pprint(batches_sorted)
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


def test_upload_files(container_client, upload_dirs):

    assert 0

def test_upload_files_keep_0(container_client, upload_dirs):
    
    assert 0

def test_upload_files_keep_1(container_client, upload_dirs):
    
    assert 0

def test_upload_files_keep_larger_than_files(container_client, upload_dirs):
    
    assert 0

def test_upload_files_empty_source(container_client, upload_dirs):
    
    assert 0


