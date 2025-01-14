"""Dataset Format handling"""

from __future__ import annotations

import abc
import enum
from typing import IO, Union

import pandas as pd
import pyarrow as pa
from loguru import logger as log
from pandas.errors import ParserError
from pyarrow import RecordBatchFileWriter

from arakawa.types import ARROW_EXT, ARROW_MIMETYPE, MIME

from .df_processor import obj_to_str, process_df, str_to_arrow_str
from .utils import guess_encoding


def write_table(table: pa.Table, sink: str | IO[bytes]):
    """Write an arrow table to a file"""
    writer = RecordBatchFileWriter(sink, table.schema)
    writer.write(table)
    writer.close()


PathOrFile = Union[str, IO]


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

    @staticmethod
    def save_file(fn: PathOrFile, df: pd.DataFrame):
        df = process_df(df)
        # NOTE - can pass expected schema and columns for output df here
        table: pa.Table = pa.Table.from_pandas(df, preserve_index=False)
        write_table(table, fn)


class CSVFormat(DFFormatter):
    content_type = MIME("text/csv")
    ext = ".csv"
    enum = "CSV"

    @staticmethod
    def load_file(fn: PathOrFile) -> pd.DataFrame:
        # TODO - fix
        if not isinstance(fn, str):
            raise ValueError("FObj not yet supported")

        try:
            return pd.read_csv(fn, engine="c", sep=",")
        except UnicodeDecodeError:
            encoding = guess_encoding(fn)
            return pd.read_csv(fn, engine="c", sep=",", encoding=encoding)
        except ParserError as e:
            log.warning(f"Error parsing CSV file ({e}), trying python fallback")
            try:
                return pd.read_csv(fn, engine="python", sep=None)
            except UnicodeDecodeError:
                encoding = guess_encoding(fn)
                return pd.read_csv(fn, engine="python", sep=None, encoding=encoding)

    @staticmethod
    def save_file(fn: PathOrFile, df: pd.DataFrame):
        df.to_csv(fn, index=False)


class ExcelFormat(DFFormatter):
    content_type = MIME(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    ext = ".xlsx"
    enum = "EXCEL"

    @staticmethod
    def load_file(fn: PathOrFile) -> pd.DataFrame:
        return pd.read_excel(fn, engine="openpyxl")

    @staticmethod
    def save_file(fn: PathOrFile, df: pd.DataFrame):
        df.to_excel(fn, index=False, engine="openpyxl")


class DatasetFormats(enum.Enum):
    """Used to switch between the different format handlers"""

    CSV = CSVFormat
    EXCEL = ExcelFormat
    ARROW = ArrowFormat


# TODO - make into enums?
df_ext_map: dict[str, DFFormatterCls] = {x.value.ext: x.value for x in DatasetFormats}
