"""Asset-based blocks"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, cast

import pandas as pd
from pandas.io.formats.style import Styler
from pydantic import AnyUrl, Field

from arakawa.common.df_processor import to_df
from arakawa.file_store import FileEntry
from arakawa.types import NPath

from .base import DataBlock
from .mixins import OptionalCaptionMixin, OptionalLabelMixin, OptionalNameMinx


class AssetBlock(OptionalNameMinx, OptionalCaptionMixin, OptionalLabelMixin, DataBlock):
    """
    AssetBlock objects form basis of all File-related blocks (abstract class, not exported)
    """

    prev_entry: FileEntry | None = Field(default=None, exclude=True)

    data: Any = Field(default=None, exclude=True)
    file: NPath | None = Field(default=None, exclude=True)

    src: AnyUrl | None = Field(default=None)
    type: str | None = Field(default=None)  # pattern=r"\w+/[\w.+\-]+"


class Media(AssetBlock):
    """
    The Media block allows you to include images, GIFs, video and audio in your apps. If the file is in a supported format, it will be displayed inline in your app.

    To include an image, you can use `ar.Media` and pass the path.

    !!! note
        Supported video, audio and image formats depend on the browser used to view the report. MP3, MP4, and all common image formats are generally supported by modern browsers
    """

    _tag = "Media"

    def __init__(
        self,
        file: NPath,
        name: str | None = None,
        label: str | None = None,
        caption: str | None = None,
    ):
        """
        Args:
            file: A ath to a file to attach to the report (e.g. a JPEG image)
            name: A unique name for the block to reference when adding text or embedding (optional)
            caption: A caption to display below the file (optional)
            label: A label used when displaying the block (optional)
        """
        file = Path(file).expanduser()
        super().__init__(file=file, name=name, caption=caption, label=label)


class Attachment(AssetBlock):
    """
    If you want to include static files like PDFs or Excel docs in your app, use the `ar.Attachment` block.

    You can also pass in a Python object directly. Once you upload the app, your users will be able to explore and download these attachments.

    !!! tip
        To attach streamable / viewable video, audio or images, use the `ar.Media` block instead
    """

    _tag = "Attachment"

    filename: str = Field(..., min_length=1, max_length=255)

    def __init__(
        self,
        data: Any = None,
        file: NPath | None = None,
        filename: str | None = None,
        caption: str | None = None,
        name: str | None = None,
        label: str | None = None,
    ):
        """
        Args:
            data: A python object to attach to the report (e.g. a dictionary)
            file: A path to a file to attach to the report (e.g. a csv file)
            filename: A name to be used when downloading the file (optional)
            caption: A caption to display below the file (optional)
            name: A unique name for the block to reference when adding text or embedding (optional)
            label: A label used when displaying the block (optional)

        !!! note

            Either `data` or `file` must be provided
        """
        if file:
            file = Path(file).expanduser()
            filename = filename or file.name
        elif data:
            filename = filename or "test.data"

        assert filename

        super().__init__(
            data=data,
            file=cast(Optional[Path], file),
            name=name,
            caption=caption,
            label=label,
            filename=filename,
        )


class Plot(AssetBlock):
    """
    Arakawa supports all major Python visualization libraries, allowing you to add interactive plots and visualizations to your app.

    The `ar.Plot` block takes a plot object from one of the supported Python visualization libraries and renders it in your app.

    !!! info
        Arakawa will automatically wrap your visualization or plot in a `ar.Plot` block if you pass it into your app directly.
    """

    _tag = "Plot"

    responsive: bool = Field(default=True)
    scale: float = Field(default=1.0)

    def __init__(
        self,
        data: Any,
        caption: str | None = None,
        responsive: bool = True,
        scale: float = 1.0,
        name: str | None = None,
        label: str | None = None,
    ):
        """
        Args:
            data: A `plot` object to attach
            caption: A caption to display below the plot (optional)
            responsive: Whether the plot should automatically be resized to fit, set to False if your plot looks odd (optional, default: True)
            scale: Set the scaling factor for the plt (optional, default = 1.0)
            name: A unique name for the block to reference when adding text or embedding (optional)
            label: A label used when displaying the block (optional)
        """
        super().__init__(
            data=data,
            caption=caption,
            name=name,
            label=label,
            responsive=responsive,
            scale=scale,
        )


class Table(AssetBlock):
    # NOTE - Tables are stored as HTML fragment files rather than inline within the Report document
    """
    Table blocks store the contents of a DataFrame as a HTML `table` whose style can be customized using pandas' `Styler` API.

    !!! tip
        `Table` is the best option for displaying multidimensional DataFrames, as `DataTable` will flatten your data.
    """

    _tag = "Table"

    def __init__(
        self,
        data: pd.DataFrame | Styler,
        caption: str | None = None,
        name: str | None = None,
        label: str | None = None,
    ):
        """
        Args:
            data: A pandas `Styler` instance or dataframe to generate the table from
            caption: A caption to display below the table (optional)
            name: A unique name for the block to reference when adding text or embedding (optional)
            label: A label used when displaying the block (optional)
        """
        super().__init__(data=data, caption=caption, name=name, label=label)


class DataTable(AssetBlock):
    """
    The DataTable block takes a pandas DataFrame and renders an interactive, sortable, searchable table in your app, along with advanced analysis options such as exploring data through [SandDance](https://www.microsoft.com/en-us/research/project/sanddance/).

    It supports large datasets and viewers can also download the table from the website as a CSV or Excel file.

    !!! tip
        `Table` is the best option for displaying multidimensional DataFrames, as `DataTable` will flatten your data.
    """

    _tag = "DataTable"

    rows: int = Field(..., ge=0)
    columns: int = Field(..., ge=0)

    def __init__(
        self,
        df: pd.DataFrame,
        caption: str | None = None,
        name: str | None = None,
        label: str | None = None,
    ):
        """
        Args:
            df: A pandas dataframe to attach to the report
            caption: A caption to display below the plot (optional)
            name: A unique name for the block to reference when adding text or embedding (optional)
            label: A label used when displaying the block (optional)
        """
        # create a copy of the df to process
        df = to_df(df)
        # TODO - support pyarrow schema for local reports
        (rows, columns) = df.shape
        super().__init__(
            data=df, caption=caption, name=name, label=label, rows=rows, columns=columns
        )
