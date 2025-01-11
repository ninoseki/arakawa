from __future__ import annotations

from typing import Literal

from pydantic import Field

from .base import DataBlock
from .fields import TypeAliasedField
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
    type_: Literal["DateTimeField", "DateField", "TimeField"] = Field(
        ..., alias="_type"
    )


class FileField(
    OptionalStringInitialMixin,
    OptionalRequiredMixin,
    OptionalValidationMixin,
    OptionalHelpMixin,
    ControlBlock,
):
    type_: Literal["FileField"] = TypeAliasedField()

    accept: str | None = Field(default=None)


class MultiChoiceField(
    OptionalRequiredMixin,
    OptionalValidationMixin,
    OptionalHelpMixin,
    ControlBlock,
):
    type_: Literal["MultiChoiceField"] = TypeAliasedField()

    initial: list[str] = Field(..., min_length=1)
    options: list[str] = Field(..., min_length=1)


class NumberBox(
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    ControlBlock,
):
    type_: Literal["NumberBox"] = TypeAliasedField()

    initial: int | float | None = Field(default=None)


class RangeField(
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    ControlBlock,
):
    type_: Literal["RangeField"] = TypeAliasedField()

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
    type_: Literal["ChoiceField"] = TypeAliasedField()

    options: list[str] = Field(..., min_length=1)


class SwitchField(
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    ControlBlock,
):
    type_: Literal["SwitchField"] = TypeAliasedField()

    initial: bool | None = Field(default=None)


class TagsField(
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    ControlBlock,
):
    type_: Literal["TagsField"] = TypeAliasedField()

    initial: list[str] = Field(..., min_length=1)


class TextBox(
    OptionalValidationMixin,
    OptionalStringInitialMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    ControlBlock,
):
    type_: Literal[
        "TextBox",
        "TextAreaField",
        "URLField",
        "EmailField",
        "SearchField",
        "TelephoneField",
        "PasswordField",
        "ColorField",
    ] = TypeAliasedField()


class HiddenField(ControlBlock):
    type_: Literal["HiddenField"] = TypeAliasedField()

    initial: str
