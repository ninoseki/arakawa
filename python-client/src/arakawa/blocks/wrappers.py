"""Type-driven block wrapping"""
# ruff: noqa: FA100

from pathlib import Path
from typing import Union

import pandas as pd
from altair.utils import SchemaBase
from multimethod import multimethod

from arakawa import blocks as b
from arakawa import optional_libs as opt
from arakawa.exceptions import ARError

from .base import DataBlock


@multimethod
def convert_to_block(x: object) -> DataBlock:
    raise ARError(
        f"{type(x)} not supported directly, please pass into in the appropriate ar object (including ar.Attachment if want to upload as a pickle)"
    )


# NOTE - this is currently disabled to avoid confusing users when they
# try to embed any Python object, instead they must use ar.Attachment
# @multimethod
# def convert_to_block(x: Any) -> DataBlock:
#     return b.Attachment(x)


@convert_to_block.register  # type: ignore
def _(x: str) -> DataBlock:
    return b.Text(x)


@convert_to_block.register  # type: ignore
def _(x: Path) -> DataBlock:
    return b.Attachment(file=x)


@convert_to_block.register  # type: ignore
def _(x: pd.DataFrame) -> DataBlock:
    n_cells = x.shape[0] * x.shape[1]
    return b.Table(x) if n_cells <= 250 else b.DataTable(x)


# Plots
@convert_to_block.register  # type: ignore
def _(x: SchemaBase) -> DataBlock:
    return b.Plot(x)


if opt.HAVE_BOKEH:

    @convert_to_block.register  # type: ignore
    def _(x: Union[opt.BFigure, opt.BLayout]) -> DataBlock:
        return b.Plot(x)


if opt.HAVE_PLOTLY:

    @convert_to_block.register  # type: ignore
    def _(x: opt.PFigure) -> DataBlock:
        return b.Plot(x)


if opt.HAVE_FOLIUM:

    @convert_to_block.register  # type: ignore
    def _(x: opt.Map) -> DataBlock:
        return b.Plot(x)


if opt.HAVE_MATPLOTLIB:

    @convert_to_block.register  # type: ignore
    def _(x: Union[opt.Figure, opt.Axes, opt.ndarray]) -> DataBlock:
        return b.Plot(x)
