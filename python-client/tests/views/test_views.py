"""Tests for the API that can run locally (due to design or mocked out)"""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import pandas as pd
import pytest
from _pytest.monkeypatch import MonkeyPatch
from boltons import iterutils
from dominate.tags import h2
from glom import glom
from pydantic import ValidationError

import arakawa as ar
from arakawa.blocks import BaseBlock
from arakawa.exceptions import ARError
from arakawa.file_store import B64FileEntry
from arakawa.processors import ConvertPydantic, Pipeline, PreProcessView, ViewState
from arakawa.processors.types import mk_null_pipe
from tests.builtins import gen_df, gen_plot

# Helpers
md_block_id = ar.Text(
    text="# Test markdown block <hello/> \n Test **content**", name="test-id-1"
)
md_block = ar.Text(text="# Test markdown block <hello/> \n Test **content**")
str_md_block = "Simple string Markdown"


def element_to_dict(e: BaseBlock):
    # NOTE - this validates as well
    return (
        mk_null_pipe(ar.Blocks(e))
        .pipe(ConvertPydantic(pretty_print=True))
        .state.view_json
    )


def num_blocks(view_json: dict) -> int:
    # subtract 1 for the root block
    count = len(iterutils.research(view_json, query=lambda _p, k, _v: k == "_type"))
    return count - 1


def _view_to_json_and_files(app_or_view: ar.Blocks | ar.Report) -> ViewState:
    """Create a viewstate resulting from converting the View to XML & in-mem B64 files"""
    s = ViewState(blocks=app_or_view, file_entry_klass=B64FileEntry)
    return Pipeline(s).pipe(PreProcessView()).pipe(ConvertPydantic()).state


def assert_view(
    view: ar.Report | ar.Blocks,
    expected_attachments: int | None = None,
    expected_num_blocks: int | None = None,
) -> tuple[dict, list[BinaryIO]]:
    state = _view_to_json_and_files(view)
    view_json = state.view_json
    attachments = state.store.file_list

    if expected_attachments:
        assert len(attachments) == expected_attachments

    if expected_num_blocks:
        assert num_blocks(view_json) == expected_num_blocks

    return (view_json, attachments)


################################################################################
# Generators
def gen_view_simple() -> ar.Blocks:
    return ar.Blocks(
        blocks=[
            md_block_id,
            str_md_block,
        ]
    )


def gen_view_complex_no_files() -> ar.Blocks:
    """Generate a complex layout view with simple elements"""
    select = ar.Select(blocks=[md_block, md_block], type=ar.SelectType.TABS)
    group = ar.Group(md_block, md_block, columns=2)
    toggle = ar.Toggle(md_block, md_block)

    return ar.Blocks(
        ar.Page(
            blocks=[
                ar.Group(md_block, md_block, columns=2),
                ar.Select(
                    blocks=[md_block, group, toggle], type=ar.SelectType.DROPDOWN
                ),
            ],
            title="Page Uno",
        ),
        ar.Page(
            blocks=[
                ar.Group(select, select, toggle, columns=2),
                ar.Select(
                    blocks=[md_block, md_block, md_block], type=ar.SelectType.TABS
                ),
            ],
            title="Page Duo",
        ),
        ar.Page(
            blocks=[
                ar.Group(group, group, columns=2),
                ar.Select(blocks=[select, select], type=ar.SelectType.TABS),
            ],
            title="Page Tres",
        ),
    )


def gen_view_complex_with_files(
    datadir: Path, single_file: bool = False, local_report: bool = False
) -> ar.Blocks:
    # Asset tests
    lis = [1, 2, 3]
    small_df = gen_df()
    big_df = gen_df(10000)

    # text
    # md_block
    html_block = ar.HTML(html="<h1>Hello World</h1>")
    html_block_1 = ar.HTML(html=h2("Hello World"))
    code_block = ar.Code(code="print('hello')", language="python")
    formula_block = ar.Formula(formula=r"\frac{1}{\sqrt{x^2 + 1}}")
    big_number = ar.BigNumber(heading="Tests written", value=1234)
    big_number_1 = ar.BigNumber(
        heading="Real Tests written :)", value=11, change=2, is_upward_change=True
    )
    embed_block = ar.Embed(url="https://www.youtube.com/watch?v=JDe14ulcfLA")
    divider_block = ar.Text("---")
    empty_block = ar.Empty(name="empty-block")

    # assets
    plot_asset = ar.Plot(data=gen_plot(), caption="Plot Asset")
    list_asset = ar.Attachment(data=lis, filename="List Asset")
    img_asset = ar.Media(file=datadir / "datapane-icon-192x192.png")

    # tables
    table_asset = ar.Table(data=small_df, caption="Test Basic Table")
    # local reports don't support DataTable
    dt_asset = (
        table_asset
        if local_report
        else ar.DataTable(df=big_df, name="big-table-block", caption="Test DataTable")
    )

    if single_file:
        return ar.Blocks(ar.Group(blocks=[md_block, dt_asset]))

    return ar.Blocks(
        ar.Page(
            ar.Select(
                md_block,
                html_block,
                html_block_1,
                code_block,
                formula_block,
                embed_block,
                type=ar.SelectType.TABS,
            ),
            ar.Group(big_number, big_number_1, columns=2),
            ar.Toggle(md_block, html_block, label="Test Toggle"),
        ),
        ar.Page(
            plot_asset,
            divider_block,
            empty_block,
            list_asset,
            img_asset,
            table_asset,
            dt_asset,
            ar.Empty("empty"),
        ),
    )


