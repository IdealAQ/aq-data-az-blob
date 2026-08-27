from aqblob import download_files
# Mock class from unittest might used to replace fake classes


def test_download_files(container_client, tmp_path):
    download_files(
        container_client=container_client,
        downloaded_dir_path=tmp_path,
        prefix="foo/",
        suffixes=(".wav",),
        skip_existing=True,
    )

    downloaded_files = list(tmp_path.rglob("*.wav"))

    assert len(downloaded_files) == 2
    assert (tmp_path / "foo/aaa.wav").read_bytes() == b"aaa data"
    assert (tmp_path / "foo/bbb.wav").read_bytes() == b"bbb data"


def test_download_files_skips_existing(container_client, tmp_path):
    file = tmp_path / "foo/aaa.wav"
    file.parent.mkdir(parents=True)
    file.write_bytes(b"existing data")

    download_files(
        container_client=container_client,
        downloaded_dir_path=tmp_path,
        prefix="foo/",
        suffixes=(".wav",),
        skip_existing=True,
    )

    assert file.read_bytes() == b"existing data"


def test_download_files_overwrites_existing(container_client, tmp_path):
    file = tmp_path / "foo/aaa.wav"
    file.parent.mkdir(parents=True)
    file.write_bytes(b"existing data")

    download_files(
        container_client=container_client,
        downloaded_dir_path=tmp_path,
        prefix="foo/",
        suffixes=(".wav",),
        skip_existing=False,
    )

    assert file.read_bytes() == b"aaa data"


def test_download_files_with_no_matching_blobs(container_client, tmp_path):
    download_files(
        container_client=container_client,
        downloaded_dir_path=tmp_path,
        prefix="does-not-exist/",
        suffixes=(".wav",),
        skip_existing=True,
    )

    assert list(tmp_path.rglob("*")) == []


def test_download_multiple_suffixes(container_client, tmp_path):
    download_files(
        container_client=container_client,
        downloaded_dir_path=tmp_path,
        prefix="bar/",
        suffixes=(".wav", ".txt"),
        skip_existing=True,
    )
    downloaded_files_wav = list(tmp_path.rglob("*.wav"))
    downloaded_files_txt = list(tmp_path.rglob("*.txt"))

    assert len(downloaded_files_wav) == 1
    assert len(downloaded_files_txt) == 2
