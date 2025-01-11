from __future__ import annotations

from typing import Literal, Union

from pydantic import Field, RootModel

from arakawa.types import ComputeMethod, SelectType, VAlign

from .asset import Attachment, DataTable, Media, Plot, Table
from .base import DataBlock
from .controls import (
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
)
from .fields import TypeAliasedField
from .misc_blocks import BigNumber, Empty
from .mixins import OptionalLabelMixin, OptionalNameMinx
from .text import HTML, Code, Embed, Text

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
]
AssetBlocks = Union[Media, Attachment, Plot, Table, DataTable]
TextBlocks = Union[Code, Embed, Text, HTML]
MiscBlocks = Union[BigNumber, Empty]
LayoutBlocks = Union["Select", "Group", "Toggle", "Compute"]
AllBlocks = Union[ControlBlocks, AssetBlocks, TextBlocks, MiscBlocks, LayoutBlocks]


class LayoutBlock(OptionalNameMinx, OptionalLabelMixin, DataBlock):
    blocks: list[AllBlocks] = Field(..., min_length=1)


class Page(LayoutBlock):
    type_: Literal["_Page"] = TypeAliasedField()

    title: str | None = Field(default=None, min_length=1, max_length=256)


class Group(LayoutBlock):
    type_: Literal["Group"] = TypeAliasedField()

    columns: int = Field(default=1)
    valign: VAlign
    widths: str | None = Field(default=None, min_length=2, pattern=r"\[\d+(,\s*\d+)*\]")


class Select(LayoutBlock):
    type_: Literal["Select"] = TypeAliasedField()

    type: SelectType


class Toggle(LayoutBlock):
    type_: Literal["Toggle"] = TypeAliasedField()


class Compute(LayoutBlock):
    type_: Literal["Compute"] = TypeAliasedField()

    prompt: str | None = Field(default=None)
    subtitle: str | None = Field(default=None)
    action: str | None = Field(default="")
    method: ComputeMethod = Field(default=ComputeMethod.GET)


class View(LayoutBlock):
    type_: Literal["View"] = TypeAliasedField()

    fragment: bool
    version: int = Field(..., ge=1)


class BlocksWrapper(RootModel):
    root: list[AllBlocks]
