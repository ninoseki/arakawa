from __future__ import annotations

from typing import Literal

from pydantic import AnyUrl, Field

from .base import DataBlock
from .mixins import OptionalCaptionMixin, OptionalLabelMixin, OptionalNameMinx


class AssetBlock(OptionalLabelMixin, OptionalNameMinx, OptionalCaptionMixin, DataBlock):
    src: AnyUrl
    type: str | None = Field(default=None)  # pattern=r"\w+/[\w.+\-]+"


class Media(AssetBlock):
    id: Literal["Media"] = Field(..., alias="_id")


class Attachment(AssetBlock):
    id: Literal["Attachment"] = Field(..., alias="_id")

    filename: str = Field(..., min_length=1, max_length=128)


class Plot(AssetBlock):
    id: Literal["Plot"] = Field(..., alias="_id")

    scale: float = Field(default=1.0, ge=0.0)
    responsive: bool = Field(default=True)


class Table(AssetBlock):
    id: Literal["Table"] = Field(..., alias="_id")


class DataTable(AssetBlock):
    id: Literal["DataTable"] = Field(..., alias="_id")

    rows: int = Field(..., ge=0)
    columns: int = Field(..., ge=0)
