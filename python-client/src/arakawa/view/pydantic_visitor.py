from __future__ import annotations

import dataclasses
import sys
from collections import namedtuple
from typing import TYPE_CHECKING, Any, Protocol, cast

from multimethod import DispatchError, multimethod

from arakawa import schemas
from arakawa.blocks import BaseBlock, Group
from arakawa.blocks.asset import AssetBlock
from arakawa.blocks.layout import ContainerBlock
from arakawa.blocks.text import EmbeddedTextBlock
from arakawa.exceptions import ARError
from arakawa.types import VAlign
from arakawa.utils import log
from arakawa.view.view_blocks import Blocks
from arakawa.view.visitors import ViewVisitor

if sys.version_info <= (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

if TYPE_CHECKING:
    from arakawa.processors import FileEntry, FileStore


@dataclasses.dataclass
class PydanticBuilder(ViewVisitor):
    store: FileStore
    elements: list[BaseBlock] = dataclasses.field(default_factory=list)

    _seen_names: set[str] = dataclasses.field(default_factory=set)

    def get_root(self, fragment: bool = False):
        _top_group = cast(Group, self.elements.pop())
        assert _top_group._type == "Group"
        assert not self.elements

        return schemas.View.model_validate(
            {
                "_type": "View",
                "fragment": fragment,
                "version": 1,
                "blocks": _top_group.blocks,
            }
        )

    @property
    def store_count(self) -> int:
        return len(self.store.files)

    def add_element(self, _: BaseBlock, e: BaseBlock) -> Self:
        """Add an element to the list of nodes at the current XML tree location"""
        self.elements.append(e)

        name: str | None = getattr(e, "name", None)
        if name:
            if name in self._seen_names:
                raise ARError(f"Duplicate name {name} found in the View")

            self._seen_names.add(name)

        return self

    @multimethod
    def visit(self, b: BaseBlock) -> Self:
        """Base implementation - just created an empty tag including all the initial attributes"""
        return self.add_element(b, b)

    def _visit_subnodes(self, b: ContainerBlock):
        cur_elements = self.elements
        self.elements = []
        b.traverse(self)  # visit subnodes
        res = self.elements
        self.elements = cur_elements
        return res

    @visit.register  # type: ignore
    def _(self, b: ContainerBlock) -> Self:
        sub_elements = self._visit_subnodes(b)
        b._add_attributes(blocks=sub_elements)
        return self.add_element(b, b)

    @visit.register  # type: ignore
    def _(self, b: Blocks) -> Self:
        sub_elements = self._visit_subnodes(b)

        # Blocks are converted to Group internally
        if label := getattr(b, "label", None):
            log.info(f"Found label {label} in top-level Blocks/View")

        element = Group(
            blocks=sub_elements,
            name=b.name,
            label=label,
            columns=1,
            valign=VAlign.TOP,
        )
        return self.add_element(b, element)

    @visit.register  # type: ignore
    def _(self, b: EmbeddedTextBlock) -> Self:
        return self.add_element(b, b)

    @visit.register  # type: ignore
    def _(self, b: AssetBlock):
        fe = self._add_asset_to_store(b)

        element = b.copy()
        element._add_attributes(
            type=fe.mime,
            src=f"ref://{fe.hash}",
        )
        return self.add_element(b, element)

    def _add_asset_to_store(self, b: AssetBlock) -> FileEntry:
        """Default asset store handler that operates on native Python objects"""
        # import here as a very slow module due to nested imports
        # from .. import files

        # check if we already have stored this asset to the store
        # TODO - do we just persist the asset store across the session??
        if b._prev_entry:
            if type(b._prev_entry) == self.store.fw_klass:  # noqa: E721
                self.store.add_file(b._prev_entry)
                return b._prev_entry
            b._prev_entry = None

        if b.data is not None:
            # fe = files.add_to_store(self.data, s.store)
            try:
                writer = get_writer(b)
                meta: AssetMeta = writer.get_meta(b.data)
                fe = self.store.get_file(meta.ext, meta.mime)
                writer.write_file(b.data, fe.file)
                self.store.add_file(fe)
            except DispatchError as e:
                raise ARError(
                    f"{type(b.data).__name__} not supported for {self.__class__.__name__}"
                ) from e
        elif b.file is not None:
            fe = self.store.load_file(b.file)
        else:
            raise ARError("No asset to add")

        b._prev_entry = fe
        return fe


AssetMeta = namedtuple("AssetMeta", "ext mime")


class AssetWriterP(Protocol):
    """Implement these in any class to support asset writing
    for a particular AssetBlock"""

    def get_meta(self, x: Any) -> AssetMeta: ...

    def write_file(self, x: Any, f) -> None: ...


def get_writer(b: AssetBlock) -> AssetWriterP:
    import arakawa.blocks.asset as a

    from . import asset_writers as aw

    if isinstance(b, a.Plot):
        return aw.PlotWriter()

    if isinstance(b, a.Table):
        return aw.HTMLTableWriter()  # type: ignore

    if isinstance(b, a.Attachment):
        return aw.AttachmentWriter()

    if isinstance(b, a.DataTable):
        return aw.DataTableWriter()  # type: ignore

    raise KeyError(f"No writer found for {type(b).__name__}")
