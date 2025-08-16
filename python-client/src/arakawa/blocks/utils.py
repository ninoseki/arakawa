from __future__ import annotations

import json
import math
import secrets
from collections.abc import Sized
from numbers import Number
from typing import Annotated, Any

from pydantic import BeforeValidator


def gen_name() -> str:
    """Return a (safe) name for use in a Block"""
    return f"id-{secrets.token_urlsafe(8)}"


def convert_optional_str_or_number(v: Any) -> str | None:
    """
    Convert a value to a str for use as an ElementBuilder attribute
    - also handles None to a string for optional field values
    """
    if v is None:
        return v

    if isinstance(v, Sized) and len(v) == 0:
        return None

    if isinstance(v, str):
        return v

    if isinstance(v, Number) and not isinstance(v, bool):
        if math.isinf(v) and v > 0:  # type: ignore
            return "INF"

        if math.isinf(v) and v < 0:  # type: ignore
            return "-INF"

        if math.isnan(v):  # type: ignore
            return "NaN"

        return str(v)

    return json.dumps(v)


def convert_str_or_number(v: Any) -> str:
    """
    Convert a value to a str for use as an ElementBuilder attribute
    - also handles None to a string for optional field values
    """
    converted = convert_optional_str_or_number(v)
    if converted is None:
        raise ValueError("Value cannot be None or nullable")

    return converted


OptionalNumberStr = Annotated[
    str | None, BeforeValidator(convert_optional_str_or_number)
]
NumberStr = Annotated[str, BeforeValidator(convert_str_or_number)]
