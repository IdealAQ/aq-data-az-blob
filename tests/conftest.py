# tests/conftest.py

import pytest

from .fakes import FakeContainerClient, FakeBlobProperties

blobs_01 = {
        "foo/aaa.wav": b"aaa data",
        "foo/bbb.wav": b"bbb data",
        "bar/ccc.wav": b"ccc data",
    }


@pytest.fixture
def container_client():
    return FakeContainerClient(blobs_01)