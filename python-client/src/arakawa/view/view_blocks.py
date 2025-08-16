from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import TYPE_CHECKING

from pydantic import Field, field_validator

from arakawa.blocks import Block, Group, Page
from arakawa.blocks.base import BlockOrPrimitive
from arakawa.blocks.layout import ContainerBlock

if sys.version_info <= (3, 11):
    from typing_extensions import Self
else:
    from typing import Self


if TYPE_CHECKING:
    from arakawa.processors.types import Formatting


class Blocks(ContainerBlock):
    """Container that holds a collection of blocks"""

    # This is essentially an easy-to-use wrapper around a list of blocks
    # that is composable.
    # TODO - move to arakawa.blocks ?

    _tag = "Blocks"

    def __init__(
        self,
        *arg_blocks: BlockOrPrimitive,
        blocks: list[BlockOrPrimitive] | None = None,
        **kwargs,
    ):
        # if passed a single View into a View object, pull out the contained blocks and use instead
        if len(arg_blocks) == 1 and isinstance(arg_blocks[0], Blocks):
            arg_blocks = tuple(arg_blocks[0].blocks)

        super().__init__(*arg_blocks, blocks=blocks, **kwargs)

    def __or__(self, other: Self):
        x = Group(blocks=self.blocks) if len(self.blocks) > 1 else self.blocks[0]
        y = Group(blocks=other.blocks) if len(other.blocks) > 1 else other.blocks[0]
        z = Group(x, y, columns=2)
        return Blocks(z)

    @classmethod
    def from_notebook(
        cls,
        opt_out: bool = True,
        show_code: bool = False,
        show_markdown: bool = True,
        template: str = "auto",
    ) -> Self:
        from arakawa.ipython import templates as ip_t
        from arakawa.ipython.utils import cells_to_blocks

        blocks = cells_to_blocks(
            opt_out=opt_out, show_code=show_code, show_markdown=show_markdown
        )
        app_template_cls = ip_t._registry.get(template) or ip_t.guess_template(blocks)
        app_template = app_template_cls(blocks)
        app_template.transform()
        app_template.validate()
        return cls(blocks=app_template.blocks)

    def get_view(self):
        from arakawa.file_store import DummyFileEntry, FileStore

        from .pydantic_visitor import PydanticBuilder

        builder = PydanticBuilder(FileStore(DummyFileEntry))
        self._accept(builder)
        return builder.get_root()

    def pprint(self) -> None:
        from .visitors import PrettyPrinter

        self._accept(PrettyPrinter())

    @classmethod
    def wrap_blocks(cls, x: Self | list[BlockOrPrimitive] | BlockOrPrimitive) -> Self:
        if isinstance(x, Blocks):
            return x.model_copy()  # type: ignore

        if isinstance(x, list):
            return cls(*x)

        return cls(x)


class ViewBlock(ContainerBlock):
    _tag = "View"

    fragment: bool = Field(...)
    version: str = Field(...)

    @field_validator("blocks", mode="after")
    @classmethod
    def _validate_blocks(cls, blocks: list[Block]):
        for b in blocks:
            if isinstance(b, ContainerBlock):
                for nested in b.blocks:
                    assert not isinstance(nested, Page), (
                        "Layout block cannot contain Page block"
                    )

        return blocks


class View(Blocks):
    """
    The `View` block is a top-level block that contains all the blocks that make up the report. It is the root of the report tree.
    """

    __init__ = Blocks.__init__


BlocksT = (
    Blocks | list[BlockOrPrimitive] | Mapping[str, BlockOrPrimitive] | BlockOrPrimitive
)


class Report(Blocks):
    """
    App documents collate plots, text, tables, and files into an interactive document that
    can be analyzed and shared by users in their browser
    """

    __init__ = Blocks.__init__

    def save(
        self,
        path: str,
        open: bool = False,
        name: str | None = None,
        formatting: Formatting | None = None,
        cdn_base: str | None = None,
        standalone: bool = False,
    ) -> None:
        """Save a report as an HTML file.

        Args:
            path: A file path to store the document.
            open: Open in your browser after creating. Default to False.
            name: A name of a report. Optional. Uses path if not provided.
            formatting: Sets the basic app styling.
            cdn_base: Base URL of CDN. Defaults to None.
            standalone: Whether or not to inline assets in an HTML instead of loading via CDN or not. Defaults to False.
        """
        from ..processors import save_report

        save_report(
            blocks=self,
            path=path,
            open=open,
            name=name,
            formatting=formatting,
            cdn_base=cdn_base,
            standalone=standalone,
        )

    def stringify(
        self,
        name: str | None = None,
        formatting: Formatting | None = None,
        cdn_base: str | None = None,
        resizable: bool = True,
        standalone: bool = False,
    ) -> str:
        """Stringify a report as an HTML string.

        Args:
            name: A name of a report. Optional. Uses path if not provided.
            formatting: Sets the basic app styling.
            cdn_base: Base URL of CDN. Defaults to None.
            resizable: Wether or not to allow make an iframed report resizable or not. Defaults to True.
            standalone: Whether or not to inline assets in an HTML instead of loading via CDN or not. Defaults to False.
        """
        from ..processors import stringify_report

        return stringify_report(
            blocks=self,
            name=name,
            formatting=formatting,
            cdn_base=cdn_base,
            resizable=resizable,
            standalone=standalone,
        )
