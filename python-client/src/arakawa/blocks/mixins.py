from __future__ import annotations

from functools import partial
from typing import Annotated

from pydantic import (
    BeforeValidator,
    Field,
    computed_field,
    field_validator,
)

from arakawa.common.utils import is_valid_id

from .base import DataBlock


def truncate_optional_string(x: str | None, *, max_length: int) -> str | None:
    if x is None or len(x) <= max_length:
        return x

    return f"{x[: max_length - 3]}..."


class OptionalLabelMixin(DataBlock):
    label: Annotated[
        str | None, BeforeValidator(partial(truncate_optional_string, max_length=256))
    ] = Field(
        default=None,
        description="A label to display above the block",
        min_length=1,
        max_length=256,
    )


class OptionalCaptionMixin(DataBlock):
    caption: Annotated[
        str | None, BeforeValidator(partial(truncate_optional_string, max_length=512))
    ] = Field(
        default=None,
        description="A caption to display below the block",
        min_length=1,
        max_length=512,
    )


class OptionalNameMinx(DataBlock):
    # TODO: deprecate name and use id only
    name: str | None = Field(default=None, deprecated=True, exclude=True)

    @computed_field
    @property
    def id(self) -> str | None:
        return self.name

    @field_validator("name", mode="after")
    @classmethod
    def _validate_name(cls, v: str | None):
        if v and not is_valid_id(v):
            raise ValueError(f"Invalid name '{v}' for block")

        return v


class NameMixin(DataBlock):
    # TODO: deprecate name and use id only
    name: str = Field(..., deprecated=True, exclude=True)

    @computed_field
    @property
    def id(self) -> str | None:
        return self.name

    @field_validator("name", mode="after")
    @classmethod
    def _validate_name(cls, v: str):
        if not is_valid_id(v):
            raise ValueError(f"Invalid name '{v}' for block")

        return v
