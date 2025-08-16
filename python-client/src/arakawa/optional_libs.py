"""
Dynamic handling for optional libraries - this module is imported on demand
"""

from __future__ import annotations

from packaging import version as v
from packaging.specifiers import SpecifierSet

from arakawa.utils import log

# NOTE - need to update this and keep in sync with JS
BOKEH_V_SPECIFIER = SpecifierSet(">=3.7.3,<3.8.0")
PLOTLY_V_SPECIFIER = SpecifierSet("~=6.0")
FOLIUM_V_SPECIFIER = SpecifierSet("~=0.18")
GREAT_TABLES_V_SPECIFIER = SpecifierSet("~=0.16")
POLARS_V_SPECIFIER = SpecifierSet("~=1.0")
NETWORKX_V_SPECIFIER = SpecifierSet("~=3.2")


def _check_version(name: str, _v: v.Version, ss: SpecifierSet):
    if _v not in ss:
        log.warning(
            f"{name} version {_v} is not supported, these plots may not display correctly, please install version {ss}"
        )


# Optional Plotting library import handling
# Matplotlib
try:
    from matplotlib.axes import Axes  # noqa: F401
    from matplotlib.figure import Figure  # noqa: F401
    from numpy import ndarray  # noqa: F401

    HAVE_MATPLOTLIB = True
except ImportError:
    log.debug("No matplotlib found")
    HAVE_MATPLOTLIB = False

# Folium
try:
    import folium
    from folium import Map  # noqa: F401

    _check_version("Folium", v.Version(folium.__version__), FOLIUM_V_SPECIFIER)
    HAVE_FOLIUM = True
except ImportError:
    HAVE_FOLIUM = False
    log.debug("No folium found")

# Bokeh
try:
    import bokeh
    from bokeh.models import LayoutDOM as BLayout  # noqa: F401
    from bokeh.plotting import figure as BFigure  # noqa: F401, N812

    _check_version("Bokeh", v.Version(bokeh.__version__), BOKEH_V_SPECIFIER)
    HAVE_BOKEH = True
except ImportError:
    HAVE_BOKEH = False
    log.debug("No Bokeh Found")

# Plotly
try:
    import plotly
    from plotly.graph_objects import Figure as PFigure  # noqa: F401

    _check_version("Plotly", v.Version(plotly.__version__), PLOTLY_V_SPECIFIER)
    HAVE_PLOTLY = True
except ImportError:
    HAVE_PLOTLY = False
    log.debug("No Plotly Found")

# Great Tables
try:
    import great_tables
    from great_tables import GT as GTTable  # noqa: F401, N811

    _check_version(
        "Great Tables", v.Version(great_tables.__version__), GREAT_TABLES_V_SPECIFIER
    )
    HAVE_GREAT_TABLES = True
except ImportError:
    HAVE_GREAT_TABLES = False
    log.debug("No Great Tables Found")

# Polars
try:
    import polars as pl
    from polars import DataFrame as PlDataFrame  # noqa: F401

    _check_version("Polars", v.Version(pl.__version__), POLARS_V_SPECIFIER)
    HAVE_POLARS = True
except ImportError:
    HAVE_POLARS = False
    log.debug("No Polars Found")

# NetworkX
try:
    import networkx
    from networkx import Graph as NXGraph  # noqa: F401

    _check_version("NetworkX", v.Version(networkx.__version__), NETWORKX_V_SPECIFIER)
    HAVE_NETWORKX = True
except ImportError:
    HAVE_NETWORKX = False
    log.debug("No NetworkX Found")
