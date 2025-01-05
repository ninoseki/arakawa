from __future__ import annotations

import secrets

from arakawa.types import NumberValue

from .base import BaseBlock, BlockId, DataBlock


def gen_name() -> str:
    """Return a (safe) name for use in a Block"""
    return f"id-{secrets.token_urlsafe(8)}"


class Empty(BaseBlock):
    """
    An empty block that can be updated / replaced later

    Args:
        name: A unique name for the block to reference when updating the report
    """

    _tag = "Empty"

    def __init__(self, name: BlockId):
        super().__init__(name=name)


class BigNumber(DataBlock):
    """
    A single number or change can often be the most important thing in an app.

    The `BigNumber`block allows you to present KPIs, changes, and statistics in a friendly way to your viewers.

    You can optionally set intent, and pass in numbers or text.
    """

    _tag = "BigNumber"

    def __init__(
        self,
        heading: str,
        value: NumberValue,
        change: NumberValue | None = None,
        prev_value: NumberValue | None = None,
        is_positive_intent: bool | None = None,
        is_upward_change: bool | None = None,
        name: BlockId | None = None,
        label: str | None = None,
    ):
        """
        Args:
            heading: A title that gives context to the displayed number
            value: The value of the number
            prev_value: The previous value to display as comparison (optional)
            change: The amount changed between the value and previous value (optional)
            is_positive_intent: Displays the change on a green background if `True`, and red otherwise. Follows `is_upward_change` if not set (optional)
            is_upward_change: Whether the change is upward or downward (required when `change` is set)
            name: A unique name for the block to reference when adding text or embedding (optional)
            label: A label used when displaying the block (optional)
        """
        if change:
            if is_upward_change is None:
                # We can't reliably infer the direction of change from the change string
                raise ValueError(
                    'Argument "is_upward_change" is required when "change" is set'
                )
            if is_positive_intent is None:
                # Set the intent to be the direction of change if not specified (up = green, down = red)
                is_positive_intent = is_upward_change

        super().__init__(
            heading=heading,
            value=value,
            change=change,
            prev_value=prev_value,
            is_positive_intent=bool(is_positive_intent),
            is_upward_change=bool(is_upward_change),
            name=name,
            label=label,
        )
