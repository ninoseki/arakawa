from __future__ import annotations

from typing import Literal

from pydantic import AnyUrl, Field

from .base import DataBlock
from .mixins import OptionalCaptionMixin, OptionalLabelMixin, OptionalNameMinx


class AssetBlock(OptionalLabelMixin, OptionalNameMinx, OptionalCaptionMixin, DataBlock):
    src: AnyUrl
    type: str | None = Field(default=None)  # pattern=r"\w+/[\w.+\-]+"


class Media(AssetBlock):
    type_: Literal["Media"] = Field(..., alias="_type")


class Attachment(AssetBlock):
    type_: Literal["Attachment"] = Field(..., alias="_type")

    filename: str = Field(..., min_length=1, max_length=128)


class Plot(AssetBlock):
    type_: Literal["Plot"] = Field(..., alias="_type")

    scale: float = Field(default=1.0, ge=0.0)
    responsive: bool = Field(default=True)


class Table(AssetBlock):
    type_: Literal["Table"] = Field(..., alias="_type")


class DataTable(AssetBlock):
    type_: Literal["DataTable"] = Field(..., alias="_type")

    rows: int = Field(..., ge=0)
    columns: int = Field(..., ge=0)
