from __future__ import annotations

from typing import Literal

from pydantic import Field

from arakawa.types import NumberValue

from .base import DataBlock
from .fields import TypeAliasedField
from .mixins import NameMixin


class Empty(NameMixin, DataBlock):
    type_: Literal["Empty"] = TypeAliasedField()


class BigNumber(DataBlock):
    type_: Literal["BigNumber"] = TypeAliasedField()

    heading: str = Field(..., min_length=1, max_length=128)
    value: NumberValue = Field(..., min_length=1, max_length=128)
    change: NumberValue | None = Field(default=None, min_length=1, max_length=128)
    pre_value: NumberValue | None = Field(default=None, min_length=1, max_length=128)
    is_positive_intent: bool | None = Field(default=None)
    is_upward_change: bool | None = Field(default=None)
