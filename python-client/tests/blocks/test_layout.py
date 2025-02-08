from __future__ import annotations

import pytest
from pydantic import ValidationError

from arakawa.blocks.layout import Group


@pytest.mark.parametrize(
    ("columns", "widths"),
    [
        (0, []),
        (1, [1]),
        (1, [1.0]),
        (2, [1, 2]),
        (2, [1, 2.0]),
    ],
)
def test_group(columns: int, widths: list[int | float]):
    assert Group("test", columns=columns, widths=widths)


@pytest.mark.parametrize(
    ("columns", "widths"),
    [
        # columns != len(widths)
        (1, []),
        (2, [1]),
        # negative columns
        (-1, [1]),
        # negative widths
        (1, [-1]),
        (1, [-1.0]),
        (2, [1, -1.0]),
    ],
)
def test_group_with_invalid_combination(columns: int, widths: list[int | float]):
    with pytest.raises(ValidationError):
        assert Group("test", columns=columns, widths=widths)
