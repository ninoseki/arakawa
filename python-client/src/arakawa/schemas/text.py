from __future__ import annotations

from typing import Literal

from pydantic import AnyHttpUrl, Field

from .base import DataBlock
from .fields import TypeAliasedField
from .mixins import OptionalCaptionMixin, OptionalLabelMixin, OptionalNameMinx


class TextBase(OptionalLabelMixin, OptionalNameMinx, DataBlock):
    content: str = Field(..., min_length=1, pattern=r"(.|\s)*\S(.|\s)*")


class Text(TextBase):
    type_: Literal["Text", "Formula"] = TypeAliasedField()


class HTML(TextBase):
    type_: Literal["HTML"] = TypeAliasedField()

    sandbox: str | None = Field(default=None)


class Code(OptionalCaptionMixin, TextBase):
    type_: Literal["Code"] = TypeAliasedField()

    language: str = Field(..., min_length=1, max_length=128)


class Embed(TextBase):
    type_: Literal["Embed"] = TypeAliasedField()

    url: AnyHttpUrl
    title: str = Field(..., min_length=1, max_length=256)
    provider_name: str = Field(..., min_length=1, max_length=128)
