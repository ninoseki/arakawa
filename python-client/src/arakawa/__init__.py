# Copyright 2020 StackHut Limited (trading as Datapane)
# SPDX-License-Identifier: Apache-2.0
try:
    from . import _version
except ImportError:
    # NOTE - could use subprocess to get from git?
    __rev__ = "local"
    __is_dev_build__ = True
else:
    __rev__ = _version.__rev__
    __is_dev_build__ = getattr(_version, "__is_dev_build__", False)
    del _version

__version__ = "0.17.0"


# Public API re-exports
from .blocks import (  # noqa: F401
    HTML,
    Attachment,
    BigNumber,
    Block,
    Code,
    DataTable,
    Embed,
    Empty,
    Formula,
    Group,
    Media,
    Page,
    Plot,
    Select,
    SelectType,
    Table,
    Text,
    Toggle,
    VAlign,
    wrap_block,
)
from .client import enable_logging, print_debug_info  # noqa: F401
from .exceptions import ARError  # noqa: F401
from .processors import (  # noqa: F401
    FontChoice,
    Formatting,
    TextAlignment,
    Width,
    build_report,
    save_report,
    stringify_report,
)
from .view import Blocks, Report, View  # noqa: F401

from . import builtins  # noqa: F401 # isort: skip

X = wrap_block
