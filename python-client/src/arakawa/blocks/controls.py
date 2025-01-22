from __future__ import annotations

from pydantic import Field, computed_field

from .base import DataBlock
from .mixins import NameMixin, OptionalLabelMixin


class ControlBlock(NameMixin, DataBlock):
    """
    Abstract block for all the control blocks.
    """

    @computed_field(alias="name")
    @property
    def name_(self) -> str:
        return self.name


class OptionalHelpMixin(DataBlock):
    help: str | None = Field(default=None)


class OptionalRequiredMixin(DataBlock):
    required: bool | None = Field(default=None)


class OptionalValidationMixin(DataBlock):
    validation: str | None = Field(default=None)


class OptionalStringInitialMixin(DataBlock):
    initial: str | None = Field(default=None)


class BaseDateTime(
    OptionalStringInitialMixin,
    OptionalRequiredMixin,
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalLabelMixin,
    ControlBlock,
):
    """
    Abstract block for DateTime, Date and Time blocks.
    """

    def __init__(
        self,
        name: str,
        help: str | None = None,
        initial: str | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (str): A name.
            help (str | None, optional): A help text. Defaults to None.
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
            help=help,
            validation=validation,
        )


class DateTimeField(BaseDateTime):
    """
    DateTimeField allows you to add a datetime type input.
    """

    _tag = "DateTimeField"

    __init__ = BaseDateTime.__init__


class DateField(BaseDateTime):
    """
    DateField allows you to add a date type input.
    """

    _tag = "DateField"

    __init__ = BaseDateTime.__init__


class TimeField(BaseDateTime):
    """
    TimeField allows you to add a time type input.
    """

    _tag = "TimeField"

    __init__ = BaseDateTime.__init__


