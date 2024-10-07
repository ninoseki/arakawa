from __future__ import annotations

import random
from typing import Any

import altair as alt
import numpy as np
import pandas as pd

from arakawa import Blocks
from arakawa import blocks as b


def gen_df(dim: int = 4) -> pd.DataFrame:
    """Return a test simple df"""
    axis = list(range(0, dim))
    data = {"x": axis, "y": axis}
    return pd.DataFrame.from_dict(data)


def gen_table_df(rows: int = 4, alphabet: str = "ABCDEF") -> pd.DataFrame:
    """Return a test complex df for adding to a DataTable"""
    data = [{x: random.randint(0, 1000) for x in alphabet} for _ in range(0, rows)]
    return pd.DataFrame.from_records(data)


def gen_plot() -> alt.Chart:
    """Generate a sample Altair plot"""
    return alt.Chart(gen_df()).mark_line().encode(x="x", y="y")


def demo() -> Blocks:
    """
    Generate a sample demo view

    Returns:
        An Arakawa View object for saving or uploading
    """

    import altair as alt
    import folium
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    from bokeh.plotting import figure

    def _gen_bokeh(**kw):
        p = figure(
            title="simple line example", x_axis_label="x", y_axis_label="y", **kw
        )
        p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], legend_label="Temp.", line_width=2)
        return p

    def _gen_plotly():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[0, 1, 2, 3, 4, 5], y=[1.5, 1, 1.3, 0.7, 0.8, 0.9]))
        fig.add_trace(go.Bar(x=[0, 1, 2, 3, 4, 5], y=[1, 0.5, 0.7, -1.2, 0.3, 0.4]))
        return fig

    def _gen_matplotlib():
        # pd.set_option("plotting.backend", "matplotlib")
        fig, ax = plt.subplots()
        df = gen_df()
        ax.plot(df["x"], df["y"])
        # gen_df().plot.scatter("x", "y", ax=ax)
        return fig

    def _gen_html(w: int = 30, h: int = 30):
        return b.HTML(
            f"""
    <div style="width: {w}rem; height: {h}rem; background-color: rgba(0, 0, 255, 0.2); position: relative">
        <div style="position: absolute; right: 50%; bottom: 50%; transform: translate(50%, 50%);">
            HTML Block
        </div>
    </div>"""
        )

    def _color_large_vals(s: Any):
        return [
            "background-color: rgba(255, 0, 0, 0.3)" if val > 800 else "" for val in s
        ]

    def _gen_folium():
        return folium.Map(
            location=[45.372, -121.6972], zoom_start=12, tiles="OpenStreetMap"
        )

    df1 = gen_table_df(10)
    styler1 = df1.style.apply(_color_large_vals, axis=1).hide(axis="index")

    def _vega_sine():
        x = np.arange(100)
        source = pd.DataFrame({"x": x, "f(x)": np.sin(x / 5)})

        return alt.Chart(source).mark_line().encode(x="x", y="f(x)")

    vega_sine = _vega_sine()

    def _vega_bar():
        source = pd.DataFrame(
            {
                "a": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                "b": [28, 55, 43, 91, 81, 53, 19, 87, 52],
            }
        )

        return alt.Chart(source).mark_bar().encode(x="a", y="b")

    vega_bar = _vega_bar()

    basics = """
This page describes Arakawa, an API for creating data-driven reports from Python.
Arakawa reports are comprised of blocks, which can be collected together and laid-out to form multiple-pages reports.
Some of the basic blocks include tables and plots.

## Tables

The Table block displays a tabular set of data, and takes either a dataframe or a pandas Styler "styled" object,

```python
ar.Table(df, caption="A Table")
```

{{table}}

The DataTable block also takes a dataframe and allows the user to search and filter the data when viewing the report


## Plots

The Plot block supports Altair, Bokeh, Plotly, Matplotlib, and Folium plots,

```python
ar.Plot(altair_plot, caption="A Plot")
```

{{plot}}

## Other Blocks

Arakawa has many other block types, including formulas, files, embeds, images, and big numbers - see the Blocks page for more info.

Additionally layout blocks provide the ability nest blocks to create groups of columns and user selections - see the Layout page for more info.

{{other}}


    """
    other = b.Group(
        b.BigNumber(
            heading="Datapane Blocks", value=11, prev_value=6, is_upward_change=True
        ),
        b.Formula(r"\frac{1}{\sqrt{x^2 + 1}}", caption="Simple formula"),
        columns=0,
    )
    page_1 = b.Text(basics, label="Intro").format(
        table=b.Table(gen_table_df(), caption="A table"), plot=vega_sine, other=other
    )

    layout = """
Blocks on a page can be laid-out in Datapane using a flexible row and column system. furthermore, multiple blocks can be
nested into a single block where the user can select between which block, e.g. a plot, to view.
See https://docs.datapane.com/reports/layout-and-customization for more info.

## Group Blocks

Group blocks allow you to take a list of blocks, and lay-them out over a number of `rows` and `columns`, allowing you to create 2-column layouts, grids, and more,

```python
ar.Group(plot1, plot2, columns=2)
cells = [ar.Text(f"### Cell {x}") for x in range(6)]
ar.Group(*cells, columns=0)  # 0 implies auto
```

{{group1}}

{{group2}}

## Select Blocks

Select blocks allow you to collect a list of blocks, e.g. plots, and allow the user to select between them, either via tabs or a dropdown list.

```python
ar.Select(plot1, plot2, type=ar.SelectType.TABS)
ar.Select(plot1, plot2, type=ar.SelectType.DROPDOWN)
```

{{select1}}

{{select2}}


Both Group and Select blocks can be nested within one another, in any order to create, for instance dropdowns with 2 columns inside, as below

```python
group1 = ar.Group(plot1, plot2, columns=2)
ar.Select(group1, df)
```

{{nested}}
"""

    group1 = b.Group(vega_bar, vega_sine, columns=2)
    group2 = b.Group(*[f"### Cell {x}" for x in range(6)], columns=3)
    select1 = b.Select(vega_bar, vega_sine, type=b.SelectType.TABS, name="vega_select")
    select2 = b.Select(vega_bar, vega_sine, type=b.SelectType.DROPDOWN)

    nested = b.Select(group1, b.Table(gen_table_df()))
    page_2 = b.Text(layout, label="Layout").format(
        group1=group1, group2=group2, select1=select1, select2=select2, nested=nested
    )

    adv_blocks = r"""
A list and demonstration of all the blocks supported by Arakawa - see https://docs.datapane.com/reports/blocks for more info.

## Plot Blocks

```python
ar.Group(ar.Plot(altair_plot, caption="Altair Plot"),
         ar.Plot(bokeh_plot, caption="Bokeh Plot"),
         ar.Plot(matplotlib_plot, caption="Matplotlib Plot"),
         ar.Plot(plotly_plot, caption="Plotly Plot"),
         ar.Plot(folium_plot, caption="Folium Plot"),
         columns=2)
```

{{plots}}

## Table Blocks

```python
ar.Table(df, caption="Basic Table")
ar.Table(styled_df, caption="Styled Table")
ar.DataTable(df, caption="Interactive DataTable")
```

{{tables}}

## Text Blocks

```python
ar.Text("Hello, __world__!")
ar.Code("print('Hello, world!')")
ar.Formula(r"\frac{1}{\sqrt{x^2 + 1}}")
ar.HTML("<h1>Hello World</h1>")
ar.BigNumber(heading="Datapane Blocks", value=11, prev_value=6, is_upward_change=True)
```

{{text}}

## Embedding

You can embed any URLs that spport the OEmbed protocol, including YouTube and Twitter.

```python
ar.Embed("https://www.youtube.com/watch?v=JDe14ulcfLA")
ar.Embed("https://twitter.com/datapaneapp/status/1300831345413890050")
```

{{embed}}

## Media and Attachments

Files and Python objects can be added to An Arakawa report, and be viewed (depending on browser support) and downloaded.

```python
ar.Media(file="./logo.png")
ar.Attachment(data=[1,2,3])
```

{{media}}
"""

    plots = b.Group(
        b.Plot(vega_sine, name="vega", caption="Altair Plot"),
        b.Plot(_gen_bokeh(), name="bokeh", caption="Bokeh Plot"),
        b.Plot(_gen_matplotlib(), name="matplotlib", caption="Matplotlib Plot"),
        b.Plot(_gen_plotly(), name="plotly", caption="Plotly Plot"),
        b.Plot(_gen_folium(), name="folium", caption="Folium Plot"),
        name="plots_group",
        columns=2,
    )
    tables = b.Group(
        b.Table(df1, name="table1", caption="Basic Table"),
        b.Table(styler1, name="styled-table", caption="Styled Table"),
        b.DataTable(
            gen_table_df(1000), name="data_table", caption="Interactive DataTable"
        ),
    )
    text = b.Group(
        b.Text("Hello, __world__!", name="markdown"),
        b.Code("print('Hello, world!'", name="code"),
        b.Formula(r"\frac{1}{\sqrt{x^2 + 1}}"),
        b.HTML("<h1>Hello World</h1>", name="HTML"),
        b.BigNumber(
            heading="Datapane Blocks",
            value=11,
            prev_value=6,
            is_upward_change=True,
            name="big_num",
        ),
        columns=0,
    )
    embed = b.Group(
        b.Embed("https://www.youtube.com/watch?v=JDe14ulcfLA", name="youtube_embed"),
        b.Embed("https://twitter.com/datapaneapp/status/1300831345413890050"),
        columns=2,
    )
    media = b.Group(
        b.Attachment(data=[1, 2, 3]),
        columns=2,
    )

    page_3 = b.Text(adv_blocks, label="Blocks").format(
        plots=plots, tables=tables, text=text, embed=embed, media=media
    )

    return Blocks(b.Select(page_1, page_2, page_3))
