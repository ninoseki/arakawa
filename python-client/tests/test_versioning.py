import pytest

from arakawa.versioning import convert2semver


@pytest.mark.parametrize(
    "pep440_version,expected",
    [
        ("0.0.1a0", "0.0.1-alpha"),
        ("0.0.1a1", "0.0.1-alpha.1"),
        ("0.0.1b0", "0.0.1-beta"),
        ("0.0.1b1", "0.0.1-beta.1"),
        ("0.0.1", "0.0.1"),
        ("1.0.1", "1.0.1"),
    ],
)
def test_convert2semver(pep440_version: str, expected: str):
    assert str(convert2semver(pep440_version)) == expected
