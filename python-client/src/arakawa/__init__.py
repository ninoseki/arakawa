# Copyright 2020 StackHut Limited (trading as Datapane)
# SPDX-License-Identifier: Apache-2.0

try:
    from ._version import version

    __version__ = version
except ImportError:
    __version__ = "0.0.0"

# Public API re-exports
from .blocks import (  # noqa: F401
    HTML,
    Attachment,
    BigNumber,
    Block,
    ChoiceField,
    Code,
    ColorField,
    Compute,
    DataTable,
    DateField,
    DateTimeField,
    EmailField,
    Embed,
    Empty,
    FileField,
    Formula,
    GreatTables,
    Group,
    HiddenField,
    Media,
    MultiChoiceField,
    NumberBox,
    Page,
    PasswordField,
    Plot,
    RangeField,
    SearchField,
    Select,
    SelectType,
    SwitchField,
    Table,
    TagsField,
    TelephoneField,
    Text,
    TextareaField,
    TextBox,
    TimeField,
    Toggle,
    URLField,
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
