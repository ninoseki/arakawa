from __future__ import annotations

from typing import Literal, Union

from pydantic import Field

from arakawa.types import MethodType, SelectType, VAlign

from .asset import Attachment, DataTable, Media, Plot, Table
from .base import DataBlock
from .controls import (
    DateTimeField,
    FileField,
    HiddenField,
    MultiChoiceField,
    NumberBox,
    RangeField,
    SwitchField,
    TagsField,
    TextBox,
)
from .misc_blocks import BigNumber, Empty
from .mixins import OptionalLabelMixin, OptionalNameMinx
from .text import HTML, Code, Embed, Text

ControlBlocks = Union[
    DateTimeField,
    HiddenField,
    MultiChoiceField,
    NumberBox,
    RangeField,
    SwitchField,
    TagsField,
    TextBox,
    FileField,
]
AssetBlocks = Union[Media, Attachment, Plot, Table, DataTable]
TextBlocks = Union[Code, Embed, Text, HTML]
MiscBlocks = Union[BigNumber, Empty]
LayoutBlocks = Union["Select", "Group", "Toggle", "Compute"]
AllBlocks = Union[ControlBlocks, AssetBlocks, TextBlocks, MiscBlocks, LayoutBlocks]


class LayoutBlock(OptionalNameMinx, OptionalLabelMixin, DataBlock):
    blocks: list[AllBlocks] = Field(..., min_length=1)


class Page(LayoutBlock):
    id: Literal["_Page"] = Field(..., alias="_id")

    title: str | None = Field(default=None, min_length=1, max_length=256)


class Group(LayoutBlock):
    id: Literal["Group"] = Field(..., alias="_id")

    columns: int = Field(default=1)
    valign: VAlign
    widths: str | None = Field(default=None, min_length=2, pattern=r"\[\d+(,\s*\d+)*\]")


class Select(LayoutBlock):
    id: Literal["Select"] = Field(..., alias="_id")

    type: SelectType


class Toggle(LayoutBlock):
    id: Literal["Toggle"] = Field(..., alias="_id")


class Compute(LayoutBlock):
    id: Literal["Compute"] = Field(..., alias="_id")

    prompt: str | None = Field(default=None)
    subtitle: str | None = Field(default=None)
    action: str | None = Field(default="")
    method: MethodType = Field(default=MethodType.GET)


class View(LayoutBlock):
    id: Literal["View"] = Field(..., alias="_id")

    fragment: bool
    version: int = Field(..., ge=1)
