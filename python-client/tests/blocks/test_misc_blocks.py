from typing import Any

import numpy as np
import pytest

from arakawa.blocks.misc_blocks import BigNumber


@pytest.mark.parametrize(
    ("block", "expected"),
    [
        (
            BigNumber(
                heading="test",
                value=np.int64(2),
                prev_value=np.int64(1),
                change=np.int64(1),
                is_upward_change=True,
            ),
            {
                "heading": "test",
                "value": "2",
                "prevValue": "1",
                "change": "1",
                "_tag": "BigNumber",
                "isPositiveIntent": True,
                "isUpwardChange": True,
            },
        ),
        (
            BigNumber(
                heading="test",
                value=np.int64(1),
                change=None,
            ),
            {
                "heading": "test",
                "value": "1",
                "_tag": "BigNumber",
                "isPositiveIntent": False,
                "isUpwardChange": False,
            },
        ),
    ],
)
def test_big_number_annotations(block: BigNumber, expected: Any):
    dumped = block.model_dump(by_alias=True, exclude_none=True)
    assert dumped == expected
