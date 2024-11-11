"""
Arakawa Processors

API for processing Views, e.g. rendering it locally and publishing to a remote server
"""

from __future__ import annotations

from arakawa.view import Blocks, BlocksT

from .file_store import B64FileEntry
from .processors import (
    ConvertXML,
    ExportHTMLInlineAssets,
    ExportHTMLStringInlineAssets,
    ExportHTMLStringInlineNonResizableAssets,
    PreProcessView,
)
from .types import Formatting, Pipeline, ViewState


################################################################################
def save_report(
    blocks: BlocksT,
    path: str,
    open: bool = False,
    name: str | None = None,
    formatting: Formatting | None = None,
    cdn_base: str | None = None,
) -> None:
    """Save the app document to a local HTML file

    Args:
        blocks: The `Blocks` object or a list of Blocks
        path: File path to store the document
        open: Open in your browser after creating (default: False)
        name: Name of the document (optional: uses path if not provided)
        formatting: Sets the basic app styling
    """
    s = ViewState(blocks=Blocks.wrap_blocks(blocks), file_entry_klass=B64FileEntry)
    _: str = (
        Pipeline(s)
        .pipe(PreProcessView(is_finalized=True))
        .pipe(ConvertXML())
        .pipe(
            ExportHTMLInlineAssets(
                path=path,
                open=open,
                name=name or "Report",
                formatting=formatting,
                cdn_base=cdn_base,
            )
        )
        .result
    )


def stringify_report(
    blocks: BlocksT,
    name: str | None = None,
    formatting: Formatting | None = None,
    cdn_base: str | None = None,
    resizable: bool = True,
) -> str:
    """Stringify the app document to a HTML string

    Args:
        blocks: The `Blocks` object or a list of Blocks
        name: Name of the document (optional: uses path if not provided)
        formatting: Sets the basic app styling
        resizable: Whether the app should be resizable. Defaults to True.
    """
    s = ViewState(blocks=Blocks.wrap_blocks(blocks), file_entry_klass=B64FileEntry)
    klass = (
        ExportHTMLStringInlineAssets
        if resizable
        else ExportHTMLStringInlineNonResizableAssets
    )
    export = klass(
        name=name or "Report",
        formatting=formatting,
        cdn_base=cdn_base,
    )
    return (
        Pipeline(s)
        .pipe(PreProcessView(is_finalized=False))
        .pipe(ConvertXML())
        .pipe(export)
        .result
    )
