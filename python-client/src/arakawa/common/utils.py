from __future__ import annotations

import datetime
import importlib.resources as ir
import locale
import mimetypes
import sys
import time
from pathlib import Path

import chardet
from chardet.universaldetector import UniversalDetector
from loguru import logger as log

from .ar_types import MIME

################################################################################
# CONSTANTS
ON_WINDOWS = sys.platform == "win32"

################################################################################
# MIME-type handling
mimetypes.init(files=[str(ir.files("arakawa.resources") / "mime.types")])

# TODO - hardcode as temporary fix until mimetypes double extension issue is sorted
_double_ext_map = {
    ".vl.json": "application/vnd.vegalite.v5+json",
    ".vl2.json": "application/vnd.vegalite.v2+json",
    ".vl3.json": "application/vnd.vegalite.v3+json",
    ".vl4.json": "application/vnd.vegalite.v4+json",
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
    return f'{x.isoformat(timespec="seconds")}{"" if x.tzinfo else "Z"}'
