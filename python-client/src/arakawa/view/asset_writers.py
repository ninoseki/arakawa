"""
# TODO - optimize import handling here
"""
# ruff: noqa: FA100

import json
import pickle
from contextlib import suppress
from io import TextIOWrapper
from typing import Any, Union

import pandas as pd
from altair.utils import SchemaBase
from multimethod import multimethod
from pandas.io.formats.style import Styler

from arakawa import optional_libs as opt
from arakawa.common import ArrowFormat
from arakawa.exceptions import ARError
from arakawa.utils import log

from .pydantic_visitor import AssetMeta


class ARTextIOWrapper(TextIOWrapper):
    """Custom IO Wrapper that detaches before closing - see https://bugs.python.org/issue21363"""

    def __init__(self, f, *a, **kw):
        super().__init__(f, *a, encoding="utf-8", **kw)

    def __del__(self):
        # don't close the underlying stream
        with suppress(Exception):
            self.flush()
        with suppress(Exception):
            self.detach()


class AttachmentWriter:
    @multimethod
    def get_meta(self, _: Any) -> AssetMeta:
        return AssetMeta(ext=".pkl", mime="application/vnd.pickle+binary")

    @get_meta.register  # type: ignore
    def _(self, _: str) -> AssetMeta:
        return AssetMeta(ext=".json", mime="application/json")

    @multimethod
    def write_file(self, x: Any, f) -> None:
        pickle.dump(x, f)

    @write_file.register  # type: ignore
    def _(self, x: str, f) -> None:
        out: str = json.dumps(json.loads(x))
        f.write(out.encode())


class DataTableWriter:
    def get_meta(self, _: pd.DataFrame) -> AssetMeta:
        return AssetMeta(mime=ArrowFormat.content_type, ext=ArrowFormat.ext)

    def write_file(self, x: pd.DataFrame, f) -> None:
        if x.size == 0:
            raise ARError("Empty DataFrame provided")
        # process_df called in Arrow.save_file
        ArrowFormat.save_file(f, x)


class HTMLTableWriter:
    def get_meta(self, _: Union[pd.DataFrame, Styler]) -> AssetMeta:
        return AssetMeta(mime="application/vnd.arakawa.table+html", ext=".tbl.html")

    @multimethod
    def write_file(self, x: pd.DataFrame, f) -> None:
        self._check(x)
        out = x.to_html().encode()
        f.write(out)

    @write_file.register  # type: ignore
    def _(self, x: Styler, f) -> None:
        self._check(x.data)  # type: ignore
        out = x.to_html().encode()
        f.write(out)

    def _check(self, df: pd.DataFrame) -> None:
        n_cells = df.shape[0] * df.shape[1]
        if n_cells > 500:
            log.warning(
                "Table is over recommended size, consider using ar.DataTable instead or aggregating the df first"
            )


class PlotWriter:
    obj_type: Any

    # Altair (always installed)
    @multimethod
    def get_meta(self, _: SchemaBase) -> AssetMeta:
        return AssetMeta(mime="application/vnd.vegalite.v5+json", ext=".vl.json")

    @multimethod
    def write_file(self, x: SchemaBase, f) -> None:
        json.dump(x.to_dict(), ARTextIOWrapper(f))

    if opt.HAVE_FOLIUM:

        @get_meta.register  # type: ignore
        def _(self, _: opt.Map) -> AssetMeta:
            return AssetMeta(mime="application/vnd.folium+html", ext=".fl.html")

        @write_file.register  # type: ignore
        def _(self, x: opt.Map, f) -> None:
            html: str = x.get_root().render()
            f.write(html.encode())

    if opt.HAVE_BOKEH:

        @get_meta.register  # type: ignore
        def _(self, _: Union[opt.BFigure, opt.BLayout]) -> AssetMeta:
            return AssetMeta(mime="application/vnd.bokeh.show+json", ext=".bokeh.json")

        @write_file.register  # type: ignore
        def _(self, x: Union[opt.BFigure, opt.BLayout], f):
            from bokeh.embed import json_item

            json.dump(json_item(x), ARTextIOWrapper(f))

    if opt.HAVE_PLOTLY:

        @get_meta.register  # type: ignore
        def _(self, _: opt.PFigure) -> AssetMeta:
            return AssetMeta(mime="application/vnd.plotly.v1+json", ext=".pl.json")

        @write_file.register  # type: ignore
        def _(self, x: opt.PFigure, f):
            json.dump(x.to_json(), ARTextIOWrapper(f))

    if opt.HAVE_MATPLOTLIB:

        @get_meta.register  # type: ignore
        def _(self, _: Union[opt.Axes, opt.Figure, opt.ndarray]) -> AssetMeta:
            return AssetMeta(mime="image/svg+xml", ext=".svg")

        @write_file.register  # type: ignore
        def _(self, x: opt.Figure, f) -> None:
            x.savefig(ARTextIOWrapper(f), format="svg", bbox_inches="tight")

        @write_file.register  # type: ignore
        def _(self, x: opt.Axes, f) -> None:
            self.write_file(x.get_figure(), f)

        @write_file.register  # type: ignore
        def _(self, x: opt.ndarray, f) -> None:
            fig = x.flatten()[0].get_figure()
            self.write_file(fig, f)
