"""Dataset Format handling"""

from __future__ import annotations

import abc
from typing import IO

import pandas as pd
import pyarrow as pa
from base64io import Base64IO
from multimethod import multimethod
from pyarrow import RecordBatchFileWriter

from arakawa import optional_libs as opt
from arakawa.types import ARROW_EXT, ARROW_MIMETYPE, MIME

from .df_processor import obj_to_str, process_df, str_to_arrow_str

PathOrFile = str | IO | Base64IO


def write_table(table: pa.Table, sink: PathOrFile):
    """Write an arrow table to a file"""
    writer = RecordBatchFileWriter(sink, table.schema)
    writer.write(table)
    writer.close()


class DFFormatter(abc.ABC):
    # TODO - tie to mimetypes lib
    content_type: MIME
    ext: str
    enum: str

    @staticmethod
    @abc.abstractmethod
    def load_file(fn: PathOrFile) -> pd.DataFrame:
        pass

    @staticmethod
    @abc.abstractmethod
    def save_file(fn: PathOrFile, df: pd.DataFrame):
        pass


DFFormatterCls = type[DFFormatter]


class ArrowFormat(DFFormatter):
    content_type = ARROW_MIMETYPE
    ext = ARROW_EXT
    enum = "ARROW"

    @staticmethod
    def load_file(fn: PathOrFile) -> pd.DataFrame:
        df = pa.ipc.open_file(fn).read_pandas()
        # NOTE - need to convert categories from object to string https://github.com/apache/arrow/issues/33070
        obj_to_str(df)
        str_to_arrow_str(df)
        return df

    @multimethod
    def save_file(fn: PathOrFile, df: pd.DataFrame):  # type: ignore # noqa: N805
        df = process_df(df)
        # NOTE - can pass expected schema and columns for output df here
        table: pa.Table = pa.Table.from_pandas(df, preserve_index=False)
        write_table(table, fn)

    if opt.HAVE_POLARS:

        @save_file.register  # type: ignore
        def _(fn: PathOrFile, df: opt.PlDataFrame):  # type: ignore # noqa: N805
            table: pa.Table = df.to_arrow()
            write_table(table, fn)

    save_file = staticmethod(save_file)  # type: ignore
