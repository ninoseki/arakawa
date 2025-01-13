# Arakawa

[![PyPI version](https://badge.fury.io/py/arakawa.svg)](https://badge.fury.io/py/arakawa)
[![npm version](https://badge.fury.io/js/arakawa.svg)](https://badge.fury.io/js/arakawa)

<p align='center'>
  <h2 align='center'>Build interactive reports in seconds using Python.</h2>
</p>

Arakawa makes it simple to build interactive reports in seconds using Python.

Import Arakawa's Python library into your script or notebook and build reports programmatically by wrapping components such as:

- Pandas DataFrames
- Plots from Python visualization libraries such as Bokeh, Altair, Plotly, and Folium
- Markdown and text
- Files, such as images, PDFs, JSON data, etc.
- Interactive forms which run backend Python functions

Arakawa reports are interactive and can also contain pages, tabs, drop downs, and more. Once created, reports can be exported as HTML, shared as standalone files, or embedded into your own application, where your viewers can interact with your data and visualizations.

## Getting Started

Check out our [Quickstart](https://ninoseki.github.io/arakawa/quickstart) to build a report in 3m.

### Installing Arakawa

```bash
pip install arakawa
# or
conda install -c conda-forge
```

## Examples

### 📊 Share plots, data, and more as reports

Create reports from pandas DataFrames, plots from your favorite libraries, and text.

<p>

<img width='485px' align='left' alt="Simple example with text, plot and table" src="https://raw.githubusercontent.com/ninoseki/arakawa/refs/heads/main/python-client/images/simple_example.png">

<p>

```python
import altair as alt
from vega_datasets import data
import arakawa as ar

df = data.iris()
fig = (
    alt.Chart(df)
    .mark_point()
    .encode(
        x="petalLength:Q",
        y="petalWidth:Q",
        color="species:N"
    )
)
view = ar.Blocks(
    ar.Plot(fig),
    ar.DataTable(df)
)
ar.save_report(view, path="simple_example.html")
```

</p>

### 🎛 Layout using interactive blocks

Add dropdowns, selects, grid, pages, and 10+ other interactive blocks.

<p>

<img width='485px' align='left' alt="Complex layout" src="https://raw.githubusercontent.com/ninoseki/arakawa/refs/heads/main/python-client/images/layout_example.png">

<p>

```python
...

view = ar.Blocks(
    ar.Formula("x^2 + y^2 = z^2"),
    ar.Group(
        ar.BigNumber(
            heading="Number of percentage points",
            value="84%",
            change="2%",
            is_upward_change=True
        ),
        ar.BigNumber(
            heading="Simple Statistic", value=100
        ), columns=2
    ),
    ar.Select(
        ar.Plot(fig, label="Chart"),
        ar.DataTable(df, label="Data")
    ),
)
ar.save_report(view, path="layout_example.html")
```

See [the documentation](https://ninoseki.github.io/arakawa/) for more details.

## Acknowledgement

This project is fork of [datapane/datapane](https://github.com/datapane/datapane) and original codes are written by StackHut Limited (trading as Datapane).
