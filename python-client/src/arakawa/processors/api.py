"""
Arakawa Processors

API for processing Views, e.g. rendering it locally and publishing to a remote server
"""

from __future__ import annotations

from arakawa.view import Blocks, BlocksT

from .file_store import B64FileEntry
from .processors import (
    ConvertPydantic,
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
    standalone: bool = False,
) -> None:
    """Save the app document to a local HTML file

    Args:
        blocks: The `Blocks` object or a list of Blocks
        path: File path to store the document
        open: Open in your browser after creating (default: False)
        name: Name of the document (optional: uses path if not provided)
        formatting: Sets the basic app styling
        cdn_base: Base URL of CDN. Defaults to None.
        standalone: Inline the app source in the HTML app file rather than loading via CDN. Defaults to False.
    """
    s = ViewState(blocks=Blocks.wrap_blocks(blocks), file_entry_klass=B64FileEntry)

    _ = (
        Pipeline(s)
        .pipe(PreProcessView(is_finalized=True))
        .pipe(ConvertPydantic())
        .pipe(
            ExportHTMLInlineAssets(
                path=path,
                open=open,
                name=name or "Report",
                formatting=formatting,
                cdn_base=cdn_base,
                standalone=standalone,
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
    standalone: bool = False,
) -> str:
    """Stringify the app document to a HTML string

    Args:
        blocks: The `Blocks` object or a list of Blocks
        name: Name of the document (optional: uses path if not provided)
        formatting: Sets the basic app styling
        resizable: Whether the app should be resizable. Defaults to True.
        cdn_base: Base URL of CDN. Defaults to None.
        standalone: Inline the app source in the HTML app file rather than loading via CDN. Defaults to False.
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
        standalone=standalone,
    )
    return (
        Pipeline(s)
        .pipe(PreProcessView(is_finalized=True))
        .pipe(ConvertPydantic())
        .pipe(export)
        .result
    )
