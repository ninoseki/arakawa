# Copyright 2020 StackHut Limited (trading as Datapane)
# SPDX-License-Identifier: Apache-2.0
import importlib.metadata

__version__ = importlib.metadata.version(__name__)

# Public API re-exports
from .blocks import (  # noqa: F401
    HTML,
    Attachment,
    BigNumber,
    Block,
    Code,
    Compute,
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
    TextBox,
    Toggle,
    VAlign,
    wrap_block,
)
from .exceptions import ARError  # noqa: F401
from .processors import (  # noqa: F401
    FontChoice,
    Formatting,
    TextAlignment,
    Width,
    save_report,
    stringify_report,
)
from .utils import enable_logging, print_debug_info  # noqa: F401
from .view import Blocks, Report, View  # noqa: F401

from . import builtins  # noqa: F401 # isort: skip

X = wrap_block
