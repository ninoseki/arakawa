from __future__ import annotations

from .base import BlockId, DataBlock


class ControlBlock(DataBlock):
    """
    Abstract block for all the control blocks.
    """


class BaseDateTimeBlock(ControlBlock):
    """
    Abstract block for DateTime, Date and Time blocks.
    """

    def __init__(
        self,
        name: BlockId,
        label: str | None = None,
        initial: str | None = None,
        required: bool | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            label (str | None, optional): A label. Defaults to None.
            initial (str | None, optional): An initial value. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
        """
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
        )


class DateTimeField(BaseDateTimeBlock):
    """
    DateTimeField allows you to add a datetime type input.
    """

    _tag = "DateTime"


class DateField(BaseDateTimeBlock):
    """
    DateField allows you to add a date type input.
    """

    _tag = "Date"


class TimeField(BaseDateTimeBlock):
    """
    TimeField allows you to add a time type input.
    """

    _tag = "Time"


class FileField(ControlBlock):
    """
    FileField allows you to add a file type input.
    """

    _tag = "File"

    def __init__(
        self,
        name: BlockId,
        label: str | None = None,
        required: bool | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
        """
        super().__init__(
            name=name,
            label=label,
            required=required,
        )


class MultiChoiceField(ControlBlock):
    """
    MultiChoiceField allows you to have a multiple select type input.
    """

    _tag = "MultiChoice"

    def __init__(
        self,
        name: BlockId,
        initial: list[str],
        options: list[str],
        label: str | None = None,
        required: bool | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            initial (list[str]): An initial value.
            options (list[str]): Options.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
        """
        super().__init__(
            initial=initial,
            options=options,
            name=name,
            label=label,
            required=required,
        )


class NumberBox(ControlBlock):
    """
    NumberBox allows you to add a number type input.
    """

    _tag = "NumberBox"

    def __init__(
        self,
        name: BlockId,
        label: str | None = None,
        initial: int | float | None = None,
        required: bool | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            label (str | None, optional): A label . Defaults to None.
            initial (int | float | None, optional): An initial value. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
        """
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
        )


class RangeField(ControlBlock):
    """
    RangeField allows you to add a range type input.
    """

    _tag = "Range"

    def __init__(
        self,
        name: BlockId,
        min_: int | float,
        max_: int | float,
        step: int | float,
        label: str | None = None,
        initial: int | float | None = None,
        required: bool | None = None,
    ):
        """
        Args:
            name (BlockId): Name.
            min_ (int | float): A min value.
            max_ (int | float): A max value.
            step (int | float): A step value.
            label (str | None, optional): A label. Defaults to None.
            initial (int | float | None, optional): An initial value. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
        """
        initial = initial or min_
        super().__init__(
            min=min_,
            max=max_,
            step=step,
            name=name,
            label=label,
            initial=initial,
            required=required,
        )


class ChoiceField(ControlBlock):
    """
    ChoiceField allows you to add a select type input.
    """

    _tag = "Choice"

    def __init__(
        self,
        name: BlockId,
        options: list[str],
        label: str | None = None,
        initial: str | None = None,
        required: bool | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            options (list[str]): Options.
            label (str | None, optional): A label. Defaults to None.
            initial (str | None, optional): An initial value. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
        """
        super().__init__(
            options=options,
            name=name,
            label=label,
            initial=initial,
            required=required,
        )


class SwitchField(ControlBlock):
    """
    SwitchField allows you to add a checkbox type input.
    """

    _tag = "Switch"

    def __init__(
        self,
        name: BlockId,
        label: str | None = None,
        initial: bool | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            label (str | None, optional): A label. Defaults to None.
            initial (bool | None, optional): An initial value. Defaults to None.
        """
        super().__init__(
            name=name,
            label=label,
            initial=initial,
        )


class TagsField(ControlBlock):
    """
    TagsField allows you to add a multi select type input along with the free form input.
    """

    _tag = "Tags"

    def __init__(
        self,
        name: BlockId,
        initial: list[str],
        label: str | None = None,
        required: bool | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            label (str | None, optional): A label. Defaults to None.
            initial (list[str]): An initial value.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
        """
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
        )


class TextBox(ControlBlock):
    """
    TextBox allows you to add a text type input.
    """

    _tag = "TextBox"

    def __init__(
        self,
        name: BlockId,
        label: str | None = None,
        initial: str | None = None,
        required: bool | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            label (str | None, optional): A label.. Defaults to None.
            initial (str | None, optional): An initial value. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
        """
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
        )
