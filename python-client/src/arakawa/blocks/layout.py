from __future__ import annotations

import sys
from collections import deque
from functools import reduce
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import (
    Field,
    NonNegativeInt,
    PositiveFloat,
    PositiveInt,
    field_validator,
    model_validator,
)

from arakawa.exceptions import ARError
from arakawa.types import ComputeMethod, SelectType, VAlign
from arakawa.utils import log

from .base import BlockOrPrimitive, DataBlock, wrap_block
from .misc_blocks import Empty
from .mixins import OptionalLabelMixin, OptionalNameMinx

if sys.version_info <= (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

if TYPE_CHECKING:
    from . import Block
    from .base import VV


class ContainerBlock(OptionalNameMinx, OptionalLabelMixin, DataBlock):
    """
    Abstract Block that supports nested/contained blocks
     - represents a subtree in the document
    """

    # TODO: don't use Any
    blocks: list[Any] = Field(..., min_length=1)

    # how many blocks must there be in the container
    report_minimum_blocks: ClassVar[int] = 1

    def __init__(
        self,
        *arg_blocks: BlockOrPrimitive,
        blocks: list[BlockOrPrimitive] | None = None,
        **kwargs,
    ):
        blocks = [wrap_block(b) for b in blocks or list(arg_blocks)]
        super().__init__(blocks=blocks, **kwargs)

    @field_validator("blocks", mode="after")
    @classmethod
    def _validate_blocks(cls, blocks: list[Any]):
        for b in blocks:
            assert isinstance(b, DataBlock), f"Invalid block type: {type(b)}"

        return blocks

    def __iter__(self):
        return BlockListIterator(self.blocks.__iter__())

    def __add__(self, other: Self) -> Self:
        self.blocks.extend(other.blocks)
        return self

    def __and__(self, other: Self) -> Self:
        self.blocks.extend(other.blocks)
        return self

    @classmethod
    def empty(cls) -> Self:
        return cls(blocks=[Empty()])

    def traverse(self, visitor: VV) -> VV:
        # perform a depth-first traversal of the contained blocks
        return reduce(
            lambda _visitor, block: block._accept(_visitor), self.blocks, visitor
        )


class Page(ContainerBlock):
    """
    Apps on Arakawa can have multiple pages, which are presented to users as tabs at the top of your app. These can be used similarly to sheets in an Excel document.

    To add a page, use the `ar.Page` block at the top-level of your app, and give it a title with the `title` parameter.

    !!! info
        Pages cannot be nested, and can only exist at the root level of your `ar.App` object. If you're using pages, all other blocks must be contained inside a Page block.

    !!! note
        This is included for backwards-compatibility, and can be replaced by using Selects going forwards.
    """

    _tag: str = "_Page"

    title: str | None = Field(default=None, min_length=1, max_length=256)

    def __init__(
        self,
        *arg_blocks: BlockOrPrimitive,
        blocks: list[BlockOrPrimitive] | None = None,
        title: str | None = None,
        name: str | None = None,
    ):
        """
        Args:
            *arg_blocks: Blocks to add to Page
            blocks: Allows providing the report blocks as a single list
            title: The page title (optional)
            name: A unique id for the Page to aid querying (optional)

        !!! tip
            Page can be passed using either arg parameters or the `blocks` kwarg, e.g. `ar.Page(group, select)` or `ar.Group(blocks=[group, select])`
        """
        super().__init__(*arg_blocks, blocks=blocks, title=title, name=name)
        if any(isinstance(b, Page) for b in self.blocks):
            raise ARError("Nested pages not supported, please use Selects and Groups")


class Select(ContainerBlock):
    """
    Selects act as a container that holds a list of nested Blocks objects, such
    as Tables, Plots, etc.. - but only one may be __visible__, or "selected", at once.

    The user can choose which nested object to view dynamically using either tabs or a dropdown.

    !!! note
        Select expects a list of Blocks, e.g. a Plot or Table, but also includes Select or Groups themselves, but if a Python object is passed, e.g. a Dataframe, Arakawa will attempt to convert it automatically.

    """

    _tag = "Select"
    report_minimum_blocks = 2

    type: SelectType = Field(...)

    def __init__(
        self,
        *arg_blocks: BlockOrPrimitive,
        blocks: list[BlockOrPrimitive] | None = None,
        type: SelectType = SelectType.TABS,
        name: str | None = None,
        label: str | None = None,
    ):
        """
        Args:
            *arg_blocks: Page to add to report
            blocks: Allows providing the report blocks as a single list
            type: An instance of SelectType that indicates if the select should use tabs or a dropdown (default: Tabs)
            name: A unique id for the blocks to aid querying (optional)
            label: A label used when displaying the block (optional)

        !!! tip
            Select can be passed using either arg parameters or the `blocks` kwarg, e.g. `ar.Select(table, plot, type=ar.SelectType.TABS)` or `ar.Select(blocks=[table, plot])`
        """
        super().__init__(*arg_blocks, blocks=blocks, name=name, label=label, type=type)
        if len(self.blocks) < self.report_minimum_blocks:
            log.info("Creating a Select with less than 2 objects")


class Group(ContainerBlock):
    """
    If you pass a list of blocks (such as `Plot` and `Table`) to an app, they are -- by default -- laid out in a single column with a row per block.

    If you would like to customize the rows and columns, Arakawa provides a `Group` block which takes a list of blocks and a number of columns and lays them out in a grid.

    !!! tip
        As `Group` blocks are blocks themselves, they are composable, and you can create more custom layers of nested blocks, for instance nesting 2 rows in the left column of a 2 column layout
    """

    _tag = "Group"

    columns: NonNegativeInt = Field(default=1)
    valign: VAlign
    widths: list[PositiveInt | PositiveFloat] | None = Field(default=None)

    @model_validator(mode="after")
    def _validate_columns_and_widths(self):
        if self.widths is None:
            return self

        if len(self.widths) != self.columns:
            raise ValueError(
                "Group 'widths' list length does not match number of columns"
            )

        return self

    def __init__(
        self,
        *arg_blocks: BlockOrPrimitive,
        blocks: list[BlockOrPrimitive] | None = None,
        name: str | None = None,
        label: str | None = None,
        widths: list[int | float] | None = None,
        valign: VAlign = VAlign.TOP,
        columns: int = 1,
    ):
        """
        Args:
            *arg_blocks: Group to add to report
            blocks: Allows providing the report blocks as a single list
            name: A unique id for the blocks to aid querying (optional)
            label: A label used when displaying the block (optional)
            widths: A list of numbers representing the proportion of vertical space given to each column (optional)
            valign: The vertical alignment of blocks in the Group (default = VAlign.TOP)
            columns: Display the contained blocks, e.g. Plots, using _n_ columns (default = 1), setting to 0 auto-wraps the columns

        !!! note
            Group can be passed using either arg parameters or the `blocks` kwarg, e.g. `ar.Group(plot, table, columns=2)` or `ar.Group(blocks=[plot, table], columns=2)`.
        """
        return super().__init__(
            *arg_blocks,
            blocks=blocks,
            name=name,
            label=label,
            widths=widths,
            valign=valign,
            columns=columns,
        )


class Toggle(ContainerBlock):
    """
    Toggles act as a container that holds a list of nested Block objects, whose visibility can be toggled on or off by the report viewer
    """

    _tag = "Toggle"

    report_minimum_blocks = 1

    def __init__(
        self,
        *arg_blocks: BlockOrPrimitive,
        blocks: list[BlockOrPrimitive] | None = None,
        name: str | None = None,
        label: str | None = None,
    ):
        """
        Args:
            *arg_blocks: Group to add to report
            blocks: Allows providing the report blocks as a single list
            name: A unique id for the blocks to aid querying (optional)
            label: A label used when displaying the block (optional)
        """
        super().__init__(*arg_blocks, blocks=blocks, name=name, label=label)
        self._wrap_blocks()

    def _wrap_blocks(self) -> None:
        """Wrap the list of blocks in a top-level block element if needed"""
        if len(self.blocks) > 1:
            # only wrap if not all blocks are a Group object
            self.blocks = [Group(blocks=self.blocks)]


class Compute(ContainerBlock):
    """
    Compute acts as a container that holds a list of ControlBlock objects to compose an HTML form.
    """

    _tag = "Compute"

    prompt: str | None = Field(default=None)
    subtitle: str | None = Field(default=None)
    action: str | None = Field(default="")
    method: ComputeMethod = Field(default=ComputeMethod.GET)

    def __init__(
        self,
        *arg_blocks: BlockOrPrimitive,
        blocks: list[BlockOrPrimitive] | None = None,
        name: str | None = None,
        label: str | None = None,
        prompt: str | None = None,
        subtitle: str | None = None,
        action: str | None = "",
        method: ComputeMethod = ComputeMethod.GET,
    ):
        """
        Args:
            *arg_blocks: Compute to add to report.
            blocks (list[BlockOrPrimitive] | None, optional): Blocks to compose a form. Defaults to None.
            name (str | None, optional): A name. Defaults to None.
            label (str | None, optional): A label. Defaults to None.
            prompt (str | None, optional): A prompt. Defaults to None.
            subtitle (str | None, optional): A subtitle. Defaults to None.
            action (str | None, optional): The form action. Defaults to "".
            method (MethodType, optional): The form method. Defaults to MethodType.GET.
        """
        super().__init__(
            *arg_blocks,
            action=action or "",
            method=method,
            blocks=blocks,
            name=name,
            label=label,
            prompt=prompt,
            subtitle=subtitle,
        )


class BlockListIterator:
    """
    Wrapper around default list iterator that supports depth-first traversal of blocks.
    """

    def __init__(self, _iter):
        # linearize all blocks into a deque as we traverse
        self.nested = deque(_iter)

    def __next__(self) -> Block:
        try:
            b: Block = self.nested.popleft()
        except IndexError as e:
            raise StopIteration() from e

        if isinstance(b, ContainerBlock):
            # add the nested iter contents for next "next" call, hence traversing the tree
            self.nested.extendleft(reversed(b.blocks))
        return b

    def __iter__(self):
        return self
