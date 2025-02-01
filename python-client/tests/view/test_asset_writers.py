import tempfile
from typing import cast

import polars as pl
import pytest

from arakawa.view.asset_writers import DataTableWriter, HTMLTableWriter
from tests.parser import TagsRecorderParser


@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile() as f:
        yield f


@pytest.fixture
def df():
    return pl.DataFrame(
        {
            "a": [1, 2, 3],
            "b": ["foo", "bar", "baz"],
        }
    )


def test_data_table_writer_with_polars(
    df: pl.DataFrame, temp_file: tempfile._TemporaryFileWrapper
):
    writer = DataTableWriter()
    writer.write_file(df, temp_file.name)

    arrow_df = pl.read_ipc(temp_file)
    assert df.equals(arrow_df)


@pytest.fixture
def parser():
    return TagsRecorderParser()


def test_table_writer_with_polars(
    df: pl.DataFrame,
    temp_file: tempfile._TemporaryFileWrapper,
    parser: TagsRecorderParser,
):
    writer = HTMLTableWriter()
    writer.write_file(df, temp_file)

    temp_file.seek(0)
    table = cast(bytes, temp_file.read()).decode()

    parser.feed(table)
    assert "table" in parser.start_tags
    assert "table" in parser.end_tags
    assert parser.is_valid()
