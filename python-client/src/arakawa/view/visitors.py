import abc
import dataclasses as dc
from collections.abc import Generator
from contextlib import contextmanager
from copy import copy
from typing import TYPE_CHECKING

from multimethod import multimethod

from arakawa import blocks as bk
from arakawa.blocks import BaseBlock
from arakawa.blocks.layout import ContainerBlock
from arakawa.exceptions import ARError
from arakawa.utils import log

from .view_blocks import Blocks

if TYPE_CHECKING:
    from arakawa.blocks.base import VV


@dc.dataclass
class ViewVisitor(abc.ABC):  # noqa: B024
    def visit(self: "VV", _: BaseBlock) -> "VV":
        return self


@dc.dataclass
class PrettyPrinter(ViewVisitor):
    """Print out the view in an indented, XML-like tree form"""

    indent: int = 1

    @multimethod
    def visit(self, b: BaseBlock):
        pass

    @visit.register  # type: ignore
    def _(self, b: ContainerBlock):
        self.indent += 2
        _ = b.traverse(self)
        self.indent -= 2


# TODO - split out into BlockBuilder helper here
@dc.dataclass
class PreProcess(ViewVisitor):
    """Block-level preprocessor, operations include,
    - Inline consecutive unnamed Text blocks
    - auto-column processing (TODO)

    We may need multiple passes here to make things easier

    We also transform the AST during the XMLBuilder visitor, and post-XML conversion in the ConvertXML processor.
    Where the transform should be placed is still under consideration, and depends on the nature of the transform.
    Some may be easier as a simple XSLT transform, others as more complex Python code operation either on the Blocks AST
    or the XML DOM via lxml.
    """

    in_collapsible_group: bool = False
    # is_finalized determines if we allow dynamic blocks or validate based on their static/current sub-blocks
    is_finalized: bool = True
    current_state: list[BaseBlock] = dc.field(default_factory=list)
    current_text: list[bk.Text] = dc.field(default_factory=list)

    @multimethod
    def visit(self, b: BaseBlock):
        self.merge_text()
        self.current_state.append(copy(b))

    @visit.register  # type: ignore
    def _(self, b: bk.Text):
        if b.name is None:
            self.current_text.append(b)
        else:
            self.merge_text()
            self.current_state.append(copy(b))

    @visit.register  # type: ignore
    def _(self, b: ContainerBlock):
        self.merge_text()

        if len(b.blocks) < b.report_minimum_blocks:
            msg = f"{b.__class__.__name__} has less than {b.report_minimum_blocks} objects"
            if self.is_finalized:
                raise ARError(msg)
            log.warning(msg)

        with self.fresh_state(b):
            self.in_collapsible_group = isinstance(b, Blocks) or (
                isinstance(b, bk.Group) and b.columns == 1
            )
            _ = b.traverse(self)
            self.merge_text()

    def merge_text(self):
        # log.debug("Merging text nodes")
        if self.current_text:
            t1: bk.Text  # noqa: F842

            if self.in_collapsible_group:
                new_text = "\n\n".join(t1.content for t1 in self.current_text)
                self.current_state.append(bk.Text(new_text))
            else:
                self.current_state.extend(copy(t1) for t1 in self.current_text)

            self.current_text = []

    @property
    def root(self) -> BaseBlock:
        return self.current_state[0]

    @contextmanager
    def fresh_state(self, b: ContainerBlock) -> Generator[None, None, None]:
        x = self.current_state
        self.current_state = []

        yield None

        # build a new instance of the container block
        b1 = copy(b)
        b1.blocks = self.current_state
        x.append(b1)
        self.current_state = x
