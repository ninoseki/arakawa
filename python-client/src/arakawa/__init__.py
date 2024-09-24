# Copyright 2020 StackHut Limited (trading as Datapane)
# SPDX-License-Identifier: Apache-2.0
import sys
from pathlib import Path

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
from .client import (  # noqa: F401
    IN_PYTEST,
    ARMode,
    enable_logging,
    get_ar_mode,
    print_debug_info,
    set_ar_mode,
)
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
from .view import App, Blocks, Report, View  # noqa: F401

from . import builtins  # noqa: F401 # isort: skip

X = wrap_block


script_name = sys.argv[0]
script_exe = Path(script_name).stem
by_datapane = False  # hardcode for now as not using legacy runner
if script_exe == "datapane" or script_name == "-m":  # or "pytest" in script_name:
    # argv[0] will be "-m" as client module as submodule of this module
    set_ar_mode(ARMode.SCRIPT)
elif by_datapane or script_exe == "dp-runner":
    set_ar_mode(ARMode.FRAMEWORK)
else:
    set_ar_mode(ARMode.LIBRARY)
