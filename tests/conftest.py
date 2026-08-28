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
    Path("/data/aaa/bbb/11-11-11.txt"),
    Path("/data/aaa/aaa/33-33-33.txt"),
    Path("/data/aaa/aaa/11-11-11.txt"),
    Path("/data/aaa/aaa/22-22-22.txt"),
    Path("/data/aaa/bbb/22-22-22.txt"),
    Path("/data/bbb/aaa/33-33-33.txt"),
    Path("/data/bbb/aaa/11-11-11.txt"),
    Path("/data/bbb/aaa/22-22-22.txt"),
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
    return files_01


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

    return dirs