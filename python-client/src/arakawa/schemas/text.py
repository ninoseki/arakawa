from __future__ import annotations

from typing import Literal

from pydantic import AnyHttpUrl, Field

from .base import DataBlock
from .mixins import OptionalCaptionMixin, OptionalLabelMixin, OptionalNameMinx


class TextBase(OptionalLabelMixin, OptionalNameMinx, DataBlock):
    content: str = Field(..., min_length=1, pattern=r"(.|\s)*\S(.|\s)*")


class Text(TextBase):
    type_: Literal["Text", "Formula"] = Field(..., alias="_type")


class HTML(TextBase):
    type_: Literal["HTML"] = Field(..., alias="_type")

    sandbox: str | None = Field(default=None)


class Code(OptionalCaptionMixin, TextBase):
    type_: Literal["Code"] = Field(..., alias="_type")

    language: str = Field(..., min_length=1, max_length=128)


class Embed(TextBase):
    type_: Literal["Embed"] = Field(..., alias="_type")

    url: AnyHttpUrl
    title: str = Field(..., min_length=1, max_length=256)
    provider_name: str = Field(..., min_length=1, max_length=128)
