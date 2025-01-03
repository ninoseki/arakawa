from __future__ import annotations

from typing import Literal

from pydantic import Field

from .base import DataBlock
from .mixins import NameMixin


class ControlBlock(NameMixin, DataBlock):
    pass


class OptionalHelpMixin(DataBlock):
    help: str | None = Field(default=None)


class OptionalRequiredMixin(DataBlock):
    required: bool | None = Field(default=None)


class OptionalValidationMixin(DataBlock):
    validation: str | None = Field(default=None)


class OptionalStringInitialMixin(DataBlock):
    initial: str | None = Field(default=None)


class DateTimeField(
    OptionalStringInitialMixin,
    OptionalRequiredMixin,
    OptionalValidationMixin,
    OptionalHelpMixin,
    ControlBlock,
):
    id: Literal["DateTimeField", "DateField", "TimeField"] = Field(..., alias="_id")


class FileField(
    OptionalStringInitialMixin,
    OptionalRequiredMixin,
    OptionalValidationMixin,
    OptionalHelpMixin,
    ControlBlock,
):
    id: Literal["FileField"] = Field(..., alias="_id")

    accept: str | None = Field(default=None)


class MultiChoiceField(
    OptionalRequiredMixin,
    OptionalValidationMixin,
    OptionalHelpMixin,
    ControlBlock,
):
    id: Literal["MultiChoiceField"] = Field(..., alias="_id")

    initial: list[str] = Field(..., min_length=1)
    options: list[str] = Field(..., min_length=1)


class NumberBox(
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    ControlBlock,
):
    id: Literal["NumberBox"] = Field(..., alias="_id")

    initial: int | float | None = Field(default=None)


class RangeField(
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    ControlBlock,
):
    id: Literal["RangeField"] = Field(..., alias="_id")

    initial: int | float
    min: int | float
    max: int | float
    step: int | float


class ChoiceField(
    OptionalValidationMixin,
    OptionalStringInitialMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    ControlBlock,
):
    id: Literal["ChoiceField"] = Field(..., alias="_id")

    options: list[str] = Field(..., min_length=1)


class SwitchField(
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    ControlBlock,
):
    id: Literal["SwitchField"] = Field(..., alias="_id")

    initial: bool | None = Field(default=None)


class TagsField(
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    ControlBlock,
):
    id: Literal["TagsField"] = Field(..., alias="_id")

    initial: list[str] = Field(..., min_length=1)


class TextBox(
    OptionalValidationMixin,
    OptionalStringInitialMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    ControlBlock,
):
    id: Literal[
        "TextBox",
        "TextAreaField",
        "URLField",
        "EmailField",
        "SearchField",
        "TelephoneField",
        "PasswordField",
        "ColorField",
    ] = Field(..., alias="_id")


class HiddenField(ControlBlock):
    id: Literal["HiddenField"] = Field(..., alias="_id")

    initial: str
