# tests/conftest.py

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


@pytest.fixture
def container_client():
    return FakeContainerClient(blobs_01)
