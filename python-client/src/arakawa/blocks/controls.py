from __future__ import annotations

from .base import BlockId, DataBlock


class ControlBlock(DataBlock):
    pass


class BaseDateTimeBlock(ControlBlock):
    def __init__(
        self,
        name: BlockId | None = None,
        label: str | None = None,
        initial: str | None = None,
        required: bool | None = None,
    ):
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
        )


class DateTime(BaseDateTimeBlock):
    _tag = "DateTime"


class Date(BaseDateTimeBlock):
    _tag = "Date"


class Time(BaseDateTimeBlock):
    _tag = "Time"


class File(ControlBlock):
    _tag = "File"

    def __init__(
        self,
        name: BlockId | None = None,
        label: str | None = None,
        required: bool | None = None,
    ):
        super().__init__(
            name=name,
            label=label,
            required=required,
        )


class MultiChoice(ControlBlock):
    _tag = "MultiChoice"

    def __init__(
        self,
        initial: list[str],
        options: list[str],
        name: BlockId | None = None,
        label: str | None = None,
        required: bool | None = None,
    ):
        super().__init__(
            initial=initial,
            options=options,
            name=name,
            label=label,
            required=required,
        )


class NumberBox(ControlBlock):
    _tag = "NumberBox"

    def __init__(
        self,
        name: BlockId | None = None,
        label: str | None = None,
        initial: int | float | None = None,
        required: bool | None = None,
    ):
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
        )


class Range(ControlBlock):
    _tag = "Range"

    def __init__(
        self,
        min: int | float,
        max: int | float,
        step: int | float,
        name: BlockId | None = None,
        label: str | None = None,
        initial: int | float | None = None,
        required: bool | None = None,
    ):
        super().__init__(
            min=min,
            max=max,
            step=step,
            name=name,
            label=label,
            initial=initial,
            required=required,
        )


class Choice(ControlBlock):
    _tag = "Choice"

    def __init__(
        self,
        options: list[str],
        name: BlockId | None = None,
        label: str | None = None,
        initial: str | None = None,
        required: bool | None = None,
    ):
        super().__init__(
            options=options,
            name=name,
            label=label,
            initial=initial,
            required=required,
        )


class Switch(ControlBlock):
    _tag = "Switch"

    def __init__(
        self,
        name: BlockId | None = None,
        label: str | None = None,
        initial: bool | None = None,
        required: bool | None = None,
    ):
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
        )


class Tags(ControlBlock):
    _tag = "Tags"

    def __init__(
        self,
        initial: list[str],
        name: BlockId | None = None,
        label: str | None = None,
        required: bool | None = None,
    ):
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
        )


class TextBox(ControlBlock):
    _tag = "TextBox"

    def __init__(
        self,
        name: BlockId | None = None,
        label: str | None = None,
        initial: str | None = None,
        required: bool | None = None,
    ):
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
        )
