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
        help_: str | None = None,
        initial: str | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            help_ (str | None, optional): A help text. Defaults to None.
            initial (str | None, optional): An initial value. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
            help=help_,
            validation=validation,
        )


class DateTimeField(BaseDateTimeBlock):
    """
    DateTimeField allows you to add a datetime type input.
    """

    _tag = "DateTimeField"


class DateField(BaseDateTimeBlock):
    """
    DateField allows you to add a date type input.
    """

    _tag = "DateField"


class TimeField(BaseDateTimeBlock):
    """
    TimeField allows you to add a time type input.
    """

    _tag = "TimeField"


class FileField(ControlBlock):
    """
    FileField allows you to add a file type input.
    """

    _tag = "FileField"

    def __init__(
        self,
        name: BlockId,
        accept: str | None = None,
        help_: str | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            help_ (str | None, optional): A help text. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
            accept (str | None, optional): An accept value. Defaults to None.
        """
        super().__init__(
            name=name,
            label=label,
            required=required,
            help=help_,
            validation=validation,
            accept=accept,
        )


class MultiChoiceField(ControlBlock):
    """
    MultiChoiceField allows you to have a multiple select type input.
    """

    _tag = "MultiChoiceField"

    def __init__(
        self,
        name: BlockId,
        initial: list[str],
        options: list[str],
        help_: str | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            initial (list[str]): An initial value.
            options (list[str]): Options.
            help_ (str | None, optional): A help text. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        super().__init__(
            initial=initial,
            options=options,
            name=name,
            label=label,
            required=required,
            help=help_,
            validation=validation,
        )


class NumberBox(ControlBlock):
    """
    NumberBox allows you to add a number type input.
    """

    _tag = "NumberBox"

    def __init__(
        self,
        name: BlockId,
        help_: str | None = None,
        initial: int | float | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            help_ (str | None, optional): A help text. Defaults to None.
            initial (int | float | None, optional): An initial value. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
            help=help_,
            validation=validation,
        )


class RangeField(ControlBlock):
    """
    RangeField allows you to add a range type input.
    """

    _tag = "RangeField"

    def __init__(
        self,
        name: BlockId,
        min_: int | float,
        max_: int | float,
        step: int | float,
        help_: str | None = None,
        initial: int | float | None = None,
        label: str | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (BlockId): Name.
            min_ (int | float): A min value.
            max_ (int | float): A max value.
            step (int | float): A step value.
            help_ (str | None, optional): A help text. Defaults to None.
            initial (int | float | None, optional): An initial value. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        initial = initial or min_
        super().__init__(
            min=min_,
            max=max_,
            step=step,
            name=name,
            label=label,
            initial=initial,
            help=help_,
            validation=validation,
        )


class ChoiceField(ControlBlock):
    """
    ChoiceField allows you to add a select type input.
    """

    _tag = "ChoiceField"

    def __init__(
        self,
        name: BlockId,
        options: list[str],
        help_: str | None = None,
        initial: str | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            options (list[str]): Options.
            help_ (str | None, optional): A help text. Defaults to None.
            initial (str | None, optional): An initial value. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        super().__init__(
            options=options,
            name=name,
            label=label,
            initial=initial,
            required=required,
            help=help_,
            validation=validation,
        )


class SwitchField(ControlBlock):
    """
    SwitchField allows you to add a checkbox type input.
    """

    _tag = "SwitchField"

    def __init__(
        self,
        name: BlockId,
        help_: str | None = None,
        initial: bool | None = None,
        label: str | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            help_ (str | None, optional): A help text. Defaults to None.
            initial (bool | None, optional): An initial value. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            help=help_,
            validation=validation,
        )


class TagsField(ControlBlock):
    """
    TagsField allows you to add a multi select type input along with the free form input.
    """

    _tag = "TagsField"

    def __init__(
        self,
        name: BlockId,
        initial: list[str],
        help_: str | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            initial (list[str]): An initial value.
            help_ (str | None, optional): A help text. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
            help=help_,
            validation=validation,
        )


class BaseTextField(ControlBlock):
    def __init__(
        self,
        name: BlockId,
        help_: str | None = None,
        initial: str | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (BlockId): A name.
            help_ (str | None, optional): A help text. Defaults to None.
            initial (str | None, optional): An initial value. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        super().__init__(
            name=name,
            label=label,
            initial=initial,
            required=required,
            validation=validation,
            help=help_,
        )


class TextBox(BaseTextField):
    """
    TextBox allows you to add a text type input.
    """

    _tag = "TextBox"


class URLField(BaseTextField):
    """
    URLField allows you to add a url type input.
    """

    _tag = "URLField"


class EmailField(BaseTextField):
    """
    EmailField allows you to add an email type input.
    """

    _tag = "EmailField"


class SearchField(BaseTextField):
    """
    SearchField allows you to add a search type input.
    """

    _tag = "SearchField"


class TelephoneField(BaseTextField):
    """
    TelephoneField allows you to add a tel type input.
    """

    _tag = "TelephoneField"


class PasswordField(BaseTextField):
    """
    PasswordField allows you to add a password type input.
    """

    _tag = "PasswordField"


class TextareaField(BaseTextField):
    """
    TextareaField allows you to add a search type input.
    """

    _tag = "TextareaField"


class HiddenField(ControlBlock):
    """
    HiddenField allows you to add a hidden type input.
    """

    _tag = "HiddenField"

    def __init__(
        self,
        name: BlockId,
        initial: str,
    ):
        """
        Args:
            name (BlockId): A name.
            initial (str): An initial value.
        """
        super().__init__(
            name=name,
            initial=initial,
        )


class ColorField(BaseTextField):
    """
    ColorField allows you to add a color picker.
    """

    _tag = "ColorField"
