from aqblob import list_blobs


def test_list_blobs(container_client):
    blobs = list_blobs(
        container_client=container_client,
        prefix="foo",
    )

    assert len(blobs) == 3
    assert all(s.startswith("foo") for s in blobs)


def test_list_blobs_all(container_client):
    blobs = list_blobs(
        container_client=container_client,
        prefix="",
    )

    assert len(blobs) == 7


def test_list_blobs_with_no_matching_blobs(container_client):
    blobs = list_blobs(
        container_client=container_client,
        prefix="does-not-exist/",
    )

    assert len(blobs) == 0
