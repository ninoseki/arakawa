import pytest

from arakawa.common.utils import should_compress_mime_type_for_upload


@pytest.mark.parametrize(
    ("mime_type", "value"),
    [
        # Some common types:
        # - Should compress:
        ("text/html", True),
        ("text/xml", True),
        ("application/json", True),
        ("application/geo+json", True),
        ("application/rss+xml", True),
        ("image/svg+xml", True),
        # - Should not:
        ("audio/mpeg", False),
        ("image/png", False),
        ("video/mp4", False),
        ("application/zip", False),
        # Our special cases:
        ("application/vnd.vegalite.v5+json", True),
        ("application/vnd.arakawa.table+html", True),
        ("application/vnd.pickle+binary", True),
        ("application/vnd.apache.arrow+binary", True),
        ("application/x-tgz", False),
    ],
)
def test_should_compress_mime_type(mime_type, value):
    assert should_compress_mime_type_for_upload(mime_type) == value
