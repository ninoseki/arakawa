"""
Dynamic handling for optional libraries - this module is imported on demand
"""

from __future__ import annotations

from packaging import version as v
from packaging.specifiers import SpecifierSet

from arakawa.utils import log

# NOTE - need to update this and keep in sync with JS
BOKEH_V_SPECIFIER = SpecifierSet(">=3.4.0,<3.5.0")
PLOTLY_V_SPECIFIER = SpecifierSet("~=5.24")
FOLIUM_V_SPECIFIER = SpecifierSet("~=0.18")


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
