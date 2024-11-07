from __future__ import annotations

from .base import BlockId, DataBlock


class ControlBlock(DataBlock):
    pass


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
