from __future__ import annotations

from typing import Literal

from pydantic import AnyHttpUrl, Field

from .base import DataBlock
from .mixins import OptionalCaptionMixin, OptionalLabelMixin, OptionalNameMinx


class TextBase(OptionalLabelMixin, OptionalNameMinx, DataBlock):
    content: str = Field(..., min_length=1, pattern=r"(.|\s)*\S(.|\s)*")


class Text(TextBase):
    id: Literal["Text", "Formula"] = Field(..., alias="_id")


class HTML(TextBase):
    id: Literal["HTML"] = Field(..., alias="_id")

    sandbox: str | None = Field(default=None)


class Code(OptionalCaptionMixin, TextBase):
    id: Literal["Code"] = Field(..., alias="_id")

    language: str = Field(..., min_length=1, max_length=128)


class Embed(TextBase):
    id: Literal["Embed"] = Field(..., alias="_id")

    url: AnyHttpUrl
    title: str = Field(..., min_length=1, max_length=256)
    provider_name: str = Field(..., min_length=1, max_length=128)
