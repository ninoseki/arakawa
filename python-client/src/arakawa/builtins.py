"""
Arakawa built-in helper functions to make creating your reports a bit simpler and reduce common tasks
"""

from __future__ import annotations

from pathlib import Path
from typing import cast

from . import Blocks
from . import blocks as b
from .types import NPath


def add_code(
    block: b.BlockOrPrimitive, code: str, language: str = "python"
) -> b.Select:
    """
    Attach code fragment to an existing plot/figure/dataframe for use within a report

    Args:
        block: The existing object to add code to - can be either an existing ar Block or an Python object
        code: The code fragment to add
        language: The language of the code fragment (optional)

    Returns:
        A Select block that provides the figure and the code in tabs that can be selected by the user
    """

    w_block = b.wrap_block(block)
    w_block._add_attributes(label="Figure")
    return b.Select(
        w_block, b.Code(code, language, label="Code"), type=b.SelectType.TABS
    )


def build_md_view(
    text_or_file: str | NPath,
    *args: b.BlockOrPrimitive,
    **kwargs: b.BlockOrPrimitive,
) -> Blocks:
    """
    An easy way to build a complete report from a single top-level markdown text / file template.
    Any additional context can be passed in and will be inserted into the Markdown template.

    Args:
        text_or_file: The markdown text, or path to a markdown file, using {{}} for templating
        *args: positional template context arguments
        **kwargs: keyword template context arguments

    Returns:
        An Arakawa App object for saving or uploading

    ..tip:: Either text or file is required as input
    ..tip:: Context, via args/kwargs can be plain Python objects, e.g. dataframes, and plots, or Arakawa blocks, e.g. ar.Plot, etc.

    """
    try:
        b_text = (
            b.Text(file=text_or_file)
            if Path(text_or_file).exists()
            else b.Text(text=cast(str, text_or_file))
        )
    except OSError:
        b_text = b.Text(text=cast(str, text_or_file))

    group = b_text.format(*args, **kwargs)
    return Blocks(group)
