import dataclasses
from collections import namedtuple
from typing import TYPE_CHECKING, Any, Protocol

from lxml import etree
from lxml.builder import ElementMaker
from multimethod import DispatchError, multimethod
from typing_extensions import Self

from arakawa.blocks import BaseBlock
from arakawa.blocks.asset import AssetBlock
from arakawa.blocks.layout import ContainerBlock
from arakawa.blocks.text import EmbeddedTextBlock
from arakawa.common.viewxml_utils import ElementT, mk_attribs
from arakawa.exceptions import ARError
from arakawa.utils import log
from arakawa.view.view_blocks import Blocks
from arakawa.view.visitors import ViewVisitor

if TYPE_CHECKING:
    from arakawa.processors import FileEntry, FileStore

E = ElementMaker()  # XML Tag Factory


@dataclasses.dataclass
class XMLBuilder(ViewVisitor):
    """Convert the Blocks into an XML document"""

    store: "FileStore"
    # element: t.Optional[etree.Element] = None  # Empty Group Element?
    elements: list[ElementT] = dataclasses.field(default_factory=list)

    def get_root(self, fragment: bool = False) -> ElementT:
        """Return the top-level ViewXML"""
        # create the top-level

        # get the top-level root
        _top_group: ElementT = self.elements.pop()
        assert _top_group.tag == "Group"
        assert not self.elements

        # create top-level structure
        return E.View(  # type: ignore
            # E.Internal(),
            *_top_group.getchildren(),
            **mk_attribs(version="1", fragment=fragment),
        )

    @property
    def store_count(self) -> int:
        return len(self.store.files)

    def add_element(self, _: BaseBlock, e: Any) -> Self:
        """Add an element to the list of nodes at the current XML tree location"""
        self.elements.append(e)
        return self

    # xml convertors
    @multimethod
    def visit(self, b: BaseBlock) -> Self:
        """Base implementation - just created an empty tag including all the initial attributes"""
        _E = getattr(E, b._tag)  # noqa: N806
        return self.add_element(b, _E(**b._attributes))

    def _visit_subnodes(self, b: ContainerBlock) -> list[ElementT]:
        cur_elements = self.elements
        self.elements = []
        b.traverse(self)  # visit subnodes
        res = self.elements
        self.elements = cur_elements
        return res

    @visit.register  # type: ignore
    def _(self, b: ContainerBlock) -> Self:
        sub_elements = self._visit_subnodes(b)
        # build the element
        _E = getattr(E, b._tag)  # noqa: N806
        element = _E(*sub_elements, **b._attributes)
        return self.add_element(b, element)

    @visit.register  # type: ignore
    def _(self, b: Blocks) -> Self:
        sub_elements = self._visit_subnodes(b)

        # Blocks are converted to Group internally
        if label := b._attributes.get("label"):
            log.info(f"Found label {label} in top-level Blocks/View")
        element = E.Group(*sub_elements, columns="1", valign="top")
        return self.add_element(b, element)

    @visit.register  # type: ignore
    def _(self, b: EmbeddedTextBlock) -> Self:
        # NOTE - do we use etree.CDATA wrapper?
        _E = getattr(E, b._tag)  # noqa: N806
        return self.add_element(b, _E(etree.CDATA(b.content), **b._attributes))

    @visit.register  # type: ignore
    def _(self, b: AssetBlock):
        """Main XMl creation method - visitor method"""
        fe = self._add_asset_to_store(b)

        _E = getattr(E, b._tag)  # noqa: N806

        e: etree._Element = _E(
            type=fe.mime,
            # size=conv_attrib(fe.size),
            # hash=fe.hash,
            **{**b._attributes, **b.get_file_attribs()},
            # src=f"attachment://{self.store_count}",
            src=f"ref://{fe.hash}",
        )

        if b.caption:
            e.set("caption", b.caption)

        return self.add_element(b, e)

    def _add_asset_to_store(self, b: AssetBlock) -> "FileEntry":
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