################################################################################
# View Tests
def test_gen_view_single():
    # view with single block
    view = ar.Blocks("test block")
    assert_view(view, 0)
    assert len(view.blocks) == 1
    assert isinstance(view.blocks[0], ar.Text)


def test_gen_view_simple():
    view = gen_view_simple()
    assert_view(view, 0, 2)
    # TODO - replace accessors here with glom / boltons / toolz
    assert len(view.blocks) == 2
    assert isinstance(view.blocks[1], ar.Text)
    assert view.blocks[0].name == "test-id-1"


def test_gen_view_nested_mixed():
    view = ar.Blocks(
        ar.Group(
            md_block_id,
            str_md_block,
        ),
        "Simple string Markdown #2",
    )

    assert_view(view, 0, 4)
    assert len(glom(view, "blocks")) == 2
    assert isinstance(glom(view, "blocks.0"), ar.Group)
    assert isinstance(view.blocks[0], ar.Group)
    assert isinstance(view.blocks[1], ar.Text)
    assert glom(view, "blocks.0.blocks.0.name") == "test-id-1"


def test_gen_view_primitives(datadir: Path):
    # check we don't allow arbitrary python primitives - must be pickled directly via ar.Attachment
    with pytest.raises(ARError):
        _ = ar.Blocks([1, 2, 3]).get_view()

    view = ar.Blocks(
        "Simple string Markdown #2",  # Markdown
        gen_df(),  # Table
        gen_plot(),  # Plot
        datadir / "datapane-icon-192x192.png",  # Attachment
    )
    assert_view(view, 3)
    assert glom(view, ("blocks", ["_tag"])) == ["Text", "Table", "Plot", "Attachment"]


def test_gen_failing_views():
    # nested pages
    with pytest.raises(ARError):
        v = ar.Blocks(ar.Page(ar.Page(md_block)))
        _view_to_json_and_files(v)

    # we only transform top-level pages
    with pytest.raises(ValidationError):
        v = ar.Blocks(ar.Group(ar.Page(md_block)))
        _view_to_json_and_files(v)

    # page/pages with 0 objects
    with pytest.raises(ValidationError):
        v = ar.Blocks(ar.Page(blocks=[]))
        _view_to_json_and_files(v)

    # select with 1 object
    with pytest.raises(ARError):
        v = ar.Blocks(ar.Page(ar.Select(blocks=[md_block])))
        _view_to_json_and_files(v)

    # empty text block
    with pytest.raises(ValidationError):
        v = ar.Blocks(ar.Text(" "))
        _view_to_json_and_files(v)

    # empty df
    with pytest.raises(ARError):
        v = ar.Blocks(ar.DataTable(pd.DataFrame()))
        _view_to_json_and_files(v)

    # invalid names
    with pytest.raises(ARError):
        v = ar.Blocks(ar.Text("a", name="my-name"), ar.Text("a", name="my-name"))
        _view_to_json_and_files(v)

    # invalid names
    with pytest.raises(ARError):
        v = ar.Blocks(
            ar.Group(
                ar.Text("foo", name="my-name"),
                ar.Text("bar", name="bar"),
                name="my-name",
            )
        )
        _view_to_json_and_files(v)

    with pytest.raises(ValidationError):
        ar.Blocks(ar.Text("a", name="3-invalid-name"))


def test_gen_view_nested_blocks():
    s = "# Test markdown block <hello/> \n Test **content**"
    view = ar.Blocks(
        blocks=[
            ar.Group(
                ar.Text(s, name="test-id-1"),
                "Simple string Markdown",
                label="test-group-label",
            ),
            ar.Select(
                blocks=[
                    ar.Text(s, name="test-id-2", label="test-block-label"),
                    "Simple string Markdown",
                ],
                label="test-select-label",
            ),
            ar.Toggle(
                blocks=[
                    ar.Text(s, name="test-id-3"),
                    "Simple string Markdown",
                ],
                label="test-toggle-label",
            ),
        ]
    )

    # No additional wrapper block
    assert len(view.blocks) == 3
    assert isinstance(view.blocks[0], ar.Group)
    assert isinstance(view.blocks[1], ar.Select)
    assert isinstance(view.blocks[2], ar.Toggle)
    assert isinstance(view.blocks[1].blocks[1], ar.Text)
    assert glom(view, ("blocks", ["label"])) == [
        "test-group-label",
        "test-select-label",
        "test-toggle-label",
    ]
    assert glom(view, "blocks.0.blocks.0.name") == "test-id-1"
    assert glom(view, "blocks.1.blocks.0.label") == "test-block-label"
    assert_view(view, 0)


def test_gen_view_complex_no_files():
    view = gen_view_complex_no_files()
    assert_view(view, 0)
    assert len(view.blocks) == 3


def test_gen_view_with_files(datadir: Path):
    view = gen_view_complex_with_files(datadir)
    assert_view(view, 5, 25)


def test_save_report_simple(datadir: Path, monkeypatch: MonkeyPatch):
    monkeypatch.chdir(datadir)
    view = gen_view_simple()
    ar.save_report(view, path="test_out.html", name="My Test Report")


def test_save_report_with_files(datadir: Path, monkeypatch: MonkeyPatch):
    monkeypatch.chdir(datadir)
    view = gen_view_complex_with_files(datadir, local_report=True)
    ar.save_report(view, path="test_out.html", name="Even better report")
