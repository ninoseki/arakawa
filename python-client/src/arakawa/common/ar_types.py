from collections.abc import Mapping
from datetime import timedelta
from enum import Enum
from os import PathLike
from pathlib import Path
from typing import Any, NewType, Union

# Typedefs
# A JSON-serialisable config object
SDict = dict[str, Any]
SSDict = dict[str, str]
SList = list[str]
# NOTE - mypy cannot handle recursive types like this currently. Will review in the future
JSON = Union[str, int, float, bool, None, Mapping[str, "JSON"], list["JSON"]]  # type: ignore
JDict = SDict  # should be JSON
JList = list[JSON]  # type: ignore
MIME = NewType("MIME", str)
URL = NewType("URL", str)
HTML = NewType("HTML", str)
NPath = Union[Path, PathLike, str]
Hash = NewType("Hash", str)
EnumType = int  # alias for enum values

# Constants
# NOTE - PKL_MIMETYPE and ARROW_MIMETYPE are custom mimetypes
PKL_MIMETYPE = MIME("application/vnd.pickle+binary")
ARROW_MIMETYPE = MIME("application/vnd.apache.arrow+binary")
ARROW_EXT = ".arrow"
TD_1_HOUR = timedelta(hours=1)
TD_1_DAY = timedelta(days=1)
SECS_1_HOUR: int = int(TD_1_HOUR.total_seconds())
SECS_1_WEEK: int = int(timedelta(weeks=1).total_seconds())
SIZE_1_MB: int = 1024 * 1024


class StrEnum(str, Enum):
    # TODO - replace with StrEnum in py3.11 stdlib
    def __str__(self):
        return str(self.value)
