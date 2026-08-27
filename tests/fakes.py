class FakeBlobProperties:
    def __init__(self, name: str):
        self.name = name


class FakeDownloadStream:
    def __init__(self, data: bytes):
        self.data = data

    def readall(self) -> bytes:
        return self.data


class FakeBlobClient:
    def __init__(self, data: bytes):
        self.data = data

    def download_blob(self):
        return FakeDownloadStream(self.data)


class FakeContainerClient:
    def __init__(self, blobs):
        self.blobs = blobs

    def list_blobs(self, name_starts_with=None):
        return [
            FakeBlobProperties(name)
            for name in self.blobs
            if name_starts_with is None or name.startswith(name_starts_with)
        ]

    def get_blob_client(self, blob_name):
        return FakeBlobClient(self.blobs[blob_name])
