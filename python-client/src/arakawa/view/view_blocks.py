from __future__ import annotations

from collections.abc import Mapping
from copy import copy
from typing import TYPE_CHECKING, Union

from lxml import etree
from lxml.etree import _Element as ElementT
from typing_extensions import Self

from arakawa.blocks import Group
from arakawa.blocks.base import BlockOrPrimitive
from arakawa.blocks.layout import ContainerBlock

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

    def get_dom(self) -> ElementT:
        """Return the Document structure for the View"""
        # internal debugging method
        from arakawa.processors.file_store import DummyFileEntry, FileStore

        from .xml_visitor import XMLBuilder

        builder = XMLBuilder(FileStore(DummyFileEntry))
        self.accept(builder)
        return builder.get_root()

    def get_dom_str(self) -> str:
        dom = self.get_dom()
        return etree.tostring(dom, pretty_print=True).decode()

    def pprint(self) -> None:
        from .visitors import PrettyPrinter

        self.accept(PrettyPrinter())

    @classmethod
    def wrap_blocks(cls, x: Self | list[BlockOrPrimitive] | BlockOrPrimitive) -> Self:
        if isinstance(x, Blocks):
            return copy(x)  # type: ignore

        if isinstance(x, list):
            return cls(*x)

        return cls(x)

    @property
    def has_compute(self):
        return False


class View(Blocks):
    pass


BlocksT = Union[
    Blocks,
    list[BlockOrPrimitive],
    Mapping[str, BlockOrPrimitive],
    BlockOrPrimitive,
]


class Report(Blocks):
    """
    App documents collate plots, text, tables, and files into an interactive document that
    can be analyzed and shared by users in their browser
    """

    def __init__(
        self,
        *arg_blocks: BlockOrPrimitive,
        blocks: list[BlockOrPrimitive] | None = None,
        **kwargs,
    ):
        super().__init__(*arg_blocks, blocks=blocks, **kwargs)

    def save(
        self,
        path: str,
        open: bool = False,
        name: str | None = None,
        formatting: Formatting | None = None,
        cdn_base: str | None = None,
    ) -> None:
        from ..processors import save_report

        save_report(
            blocks=self,
            path=path,
            open=open,
            name=name,
            formatting=formatting,
            cdn_base=cdn_base,
        )

    def stringify(
        self,
        name: str | None = None,
        formatting: Formatting | None = None,
        cdn_base: str | None = None,
        resizable: bool = True,
    ) -> str:
        from ..processors import stringify_report

        return stringify_report(
            blocks=self,
            name=name,
            formatting=formatting,
            cdn_base=cdn_base,
            resizable=resizable,
        )
