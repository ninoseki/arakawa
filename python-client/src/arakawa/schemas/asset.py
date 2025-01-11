from __future__ import annotations

from typing import Literal

from pydantic import AnyUrl, Field

from .base import DataBlock
from .fields import TypeAliasedField
from .mixins import OptionalCaptionMixin, OptionalLabelMixin, OptionalNameMinx


class AssetBlock(OptionalLabelMixin, OptionalNameMinx, OptionalCaptionMixin, DataBlock):
    src: AnyUrl
    type: str | None = Field(default=None)  # pattern=r"\w+/[\w.+\-]+"


class Media(AssetBlock):
    type_: Literal["Media"] = TypeAliasedField()


class Attachment(AssetBlock):
    type_: Literal["Attachment"] = TypeAliasedField()

    filename: str = Field(..., min_length=1, max_length=128)


class Plot(AssetBlock):
    type_: Literal["Plot"] = TypeAliasedField()

    scale: float = Field(default=1.0, ge=0.0)
    responsive: bool = Field(default=True)


class Table(AssetBlock):
    type_: Literal["Table"] = TypeAliasedField()


class DataTable(AssetBlock):
    type_: Literal["DataTable"] = TypeAliasedField()

    rows: int = Field(..., ge=0)
    columns: int = Field(..., ge=0)
