from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, TypeVar

from pydantic import BaseModel, ConfigDict, computed_field

if TYPE_CHECKING:
    from arakawa.view import ViewVisitor


VV = TypeVar("VV", bound="ViewVisitor")


class BaseBlock(BaseModel):
    """Base Block class - subclassed by all Block types

    ..note:: The class is not used directly.
    """

    _tag: ClassVar[str]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @computed_field(alias="_tag")
    @property
    def computed_tag(self) -> str:
        return self._tag

    @computed_field
    @property
    def id(self) -> str | None:
        raise NotImplementedError("id property must be implemented in subclass")

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

    def _accept(self, visitor: VV) -> VV:
        # NOTE: use underscore prefix to avoid conflict
        visitor.visit(self)
        return visitor


class DataBlock(BaseBlock):
    """Abstract block that represents a leaf-node in the tree, e.g. a Plot or Table

    ..note:: This class is not used directly.
    """


BlockOrPrimitive = BaseBlock | Any  # TODO - expand
BlockList = list[BaseBlock]


def wrap_block(b: BlockOrPrimitive) -> BaseBlock:
    from .wrappers import convert_to_block

    # if isinstance(b, Page):
    #     raise DPClientError("Page objects can only be at the top-level")
    if not isinstance(b, BaseBlock):
        # import here as a very slow module due to nested imports
        # from ..files import convert
        return convert_to_block(b)

    return b
