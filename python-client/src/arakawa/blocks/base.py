from __future__ import annotations

import sys
from abc import ABC
from typing import TYPE_CHECKING, Any, ClassVar, TypeVar, Union, cast

from arakawa.common.utils import is_valid_id, mk_attribs
from arakawa.exceptions import ARError

if sys.version_info <= (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

if TYPE_CHECKING:
    from arakawa.blocks import Block
    from arakawa.view import ViewVisitor


BlockId = str

VV = TypeVar("VV", bound="ViewVisitor")


class BaseBlock(ABC):
    """Base Block class - subclassed by all Block types

    ..note:: The class is not used directly.
    """

    _tag: ClassVar[str]

    def __init__(self, name: BlockId | None = None, **kwargs: Any):
        """
        Args:
            name: A unique name to reference the block, used when referencing blocks via the report editor and when embedding
        """
        self._type = self._tag
        self.name = name

        # validate name
        if name and not is_valid_id(name):
            raise ARError(f"Invalid name '{name}' for block")

        self._add_attributes(**kwargs)

    def _add_attributes(self, **kwargs):
        attrs = mk_attribs(**kwargs)
        for key, value in attrs.items():
            setattr(self, key, value)

    def _ipython_display_(self):
        """Display the block as a side effect within a Jupyter notebook"""
        from IPython.display import HTML, display

        from arakawa.ipython.environment import get_environment
        from arakawa.processors.api import stringify_report
        from arakawa.view import Blocks

        if get_environment().support_rich_display:
            html_str = stringify_report(Blocks(self))
            display(HTML(html_str))
        else:
            display(self.__str__())

    def accept(self, visitor: VV) -> VV:
        visitor.visit(self)
        return visitor

    def copy(self) -> Self:
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        return inst

    def __copy__(self):
        return self.copy()


class DataBlock(BaseBlock):
    """Abstract block that represents a leaf-node in the tree, e.g. a Plot or Table

    ..note:: This class is not used directly.
    """


BlockOrPrimitive = Union[BaseBlock, Any]  # TODO - expand
BlockList = list[BaseBlock]


def wrap_block(b: BlockOrPrimitive) -> Block:
    from .wrappers import convert_to_block

    # if isinstance(b, Page):
    #     raise DPClientError("Page objects can only be at the top-level")
    if not isinstance(b, BaseBlock):
        # import here as a very slow module due to nested imports
        # from ..files import convert
        return convert_to_block(b)

    return cast("Block", b)
