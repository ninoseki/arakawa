from __future__ import annotations

from functools import partial
from typing import Annotated

from pydantic import BeforeValidator, Field

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
    name: str | None = Field(
        default=None,
        description="A unique name for the block to reference when adding text or embedding",
    )


class NameMixin(DataBlock):
    name: str = Field(
        ...,
        description="A unique name for the block to reference when adding text or embedding",
    )
