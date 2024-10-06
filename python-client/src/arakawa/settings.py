import os

from . import __version__
from .versioning import convert2semver

AR_VERSION = os.environ.get("AR_VERSION", __version__).removeprefix("v")
AR_CDN_BASE = os.environ.get(
    "AR_CDN_BASE",
    f"https://cdn.jsdelivr.net/npm/arakawa@{convert2semver(AR_VERSION)}/dist",
)
