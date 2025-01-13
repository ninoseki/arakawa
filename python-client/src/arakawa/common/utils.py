from __future__ import annotations

import dataclasses as dc
import datetime
import importlib.resources as ir
import locale
import math
import mimetypes
import re
import sys
import time
from collections.abc import Sized
from numbers import Number
from pathlib import Path
from typing import Any

import chardet
from chardet.universaldetector import UniversalDetector
from loguru import logger as log
from micawber import ProviderException, bootstrap_basic, bootstrap_noembed, cache

from arakawa.exceptions import ARError
from arakawa.types import HTML, MIME

################################################################################
# CONSTANTS
ON_WINDOWS = sys.platform == "win32"

################################################################################
# MIME-type handling
mimetypes.init(files=[str(ir.files("arakawa.resources") / "mime.types")])

# TODO - hardcode as temporary fix until mimetypes double extension issue is sorted
_double_ext_map = {
    ".vl.json": "application/vnd.vegalite.v5+json",
    ".vl5.json": "application/vnd.vegalite.v5+json",
    ".bokeh.json": "application/vnd.bokeh.show+json",
    ".pl.json": "application/vnd.plotly.v1+json",
    ".fl.html": "application/vnd.folium+html",
    ".tbl.html": "application/vnd.arakawa.table+html",
    ".tar.gz": "application/x-tgz",
}
double_ext_map: dict[str, MIME] = {k: MIME(v) for k, v in _double_ext_map.items()}


def guess_type(filename: Path) -> MIME:
    ext = "".join(filename.suffixes)
    if ext in double_ext_map:
        return double_ext_map[ext]
    mtype, _ = mimetypes.guess_type(str(filename))
    assert mtype
    return MIME(mtype or "application/octet-stream")


def guess_encoding(fn: str) -> str:
    with open(fn, "rb") as f:
        detector = UniversalDetector()
        for line in f.readlines():
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result["encoding"]  # type: ignore


def utf_read_text(file: Path) -> str:
    """Encoding-aware text reader
    - handles cases like on Windows where a file is UTF-8, but default locale is windows-1252
    """
    if ON_WINDOWS:
        f_bytes = file.read_bytes()
        f_enc: str = chardet.detect(f_bytes)["encoding"]  # type: ignore
        # NOTE - can just special case utf-8 files here?
        def_enc = locale.getpreferredencoding()
        log.debug(f"Default encoding is {def_enc}, file encoded as {f_enc}")
        if def_enc.upper() != f_enc.upper():
            log.warning(f"Text file {file} encoded as {f_enc}, auto-converting")
        return f_bytes.decode(encoding=f_enc)
    # for linux/macOS assume utf-8
    return file.read_text()


def unixtime() -> int:
    return int(time.time())


def timestamp(x: datetime.datetime | None = None) -> str:
    """Return ISO timestamp for a datetime"""
    x = x or datetime.datetime.utcnow()
    return f"{x.isoformat(timespec='seconds')}{'' if x.tzinfo else 'Z'}"


def is_valid_id(id: str) -> bool:
    """(cached) regex to check for a xsd:ID name"""
    return re.fullmatch(r"^[a-zA-Z_][\w.-]*$", id) is not None


def conv_attrib(v: Any) -> Any | None:
    """
    Convert a value to a str for use as an ElementBuilder attribute
    - also handles None to a string for optional field values
    """
    # TODO - use a proper serialization framework here / lxml features
    if v is None:
        return v

    if isinstance(v, Sized) and len(v) == 0:
        return None

    if isinstance(v, str):
        return v

    if isinstance(v, Number) and not isinstance(v, bool):
        if math.isinf(v) and v > 0:  # type: ignore
            return "INF"

        if math.isinf(v) and v < 0:  # type: ignore
            return "-INF"

        if math.isnan(v):  # type: ignore
            return "NaN"

        return str(v)

    return v


def mk_attribs(**attribs: Any):
    """convert attributes, dropping None and empty values"""
    return {str(k): conv_attrib(v) for (k, v) in attribs.items()}


#####################################################################
# Embed Asset Helpers
providers = bootstrap_basic(cache=cache.Cache())


@dc.dataclass(frozen=True)
class Embedded:
    html: HTML
    title: str
    provider: str


def get_embed_url(url: str, width: int = 960, height: int = 540) -> Embedded:
    """Return html for an embeddable URL"""
    try:
        r = providers.request(url, maxwidth=width, maxheight=height)
    except ProviderException:
        # add NoEmbed to the list and try again
        try:
            log.debug("Initializing NoEmbed OEmbed provider")
            bootstrap_noembed(registry=providers)
            r = providers.request(url, maxwidth=width, maxheight=height)
        except ProviderException as e:
            raise ARError(
                f"No embed provider found for URL '{url}' - is there an active internet connection?"
            ) from e

    return Embedded(
        html=r["html"],
        title=r.get("title", "Title"),
        provider=r.get("provider_name", "Embedding"),
    )
