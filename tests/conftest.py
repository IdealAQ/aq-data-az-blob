# tests/conftest.py
from pathlib import Path

import pytest

from .fakes import FakeContainerClient, FakeBlobProperties

blobs_01 = {
    "foo/aaa.wav": b"aaa data",
    "foo/bbb.wav": b"bbb data",
    "foo": b"",
    "bar/ccc.wav": b"ccc data",
    "bar/ddd.txt": b"ddd data",
    "bar/eee.txt": b"eee data",
    "bar/fff.json": b"fff data",
}

files_01 = {
    "/data/aaa/bbb/11-11-11.txt": b"data aaa",
    "/data/aaa/aaa/33-33-33.txt": b"data bbb",
    "/data/aaa/aaa/22-22-22.txt": b"data ccc",
    "/data/aaa/bbb/22-22-22.txt": b"data ddd",
    "/data/bbb/aaa/33-33-33.txt": b"data eee",
    "/data/bbb/aaa/11-11-11.json": b"data fff",
    "/data/bbb/aaa/22-22-22.wav": b"data ggg",
}

batches_01 = {
    "aaa": [
        Path("/data/aaa/ccc/11-11-11.txt"),  # last
        Path("/data/aaa/aaa/22-22-22.txt"),  # first
        Path("/data/aaa/bbb/22-22-22.txt"),
    ],
    "ccc": [
        Path("/data/ccc/ddd/11-11-11.txt"),  # last
        Path("/data/ccc/bbb/22-22-22.txt"),
        Path("/data/ccc/aaa/11-11-11.txt"),  # fist
    ],
    "bbb": [
        Path("/data/bbb/aaa/11-11-11.txt"),  # fist
        Path("/data/bbb/aaa/33-33-33.txt"),  # last
        Path("/data/bbb/aaa/22-22-22.txt"),
    ],
}


@pytest.fixture
def container_client():
    return FakeContainerClient(blobs_01)


@pytest.fixture
def file_paths():
    return [Path(path) for path in files_01.keys()]


@pytest.fixture
def file_batches():
    return batches_01


@pytest.fixture
def upload_dirs(tmp_path):
    staging = tmp_path / "staging"

    dirs = {
        "source": tmp_path / "source",
        "staging": staging,
        "process": staging / "to_process",
        "archive": staging / "archive",
    }

    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    dirs["tmp"] = tmp_path

    return dirs


@pytest.fixture
def source_files(upload_dirs):
    source = upload_dirs["source"]

    files = []
    for relative_path, contents in files_01.items():
        file = source / Path(relative_path).relative_to("/data")
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_bytes(contents)
        files.append(file)

    return files