class FileField(
    OptionalStringInitialMixin,
    OptionalRequiredMixin,
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalLabelMixin,
    ControlBlock,
):
    """
    FileField allows you to add a file type input.
    """

    _tag = "FileField"

    accept: str | None = Field(default=None)

    def __init__(
        self,
        name: str,
        accept: str | None = None,
        help: str | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (str): A name.
            help (str | None, optional): A help text. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
            accept (str | None, optional): An accept value. Defaults to None.
        """
        super().__init__(
            name=name,
            accept=accept,
            help=help,
            label=label,
            required=required,
            validation=validation,
        )


class MultiChoiceField(
    OptionalRequiredMixin,
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalLabelMixin,
    ControlBlock,
):
    """
    MultiChoiceField allows you to have a multiple select type input.
    """

    _tag = "MultiChoiceField"

    initial: list[str] = Field(..., min_length=1)
    options: list[str] = Field(..., min_length=1)

    def __init__(
        self,
        name: str,
        initial: list[str],
        options: list[str],
        help: str | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (str): A name.
            initial (list[str]): An initial value.
            options (list[str]): Options.
            help (str | None, optional): A help text. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        super().__init__(
            name=name,
            initial=initial,
            options=options,
            help=help,
            label=label,
            required=required,
            validation=validation,
        )


class NumberBox(
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    OptionalLabelMixin,
    ControlBlock,
):
    """
    NumberBox allows you to add a number type input.
    """

    _tag = "NumberBox"

    initial: int | float | None = Field(default=None)

    def __init__(
        self,
        name: str,
        help: str | None = None,
        initial: int | float | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (str): A name.
            help (str | None, optional): A help text. Defaults to None.
            initial (int | float | None, optional): An initial value. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        super().__init__(
            name=name,
            help=help,
            initial=initial,
            label=label,
            required=required,
            validation=validation,
        )


class RangeField(
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalLabelMixin,
    OptionalRequiredMixin,
    ControlBlock,
):
    """
    RangeField allows you to add a range type input.
    """

    _tag = "RangeField"

    initial: int | float = Field(...)
    min: int | float = Field(...)
    max: int | float = Field(...)
    step: int | float = Field(...)

    def __init__(
        self,
        name: str,
        min: int | float,
        max: int | float,
        step: int | float,
        help: str | None = None,
        initial: int | float | None = None,
        label: str | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (str): Name.
            min (int | float): A min value.
            max (int | float): A max value.
            step (int | float): A step value.
            help (str | None, optional): A help text. Defaults to None.
            initial (int | float | None, optional): An initial value. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        initial = initial or min
        super().__init__(
            name=name,
            help=help,
            initial=initial,
            label=label,
            max=max,
            min=min,
            step=step,
            validation=validation,
        )


class ChoiceField(
    OptionalValidationMixin,
    OptionalStringInitialMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    OptionalLabelMixin,
    ControlBlock,
):
    """
    ChoiceField allows you to add a select type input.
    """

    _tag = "ChoiceField"

    options: list[str] = Field(..., min_length=1)  # type: ignore

    def __init__(
        self,
        name: str,
        options: list[str],
        help: str | None = None,
        initial: str | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (str): A name.
            options (list[str]): Options.
            help (str | None, optional): A help text. Defaults to None.
            initial (str | None, optional): An initial value. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        super().__init__(
            name=name,
            options=options,
            help=help,
            initial=initial,
            label=label,
            required=required,
            validation=validation,
        )


class SwitchField(
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    OptionalLabelMixin,
    ControlBlock,
):
    """
    SwitchField allows you to add a checkbox type input.
    """

    _tag = "SwitchField"

    initial: bool | None = Field(default=None)

    def __init__(
        self,
        name: str,
        help: str | None = None,
        initial: bool | None = None,
        label: str | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (str): A name.
            help (str | None, optional): A help text. Defaults to None.
            initial (bool | None, optional): An initial value. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        super().__init__(
            name=name, help=help, initial=initial, label=label, validation=validation
        )


class TagsField(
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalRequiredMixin,
    OptionalLabelMixin,
    ControlBlock,
):
    """
    TagsField allows you to add a multi select type input along with the free form input.
    """

    _tag = "TagsField"

    initial: list[str] = Field(..., min_length=1)  # type: ignore

    def __init__(
        self,
        name: str,
        initial: list[str],
        help: str | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (str): A name.
            initial (list[str]): An initial value.
            help (str | None, optional): A help text. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            required (bool | None, optional): Whether it's required or not. Defaults to None.
            validation (str | None, optional): A formkit validation in addition to required. Defaults to None.
        """
        super().__init__(
            name=name,
            initial=initial,
            help=help,
            label=label,
            required=required,
            validation=validation,
        )


class BaseTextField(
    OptionalStringInitialMixin,
    OptionalRequiredMixin,
    OptionalValidationMixin,
    OptionalHelpMixin,
    OptionalLabelMixin,
    ControlBlock,
):
    caption: str | None = Field(default=None)
    help: str | None = Field(default=None)
    initial: str | None = Field(default=None)
    label: str | None = Field(default=None)
    required: bool | None = Field(default=None)
    validation: str | None = Field(default=None)

    def __init__(
        self,
        name: str,
        help: str | None = None,
        initial: str | None = None,
        label: str | None = None,
        required: bool | None = None,
        validation: str | None = None,
    ):
        """
        Args:
            name (str): A name.
            help (str | None, optional): A help text. Defaults to None.
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
            help=help,
        )


class TextBox(BaseTextField):
    """
    TextBox allows you to add a text type input.
    """

    _tag = "TextBox"

    __init__ = BaseTextField.__init__


class URLField(BaseTextField):
    """
    URLField allows you to add a url type input.
    """

    _tag = "URLField"

    __init__ = BaseTextField.__init__


class EmailField(BaseTextField):
    """
    EmailField allows you to add an email type input.
    """

    _tag = "EmailField"

    __init__ = BaseTextField.__init__


class SearchField(BaseTextField):
    """
    SearchField allows you to add a search type input.
    """

    _tag = "SearchField"

    __init__ = BaseTextField.__init__


class TelephoneField(BaseTextField):
    """
    TelephoneField allows you to add a tel type input.
    """

    _tag = "TelephoneField"

    __init__ = BaseTextField.__init__


class PasswordField(BaseTextField):
    """
    PasswordField allows you to add a password type input.
    """

    _tag = "PasswordField"

    __init__ = BaseTextField.__init__


class TextareaField(BaseTextField):
    """
    TextareaField allows you to add a search type input.
    """

    _tag = "TextareaField"

    __init__ = BaseTextField.__init__


class HiddenField(ControlBlock):
    """
    HiddenField allows you to add a hidden type input.
    """

    _tag = "HiddenField"

    initial: str = Field(...)

    def __init__(
        self,
        name: str,
        initial: str,
    ):
        """
        Args:
            name (str): A name.
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

    __init__ = BaseTextField.__init__
