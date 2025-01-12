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
    """Save a report as an HTML file.

    Args:
        blocks: A `Blocks` object or a list of Blocks.
        path: A file path to store the document.
        open: Open in your browser after creating. Default to False.
        name: A name of a report. Optional. Uses path if not provided.
        formatting: Sets the basic app styling.
        cdn_base: Base URL of CDN. Defaults to None.
        standalone: Whether or not to inline assets in an HTML instead of loading via CDN or not. Defaults to False.
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
    """Stringify a report as an HTML string.

    Args:
        blocks: A `Blocks` object or a list of Blocks.
        name: A name of a report. Optional. Uses path if not provided.
        formatting: Sets the basic app styling.
        cdn_base: Base URL of CDN. Defaults to None.
        resizable: Wether or not to allow make an iframed report resizable or not. Defaults to True.
        standalone: Whether or not to inline assets in an HTML instead of loading via CDN or not. Defaults to False.
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
