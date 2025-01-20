from typing import Union

from .asset import Attachment, DataTable, Media, Plot, Table
from .base import (  # noqa: F401
    BaseBlock,
    BlockList,
    BlockOrPrimitive,
    DataBlock,
    wrap_block,
)
from .controls import (
    ChoiceField,
    ColorField,
    DateField,
    DateTimeField,
    EmailField,
    FileField,
    HiddenField,
    MultiChoiceField,
    NumberBox,
    PasswordField,
    RangeField,
    SearchField,
    SwitchField,
    TagsField,
    TelephoneField,
    TextareaField,
    TextBox,
    TimeField,
    URLField,
)
from .layout import (  # noqa: F401
    Compute,
    Group,
    Page,
    Select,
    SelectType,
    Toggle,
)
from .misc_blocks import BigNumber, Empty
from .text import HTML, Code, Embed, Formula, Text

Block = BaseBlock

AssetBlocks = Union[Media, Attachment, Plot, Table, DataTable]
TextBlocks = Union[Code, Embed, Text, HTML, Formula]
MiscBlocks = Union[BigNumber, Empty]
LayoutBlocks = Union[Select, Group, Toggle, Compute]
ControlBlocks = Union[
    ChoiceField,
    DateTimeField,
    FileField,
    HiddenField,
    MultiChoiceField,
    NumberBox,
    RangeField,
    SwitchField,
    TagsField,
    TextBox,
    ColorField,
    SearchField,
    DateField,
    EmailField,
    PasswordField,
    TelephoneField,
    TextareaField,
    TimeField,
    URLField,
]
AllBlocks = Union[ControlBlocks, AssetBlocks, TextBlocks, MiscBlocks, LayoutBlocks]
